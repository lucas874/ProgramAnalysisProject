import jmespath 
from helpers_constants import *
from utilities import *
from interpret import Interpreter
from copy import deepcopy
from state import State

class AbstractInterpreter:
        def __init__(self, program : Program, abstraction):
            self.program = program
            self.abstraction = abstraction
            self.worklist = []
            self.states = []
            self.interpret = Interpreter(abstraction, program) 

        def print_state(self, bytecode):
            for i, (inst, state) in enumerate(zip(bytecode, self.states)):
                if state is None: print(f"{inst}: {state}")
                else: print(f"i={i}: {inst['opr']}: locals: {state.locals} stack: {state.stack} heap: {state.heap}: exception: {state.exception}")

        def analyse(self, m): # Expect m to be (class, method)
            locals, heap = self.get_args(m)
            stack = []
            bytecode = self.program.bytecode[m]
            self.states = [None for inst in bytecode] 
            int_constants = self.get_integer_constants(bytecode) # figure out how to handle this elsewhere...

            self.worklist = [0] # start at first instruction
            self.states[0] = State(locals, stack, heap)
             
            while self.worklist:# and not self.exceptions():
                i = self.worklist.pop()
                bc = bytecode[i] 

                for new_state, i_ in self.abstract_step(bc, i):
                    if new_state.is_exception_state(): self.worklist = []  # Stop intepretation if exception?
                    
                    self.merge_fwd(i_, new_state, int_constants)
                    self.print_state(bytecode) 
                    print("\n\n")

            print("Final state: ")
            self.print_state(bytecode)
            return self.states

        def generate_value(self, param):
            return self.abstraction.from_type(param["type"]["base"])
        
        def generate_array(self): 
            return self.abstraction.generate_array()

        def get_args(self, m):
            query = f"methods[?name=='{m[1]}']"
            method = jmespath.search(query, self.program.classes[m[0]])[0] # hope it's actually there
            locals = {}
            heap = {} 
            
            for i, p in enumerate(method["params"]): 
                if "base" in p["type"]: locals[i] = self.generate_value(p)
                elif "kind" in p["type"] and p["type"]["kind"] == "array":
                    arr_ref = f"arr_arg{i}"
                    arr = self.generate_array()
                    locals[i] = arr_ref
                    heap[arr_ref] = arr
            
            return locals, heap

        def merge(self, old_state, new_state, *args): 
            return State.merge(old_state, new_state, self.abstraction.wide, *args)

        def merge_fwd(self, i, new_state, *args): # i points to an instruction. locals, state. K is list of integer constants in program 
            res = self.merge(self.states[i], new_state, *args) 
            
            if res != self.states[i]:
                self.worklist.append(i)
 
            self.states[i] = res
        
        def abstract_step(self, bc, i):
            state_i = self.states[i]
              
            return self.interpret.step(bc, state_i, i) # DEEPCOPY was here. Now copies made in state class. Consider this... 

        def get_integer_constants(self, bytecode): 
            int_constants = {d["value"] for d in jmespath.search("[*].value ", bytecode) if d["type"] == "integer"}
            zeros = {0 for inst in bytecode if inst["opr"] == 'ifz'} 
            
            return list(int_constants | zeros)

