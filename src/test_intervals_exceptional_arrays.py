import pytest
from abstract_interpreter import *
from helpers_constants import *
from intervals import *
from utilities import *
from state import *

# always... should be successful. dependsOnLattice.. should not
# should all be successful
@pytest.fixture(scope="session", autouse=True)
def setup():
    global program

    # read the json files
    json_file_path = "../exceptional"
    cls_json_files = extract_files_by_extension(json_file_path, "json")
    classes = get_classes(cls_json_files)
    program = Program(classes)

def test_Arrays_alwaysThrows1(): 
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows1'))

    assert final_states[-1].exception == ExceptionType.IndexOutOfBoundsException # -1 because at return statement
 
def test_Arrays_alwaysThrows2(): 
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows2'))
     
    assert final_states[-1].exception == ExceptionType.IndexOutOfBoundsException

def test_Arrays_alwaysThrows3():
    
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows3'))
    
    assert final_states[13].exception == ExceptionType.IndexOutOfBoundsException # 13 because state right after perform array store that leads to exception

def test_Arrays_alwaysThrows4():
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows4'))
    
    assert final_states[7].exception == ExceptionType.IndexOutOfBoundsException # 7 is state right after array load that leads to exception

def test_Arrays_alwaysThrows5(): 
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows5'))
     
    assert final_states[31].exception == ExceptionType.IndexOutOfBoundsException # 31 state right after dangerous array load

def test_Arrays_itDependsOnLattice1():
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice1'))
    
    # Fails. But a perfectly precise abstraction would not.  
    assert final_states[-1].exception == None

def test_Arrays_itDependsOnLattice2():
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice2'))
    
    assert final_states[-1].exception == None
    
def test_Arrays_itDependsOnLattice3():
    interpreter = AbstractInterpreter(program, Interval)
    
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice3'))
    
    assert final_states[-1].exception == None 

def test_Arrays_itDependsOnLattice4():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice4'))
     
    assert final_states[-1].exception == None 

def test_Arrays_itDependsOnLattice5():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice5'))
     
    assert final_states[-1].exception == None 

def test_Arrays_neverThrows1():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows1'))
    
    assert final_states[-1].exception == None 
    

def test_Arrays_neverThrows2():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows2'))
     
    
    assert final_states[-1].exception == None 


def test_Arrays_neverThrows3():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows3'))
 
    assert final_states[-1].exception == None 


def test_Arrays_bubbleSort1():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'bubbleSort1'))
 
    assert final_states[-1].exception == None 
""" 
def test_Arrays_neverThrows3():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows3'))
 
    assert final_states[-1].exception == None 

 """