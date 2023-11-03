from copy import deepcopy
import jmespath 
from intervals import Interval
from state import State
from helpers_constants import *

class Interpreter:
    def __init__(self, abstraction, program):
        self.abstraction = abstraction
        self.program = program # just needed for get... which could be hardcoded anyway
        self.arrays_allocated = 0 # have this field in interpreter is ok... maybe put in state but challenging because frozen

    def step(self, bc, state, i): 
            if bc["opr"] == "return":
                bc["opr"] = "return_m" # I know ugly but there were many :)
            if bc["opr"] == "if":
                bc["opr"] = "if_m"
            if hasattr(self, bc["opr"]):
                return getattr(self, bc["opr"])(bc, state, i) 
            else:
                raise Exception("Not implemented") 

    def push(self, bc, state, i): 
            value = self.abstraction.from_value(bc["value"])
            
            if "value" in bc:
                return [(State.add_to_stack(state, value), i+1)]
            else: 
                raise Exception("Review implementation of push")

    def pop(self, b, l, s, i):
        if b["words"] == 1:
            if len(s) < 1: raise Exception("Not enough values on stack") 
            return [(l, s[:-1], i + 1)]
        
        elif b["words"] == 2:
            if len(s) < 2: raise Exception("Not enough values on stack") 
            return [(l, s[:-2], i + 1)] 
         
    def return_m(self, bc, state, i): 
        return [(State.cpy(state), i)]  # what to return here
   
    def load(self, b, state, i):
        value = state.locals[b["index"]]
        if isinstance(value, self.abstraction): # could be some value of our abstraction type OR a reference so check.
            value = state.locals[b["index"]].cpy_set_index(b["index"])
          
        return [(State.add_to_stack(state, value), i+1)]   

    def binary(self, b, state, i): 
        if len(state.stack) < 2: raise Exception("Not enough operands on stack") # We must have at least two elements on stack
         
        val1 = state.stack[-2]
        val2 = state.stack[-1] 

        if type(val1) != type(val2): raise Exception("Type mismatch")

        new_stack = deepcopy(state.stack[:-2])

        match b["operant"]:
            case "add":
                #return [(l, s[:-2]+[val1 + val2], i+1)] 
                #new_stack += [val1 + val2]
                result = val1 + val2
            case "sub":
                #return [(l, s[:-2]+[val1 - val2], i+1)] 
                #new_stack += [val1 - val2]
                result = val1 - val2
            case "mul":
                #return [(l, s[:-2]+[val1 * val2], i+1)] 
                #new_stack += [val1 * val2]
                result = val1 * val2
            case "div": 
                #return [(l, s[:-2]+[val1 / val2], i+1)] # Exception checked in AbstractInt
                #new_stack += [val1 / val2]
                result = val1 / val2
            case "rem":
                #return [(l, s[:-2]+[val1 % val2], i+1)] 
                #new_stack += [val1 % val2]
                result = val1 % val2

        new_stack += [result]
        
        if is_exception(result): # Weird to include exception on stack too. but we do that so that we can merge states still 
            return [(State(deepcopy(state.locals), new_stack, deepcopy(state.heap), result), i+1)] 
        
        
        return [(State.new_stack(state, new_stack), i+1)] 
     
    def store(self, b, state, i): 
        idx = b["index"]
        # hope I understood it correctly. Think we remove the element from the operand stack too.
        return [(State.store(state, idx), i+1)] 

    def incr(self, b, state, i):
        #increment local in $index by $amount
         
        idx = b["index"]
        new_l = deepcopy(state.locals)
        
        new_l[idx] += self.abstraction.from_integer(b["amount"])
        
        return [(State.new_locals(state, new_l), i+1)]

    def goto(self, b, state, i): 
        return [(State.cpy(state), b["target"])]

    def conditional(self, b, state, val1, val2, new_stack, i): # lots of arguments, but this way we can use same function for if and ifz
        return_vals = []
        match b["condition"]:
            case "gt": # all cases except eq, neq follow this pattern. two 'easy cases' and a difficult case leading to two new states
                if val1 > val2: return_vals.append((State.new_stack(state, new_stack), b["target"])) # return state that is old state with two elements popped from stack jump to target address
                elif val1 <= val2: return_vals.append((State.new_stack(state, new_stack), i+1)) # same but jump to next address 
                else:
                    l_branch, l_no_branch = self.abstraction.tricky_gt(deepcopy(state.locals), deepcopy(state.locals), val1, val2)
                    return_vals = [(State.new_locals_new_stack(state, l_branch, new_stack), b["target"]), (State.new_locals_new_stack(state, l_no_branch, new_stack), i+1)]

            case "ge":
                if val1 >= val2: return_vals.append((State.new_stack(state, new_stack), b["target"]))
                elif val1 < val2: return_vals.append((State.new_stack(state, new_stack), i+1))
                else:
                    l_branch, l_no_branch = self.abstraction.tricky_ge(deepcopy(state.locals), deepcopy(state.locals), val1, val2)                     
                    return_vals = [(State.new_locals_new_stack(state, l_branch, new_stack), b["target"]), (State.new_locals_new_stack(state, l_no_branch, new_stack), i+1)] 

            case "lt":
                if val1 < val2: return_vals.append((State.new_stack(state, new_stack), b["target"]))
                elif val1 >= val2: return_vals.append((State.new_stack(state, new_stack), i+1)) 
                else: 
                    l_branch, l_no_branch = self.abstraction.tricky_lt(deepcopy(state.locals), deepcopy(state.locals), val1, val2)                     
                    return_vals = [(State.new_locals_new_stack(state, l_branch, new_stack), b["target"]), (State.new_locals_new_stack(state, l_no_branch, new_stack), i+1)]

            case "le": 
                if val1 <= val2: return_vals.append((State.new_stack(state, new_stack), b["target"]))
                elif val1 > val2: return_vals.append((State.new_stack(state, new_stack), i+1)) 
                else:  
                    l_branch, l_no_branch = self.abstraction.tricky_le(deepcopy(state.locals), deepcopy(state.locals), val1, val2)                      
                    return_vals = [(State.new_locals_new_stack(state, l_branch, new_stack), b["target"]), (State.new_locals_new_stack(state, l_no_branch, new_stack), i+1)]
 
            case "eq" | "is":
                if val1.eq(val2): return_vals.append((State.new_stack(state, new_stack), b["target"]))
                elif val1.neq(val2):
                    return_vals.append((State.new_stack(state, new_stack), i+1))
                else: 
                    return_vals = [(State.new_stack(state, new_stack), b["target"]), (State.new_stack(state, new_stack), b["target"])]
            case "ne" | "isnot":
                if val1.neq(val2): return_vals.append((State.new_stack(state, new_stack), b["target"]))
                if val1.eq(val2): return_vals.append((State.new_stack(state, new_stack), i+1)) 
                else:
                    return_vals = [(State.new_stack(state, new_stack), b["target"]), (State.new_stack(state, new_stack), b["target"])] 

        return return_vals

    
    def if_m(self, b, state, i):
        if len(state.stack) < 2: raise Exception("Not enough operands on stack") # We must have at least two elements on stack
         
        val1 = state.stack[-2]
        val2 = state.stack[-1] 
        new_stack = deepcopy(state.stack[:-2])

        return self.conditional(b, state, val1, val2, new_stack, i) 
  
    def ifz(self, b, state, i): 
        val = state.stack[-1]
        zero = self.abstraction.from_integer(0)
        new_stack = deepcopy(state.stack[:-1])
        return_vals = []
        
        match b["condition"]: 
            case "eq" | "is": 
                if isinstance(val, self.abstraction): 
                    return self.conditional(b, state, val, zero, new_stack, i) 
                else:
                    if val is None:
                        return_vals.append((State.new_stack(state, new_stack), b["target"])) #branch
                        #return_vals.append(, b["target"])) # branch
                    else:
                        return_vals.append((State.new_stack(state, new_stack), i+1)) # do not branch
                
            case "ne" | "isnot": 
                if isinstance(val, self.abstraction):
                    return self.conditional(b, state, val, zero, new_stack, i)
                else:
                    if val is not None:
                        return_vals.append((State.new_stack(state, new_stack), b["target"])) # branch
                    else:
                        return_vals.append((State.new_stack(state, new_stack), i+1)) # do not branch
            
            case _: 
                return self.conditional(b, state, val, zero, new_stack, i)

        return return_vals  
    
    def get(self, b, state, i):
        # not static the objectref will be on operand stack. else retrieve from class?
        if b["static"]:
            class_ = b["field"]["class"]
            if class_ == "java/lang/System": # hardcoding only really considering when we expect calls to println later
                new_stack = deepcopy(state.stack) + [class_]
            else:
                field_name = b["field"]["name"] 
                query_string = f"fields[?name=='{field_name}']"
                res = jmespath.search(query_string, self.program.classes[class_]) 
                
                if res == [] or "value" not in res[0]: raise Exception("Review get() please") # should not happen?
                
                field_value = res[0]["value"]
                new_stack = deepcopy(state.stack) + [field_value]
            
            return [(State.new_stack(state, new_stack), i+1)]
         
        return [] 
            
    def dup(self, b, state, i): 
        if b["words"] == 1:
            if len(state.stack) < 1: raise Exception("Expected non-empty stack") 
            return [(State.add_to_stack(state, state.stack[-1]), i+1)]
        elif b["words"] == 2:
            if len(state.stack) < 2: raise Exception("Expected at least two values on stack") 
            new_stack = deepcopy(state.stack) + state.stack[-2:] 
            return [(State.new_stack(state, new_stack), i+ 1)] 
        else:
            raise Exception("Not implemented") 

    def new(self, b, state, i):
        if "class" in b:
            if b["class"] == "java/lang/AssertionError": 
                #return self.new_stack_frame(l, s + [(hp.AssertError, )], pc+4) # new pc does not matter really. just skip 4 to keep on. but really we should just terminate? or not
                return [(State.cpy(state), i)]#self.new_stack_frame(l, s,  pc+3) # TRY DO NOTHING INSTEAD. DO not continue with failed state
            
        raise Exception("Not implemented")
    
    def negate(self, b, state, i):
        if b["type"] != "int": raise Exception("Not implemented")
        val = state.stack[-1]
        new_stack = deepcopy(state.stack[:-1]) + [self.abstraction(-val.h, -val.l, val.index)]
        return [(State.new_stack(state, new_stack), i + 1)]

    # array is (length, [items...]). Index arg has to be greater than or eq 0 and less than length to pass 
    def within_bounds(self, arr, index):
        length, _ = arr

        if type(length) != type(index): raise Exception("Type error")
        return index < length and index >= self.abstraction.from_integer(0)


    def newarray(self, b, state, i):
        if b["type"] == "boolean" or b["type"] == "char": raise Exception("Not implemented")

        if b["dim"] != 1: raise Exception("Not implemented") # TODO multidimensional arrays. if we want to...
        if len(state.stack) < 1: raise Exception("Expected stack of at least 1 element")

        # Stack should be ..., count -> 
        # becomes ..., arrayref ->  
        count = state.stack[-1]
        if count < self.abstraction.from_integer(0): return [(State(deepcopy(state.locals), deepcopy(state.stack[:-1]), deepcopy(state.heap), ExceptionType.NegativeArraySizeException), i+1)]

        new_arr_ref = "arr" + str(self.arrays_allocated)
        self.arrays_allocated += 1
        new_arr = self.abstraction.generate_array(count, init_val=self.abstraction.from_integer(0))
         
        new_stack = deepcopy(state.stack[:-1]) + [new_arr_ref]
        new_heap = deepcopy(state.heap)

        # an actual list now because easier implementation wise. Not important for what we are focusing on. But that way we can just use the arithmetics we have instead of sth special for sets. if representing possible values as sets.
        new_heap[new_arr_ref] = new_arr # consider whether to have length elements, set representing min max of all values or something else. in any event default val is 0.

        return [(State.new_stack_new_heap(state, new_stack, new_heap), i+1)]

    # https://docs.oracle.com/javase/specs/jvms/se19/html/jvms-6.html#jvms-6.5.aastore 
    def array_store(self, b, state, i):
        if len(state.stack) < 3: raise Exception("Expected stack of at least 3 elements")

        # stack should be: ..., arrayref, index, value ->
        # becomes ... ->
        arr_ref = state.stack[-3]
        index = state.stack[-2]
        value = state.stack[-1] 

        new_stack = deepcopy(state.stack[:-3])
        new_heap = deepcopy(state.heap)

        # Check bounds and go to exception state if out of bounds
        if not self.within_bounds(new_heap[arr_ref], index): return [(State(deepcopy(state.locals), new_stack, new_heap, ExceptionType.IndexOutOfBoundsException), i+1)]

        new_heap[arr_ref] = self.abstraction.handle_array(new_heap[arr_ref], value)            
        
        return [(State.new_stack_new_heap(state, new_stack, new_heap), i+1)]

    def array_load(self, b, state, i):
        if len(state.stack) < 2: raise Exception("Expected stack of at least 2 elements")       

        # stack should be: ..., arrayref, index ->
        # becomes ..., value ->
        arr_ref = state.stack[-2]
        index = state.stack[-1]

        new_stack = deepcopy(state.stack[:-2])

        # Check bounds and go to exception state if out of bounds
        if not self.within_bounds(state.heap[arr_ref], index): return [(State(deepcopy(state.locals), new_stack, deepcopy(state.heap), ExceptionType.IndexOutOfBoundsException), i+1)]

        # Array is tuple (count, items). Items represented as a single value of the astraction
        new_stack += [state.heap[arr_ref][1]]

        return [(State.new_stack(state, new_stack), i+1)]

    def arraylength(self, b, state, i):
        if len(state.stack) < 1: raise Exception("Expected stack of at least 1 elements")       

        # stack should be ..., arrayref ->
        arr_ref = state.stack[-1]
        
        if arr_ref not in state.heap: raise Exception("Array ref not defined") # We do not perform this check elsewhere. just remove assume never happens

        new_stack = deepcopy(state.stack[:-1]) + [state.heap[arr_ref][0]]
        return [(State.new_stack(state, new_stack), i+1)]

        
