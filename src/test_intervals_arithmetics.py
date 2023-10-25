import pytest
from abstract_interpreter import *
from helpers_constants import *
from intervals import *
from utilities import *

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
    expected_final_os = [ArithException] 
    assert final_states[-1] == ({}, expected_final_os) # -1 because at return statement
 
def test_Arithmetics_alwaysThrows2(): 
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows2'))
    expected = ({0: Interval(INT_MIN, INT_MAX, None), 1: Interval(l=0, h=0, index=1)}, [ArithException]) # j and k in locals arith on stack
    
    assert final_states[-1] == expected

def test_Arithmetics_alwaysThrows3():
    
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows3'))
    expected = ({0: Interval(INT_MIN, INT_MAX, None), 1: Interval(INT_MIN, INT_MAX, None)}, ["ArithmeticException"])
    assert final_states[-1] == expected 


def test_Arithmetics_alwaysThrows4():
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows4'))
    expected_os = [ArithException]
    assert final_states[-1][1] == expected_os 

def test_Arithmetics_alwaysThrows5(): 
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'alwaysThrows5'))
    
    expected_final_os = [ArithException]
    assert final_states[-1][1] == expected_final_os

def test_Arithmetics_itDependsOnLattice1():
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice1'))
    
    expected_final_locals_os = ({0: Interval(l=2, h=2, index=None)}, [Interval(l=1, h=1, index=None)])
    assert final_states[-1] == expected_final_locals_os


def test_Arithmetics_itDependsOnLattice2():
    interpreter = AbstractInterpreter(program, Interval)
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice2'))
    
    expected_final_locals_os = ({0: Interval(-998, -998, None)}, [Interval(-1, -1, None)])
    assert final_states[-1] == expected_final_locals_os


def test_Arithmetics_itDependsOnLattice3():
    interpreter = AbstractInterpreter(program, Interval)
    
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice3'))
    
    expected_final_os =[ArithException]
     
    assert final_states[-1][1] == expected_final_os 


def test_Arithmetics_itDependsOnLattice4():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'itDependsOnLattice4'))
    
    expected_final_locals_os =({0: Interval(0,0, None)}, [ArithException]) # .....
    
    assert final_states[-1] == expected_final_locals_os


def test_Arithmetics_neverThrows1():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows1'))
    
    expected_final_state = ({0: Interval(l=3, h=3, index=None)}, [Interval(l=0, h=0, index=None)])

    
    assert final_states[-1] == expected_final_state 

def test_Arithmetics_neverThrows2():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows2'))
     
    expected_final_state = ({0: Interval(l=1, h=INT_MAX, index=None)}, [Interval(l=0, h=0, index=None)])
    
    assert final_states[-1] == expected_final_state

def test_Arithmetics_neverThrows3():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows3'))
     

    # fail 
    
    assert final_states[-1][-1] == [] 
    

def test_Arithmetics_neverThrows4():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows4'))
     

    # fail 
    assert final_states[-1] == [] 


def test_Arithmetics_neverThrows5():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows5'))
     

    # fail 
    assert final_states[-1] == [] 

def test_Arithmetics_speedVsPrecision():
    interpreter = AbstractInterpreter(program, Interval) 
    final_states = interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'speedVsPrecision'))
     

    # fail 
    assert final_states[-1][1] == [ArithException] 