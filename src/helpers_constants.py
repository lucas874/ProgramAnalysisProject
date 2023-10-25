import jmespath 

INT_MIN = -(2**31)
INT_MAX = 2**31 - 1

IndexException = "IndexOutOfBoundsException"
ArithException = "ArithmeticException" 
NullPtrException = "NullPointerException"
UnspptdOpException = "UnsupportedOperationException" 
AssertError = "Assertion Failed"

EXCEPTIONS = set([IndexException, ArithException, NullPtrException, UnspptdOpException])

class Program: 
    def __init__(self, classes):
        self.classes = classes
        self.bytecode = {}

        for cls_name, value in classes.items():
            ms = jmespath.search("methods[?annotations[?type=='dtu/compute/exec/Case']].[name, code.bytecode]", value)
            for m in ms:
                self.bytecode[(cls_name, m[0])] = m[1]