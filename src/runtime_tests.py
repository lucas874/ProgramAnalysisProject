import timeit
import logging
from abstract_interpreter import *
from helpers_constants import *
from intervals import *
from pentagons import *
from utilities import *
from state import *
import math
logging.basicConfig(filename='metrics/runtime_ghon.log', filemode='w', format='%(asctime)s %(levelname)-10s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

def setup():
    global program
    global n # number of iterations
    n = 100
    # read the json files
    json_file_path = "course-02242-examples"
    cls_json_files = extract_files_by_extension(json_file_path, "json")
    classes = get_classes(cls_json_files)
    program = Program(classes)

def log_transformation(runtime):
    for t in runtime:
        t = math.log(t*1000, 10)
    return runtime

def intervals_runtime_arrays_alwaysThrows1():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::alwaysThrows1: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_alwaysThrows2():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::alwaysThrows2: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_alwaysThrows3():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::alwaysThrows3: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_alwaysThrows4():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows4'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::alwaysThrows4: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_alwaysThrows5():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows5'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::alwaysThrows5: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_dependsOnLattice1():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::dependsOnLattice1: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_dependsOnLattice2():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::dependsOnLattice2: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_dependsOnLattice3():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::dependsOnLattice3: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_bubbleSort():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'bubbleSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::bubbleSort: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_bubbleSort1():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'bubbleSort1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::bubbleSort1: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_insertionSort():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'insertionSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::insertionSort: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_insertionSort1():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'insertionSort1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::insertionSort1: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_selectionSort():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'selectionSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::selectionSort: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_gnomeSort():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'gnomeSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::gnomeSort: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_cycleSort():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'cycleSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::cycleSort: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_binarySearch():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'binarySearch'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::binarySearch: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_printArray():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'printArray'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::printArray: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_deconv():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Rosetta', 'deconv'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::deconv: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_shuffle():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Rosetta', 'shuffle'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::shuffle: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_hundredDoors():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Rosetta', 'hundredDoors'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::hundredDoors: {0}".format(log_transformation(t)))


def pentagons_runtime_arrays_alwaysThrows1():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::alwaysThrows1: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_alwaysThrows2():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::alwaysThrows2: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_alwaysThrows3():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::alwaysThrows3: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_alwaysThrows4():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows4'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::alwaysThrows4: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_alwaysThrows5():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'alwaysThrows5'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::alwaysThrows5: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_dependsOnLattice1():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::dependsOnLattice1: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_dependsOnLattice2():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::dependsOnLattice2: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_dependsOnLattice3():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::dependsOnLattice3: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_dependsOnLattice4():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice4'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::dependsOnLattice4: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_bubbleSort():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'bubbleSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::bubbleSort: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_bubbleSort1():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'bubbleSort1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::bubbleSort1: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_insertionSort():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'insertionSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::insertionSort: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_insertionSort1():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'insertionSort1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::insertionSort1: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_selectionSort():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'selectionSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::selectionSort: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_gnomeSort():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'gnomeSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::gnomeSort: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_cycleSort():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'cycleSort'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::cycleSort: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_binarySearch():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'binarySearch'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::binarySearch: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_printArray():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Sorting', 'printArray'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::printArray: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_deconv():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Rosetta', 'deconv'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::deconv: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_shuffle():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Rosetta', 'shuffle'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::shuffle: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_hundredDoors():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Rosetta', 'hundredDoors'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::hundredDoors: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_dependsOnLattice4():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice4'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::dependsOnLattice4: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_dependsOnLattice5():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice5'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::dependsOnLattice5: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_dependsOnLattice5():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'dependsOnLattice5'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::dependsOnLattice5: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_neverThrows1():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::neverThrows1: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_neverThrows1():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows1'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::neverThrows1: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_neverThrows2():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::neverThrows2: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_neverThrows2():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows2'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::neverThrows2: {0}".format(log_transformation(t)))

def intervals_runtime_arrays_neverThrows3():
    setup = """interpreter = AbstractInterpreter(program, Interval)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Intervals::neverThrows3: {0}".format(log_transformation(t)))

def pentagons_runtime_arrays_neverThrows3():
    setup = """interpreter = AbstractInterpreter(program, Pentagon)"""
    func = """interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'neverThrows3'))"""
    t = timeit.repeat(stmt=func, setup=setup, globals=globals(), repeat=10, number=n)
    logging.info("Pentagon::neverThrows3: {0}".format(log_transformation(t)))

if __name__ == '__main__':
    setup()
    intervals_runtime_arrays_dependsOnLattice4()
    pentagons_runtime_arrays_dependsOnLattice4()
    intervals_runtime_arrays_dependsOnLattice5()
    pentagons_runtime_arrays_dependsOnLattice5()
    intervals_runtime_arrays_neverThrows1()
    pentagons_runtime_arrays_neverThrows1()
    intervals_runtime_arrays_neverThrows2()
    pentagons_runtime_arrays_neverThrows2()
    intervals_runtime_arrays_neverThrows3()
    pentagons_runtime_arrays_neverThrows3()
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
    intervals_runtime_arrays_bubbleSort1()
    pentagons_runtime_arrays_bubbleSort1()
    intervals_runtime_arrays_insertionSort()
    pentagons_runtime_arrays_insertionSort()
    intervals_runtime_arrays_insertionSort1()
    pentagons_runtime_arrays_insertionSort1()
    intervals_runtime_arrays_selectionSort()
    pentagons_runtime_arrays_selectionSort()
    intervals_runtime_arrays_gnomeSort()
    pentagons_runtime_arrays_gnomeSort()
    intervals_runtime_arrays_cycleSort()
    pentagons_runtime_arrays_cycleSort()
    intervals_runtime_arrays_binarySearch()
    pentagons_runtime_arrays_binarySearch()
    intervals_runtime_arrays_deconv()
    pentagons_runtime_arrays_deconv()
    intervals_runtime_arrays_shuffle()
    pentagons_runtime_arrays_shuffle()
    intervals_runtime_arrays_hundredDoors()
    pentagons_runtime_arrays_hundredDoors()