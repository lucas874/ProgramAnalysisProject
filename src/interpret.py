from copy import deepcopy
import jmespath 
from intervals import Interval

class Interpreter:
    def __init__(self, abstraction, program):
        self.abstraction = abstraction
        self.program = program # just needed for get... which could be hardcoded anyway

    def step(self, bc, l, s, i): 
            if bc["opr"] == "return":
                bc["opr"] = "return_m" # I know ugly but there were many :)
            if bc["opr"] == "if":
                bc["opr"] = "if_m"
            if hasattr(self, bc["opr"]):
                return getattr(self, bc["opr"])(bc, l, s, i) 
            else:
                raise Exception("Not implemented") 

    def push(self, bc, l, s, i): 
            value = self.abstraction.from_value(bc["value"])
            
            if "value" in bc:
                return [(l, s + [value], i+1)]
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
   
    def load(self, b, l, s, i):
        # Only consider ints for now. 
        print(l) 
        value = l[b["index"]].cpy_set_index(b["index"]) 
        return [(l, s + [value], i+1)]   

    def binary(self, b, l, s, i): 
        if len(s) < 2: raise Exception("Not enough operands on stack") # We must have at least two elements on stack
         
        val1 = s[-2]
        val2 = s[-1] 

        if type(val1) != type(val2): raise Exception("Type mismatch")

        match b["operant"]:
            case "add":
                return [(l, s[:-2]+[val1 + val2], i+1)] 
            case "sub":
                return [(l, s[:-2]+[val1 - val2], i+1)] 
            case "mul":
                return [(l, s[:-2]+[val1 * val2], i+1)] 
            case "div": 
                return [(l, s[:-2]+[val1 / val2], i+1)] # Exception checked in AbstractInt
            case "rem": 
                return [(l, s[:-2]+[val1 % val2], i+1)] 

        return True
     
    def store(self, b, l, s, i): 
        idx = b["index"]
        l[idx] = s.pop() # hope I understood it correctly. Think we remove the element from the operand stack too.
        return [(l, s, i+1)] 

    def incr(self, b, l, s, i):
        #increment local in $index by $amount
         
        idx = b["index"]
        l[idx]+= self.abstraction.from_integer(b["amount"])
        return [(l, s, i+1)]

    def goto(self, b, l, s, i): 
        return [(l, s, b["target"])]  
    
    def if_m(self, b, l, s, i):
        val2 = s.pop()
        val1 = s.pop()
        return_vals = []
        
        match b["condition"]:
            case "gt":
                if val1 > val2: return_vals.append((l, s, b["target"]))
                elif val1 <= val2: return_vals.append((l, s, i+1))
                else: 
                    l_branch = deepcopy(l)
                    l_no_branch = deepcopy(l)
                    
                    if val1.index is not None and val2.is_constant():
                        new_h = max(val1.h, val2.h+1)
                        new_l = max(val1.l, val2.h+1)
                        l_branch[val1.index] = self.abstraction(new_l, new_h, None)
                        new_h = val2.l
                        new_l = min(val1.l, new_h)
                        l_no_branch[val1.index] = self.abstraction(new_l, new_h, None)

                    elif val2.index is not None and val1.is_constant():
                    
                        new_h = val1.l - 1
                        new_l = min(val2.l, new_h)
                        l_branch[val2.index] = self.abstraction(new_l, new_h, None)
                        new_h = max(val1.h, val2.h)
                        new_l = min(val1.h, new_h)
                        l_no_branch[val2.index] = self.abstraction(new_l, new_h, None)

                    
                    return_vals = [(l_branch, deepcopy(s), b["target"]), (l_no_branch, deepcopy(s), i+1)]

            case "ge":
                if val1 >= val2: return_vals.append((l, s, b["target"]))
                elif val1 < val2: return_vals.append((l, s, i+1))
                else: 
                    l_branch = deepcopy(l)
                    l_no_branch = deepcopy(l)
                    
                    if val1.index is not None and val2.is_constant():
                        new_h = max(val1.h, val2.h)
                        new_l = max(val1.l, val2.h)
                        l_branch[val1.index] = self.abstraction(new_l, new_h, None)
                        new_h = val2.l
                        new_l = min(val1.l, new_h)
                        l_no_branch[val1.index] = self.abstraction(new_l, new_h, None)

                    elif val2.index is not None and val1.is_constant():
                        new_h = val1.l
                        new_l = min(val1.l, new_h)
                        l_branch[val2.index] = self.abstraction(new_l, new_h, None)
                        new_h = max(val1.h, val2.l)
                        new_l = max(val2.l, new_h)
                        l_no_branch[val2.index] = self.abstraction(new_l, new_h, None)
 
                    return_vals = [(l_branch, deepcopy(s), b["target"]), (l_no_branch, deepcopy(s), i+1)]


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