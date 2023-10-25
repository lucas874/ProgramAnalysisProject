import json
import glob
from helpers_constants import *

def extract_files_by_extension(path: str, extension: str) -> list[str]:
    """
    extract the jave files present in the directory
    """
    if path[-1] != "/": # works fine in Windows if that was the question
        path += "/"

    pattern =  "**/*." + extension 
    return [name for name in glob.glob(path + pattern, recursive=True)]

def get_classes(json_files):
    classes = {}
    for file in json_files:
        with open(file) as f:
            json_data = json.load(f)
            classes[json_data["name"]] = json_data
    return classes

def find_methods(classes):
    methods = {}
    for cls in classes.values():
        #print(cls)
        m = []
        for method in cls["methods"]:
            if method["name"] != "<init>":
                m.append(method["name"])
        methods[cls["name"]] = m
    return methods
   
def pretty_print_bytecode(program, am):
    print(am[0] + "." + am[1] + ":")
    for i,inst in enumerate(program.bytecode[am]):
        print(i, ": ", inst)