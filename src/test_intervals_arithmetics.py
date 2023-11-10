import pytest
from abstract_interpreter import *
from helpers_constants import *
from intervals import *
from utilities import *
from state import *

# All tests should be successful

@pytest.fixture(scope="session", autouse=True)
def setup():
    global program

    # read the json files
    json_file_path = "../exceptional"
    cls_json_files = extract_files_by_extension(json_file_path, "json")
    classes = get_classes(cls_json_files)
    program = Program(classes)

def test_Arithmetics_alwaysThrows1(): 
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows1'))

    assert final_states[-1].exception == ExceptionType.ArithmeticException # -1 because at return statement
 
def test_Arithmetics_alwaysThrows2(): 
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows2'))
     
    assert final_states[-1].exception == ExceptionType.ArithmeticException

def test_Arithmetics_alwaysThrows3():
    
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows3'))
    
    assert final_states[-1].exception == ExceptionType.ArithmeticException 

def test_Arithmetics_alwaysThrows4():
    interpreter = AbstractInterpreter(program, Interval)
    pretty_print_bytecode(program, ('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows4'))
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows4'))
    
    assert final_states[-1].exception == ExceptionType.ArithmeticException

def test_Arithmetics_alwaysThrows5(): 
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows5'))
     
    assert final_states[-1].exception == ExceptionType.ArithmeticException 

def test_Arithmetics_itDependsOnLattice1():
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice1'))
    
    expected = State({0: Interval(l=2, h=2, index=None)}, [Interval(l=1, h=1, index=None)], {})
    assert final_states[-1] == expected

def test_Arithmetics_itDependsOnLattice2():
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice2'))
    
    expected = State({0: Interval(-998, -998, None)}, [Interval(-1, -1, None)], {})
    assert final_states[-1] == expected

def test_Arithmetics_itDependsOnLattice3():
    interpreter = AbstractInterpreter(program, Interval)
    
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice3'))
     
    assert final_states[-1].exception == ExceptionType.ArithmeticException

def test_Arithmetics_itDependsOnLattice4():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice4'))
     
    assert final_states[-1].exception == ExceptionType.ArithmeticException

def test_Arithmetics_neverThrows1():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows1'))
    
    expected = State({0: Interval(l=3, h=3, index=None)}, [Interval(l=0, h=0, index=None)], {})
 
    assert final_states[-1] == expected

def test_Arithmetics_neverThrows2():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows2'))
     
    expected = State({0: Interval(l=1, h=INT_MAX, index=None)}, [Interval(l=0, h=0, index=None)], {})
    
    assert final_states[-1] == expected

def test_Arithmetics_neverThrows3():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows3'))
     
    expected = State({0: Interval(l=1, h=2147483647, index=None), 1: Interval(l=-2147483645, h=2147483647, index=1)}, [Interval(l=0, h=0, index=None)], {})
    
    assert final_states[-1] == expected 

def test_Arithmetics_neverThrows4():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows4'))
     
    assert final_states[-1] == None # Java code has statement assert i > 0 && i < 0; should fail right? Not satisfiable so none bc fails assertion and never reach instruction leading to "final state"

def test_Arithmetics_neverThrows5():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows5'))
     
    expected = State({0: Interval(l=1, h=2147483647, index=None), 1: Interval(l=-2147483648, h=2147483647, index=None)}, [Interval(l=-2147483648, h=2147483647, index=None)], {})

    assert final_states[-1] == expected 

def test_Arithmetics_speedVsPrecision():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'speedVsPrecision'))
 
    assert final_states[-1].exception == ExceptionType.ArithmeticException
