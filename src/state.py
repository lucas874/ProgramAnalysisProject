from dataclasses import dataclass
from helpers_constants import *
from copy import deepcopy 

@dataclass(frozen=True)
class State: # State consists of local variables, operand stack and heap
    locals: dict
    stack: list 
    heap: dict

    @classmethod
    def cpy(cls, other):
        return deepcopy(other)

    @classmethod
    def add_to_locals(cls, old_state, index, value):
        ns = deepcopy(old_state)
        ns.locals[index] = value 
        print(id(old_state.locals), id(old_state.stack), id(old_state.heap))
        print(id(ns.locals), id(ns.stack), id(ns.heap))
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
    
    # use *args for things like K in the intervals widening etc. 
    @classmethod
    def merge_locals(cls, old_locals, new_locals, wide, *args):
        union = set(old_locals) | set(new_locals)
        merged = {}
        print("UNION IS: ", union) 
        print("OLD LOCALS: ", old_locals, "NEW LOCALS: ", new_locals)
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
        print("OLD STACK ", old_stack)
        print("NEW STACK ", new_stack)
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

        return State(mlc, ms, mh)



    
    
    

