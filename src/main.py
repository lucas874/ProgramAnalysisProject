from helpers_constants import *
from abstract_interpreter import *
from intervals import *
from pentagons import *
import sys

def usage(argv):
    print(f"python3 {argv[0]} <some class. with package too. as path. relative to json file path look in code for this.> <some method> <[i]nterval/[p]entagon>")
    print(f"example: python3 main.py eu/bogoe/dtu/exceptional/Arithmetics neverThrows5")

def main():
    if len(sys.argv) != 4:
        usage(sys.argv)
        sys.exit(1)

    # read the json files  and get classes
    json_file_path = "../course-02242-examples/"
    #json_file_path = "../exceptional/"
    cls_json_files = extract_files_by_extension(json_file_path, "json")
    classes = get_classes(cls_json_files)
     
    # program holds all loaded methods
    program = Program(classes)
    abstraction = Interval if sys.argv[3] == "i" else (Pentagon if sys.argv[3] == "p" else Interval)
    interpreter = AbstractInterpreter(program, abstraction, debug=True)
    class_ = sys.argv[1]
    method = sys.argv[2] 
    #for k in program.bytecode:
    #    print(k) 
    pretty_print_bytecode(program,(class_, method))
    interpreter.analyse((class_, method)) 

if __name__ == "__main__":
    main()