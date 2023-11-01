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
                else: print(f"i={i}: {inst['opr']}: locals: {state.locals} stack: {state.stack} heap: {state.heap}")

        def analyse(self, m): # Expect m to be (class, method)
            locals = self.get_args(m)
            stack = []
            bytecode = self.program.bytecode[m]
            self.states = [None for inst in bytecode] 
            int_constants = self.get_integer_constants(bytecode) # figure out how to handle this elsewhere...

            self.worklist = [0] # start at first instruction
            self.states[0] = State(locals, stack, {})
             
            while self.worklist:# and not self.exceptions():
                i = self.worklist.pop()
                bc = bytecode[i] 

                for new_state, i_ in self.abstract_step(bc, i):  
                    self.merge_fwd(i_, new_state, int_constants)
                    self.print_state(bytecode) 
                    print("\n\n")

            print("Final state: ")
            self.print_state(bytecode)
            return self.states

        def exceptions(self):

            for state in self.states:
                if state is not None:
                    for v in state[1]:
                        if v in EXCEPTIONS: return True

        def generate_value(self, param):
            if "base" in param["type"]: return self.abstraction.from_type(param["type"]["base"])

        def get_args(self, m):
            query = f"methods[?name=='{m[1]}']"
            method = jmespath.search(query, self.program.classes[m[0]])[0] # hope it's actually there
            locals = {}
            
            for i, p in enumerate(method["params"]): 
                locals[i] = self.generate_value(p) 

            return locals 

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

