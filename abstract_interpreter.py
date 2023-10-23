import jmespath 
from helpers_constants import *
from utilities import *
from interpret import Interpreter
from copy import deepcopy

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
                else: print(f"i={i}: {inst['opr']}: locals: {state[0]} stack: {state[1]}")

        def analyse(self, m): # Expect m to be (class, method)
            locals = self.get_args(m)
            stack = []
            bytecode = self.program.bytecode[m]
            self.states = [None for inst in bytecode] 
            int_constants = self.get_integer_constants(bytecode)

            self.worklist = [0] # start at first instruction
            self.states[0] = (locals, stack)
             
            while self.worklist:# and not self.exceptions():
                i = self.worklist.pop()
                bc = bytecode[i] 

                for nlc, ns, i_ in self.abstract_step(bc, i): 
                    self.print_state(bytecode) 
                    print("\n\n")
                    self.merge_fwd(i_, nlc, ns, int_constants)

            print("Final state: ")
            self.print_state(bytecode)
            return self.states

        def exceptions(self):

            for state in self.states:
                if state is not None:
                    for v in state[1]:
                        if v in EXCEPTIONS: return True

        def get_args(self, m):
            query = f"methods[?name=='{m[1]}']"
            method = jmespath.search(query, self.program.classes[m[0]])[0] # hope it's actually there
            locals = {}
            
            for i, p in enumerate(method["params"]):
                locals[i] = self.abstraction.from_type(p["type"]["base"])

            return locals 

        def merge(self, old_state, new_state, K): 
            if old_state == None:
                return new_state
            
            # old and new locals and stacks
            olc, os = old_state 
            nlc, ns = new_state 

            # merged locals and merged stack
            # UNION OR INTERSECT HERE?? 
            mlc = {i: self.abstraction.wide(olc[i], nlc[i], K) for i in set(olc) & set(nlc)} 
            ms = [self.abstraction.wide(o, n, K) for o,n in zip(os, ns)]
            
            return (mlc, ms)

        def merge_fwd(self, i, lc, s, K): # i points to an instruction. locals, state. K is list of integer constants in program
            res = self.merge(self.states[i], (lc, s), K) 
            
            if res != self.states[i]:
                self.worklist.append(i)
 
            self.states[i] = res
        
        def abstract_step(self, bc, i):
            l,s = self.states[i]
              
            return self.interpret.step(bc, deepcopy(l), deepcopy(s), i)

        def get_integer_constants(self, bytecode): 
            int_constants = {d["value"] for d in jmespath.search("[*].value ", bytecode) if d["type"] == "integer"}
            zeros = {0 for inst in bytecode if inst["opr"] == 'ifz'} 
            
            return list(int_constants | zeros) 