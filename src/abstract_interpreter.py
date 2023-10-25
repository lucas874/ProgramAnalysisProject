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
                    self.print_state(bytecode) 
                    print("\n\n")
                    self.merge_fwd(i_, new_state, int_constants) 

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

        # use *args for things like K in the intervals widening etc. 
        def merge_locals(self, old_locals, new_locals, *args):
            union = set(old_locals) | set(new_locals)
            merged = {}
            
            for i in union:
                if i in old_locals and new_locals:
                    merged[i] = self.abstraction.wide(old_locals[i], new_locals[i], *args)
                elif i in old_locals:
                    merged[i] = old_locals[i]
                else: 
                    merged[i] = new_locals[i]
            
            return merged 

        def merge_stacks(self, old_stack, new_stack, *args):
            assert len(old_stack) == len(new_stack)
            return [self.abstraction.wide(o, n, *args) for o,n in zip(old_stack, new_stack)]

        def merge_heaps(self, old_heap, new_heap, *args):
            return {} 

        def merge(self, old_state, new_state, *args): 
            if old_state == None:
                return new_state
            
            # old and new locals and stacks
            olc, os, oh = old_state 
            nlc, ns, nh = new_state 

            # merged locals, merged stack and merged heap
            mlc = self.merge_locals(olc, nlc, *args) 
            ms = self.merge_stacks(os, ns, *args) 
            mh = self.merge_heaps(oh, nh, *args)

            return (mlc, ms)

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