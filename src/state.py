from dataclasses import dataclass
from helpers_constants import *
from copy import deepcopy 
from typing import Optional

@dataclass(frozen=True)
class State: # State consists of local variables, operand stack and heap
    locals: dict
    stack: list 
    heap: dict
    exception: Optional[ExceptionType] = None # Store exception in state. Check for exceptions and stop interpretation if so somewhere else. 

    @classmethod
    def cpy(cls, other):
        return deepcopy(other)

    @classmethod
    def add_to_locals(cls, old_state, index, value):
        ns = deepcopy(old_state)
        ns.locals[index] = value 

        return ns 

    @classmethod
    def add_to_stack(cls, old_state, value):
        return State(deepcopy(old_state.locals), deepcopy(old_state.stack) + [value], deepcopy(old_state.heap)) 

    @classmethod
    def add_to_heap(cls, old_state, key, value):
        nh = deepcopy(old_state.heap)
        nh[key] = value

        return State(deepcopy(old_state.locals), deepcopy(old_state.stack), nh) 

    @classmethod
    def new_stack(cls, old_state, new_stack): 
        return State(deepcopy(old_state.locals), new_stack, deepcopy(old_state.heap))
    
    @classmethod
    def new_locals(cls, old_state, new_locals): 
        return State(new_locals, deepcopy(old_state.stack), deepcopy(old_state.heap))
 
    @classmethod
    def store(cls, old_state, index):
        ns = deepcopy(old_state)
        ns.locals[index] = ns.stack.pop()  

        return ns
    
    @classmethod
    def new_locals_new_stack(cls, old_state, new_locals, new_stack):
        heap = deepcopy(old_state.heap)
        return State(new_locals, new_stack, heap)
    
    @classmethod
    def new_stack_new_heap(cls, old_state, new_stack, new_heap):
        locals = deepcopy(old_state.locals)
        return State(locals, new_stack, new_heap)
    
    # use *args for things like K in the intervals widening etc. 
    @classmethod
    def merge_locals(cls, old_locals, new_locals, wide, *args):
        union = set(old_locals) | set(new_locals)
        merged = {}
 
        for i in union:
            if i in old_locals and new_locals:
                merged[i] = wide(old_locals[i], new_locals[i], *args)
            elif i in old_locals:
                merged[i] = deepcopy(old_locals[i])
            else: 
                merged[i] = deepcopy(new_locals[i])
        
        return merged 

    @classmethod
    def merge_stacks(cls, old_stack, new_stack, wide, *args):

        assert len(old_stack) == len(new_stack)
        return [wide(o, n, *args) for o,n in zip(old_stack, new_stack)]

    @classmethod
    def merge_heaps(cls, old_heap, new_heap, wide, args):
        return {} 

    @classmethod
    def merge(cls, old_state, new_state, wide, *args): 
        if old_state == None: 
            return new_state
        
        # merged locals, merged stack and merged heap
        mlc = cls.merge_locals(old_state.locals, new_state.locals, wide, *args) 
        ms = cls.merge_stacks(old_state.stack, new_state.stack, wide, *args) 
        mh = cls.merge_heaps(old_state.heap, new_state.heap, wide, *args)

        
        # This looks a bit weird. But we stop at the first exception. So old state should not have one. include in merge because makes things easier
        e = new_state.exception

        return State(mlc, ms, mh, e)
    
    # Not a classmethod on purpose. should it be though? 
    def is_exception_state(self):
        return is_exception(self.exception)