from copy import deepcopy
import jmespath 
from intervals import Interval
from state import State

class Interpreter:
    def __init__(self, abstraction, program):
        self.abstraction = abstraction
        self.program = program # just needed for get... which could be hardcoded anyway

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
         
    def return_m(self, b, l, s, i): 
        return [] 
   
    def load(self, b, state, i): 
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
                new_stack += [val1 + val2]
            case "sub":
                #return [(l, s[:-2]+[val1 - val2], i+1)] 
                new_stack += [val1 - val2]
            case "mul":
                #return [(l, s[:-2]+[val1 * val2], i+1)] 
                new_stack += [val1 * val2]
            case "div": 
                #return [(l, s[:-2]+[val1 / val2], i+1)] # Exception checked in AbstractInt
                new_stack += [val1 / val2]
            case "rem":
                #return [(l, s[:-2]+[val1 % val2], i+1)] 
                new_stack += [val1 % val2]

        return [(State.new_stack(state, new_stack), i+1)] 
     
    def store(self, b, state, i): 
        idx = b["index"]
        # hope I understood it correctly. Think we remove the element from the operand stack too.
        return [(State.store(state, idx), i+1)] 

    def incr(self, b, l, s, i):
        #increment local in $index by $amount
         
        idx = b["index"]
        l[idx]+= self.abstraction.from_integer(b["amount"])
        return [(l, s, i+1)]

    def goto(self, b, l, s, i): 
        return [(l, s, b["target"])]  
    
    def if_m(self, b, state, i):
        if len(state.stack) < 2: raise Exception("Not enough operands on stack") # We must have at least two elements on stack
         
        val1 = state.stack[-2]
        val2 = state.stack[-1] 

        return_vals = []
        
        match b["condition"]:
            case "gt": # all cases except eq, neq follow this pattern. two 'easy cases'. two difficult cases. 
                if val1 > val2: return_vals.append((State.new_stack(state, deepcopy(state.stack[:-2])), b["target"])) # return state that is old state with two elements popped from stack jump to target address
                elif val1 <= val2: return_vals.append((State.new_stack(state, deepcopy(state.stack[:-2])), i+1)) # same but jump to next address 
                else:
                    l_branch, l_no_branch = self.abstraction.tricky_gt(deepcopy(state.locals), deepcopy(state.locals), val1, val2)
                    return_vals = [(State.new_locals(state, l_branch), b["target"]), (State.new_locals(state, l_no_branch), i+1)]

            case "ge":
                if val1 >= val2: return_vals.append((State.new_stack(state, deepcopy(state.stack[:-2])), b["target"]))
                elif val1 < val2: return_vals.append((State.new_stack(state, state.stack[:-2]), i+1))
                else:
                    l_branch, l_no_branch = self.abstraction.tricky_ge(deepcopy(state.locals), deepcopy(state.locals), val1, val2)                     
                    return_vals = [(State.new_locals(state, l_branch), b["target"]), (State.new_locals(state, l_no_branch), i+1)] 

            case "lt":
                if val1 < val2: return_vals.append((l, s, b["target"]))
                elif val1 >= val2: return_vals.append((l, s, i+1))
                else: 
                    l_branch = deepcopy(l)
                    l_no_branch = deepcopy(l)
                    
                    if val1.index is not None:
                        new_h = max(val1.h, val2.h)
                        new_l = max(val1.l, val2.h)
                        l_no_branch[val1.index] = self.abstraction(val1.l, val1.h, None)
                        new_h = val2.l-1
                        new_l = min(val1.l, val2.l-1)
                        l_branch[val1.index] = self.abstraction(new_l, new_h, None)


                    return_vals = [(l_branch, deepcopy(s), b["target"]), (l_no_branch, deepcopy(s), i+1)]


            case "le": 
                if val1 <= val2: return_vals.append((l, s, b["target"]))
                elif val1 > val2: return_vals.append((l, s, i+1))
                else: 
                    l_branch = deepcopy(l)
                    l_no_branch = deepcopy(l)
                    
                    if val1.index is not None and val2.is_constant():
                        new_h = max(val1.h, val2.h+1)
                        new_l = max(val1.l, val2.h+1)
                        l_no_branch[val1.index] = self.abstraction(new_l, new_h, None)
                        new_h = val2.l
                        new_l = min(val1.l, new_h)
                        l_branch[val1.index] = self.abstraction(new_l, new_h, None)

                    elif val2.index is not None and val1.is_constant():
                        new_h = val1.l-1
                        new_l = min(val1.l, new_h)
                        l_no_branch[val2.index] = self.abstraction(new_l, new_h, None)
                        new_l = max(val1.h, val2.l)
                        new_h = max(new_l, val2.h) 
                        l_branch[val2.index] = self.abstraction(new_l, new_h, None)
 
                    return_vals = [(l_branch, deepcopy(s), b["target"]), (l_no_branch, deepcopy(s), i+1)]
                
        
            case "eq" | "is":
                if isinstance(val1, self.abstraction):
                    if val1 == val2:
                        return_vals.append((deepcopy(l), deepcopy(s), b["target"])) # do not branch
                    else:
                        if val1.index is not None and val2.is_constant():  
                            l_branch[val1.index] = self.abstraction(val2.l, val2.h, None)

                        elif val2.index is not None and val1.is_constant(): 
                            l_branch[val2.index] = self.abstraction(val1.l, val1.h, None)
    
                        return_vals = [(deepcopy(l), deepcopy(s), b["target"]), (deepcopy(l), deepcopy(s), i+1)]  # do not relly learn alot. could remove val2 as lower, if val2 exactly lower? or upper
                else:
                    if val1 is not None:
                        return_vals.append((deepcopy(l), deepcopy(s), b["target"])) # branch
                    else:
                        return_vals.append((deepcopy(l), deepcopy(s), i+1)) # do not branch 
                
            case "ne" | "isnot": 
                if isinstance(val1, self.abstraction):
                    if val1 == val2:
                        return_vals.append((deepcopy(l), deepcopy(s), i+1)) # do not branch
                    else:
                        return_vals = [(deepcopy(l), deepcopy(s), b["target"]), (deepcopy(l), deepcopy(s), i+1)]  # do not relly learn alot. could remove val2 as lower, if val2 exactly lower? or upper
                else:
                    if val1 is not None:
                        return_vals.append((deepcopy(l), deepcopy(s), b["target"])) # branch
                    else:
                        return_vals.append((deepcopy(l), deepcopy(s), i+1)) # do not branch

        return return_vals  
           
    
    def ifz(self, b, l, s, i): 
        val = s.pop()  
        zero = self.abstraction.from_integer(0)
        return_vals = []

        match b["condition"]:
            case "gt":
                if val > zero: return_vals.append((l, s, b["target"]))
                elif val <= zero: return_vals.append((l, s, i+1))
                else: 
                    l_branch = deepcopy(l)
                    l_no_branch = deepcopy(l)
                    
                    if val.index is not None:
                        new_h = max(val.h, zero.h+1)
                        new_l = max(val.l, zero.h+1)
                        l_branch[val.index] = self.abstraction(new_l, new_h, None)
                        new_h = zero.l
                        new_l = min(val.l, new_h)
                        l_no_branch[val.index] = self.abstraction(new_l, new_h, None)

                    return_vals = [(l_branch, deepcopy(s), b["target"]), (l_no_branch, deepcopy(s), i+1)]

            case "ge":
                if val >= zero: return_vals.append((l, s, b["target"]))
                elif val < zero: return_vals.append((l, s, i+1))
                else: 
                    l_branch = deepcopy(l)
                    l_no_branch = deepcopy(l)
                    
                    if val.index is not None:
                        new_h = max(val.h, zero.h)
                        new_l = max(val.l, zero.h)
                        l_branch[val.index] = self.abstraction(val.l, val.h, None)
                        new_h = zero.l
                        new_l = min(val.l, zero.l)
                        l_no_branch[val.index] = self.abstraction(new_l, new_h, None)

                    return_vals = [(l_branch, deepcopy(s), b["target"]), (l_no_branch, deepcopy(s), i+1)]


            case "lt":
                if val < zero: return_vals.append((l, s, b["target"]))
                elif val >= zero: return_vals.append((l, s, i+1))
                else: 
                    l_branch = deepcopy(l)
                    l_no_branch = deepcopy(l)
                    
                    if val.index is not None:
                        new_h = max(val.h, zero.h)
                        new_l = max(val.l, zero.h)
                        l_no_branch[val.index] = self.abstraction(val.l, val.h, None)
                        new_h = zero.l-1
                        new_l = min(val.l, zero.l-1)
                        l_branch[val.index] = self.abstraction(new_l, new_h, None)


                    return_vals = [(l_branch, deepcopy(s), b["target"]), (l_no_branch, deepcopy(s), i+1)]


            case "le":
                if val <= zero: return_vals.append((l, s, b["target"]))
                elif val > zero: return_vals.append((l, s, i+1))
                else: 
                    l_branch = deepcopy(l)
                    l_no_branch = deepcopy(l)
                    
                    if val.index is not None:
                        new_h = max(val.h, zero.h)
                        new_l = max(val.l, zero.h)
                        l_no_branch[val.index] = self.abstraction(val.l, val.h, None)
                        new_h = zero.l
                        new_l = min(val.l, zero.l)
                        l_branch[val.index] = self.abstraction(new_l, new_h, None)

                    return_vals = [(l_branch, deepcopy(s), b["target"]), (l_no_branch, deepcopy(s), i+1)]
                
        
            case "eq" | "is": 
                if isinstance(val, Interval):
                    if val == zero:
                        return_vals.append((deepcopy(l), deepcopy(s), b["target"])) # do not branch
                    else:
                        return_vals = [(deepcopy(l), deepcopy(s), b["target"]), (deepcopy(l), deepcopy(s), i+1)]  # do not relly learn alot. could remove zero as lower, if zero exactly lower? or upper
                else:
                    if val is not None:
                        return_vals.append((deepcopy(l), deepcopy(s), b["target"])) # branch
                    else:
                        return_vals.append((deepcopy(l), deepcopy(s), i+1)) # do not branch
                
            case "ne" | "isnot": 
                if isinstance(val, Interval):
                    if val == zero:
                        return_vals.append((deepcopy(l), deepcopy(s), i+1)) # do not branch
                    else:
                        l_branch = deepcopy(l)
                        l_branch[val.index] = self.abstraction(0, 0, val.index)
                        return_vals = [(l_branch, deepcopy(s), b["target"]), (deepcopy(l), deepcopy(s), i+1)]  # do not relly learn alot. could remove zero as lower, if zero exactly lower? or upper
                else:
                    if val is not None:
                        return_vals.append((deepcopy(l), deepcopy(s), b["target"])) # branch
                    else:
                        return_vals.append((deepcopy(l), deepcopy(s), i+1)) # do not branch
                    

        return return_vals  
    
    def get(self, b, l, s, i):
        # not static the objectref will be on operand stack. else retrieve from class?
        if b["static"]:
            class_ = b["field"]["class"]
            field_name = b["field"]["name"] 
            query_string = f"fields[?name=='{field_name}']"
            res = jmespath.search(query_string, self.program.classes[class_]) 
            
            if res == [] or "value" not in res[0]: raise Exception("Review get() please") # should not happen?
            
            field_value = res[0]["value"]
            return [(l, s + [field_value], i+1)]
         
        return [] 
            
    def dup(self, b, l, s, i): 
        if b["words"] == 1:
            if len(s) < 1: return False
            return [(l, s+ [s[-1]], i+ 1)]
        elif b["words"] == 2:
            if len(s) < 2: return False
            return [(l, s + [s[-2:]], i+ 1)] 
        else:
            raise Exception("Not implemented") 

    def new(self, b, l, s, i):
        if "class" in b:
            if b["class"] == "java/lang/AssertionError": 
                #return self.new_stack_frame(l, s + [(hp.AssertError, )], pc+4) # new pc does not matter really. just skip 4 to keep on. but really we should just terminate? or not
                return []#self.new_stack_frame(l, s,  pc+3) # TRY DO NOTHING INSTEAD. DO not continue with failed state
        raise Exception("Not implemented")
    
    def negate(self, b, l, s, i):
        if b["type"] != "int": raise Exception("Not implemented")
        val = s.pop()
        return [(l, s + [self.abstraction(-val.h, -val.l, val.index)], i + 1)]