from dataclasses import dataclass
from helpers_constants import *
from copy import deepcopy
from intervals import * 

@dataclass(frozen=True)
class Pentagon: # Integers represented as intervals 
    intv: Interval
    index: int # Use when loading from locals 
    strictly_less_than: set

    @classmethod
    def from_type(cls, typename):
        if typename == "int" or typename == "float":
            return Pentagon(Interval.from_type(typename), None, set())
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
    def checked(cls, l, h, index=None, strictly_lt=set()):
        if l > h:
            raise Exception("ASDADADDA")
        return Pentagon(Interval.checked(l, h, index), index, strictly_lt)

    # TODO
    @classmethod # This method creates an array. Not sure how to represent the items. preferably a set. look at Formal Methods an Appetizer p. 55. Maybe not important since we focus on bounds.
    def generate_array(cls, count=None, init_val=None):
        if count == None: count = cls.checked(0, INT_MAX)
        if init_val == None: init_val = cls.checked(INT_MIN, INT_MAX)
        return (count, init_val)

    @classmethod  # using definition from two column version of the article. 2008
    def widen_set(cls, v1, v2):
        if v1.strictly_less_than >= v2.strictly_less_than: return v2.strictly_less_than
        else: return set()

    @classmethod # slides and p. 228 in book. more so p. 228. K is the set of integers explicitly mentioned in bytecode. 
    def wide(cls, v1, v2, K):
        intv = Interval.wide(v1.intv, v2.intv, K)
        strictly_lt = cls.widen_set(v1, v2)
        return cls.checked(intv.l, intv.h, index=None, strictly_lt=strictly_lt) # What about index?
        
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
        assert(isinstance(other, Pentagon))
        return self.checked(self.l + other.l, self.h + other.h, self.index)  
        
    def __sub__(self, other):
        assert( isinstance(other, Pentagon))        
        return self.checked(self.l - other.h, self.h - other.l, self.index)

    def __mul__(self, other): 
        assert( isinstance(other, Pentagon))
        pairs = [(n1, n2) for n1 in list(self) for n2 in list(other)]
        results = list(map(lambda tup: tup[0]*tup[1], pairs))

        return self.checked(min(results), max(results))
    
    def __truediv__(self, other):  # integer division
        assert( isinstance(other, Pentagon))
        if 0 in range(other.l, other.h+1): return ExceptionType.ArithmeticException
        
        pairs = [(n1, n2) for n1 in list(self) for n2 in list(other)]
        results = list(map(lambda tup: int(tup[0] / tup[1]), pairs))

        return self.checked(min(results), max(results))
    
    def __mod__(self, other):  # integer division
        assert( isinstance(other, Pentagon))
        if 0 in range(other.l, other.h+1): return ExceptionType.ArithmeticException
        
        pairs = [(n1, n2) for n1 in list(self) for n2 in list(other)]
        results = list(map(lambda tup: tup[0] % tup[1], pairs))

        return self.checked(min(results), max(results))
    
    def __gt__(self, other):
        assert(isinstance(other, Pentagon))
        return self.l > other.h

    def __ge__(self, other):
        assert(isinstance(other, Pentagon)) 
        return self.l >= other.h

    def __lt__(self, other):
        assert(isinstance(other, Pentagon))
        return self.h < other.l

    def __le__(self, other): 
        assert(isinstance(other, Pentagon))
        return self.h <= other.l

    # We can't overwrite these because gives trouble when checking if states are equal in merge
    def eq(self, other):
        assert(isinstance(other, Pentagon)) 
        return self.l == other.l and self.h == other.h and self.is_constant() 
    
    def neq(self, other): 
        return self.__lt__(other) or self.__gt__(other)