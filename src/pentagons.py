from dataclasses import dataclass
from helpers_constants import *
from copy import deepcopy
from intervals import * 
from functools import reduce

@dataclass(frozen=True)
class Pentagon: # Integers represented as intervals 
    intv: Interval 
    greater_variables: set # instance is strictly less than elements in this set. 
    
    @classmethod
    def from_type(cls, typename, index=None, heap_ptr=None):
        if typename == "int" or typename == "float":
            intv = Interval.from_type(typename, index=index, heap_ptr=heap_ptr)
            return Pentagon(intv, set()) 
        else:
            raise Exception("Type not implemented")

    @classmethod 
    def from_value(cls, value, index=None, heap_ptr=None): # From value field in bytecode json
        if value["type"] == "integer":
            intv = Interval.from_integer(value["value"], index=index, heap_ptr=heap_ptr)
            return Pentagon(intv, set()) 
        else:
            raise Exception("Type not implemented")

    @classmethod 
    def from_integer(cls, value, index=None, heap_ptr=None):
        return cls.checked(value, value, index=index, heap_ptr=heap_ptr)

    @classmethod # RECONSIDER THIS
    def checked(cls, l, h, index=None, heap_ptr=None, strictly_lt=set()):
        if l > h:
            raise Exception("ASDADADDA")
        
        intv = Interval.checked(l, h, index=index, heap_ptr=heap_ptr)
        return Pentagon(intv, strictly_lt) 
    
    @classmethod # This method creates an array. Not sure how to represent the items. preferably a set. look at Formal Methods an Appetizer p. 55. Maybe not important since we focus on bounds.
    def generate_array(cls, arr_ref=None, count=None, init_val=None): 
        if count == None: count = cls.checked(0, INT_MAX, heap_ptr=arr_ref)
        if init_val == None: init_val = cls.checked(0, 0, heap_ptr=arr_ref) # default value 0 in java
        return (count, init_val)
    
    @classmethod  # using definition from two column version of the article. 2008
    def widen_set(cls, v1, v2):
        if v1.greater_variables >= v2.greater_variables: return v2.greater_variables
        else: return set()

    @classmethod # slides and p. 228 in book. more so p. 228. K is the set of integers explicitly mentioned in bytecode. 
    def wide(cls, v1, v2, K):
        if is_exception(v1): return v1
        if is_exception(v2): return v2 # hmmm ?
        if isinstance(v1, str): # In case of references
            assert v1 == v2
            return v1 
        
        intv = Interval.wide(v1.intv, v2.intv, K)
        strictly_lt = cls.widen_set(v1, v2)
        return Pentagon(intv, strictly_lt) 

    # When manipulating array values. Used in array_store 
    # expect arr is (count, val). if count == 1 replace val by new val. else take min max etc such that old is included in new
    @classmethod
    def handle_array(cls, arr, new_val, arr_ref, state):
        count = arr[0].intv
        items = arr[1].intv 
        
        count, items = Interval.handle_array((count, items), new_val.intv, arr_ref, state)
        
        return (Pentagon(count, arr[0].greater_variables), Pentagon(items, arr[1].greater_variables))

    @classmethod # Check if p1 is a program variable that appears in p2s set of variables greater than p2
    def p1_in_p2_gt_set(cls, p1, p2):
        return (p1.intv.index is not None and p1.intv.index in p2.greater_variables) \
            or (p1.intv.heap_ptr is not None and p1.intv.heap_ptr in p2.greater_variables)

    @classmethod # Refactor pleaseeeee
    def tricky_gt(cls, l_branch, l_no_branch, val1, val2, state):
        intv1_branch, intv1_no_branch, intv2_branch, intv2_no_branch = Interval.adjust_values_gt(val1.intv, val2.intv)
        
        if val1.intv.index is not None:
            val1_branch_set = val1.greater_variables - val2.get_ptrs() # Remove v2 from v1 set if there
            val1_no_branch_set = val1.greater_variables - val2.get_ptrs()   # We have to remove v2 (if it is there) because leq may be equal
            
            if val2.intv.is_constant():
                l_branch[val1.intv.index] = Pentagon(intv1_branch, val1_branch_set) 
                l_no_branch[val1.intv.index] = Pentagon(intv1_no_branch, val1_no_branch_set) 
            else: 
                l_branch[val1.intv.index] = Pentagon(deepcopy(val1.intv), val1_branch_set) 
                l_no_branch[val1.intv.index] = Pentagon(deepcopy(val1.intv), val1_no_branch_set) 
 
        if val2.intv.index is not None:
            val2_branch_set = val2.greater_variables | val1.get_ptrs() | val1.greater_variables # Know we know v1 > v2, which means all variables greater than v1 also greater than v2 
            val2_no_branch_set = val2.greater_variables - val1.get_ptrs() # We have to remove becaue maybe eq
 
            if val1.intv.is_constant():
                l_branch[val2.intv.index] = Pentagon(intv2_branch, val2_branch_set)
                l_no_branch[val2.intv.index] = Pentagon(intv2_no_branch, val2_no_branch_set)
            else:
                l_branch[val2.intv.index] = Pentagon(deepcopy(val2.intv), val2_branch_set)
                l_no_branch[val2.intv.index] = Pentagon(deepcopy(val2.intv), val2_no_branch_set)
 
        return (l_branch, l_no_branch)

    @classmethod
    def tricky_ge(cls, l_branch, l_no_branch, val1, val2, state):
        intv1_branch, intv1_no_branch, intv2_branch, intv2_no_branch = Interval.adjust_values_ge(val1.intv, val2.intv)
        
        if val1.intv.index is not None:
            val1_branch_set = val1.greater_variables - val2.get_ptrs() # We can not longer know for sure v1 > v2 so remove v2 from v1s set if it was there 
            val1_no_branch_set = val1.greater_variables | val2.get_ptrs() | val2.greater_variables # v1 < v2
            
            if val2.intv.is_constant():
                l_branch[val1.intv.index] = Pentagon(intv1_branch, val1_branch_set) 
                l_no_branch[val1.intv.index] = Pentagon(intv1_no_branch, val1_no_branch_set) 
            else: 
                l_branch[val1.intv.index] = Pentagon(deepcopy(val1.intv), val1_branch_set) 
                l_no_branch[val1.intv.index] = Pentagon(deepcopy(val1.intv), val1_no_branch_set) 
 
        if val2.intv.index is not None:
            val2_branch_set = val2.greater_variables - val1.get_ptrs() # We can not longer know for sure v1 > v2 so remove from set if it was there 
            val2_no_branch_set = val2.greater_variables - val1.get_ptrs()
 
            if val1.intv.is_constant():
                l_branch[val2.intv.index] = Pentagon(intv2_branch, val2_branch_set)
                l_no_branch[val2.intv.index] = Pentagon(intv2_no_branch, val2_no_branch_set)
            else:
                l_branch[val2.intv.index] = Pentagon(deepcopy(val2.intv), val2_branch_set)
                l_no_branch[val2.intv.index] = Pentagon(deepcopy(val2.intv), val2_no_branch_set)
 
        return (l_branch, l_no_branch)
        """ if val1.intv.index is not None and val2.intv.is_constant():
            new_h = max(val1.intv.h, val2.intv.h)
            new_l = max(val1.intv.l, val2.intv.h)
            l_branch[val1.intv.index] = Pentagon(Interval.checked(new_l, new_h, None), val1.greater_variables - val2.get_ptrs()) # We can not longer know for sure v1 > v2 so remove v2 from v1s set if it was there 
            
            new_h = val2.intv.l - 1 # REVIEW THIS
            new_l = min(val1.intv.l, new_h)
            l_no_branch[val1.intv.index] = Pentagon(Interval.checked(new_l, new_h, None), val1.greater_variables | val2.get_ptrs() | val2.greater_variables) # v1 < v2

        elif val2.intv.index is not None and val1.intv.is_constant():
            new_h = val1.intv.l
            new_l = min(val2.intv.l, new_h)
            l_branch[val2.intv.index] = Pentagon(Interval.checked(new_l, new_h, None), val2.greater_variables - val1.get_ptrs()) # We can not longer know for sure v1 > v2 so remove from set if it was there 
            new_h = max(val1.intv.h+1, val2.intv.h)
            new_l = max(val2.intv.l, new_h)
            l_no_branch[val2.intv.index] = Pentagon(Interval.checked(new_l, new_h, None), val2.greater_variables - val1.get_ptrs())

        return (l_branch, l_no_branch) """
    
    @classmethod 
    def tricky_lt(cls, l_branch, l_no_branch, val1, val2, state):
        intv1_branch, intv1_no_branch, intv2_branch, intv2_no_branch = Interval.adjust_values_lt(val1.intv, val2.intv)
        
        if val1.intv.index is not None:
            val1_branch_set = val1.greater_variables | val2.get_ptrs() | val2.greater_variables # v1 < v2. add to set accordingly
            val1_no_branch_set = val1.greater_variables - val2.get_ptrs() # v1 <= v2. remove v2 from v1 set if there
            
            if val2.intv.is_constant():
                l_branch[val1.intv.index] = Pentagon(intv1_branch, val1_branch_set) 
                l_no_branch[val1.intv.index] = Pentagon(intv1_no_branch, val1_no_branch_set) 
            else: 
                l_branch[val1.intv.index] = Pentagon(deepcopy(val1.intv), val1_branch_set) 
                l_no_branch[val1.intv.index] = Pentagon(deepcopy(val1.intv), val1_no_branch_set) 
 
        if val2.intv.index is not None:
            val2_branch_set = val2.greater_variables - val1.get_ptrs()
            val2_no_branch_set = val2.greater_variables - val1.get_ptrs()
 
            if val1.intv.is_constant():
                l_branch[val2.intv.index] = Pentagon(intv2_branch, val2_branch_set)
                l_no_branch[val2.intv.index] = Pentagon(intv2_no_branch, val2_no_branch_set)
            else:
                l_branch[val2.intv.index] = Pentagon(deepcopy(val2.intv), val2_branch_set)
                l_no_branch[val2.intv.index] = Pentagon(deepcopy(val2.intv), val2_no_branch_set)
 
        return (l_branch, l_no_branch)
        """ if val1.intv.index is not None and val2.intv.is_constant():
            high_branch = val2.intv.l-1
            low_branch = min(val1.intv.l, high_branch)
            l_branch[val1.intv.index] = Pentagon(Interval.checked(low_branch, high_branch, None), val1.greater_variables | val2.get_ptrs() | val2.greater_variables) # v1 < v2. add to set accordingly

            high_no_branch = max(val1.intv.h, val2.intv.h)
            low_no_branch = val2.intv.h
            l_no_branch[val1.intv.index] = Pentagon(Interval.checked(low_no_branch, high_no_branch, None), val1.greater_variables - val2.get_ptrs()) # v1 <= v2. remove v2 from v1 set if there

        elif val2.intv.index is not None and val1.intv.is_constant():
            high_branch = max(val1.intv.h+1, val2.intv.h)
            low_branch = max(val1.intv.h+1, val2.intv.l)
            l_branch[val2.intv.index] = Pentagon(Interval.checked(low_branch, high_branch), val2.greater_variables - val1.get_ptrs())

            high_no_branch = min(val1.intv.l, val2.intv.h)
            low_no_branch = min(high_no_branch, val2.intv.l)
            l_no_branch[val2.intv.index] = Pentagon(Interval.checked(low_no_branch, high_no_branch, None), val2.greater_variables - val1.get_ptrs())

        if val1.intv.index is not None:
            l_branch[val1.intv.index] = Pentagon(Interval.checked(val1.intv.l, val1.intv.h, None), val1.greater_variables | val2.get_ptrs() | val2.greater_variables) # v1 < v2. add to set accordingly 
            l_no_branch[val1.intv.index] = Pentagon(Interval.checked(val1.intv.l, val1.intv.h, None), val1.greater_variables - val2.get_ptrs()) # v1 <= v2. remove v2 from v1 set if there

        elif val2.intv.index is not None and val1.intv.is_constant():
            l_branch[val2.intv.index] = Pentagon(Interval.checked(val2.intv.l, val2.intv.h), val2.greater_variables - val1.get_ptrs()) 
            l_no_branch[val2.intv.index] = Pentagon(Interval.checked(val2.intv.l, val2.intv.h, None), val2.greater_variables - val1.get_ptrs())

        return l_branch, l_no_branch """
    
    @classmethod
    def tricky_le(cls, l_branch, l_no_branch, val1, val2, state):
        intv1_branch, intv1_no_branch, intv2_branch, intv2_no_branch = Interval.adjust_values_le(val1.intv, val2.intv)
        
        if val1.intv.index is not None:
            val1_branch_set = val1.greater_variables - val2.get_ptrs()
            val1_no_branch_set = val1.greater_variables - val2.get_ptrs()
            
            if val2.intv.is_constant():
                l_branch[val1.intv.index] = Pentagon(intv1_branch, val1_branch_set) 
                l_no_branch[val1.intv.index] = Pentagon(intv1_no_branch, val1_no_branch_set) 
            else: 
                l_branch[val1.intv.index] = Pentagon(deepcopy(val1.intv), val1_branch_set) 
                l_no_branch[val1.intv.index] = Pentagon(deepcopy(val1.intv), val1_no_branch_set) 
 
        if val2.intv.index is not None:
            val2_branch_set = val2.greater_variables - val1.get_ptrs()
            val2_no_branch_set = val2.greater_variables | val1.get_ptrs() | val2.greater_variables
 
            if val1.intv.is_constant():
                l_branch[val2.intv.index] = Pentagon(intv2_branch, val2_branch_set)
                l_no_branch[val2.intv.index] = Pentagon(intv2_no_branch, val2_no_branch_set)
            else:
                l_branch[val2.intv.index] = Pentagon(deepcopy(val2.intv), val2_branch_set)
                l_no_branch[val2.intv.index] = Pentagon(deepcopy(val2.intv), val2_no_branch_set)
 
        return (l_branch, l_no_branch)

        """ if val1.intv.index is not None and val2.intv.is_constant():
            new_h = val2.intv.l
            new_l = min(val1.intv.l, new_h)
            l_branch[val1.intv.index] = Pentagon(Interval.checked(new_l, new_h, None), val1.greater_variables - val2.get_ptrs())

            new_h = max(val1.intv.h, val2.intv.h+1)
            new_l = max(val1.intv.l, val2.intv.h+1)
            l_no_branch[val1.intv.index] = Pentagon(Interval.checked(new_l, new_h, None), val1.greater_variables - val2.get_ptrs())
            
        elif val2.intv.index is not None and val1.intv.is_constant():
            new_l = max(val1.intv.h, val2.intv.l)
            new_h = max(new_l, val2.intv.h) 
            l_branch[val2.intv.index] = Pentagon(Interval.checked(new_l, new_h, None), val2.greater_variables - val1.get_ptrs())

            new_h = val1.intv.l-1
            new_l = min(val1.intv.l, new_h)
            l_no_branch[val2.intv.index] = Pentagon(Interval.checked(new_l, new_h, None), val2.greater_variables | val1.get_ptrs() | val2.greater_variables)

        if val1.intv.index is not None: 
            l_branch[val1.intv.index] = Pentagon(Interval.checked(val1.intv.l, val1.intv.h, None), val1.greater_variables - val2.get_ptrs())            
            l_no_branch[val1.intv.index] = Pentagon(Interval.checked(val1.intv.l, val1.intv.h, None), val1.greater_variables - val2.get_ptrs())

        if val2.intv.index is not None:
            l_branch[val2.intv.index] = Pentagon(Interval.checked(val2.intv.l, val2.intv.h, None), val2.greater_variables - val1.get_ptrs())
            l_no_branch[val2.intv.index] = Pentagon(Interval.checked(val2.intv.l, val2.intv.h, None), val2.greater_variables | val1.get_ptrs() | val2.greater_variables)

        return l_branch, l_no_branch """

    @classmethod
    def negate(cls, val):
        intv = Interval.negate(val.intv)
        return Pentagon(intv, set())

    def get_ptrs(self):
        ptrs = set()
        if self.intv.index is not None: ptrs.add(self.intv.index)
        if self.intv.heap_ptr is not None: ptrs.add(self.intv.heap_ptr)
        return ptrs

    def is_constant(self):
        return self.l == self.h
 
    def cpy_set_ptrs(self, index=None, heap_ptr=None):
        intv = self.intv.checked(self.intv.l, self.intv.h, index, heap_ptr)
        return Pentagon(intv, deepcopy(self.greater_variables))
    
    def cpy_set_index(self, index):
        return self.checked(self.l, self.h, index)
    
    def cpy(self):
        return self.checked(self.l, self.h)

    @classmethod 
    def cpy_ptrs(cls, v1, v2_copy_these_ptrs):
        return Pentagon(Interval.cpy_ptrs(v1.intv, v2_copy_these_ptrs.intv), v1.greater_variables) 
 
    def __iter__(self):
        for elem in [self.l, self.h]:
            yield elem 

    def __add__(self, other):
        assert(isinstance(other, Pentagon))        
        if other.intv.is_negative():
            return self.__sub__(other)
        intv = self.intv + other.intv # Come back and refine maybe
        return Pentagon(intv, set())
        
    def __sub__(self, other):
        assert( isinstance(other, Pentagon))
        if Pentagon.p1_in_p2_gt_set(self, other): meet_val = Interval(1, INT_MAX) # if self > other  
        else: meet_val = Interval(INT_MIN, INT_MAX)  
        
        intv = Interval.meet(self.intv - other.intv, meet_val)

        greater_vars = self.get_ptrs() | self.greater_variables if other.intv.l > 0 else set() 

        return Pentagon(intv, greater_vars) 

    def __mul__(self, other): # Come back and refine
        assert(isinstance(other, Pentagon))
        intv = self.intv * other.intv
        return Pentagon(intv, set()) 
    
    def __truediv__(self, other):  # integer division
        assert( isinstance(other, Pentagon))
        if 0 in range(other.intv.l, other.intv.h+1): return ExceptionType.ArithmeticException
        
        intv = self.intv / other.intv 

        return Pentagon(intv, set()) 
    
    def __mod__(self, other):  # By using fmod in interval __mod__ i think we achieved same mod semantics as java. 
        assert( isinstance(other, Pentagon))
        if 0 in range(other.intv.l, other.intv.h+1): return ExceptionType.ArithmeticException
        
        intv = self.intv % other.intv 
        greater_vars = other.get_ptrs() if other.intv.l >= 0 else set()

        return Pentagon(intv, greater_vars) 
    
    def gt(self, other, state):
        assert(isinstance(other, Pentagon))
        if self.intv.index is not None and self.intv.index in other.greater_variables:
            return True 
        if self.intv.heap_ptr is not None and self.intv.heap_ptr in other.greater_variables:
            return True  
        if self.intv.gt(other.intv, state): 
            return True
        return False        

    def ge(self, other, state):
        assert(isinstance(other, Pentagon)) 
        if self.intv.index is not None and self.intv.index in other.greater_variables:
            return True 
        if self.intv.heap_ptr is not None and self.intv.heap_ptr in other.greater_variables:
            return True  
        if self.intv.ge(other.intv, state): 
            return True
        return False 

    def lt(self, other, state): # Two column version p. 186 bottom of page. Actually we need the entire state for this. No no no talks about ORDER  not this. 
        assert(isinstance(other, Pentagon)) 
        if other.intv.index is not None and other.intv.index in self.greater_variables:
            return True
        if other.intv.heap_ptr is not None and other.intv.heap_ptr in self.greater_variables:
            return True
        if self.intv.lt(other.intv, state): 
            return True
        return False

    def le(self, other, state): 
        assert(isinstance(other, Pentagon))
        if other.intv.index is not None and other.intv.index in self.greater_variables:
            return True
        if other.intv.heap_ptr is not None and other.intv.heap_ptr in self.greater_variables:
            return True
        if self.intv.le(other.intv, state):
            return True 
        return False
 
    def eq(self, other, state):
        assert(isinstance(other, Pentagon)) 
        return self.intv.eq(other.intv, state)
    
    def neq(self, other, state):
        assert(isinstance(other, Pentagon))
        return  self.lt(other, state) or self.gt(other, state) or self.intv.neq(other.intv, state)
    
    @classmethod
    def within_bounds(cls, arr, index):
        length, _ = arr
        if type(length) != type(index): raise Exception("Type error") 
        
        # GET RID OF STATE PARAMETER if we do not need it. 
        return index.lt(length, None) and index.intv >= Interval.from_integer(0)
        
        
        
       
       
       

       
    