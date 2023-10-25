from dataclasses import dataclass
from helpers_constants import *

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

    @classmethod
    def checked(cls, l, h, index=None):
        if l > h:
            raise Exception("ASDADADDA")
        return Interval(max(l, INT_MIN), min(h, INT_MAX), index)

    @classmethod # slides and p. 228 in book. more so p. 228. K is the set of integers explicitly mentioned in bytecode. 
    def wide(cls, v1, v2, K):
        if v1 in EXCEPTIONS: return v1
        if v2 in EXCEPTIONS: return v2 # hmmm ?
        return cls.checked(cls.LB_k(v1.l, v2.l, K), cls.UB_k(v1.h, v2.h, K)) 
    
    # LBk UBk Principles of Program Analysis p.228. 
    @classmethod # Gives a lot of min/max when slie one would have given z3/z4??
    def LB_k(cls, z1, z3, K):
        if z1 <= z3: return z1
        elif z1 > z3:
            ks = [k for k in K if k <= z3]
            if ks != []: return max(ks)
            else: return INT_MIN

    def UB_k(z2, z4, K):
        if z4 <= z2: return z2
        elif z4 > z2:
            ks = [k for k in K if z4 <= k]
            if ks != []: return min(ks)
            else: return INT_MAX
 
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
        if 0 in range(other.l, other.h+1): return ArithException
        
        pairs = [(n1, n2) for n1 in list(self) for n2 in list(other)]
        results = list(map(lambda tup: int(tup[0] / tup[1]), pairs))

        return self.checked(min(results), max(results))
    
    def __mod__(self, other):  # integer division
        assert( isinstance(other, Interval))
        if 0 in range(other.l, other.h+1): return ArithException
        
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

    def __eq__(self, other):
        assert(isinstance(other, Interval))
        return self.l == other.l and self.h == other.h 
    
    def __neq__(self, other):
        return not(self.__eq__(other))

