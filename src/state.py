from dataclasses import dataclass
from helpers_constants import *
from copy import deepcopy 

@dataclass(frozen=True)
class State: # State consists of local variables, operand stack and heap
    locals: dict
    stack: list 
    heap: dict

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
    def store(cls, old_state, index):
        ns = deepcopy(old_state)
        ns.locals[index] = ns.stack.pop()  

        return ns
    




    
    
    

