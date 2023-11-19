import timeit
import logging
from abstract_interpreter import *
from helpers_constants import *
from intervals import *
from pentagons import *
from utilities import *
from state import *
logging.basicConfig(filename='logs/runtime_comparison.log', filemode='w', format='%(asctime)s %(levelname)-5s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

def setup():
    global program
    global n # number of iterations
    n = 100
    # read the json files
    json_file_path = "exceptional"
    cls_json_files = extract_files_by_extension(json_file_path, "json")
    classes = get_classes(cls_json_files)
    program = Program(classes)

def intervals_runtime_arrays_alwaysThrows1():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::alwaysThrows1: {0}".format(t))

def intervals_runtime_arrays_alwaysThrows2():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::alwaysThrows2: {0}".format(t))

def intervals_runtime_arrays_alwaysThrows3():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::alwaysThrows3: {0}".format(t))

def intervals_runtime_arrays_alwaysThrows4():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows4'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::alwaysThrows4: {0}".format(t))

def intervals_runtime_arrays_alwaysThrows5():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows5'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::alwaysThrows5: {0}".format(t))

def intervals_runtime_arrays_dependsOnLattice1():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::dependsOnLattice1: {0}".format(t))

def intervals_runtime_arrays_dependsOnLattice2():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::dependsOnLattice2: {0}".format(t))

def intervals_runtime_arrays_dependsOnLattice3():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::dependsOnLattice3: {0}".format(t))

def intervals_runtime_arrays_bubbleSort():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'bubbleSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::bubbleSort: {0}".format(t))

def intervals_runtime_arrays_insertionSort():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'insertionSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::insertionSort: {0}".format(t))

def intervals_runtime_arrays_selectionSort():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'selectionSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::selectionSort: {0}".format(t))

def intervals_runtime_arrays_binarySearch():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'binarySearch'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::binarySearch: {0}".format(t))

def intervals_runtime_arrays_printArray():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'printArray'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Intervals::printArray: {0}".format(t))

def pentagons_runtime_arrays_alwaysThrows1():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::alwaysThrows1: {0}".format(t))

def pentagons_runtime_arrays_alwaysThrows2():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::alwaysThrows2: {0}".format(t))

def pentagons_runtime_arrays_alwaysThrows3():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::alwaysThrows3: {0}".format(t))

def pentagons_runtime_arrays_alwaysThrows4():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows4'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::alwaysThrows4: {0}".format(t))

def pentagons_runtime_arrays_alwaysThrows5():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows5'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::alwaysThrows5: {0}".format(t))

def pentagons_runtime_arrays_dependsOnLattice1():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::dependsOnLattice1: {0}".format(t))

def pentagons_runtime_arrays_dependsOnLattice2():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::dependsOnLattice2: {0}".format(t))

def pentagons_runtime_arrays_dependsOnLattice3():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::dependsOnLattice3: {0}".format(t))

def pentagons_runtime_arrays_dependsOnLattice4():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice4'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::dependsOnLattice4: {0}".format(t))

def pentagons_runtime_arrays_bubbleSort():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'bubbleSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::bubbleSort: {0}".format(t))

def pentagons_runtime_arrays_insertionSort():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'insertionSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::insertionSort: {0}".format(t))

def pentagons_runtime_arrays_selectionSort():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'selectionSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::selectionSort: {0}".format(t))

def pentagons_runtime_arrays_binarySearch():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'binarySearch'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::binarySearch: {0}".format(t))

def pentagons_runtime_arrays_printArray():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/arrayaccess/Sorting', 'printArray'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=5, number=n)
    logging.info("Pentagon::printArray: {0}".format(t))

if __name__ == '__main__':
    setup()
    intervals_runtime_arrays_alwaysThrows1()
    pentagons_runtime_arrays_alwaysThrows1()
    intervals_runtime_arrays_alwaysThrows2()
    pentagons_runtime_arrays_alwaysThrows2()
    intervals_runtime_arrays_alwaysThrows3()
    pentagons_runtime_arrays_alwaysThrows3()
    intervals_runtime_arrays_alwaysThrows4()
    pentagons_runtime_arrays_alwaysThrows4()
    intervals_runtime_arrays_alwaysThrows5()
    pentagons_runtime_arrays_alwaysThrows5()
    intervals_runtime_arrays_dependsOnLattice1()
    pentagons_runtime_arrays_dependsOnLattice1()
    intervals_runtime_arrays_dependsOnLattice2()
    pentagons_runtime_arrays_dependsOnLattice2()
    intervals_runtime_arrays_dependsOnLattice3()
    pentagons_runtime_arrays_dependsOnLattice3()
    intervals_runtime_arrays_bubbleSort()
    pentagons_runtime_arrays_bubbleSort()
    intervals_runtime_arrays_insertionSort()
    pentagons_runtime_arrays_insertionSort()
    intervals_runtime_arrays_selectionSort()
    pentagons_runtime_arrays_selectionSort()
    intervals_runtime_arrays_binarySearch()
    pentagons_runtime_arrays_binarySearch()