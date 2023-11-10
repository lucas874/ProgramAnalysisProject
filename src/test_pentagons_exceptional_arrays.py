import pytest
from abstract_interpreter import *
from helpers_constants import *
from pentagons import *
from utilities import *
from state import *

# always... should be successful. dependsOnLattice.. should not

@pytest.fixture(scope="session", autouse=True)
def setup():
    global program

    # read the json files
    json_file_path = "../exceptional"
    cls_json_files = extract_files_by_extension(json_file_path, "json")
    classes = get_classes(cls_json_files)
    program = Program(classes)

def test_Arrays_alwaysThrows1(): 
    interpreter = AbstractInterpreter(program, Pentagon)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows1'))

    assert final_states[-1].exception == ExceptionType.IndexOutOfBoundsException # -1 because at return statement
 
def test_Arrays_alwaysThrows2(): 
    interpreter = AbstractInterpreter(program, Pentagon)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows2'))
     
    assert final_states[-1].exception == ExceptionType.IndexOutOfBoundsException

def test_Arrays_alwaysThrows3():
    
    interpreter = AbstractInterpreter(program, Pentagon)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows3'))
    
    assert final_states[13].exception == ExceptionType.IndexOutOfBoundsException # 13 because state right after perform array store that leads to exception

def test_Arrays_alwaysThrows4():
    interpreter = AbstractInterpreter(program, Pentagon)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows4'))
    
    assert final_states[7].exception == ExceptionType.IndexOutOfBoundsException # 7 is state right after array load that leads to exception

def test_Arrays_alwaysThrows5(): 
    interpreter = AbstractInterpreter(program, Pentagon)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows5'))
     
    assert final_states[31].exception == ExceptionType.IndexOutOfBoundsException # 31 state right after dangerous array load

def test_Arrays_itDependsOnLattice1():
    interpreter = AbstractInterpreter(program, Pentagon)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice1'))
    
    # Fails. But a perfectly precise abstraction would not. 
    expected = State({0: 'arr_arg0', 1: Pentagon(intv=Interval(l=0, h=2147483647, index=1, heap_ptr=None), greater_variables={'arr_arg0'})}, [Pentagon(intv=Interval(l=0, h=0, index=None, heap_ptr='arr_arg0'), greater_variables=set())], {'arr_arg0': (Pentagon(intv=Interval(l=0, h=2147483647, index=None, heap_ptr='arr_arg0'), greater_variables=set()), Pentagon(intv=Interval(l=0, h=0, index=None, heap_ptr='arr_arg0'), greater_variables=set()))}, exception=None) 
    assert final_states[-1] == expected

def test_Arrays_itDependsOnLattice2():
    interpreter = AbstractInterpreter(program, Pentagon)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice2'))
    
    expected = State({0: 'arr_arg0', 1: Pentagon(Interval(l=0, h=0), set())}, [Pentagon(intv=Interval(l=0, h=0, index=None, heap_ptr='arr_arg0'), greater_variables=set())], {'arr_arg0': (Pentagon(Interval(l=1, h=2147483647, index=None, heap_ptr="arr_arg0"), set()), Pentagon(Interval(l=0, h=0, index=None, heap_ptr="arr_arg0"), set()))}, exception=None)
    assert final_states[-1] == expected

def test_Arrays_itDependsOnLattice3():
    interpreter = AbstractInterpreter(program, Pentagon)
    
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice3'))
    #expected = [State(locals={0: 'arr_arg0'}, stack=[], heap={'arr_arg0': (Pentagon(intv=Interval(l=1, h=2147483647, index=None, heap_ptr='arr_arg0'), greater_variables=set()), Pentagon(intv=Interval(l=0, h=0, index=None, heap_ptr='arr_arg0'), greater_variables=set()))}, exception=None)] 
    expected = State({0: 'arr_arg0'}, stack=[], heap={'arr_arg0': (Pentagon(intv=Interval(l=1, h=2147483647, index=None, heap_ptr='arr_arg0'), greater_variables=set()), Pentagon(intv=Interval(l=0, h=0, index=None, heap_ptr='arr_arg0'), greater_variables=set()))}, exception=None) 
    
    assert final_states[-1] == expected
"""
def test_Arrays_itDependsOnLattice4():
    interpreter = AbstractInterpreter(program, Pentagon) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice4'))
     
    assert final_states[-1].exception == ExceptionType.ArithmeticException

def test_Arrays_neverThrows1():
    interpreter = AbstractInterpreter(program, Pentagon) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows1'))
    
    expected = State({0: Pentagon(l=3, h=3, index=None)}, [Interval(l=0, h=0, index=None)], {})
 
    assert final_states[-1] == expected

def test_Arrays_neverThrows2():
    interpreter = AbstractInterpreter(program, Pentagon) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows2'))
     
    expected = State({0: Pentagon(l=1, h=INT_MAX, index=None)}, [Interval(l=0, h=0, index=None)], {})
    
    assert final_states[-1] == expected

def test_Arrays_neverThrows3():
    interpreter = AbstractInterpreter(program, Pentagon) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows3'))
     
    expected = State({0: Pentagon(l=1, h=2147483647, index=None), 1: Interval(l=-2147483645, h=2147483647, index=None)}, [Interval(l=0, h=0, index=None)], {})
    
    assert final_states[-1] == expected 

def test_Arrays_neverThrows4():
    interpreter = AbstractInterpreter(program, Pentagon) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows4'))
     
    assert final_states[-1] == None # Java code has statement assert i > 0 && i < 0; should fail right? Not satisfiable so none bc fails assertion and never reach instruction leading to "final state"

def test_Arrays_neverThrows5():
    interpreter = AbstractInterpreter(program, Pentagon) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows5'))
     
    expected = State({0: Pentagon(l=1, h=2147483647, index=None), 1: Interval(l=-2147483648, h=2147483647, index=None)}, [Interval(l=-2147483648, h=2147483647, index=None)], {})

    assert final_states[-1] == expected 

def test_Arrays_speedVsPrecision():
    interpreter = AbstractInterpreter(program, Pentagon) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'speedVsPrecision'))
 
    assert final_states[-1].exception == ExceptionType.ArithmeticException """
