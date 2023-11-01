from helpers_constants import *
from abstract_interpreter import *
from intervals import *

def main():
    # read the json files
    #json_file_path = "assignment_5\decompiled"
    json_file_path = "../exceptional" 
    cls_json_files = extract_files_by_extension(json_file_path, "json")
    classes = get_classes(cls_json_files)
    
    
    # program class usage
    program = Program(classes)

    interpreter = AbstractInterpreter(program, Interval)

    #pretty_print_bytecode(program, ('eu/bogoe/dtu/exceptional/Arithmetics', 'speedVsPrecision'))
    pretty_print_bytecode(program,('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows4'))
    #interpreter.analyse(('dtu/compute/exceptional/Arrays', 'bubbleSort'))
    #interpreter.analyse(('eu/bogoe/dtu/exceptional/Arrays', 'selectionSort'))
    interpreter.analyse(('eu/bogoe/dtu/exceptional/Arithmetics', 'neverThrows4'))

if __name__ == "__main__":
    main()