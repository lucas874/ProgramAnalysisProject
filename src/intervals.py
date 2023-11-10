from dataclasses import dataclass
from helpers_constants import *
from copy import deepcopy
from typing import Optional
from math import fmod
from state import State

@dataclass(frozen=True)
class Interval: # Integers represented as intervals 
    l: int
    h: int
    index: Optional[int] = None # Use when loading from locals 
    heap_ptr: Optional[str] = None

    @classmethod
    def from_type(cls, typename, index=None, heap_ptr=None):
        if typename == "int" or typename == "float":
            return Interval(INT_MIN, INT_MAX, index, heap_ptr)
        else:
            raise Exception("Type not implemented")

    @classmethod 
    def from_value(cls, value, index=None, heap_ptr=None): # From value field in bytecode json
        if value["type"] == "integer":
            return cls.from_integer(value["value"], index=index, heap_ptr=heap_ptr)
        else:
            raise Exception("Type not implemented")

    @classmethod 
    def from_integer(cls, value, index=None, heap_ptr=None):
        return cls.checked(value, value, index=index, heap_ptr=heap_ptr)

    @classmethod # RECONSIDER THIS
    def checked(cls, l, h, index=None, heap_ptr=None):
        if l > h:
            raise Exception("ASDADADDA")
        return Interval(max(l, INT_MIN), min(h, INT_MAX), index, heap_ptr)
    
    @classmethod # This method creates an array. Not sure how to represent the items. preferably a set. look at Formal Methods an Appetizer p. 55. Maybe not important since we focus on bounds.
    def generate_array(cls, arr_ref=None, count=None, init_val=None):
        if count == None: count = cls.checked(0, INT_MAX, heap_ptr=arr_ref)
        if init_val == None: init_val = cls.checked(0, 0, heap_ptr=arr_ref) # default value 0 in java
        return (count, init_val)

    @classmethod # slides and p. 228 in book. more so p. 228. K is the set of integers explicitly mentioned in bytecode. 
    def wide(cls, v1, v2, K):
        if is_exception(v1): return v1
        if is_exception(v2): return v2 # hmmm ?
        if isinstance(v1, str): # In case of references
            assert v1 == v2
            return v1
        #if v1.index != None: assert v1.index == v2.index # REVIEW INDEX CHECK
        #if v1.heap_ptr != None or v2.heap_ptr != None: # CONSIDER does not have to be the same like in neverThrows3 arrays. but which one do we pick? Should be none in that case...
            #print(v1.heap_ptr, v2.heap_ptr)
            #assert v1.heap_ptr == v2.heap_ptr 
        return cls.checked(cls.LB_k(v1.l, v2.l, K), cls.UB_k(v1.h, v2.h, K), index=v1.index, heap_ptr=v1.heap_ptr) 
    
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

    @classmethod
    def meet(cls, v1, v2): #index??
        return cls.checked(max(v1.l, v2.l), min(v1.h, v2.h))

    # When manipulating array values. Used in array_store 
    # expect arr is (count, val). if count == 1 replace val by new val. else take min max etc such that old is included in new
    @classmethod
    def handle_array(cls, arr, new_val, arr_ref, state): 
        if arr[0].eq(cls.from_integer(1), state): 
            return (arr[0], Interval(new_val.l, new_val.h, index=arr[1].index, heap_ptr=arr[1].heap_ptr))
        else: 
            new_l = min(new_val.l, arr[1].l)
            new_h = max(new_val.h, arr[1].h) 
            return (arr[0], cls.checked(new_l, new_h, index=arr[1].index, heap_ptr=arr_ref))

    @classmethod
    def adjust_values_gt(cls, val1, val2):  # Return four intervals. Do like we do in the ifs with the values right now.
        val1_branch =  cls.checked(max(val1.l, val2.h+1), max(val1.h, val2.h+1), index=val1.index, heap_ptr=val1.heap_ptr) # val1_branch, val1_no_branch, val2_branch, val2_no_branch. Select which ones to use later 
        val1_no_branch = cls.checked(min(val1.l, val2.l), val2.l, index=val1.index, heap_ptr=val1.heap_ptr)
        val2_branch = cls.checked(min(val2.l, val1.l-1), val1.l-1, index=val2.index, heap_ptr=val2.heap_ptr)
        val2_no_branch = cls.checked(min(val1.h, max(val1.h, val2.h)), max(val1.h, val2.h), index=val2.index, heap_ptr=val2.heap_ptr)

        return val1_branch, val1_no_branch, val2_branch, val2_no_branch

    @classmethod
    def adjust_values_ge(cls, val1, val2):
        val1_branch = cls.checked(max(val1.l, val2.h), max(val1.h, val2.h), index=val1.index, heap_ptr=val1.heap_ptr)
        val1_no_branch = cls.checked(min(val1.l, val2.l - 1), val2.l - 1, index=val1.index, heap_ptr=val1.heap_ptr) # Review pls 
        val2_branch = cls.checked(min(val2.l, val1.l), val1.l, index=val2.index, heap_ptr=val2.heap_ptr)
        val2_no_branch = cls.checked(max(val2.l, val1.h+1), max(val1.h+1, val2.h), index=val2.index, heap_ptr=val2.heap_ptr)
        return val1_branch, val1_no_branch, val2_branch, val2_no_branch

    @classmethod
    def adjust_values_lt(cls, val1, val2):
        val1_branch = cls.checked(min(val1.l, val2.l-1), val2.l-1, index=val1.index, heap_ptr=val1.heap_ptr)
        val1_no_branch = cls.checked(val2.h, max(val1.h, val2.h), index=val1.index, heap_ptr=val1.heap_ptr)
        val2_branch = cls.checked(max(val1.h+1, val2.l), max(val1.h+1, val2.h), index=val2.index, heap_ptr=val2.heap_ptr)
        val2_no_branch = cls.checked(min(min(val1.l, val2.h), val2.l), min(val1.l, val2.h), index=val2.index, heap_ptr=val2.heap_ptr)

        return val1_branch, val1_no_branch, val2_branch, val2_no_branch

    @classmethod
    def adjust_values_le(cls, val1, val2): 
        val1_branch = cls.checked(min(val1.l, val2.l), val2.l, index=val1.index, heap_ptr=val1.heap_ptr)
        val1_no_branch = cls.checked(max(val1.l, val2.h+1), max(val1.h, val2.h+1), index=val1.index, heap_ptr=val1.heap_ptr)
        val2_branch = cls.checked(max(val1.h, val2.l), max(max(val1.h, val2.l), val2.h), index=val2.index, heap_ptr=val2.heap_ptr)
        val2_no_branch = cls.checked(min(val2.l, val1.l-1), val1.l-1, index=val2.index, heap_ptr=val2.heap_ptr)
        return val1_branch, val1_no_branch, val2_branch, val2_no_branch
    
    @classmethod
    def adjust_values(cls, val1, val2, op):
        match op:
            case "gt":
                return cls.adjust_values_gt(val1, val2)
            case "ge":
                return cls.adjust_values_ge(val1, val2)
            case "lt":
                return cls.adjust_values_lt(val1, val2)
            case "le":
                return cls.adjust_values_le(val1, val2)

    @classmethod
    def tricky_comparison(cls, val1, val2, state, new_stack, op):
        locals_branch = deepcopy(state.locals)
        stack_branch = new_stack 
        heap_branch = deepcopy(state.heap)
        locals_no_branch = deepcopy(state.locals)
        stack_no_branch = deepcopy(new_stack) 
        heap_no_branch = deepcopy(state.heap)

        val1_branch, val1_no_branch, val2_branch, val2_no_branch = cls.adjust_values(val1, val2, op)

        if val1.index is not None and val2.is_constant():
            locals_branch[val1.index] = val1_branch
            locals_no_branch[val1.index] = val1_no_branch
        elif val2.index is not None and val1.is_constant():
            locals_branch[val2.index] = val2_branch
            locals_no_branch[val2.index] = val2_no_branch

        if val1.heap_ptr is not None and val2.is_constant():
            heap_branch[val1.heap_ptr] = (val1_branch, heap_branch[val1.heap_ptr][1])
            heap_no_branch[val1.heap_ptr] = (val1_no_branch, heap_branch[val1.heap_ptr][1])
        elif val2.heap_ptr is not None and val1.is_constant():
            heap_branch[val2.heap_ptr] = (val2_branch, heap_branch[val2.heap_ptr][1])
            heap_no_branch[val2.heap_ptr] = (val2_no_branch, heap_branch[val2.heap_ptr][1])
        
        return (State(locals_branch, stack_branch, heap_branch), State(locals_no_branch, stack_no_branch, heap_no_branch)) 
  
    @classmethod
    def negate(cls, val):
        return cls.checked(-val.h, -val.l, index=val.index, heap_ptr=val.heap_ptr)

    def is_constant(self):
        return self.l == self.h

    def is_negative(self):
        return self.h < 0
    
    def is_positive(self):
        return self.h > 0
    
    def is_zero(self):
        return self.l == 0 and self.h == 0
    
    def cpy_set_ptrs(self, index=None, heap_ptr=None):
        return self.checked(self.l, self.h, index, heap_ptr)
    
    def cpy(self):
        return self.checked(self.l, self.h)

    @classmethod 
    def cpy_ptrs(cls, v1, other): 
        return Interval(v1.l, v1.h, other.index, other.heap_ptr)

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
        results = list(map(lambda tup: int(fmod(tup[0], tup[1])), pairs)) # Use fmod to get same mod semantics as java. see: https://en.wikipedia.org/wiki/Modulo#In_programming_languages

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

    def gt(self, other, state): # Updated. we need to use this functions when comparisons instead of overloaded directly bc of the way pentagons do comparisons and have the same interface
        return self > other
    
    def ge(self, other, state):
        return self >= other
    
    def lt(self, other, state):
        return self < other
    
    def le(self, other, state):
        return self <= other

    # We can't overwrite these because gives trouble when checking if states are equal in merge
    def eq(self, other, state):
        assert(isinstance(other, Interval)) 
        return self.l == other.l and self.h == other.h and self.is_constant() 
    
    def neq(self, other, state):
        assert(isinstance(other, Interval)) 
        return self.__lt__(other) or self.__gt__(other)
    
    @classmethod
    def within_bounds(cls, arr, index):
        length, _ = arr
        if type(length) != type(index): raise Exception("Type error")
        return index < length and index >= cls.from_integer(0)
    
    # corresponds to square bracket ordering. intv1 order intv2 if intv1.l >= intv2.l and intv1.h <= intv2.h. in other words intv1 included in intv2.
    def order(self, other):
        return self.l >= other.l and self.h <= other.h