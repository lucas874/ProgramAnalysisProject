from dataclasses import dataclass
from helpers_constants import *
from copy import deepcopy

@dataclass(frozen=True)
class Interval: # Integers represented as intervals 
    l: int
    h: int
    index: int # Use when loading from locals 

    @classmethod
    def from_type(cls, typename):
        if typename == "int" or typename == "float":
            return Interval(INT_MIN, INT_MAX, None)
        else:
            raise Exception("Type not implemented")

    @classmethod 
    def from_value(cls, value): # From value field in bytecode json
        if value["type"] == "integer":
            return cls.from_integer(value["value"])
        else:
            raise Exception("Type not implemented")

    @classmethod 
    def from_integer(cls, value):
        return cls.checked(value, value)

    @classmethod # RECONSIDER THIS
    def checked(cls, l, h, index=None):
        if l > h:
            raise Exception("ASDADADDA")
        return Interval(max(l, INT_MIN), min(h, INT_MAX), index)
    
    @classmethod # This method creates an array. Not sure how to represent the items. preferably a set. look at Formal Methods an Appetizer p. 55. Maybe not important since we focus on bounds.
    def generate_array(cls, count=None, init_val=None):
        if count == None: count = cls.checked(INT_MIN, INT_MAX)
        if init_val == None: init_val = cls.checked(INT_MIN, INT_MAX)
        return (count, init_val)

    @classmethod # slides and p. 228 in book. more so p. 228. K is the set of integers explicitly mentioned in bytecode. 
    def wide(cls, v1, v2, K):
        if is_exception(v1): return v1
        if is_exception(v2): return v2 # hmmm ?
        if isinstance(v1, str): # In case of references
            assert v1 == v2
            return v1
        return cls.checked(cls.LB_k(v1.l, v2.l, K), cls.UB_k(v1.h, v2.h, K)) 
    
    # LBk UBk Principles of Program Analysis p.228. 
    @classmethod # Gives a lot of min/max when slie one would have given z3/z4??
    def LB_k(cls, z1, z3, K): 
        if z1 <= z3: return z1
        elif z1 > z3: 
            ks = [k for k in K if k <= z3]
            if ks != []: return max(ks)
            else: return INT_MIN

    @classmethod
    def UB_k(cls, z2, z4, K): 
        if z4 <= z2: return z2
        elif z4 > z2:
            ks = [k for k in K if z4 <= k]
            if ks != []: return min(ks)
            else: return INT_MAX

    # expect arr is (count, val). if count == 1 replace val by new val. else take min max etc such that old is included in new
    @classmethod
    def handle_array(cls, arr, new_val):
        if arr[0].eq(cls.from_integer(1)): 
            return (arr[0], new_val)
        else: 
            new_l = min(new_val.l, arr[1].l)
            new_h = max(new_val.h, arr[1].h)
            return (arr[0], cls.checked(new_l, new_h))

    @classmethod
    def tricky_gt(cls, l_branch, l_no_branch, val1, val2): 
        if val1.index is not None and val2.is_constant():
            new_h = max(val1.h, val2.h+1)
            new_l = max(val1.l, val2.h+1)
            l_branch[val1.index] = cls.checked(new_l, new_h, None)
            
            new_h = val2.l
            new_l = min(val1.l, new_h)
            l_no_branch[val1.index] = cls.checked(new_l, new_h, None)

        elif val2.index is not None and val1.is_constant(): 
            new_h = val1.l - 1
            new_l = min(val2.l, new_h)
            l_branch[val2.index] = cls.checked(new_l, new_h, None)
            
            new_h = max(val1.h, val2.h)
            new_l = min(val1.h, new_h)
            l_no_branch[val2.index] = cls.checked(new_l, new_h, None)

        return (l_branch, l_no_branch)

    @classmethod
    def tricky_ge(cls, l_branch, l_no_branch, val1, val2): 
        if val1.index is not None and val2.is_constant():
            new_h = max(val1.h, val2.h)
            new_l = max(val1.l, val2.h)
            l_branch[val1.index] = cls.checked(new_l, new_h, None)
            new_h = val2.l - 1 # REVIEW THIS
            new_l = min(val1.l, new_h)
            l_no_branch[val1.index] = cls.checked(new_l, new_h, None)

        elif val2.index is not None and val1.is_constant():
            new_h = val1.l
            new_l = min(val2.l, new_h)
            l_branch[val2.index] = cls.checked(new_l, new_h, None)
            new_h = max(val1.h+1, val2.h)
            new_l = max(val2.l, new_h)
            l_no_branch[val2.index] = cls.checked(new_l, new_h, None)

        return (l_branch, l_no_branch)
    
    @classmethod 
    def tricky_lt(cls, l_branch, l_no_branch, val1, val2):
        if val1.index is not None and val2.is_constant():
            high_branch = val2.l-1
            low_branch = min(val1.l, high_branch)
            l_branch[val1.index] = cls.checked(low_branch, high_branch, None) 

            high_no_branch = max(val1.h, val2.h)
            low_no_branch = val2.h
            l_no_branch[val1.index] = cls.checked(low_no_branch, high_no_branch, None)

        elif val2.index is not None and val1.is_constant():
            high_branch = max(val1.h+1, val2.h)
            low_branch = max(val1.h+1, val2.l)
            l_branch[val2.index] = cls.checked(low_branch, high_branch)

            high_no_branch = min(val1.l, val2.h)
            low_no_branch = min(high_no_branch, val2.l)
            l_no_branch[val2.index] = cls.checked(low_no_branch, high_no_branch, None)

        return l_branch, l_no_branch
    
    @classmethod
    def tricky_le(cls, l_branch, l_no_branch, val1, val2):
        if val1.index is not None and val2.is_constant():
            new_h = max(val1.h, val2.h+1)
            new_l = max(val1.l, val2.h+1)
            l_no_branch[val1.index] = cls.checked(new_l, new_h, None)
            
            new_h = val2.l
            new_l = min(val1.l, new_h)
            l_branch[val1.index] = cls.checked(new_l, new_h, None)

        elif val2.index is not None and val1.is_constant():
            new_h = val1.l-1
            new_l = min(val1.l, new_h)
            l_no_branch[val2.index] = cls.checked(new_l, new_h, None)
            
            new_l = max(val1.h, val2.l)
            new_h = max(new_l, val2.h) 
            l_branch[val2.index] = cls.checked(new_l, new_h, None)

        return l_branch, l_no_branch

    def is_constant(self):
        return self.l == self.h

    @classmethod
    def wide1(cls, v1, v2):
        return cls.checked(min(v1.l, v2.l), max(v1.h, v2.h)) 
    
    def cpy_set_index(self, index):
        return self.checked(self.l, self.h, index)
    
    def cpy(self):
        return self.checked(self.l, self.h)

    def __iter__(self):
        for elem in [self.l, self.h]:
            yield elem 

    def __add__(self, other):
        assert(isinstance(other, Interval))
        return self.checked(self.l + other.l, self.h + other.h, self.index)  
        
    def __sub__(self, other):
        assert( isinstance(other, Interval))        
        return self.checked(self.l - other.h, self.h - other.l, self.index)

    def __mul__(self, other): 
        assert( isinstance(other, Interval))
        pairs = [(n1, n2) for n1 in list(self) for n2 in list(other)]
        results = list(map(lambda tup: tup[0]*tup[1], pairs))

        return self.checked(min(results), max(results))
    
    def __truediv__(self, other):  # integer division
        assert( isinstance(other, Interval))
        if 0 in range(other.l, other.h+1): return ExceptionType.ArithmeticException
        
        pairs = [(n1, n2) for n1 in list(self) for n2 in list(other)]
        results = list(map(lambda tup: int(tup[0] / tup[1]), pairs))

        return self.checked(min(results), max(results))
    
    def __mod__(self, other):  # integer division
        assert( isinstance(other, Interval))
        if 0 in range(other.l, other.h+1): return ExceptionType.ArithmeticException
        
        pairs = [(n1, n2) for n1 in list(self) for n2 in list(other)]
        results = list(map(lambda tup: tup[0] % tup[1], pairs))

        return self.checked(min(results), max(results))
    
    def __gt__(self, other):
        assert(isinstance(other, Interval))
        return self.l > other.h

    def __ge__(self, other):
        assert(isinstance(other, Interval)) 
        return self.l >= other.h

    def __lt__(self, other):
        assert(isinstance(other, Interval))
        return self.h < other.l

    def __le__(self, other): 
        assert(isinstance(other, Interval))
        return self.h <= other.l

    # We can't overwrite these because gives trouble when checking if states are equal in merge
    def eq(self, other):
        assert(isinstance(other, Interval)) 
        return self.l == other.l and self.h == other.h and self.is_constant() 
    
    def neq(self, other): 
        return self.__lt__(other) or self.__gt__(other)