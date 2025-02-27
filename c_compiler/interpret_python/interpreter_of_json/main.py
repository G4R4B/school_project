import json
import sys

import interpreter
from error import *

if len(sys.argv) != 2:
    print("Usage: python main.py <json_file>")
    sys.exit(1)
json_file = sys.argv[1]
with open(json_file) as f:
    data = json.load(f)


  
  
interpret = interpreter.Interpreter()

try:
    interpret.interpret(data)
except Exception as e:
    print(type(e).__name__ + ": " + str(e))
    errortype = type(e).__name__
    match errortype:
        case "CallException":
            sys.exit(5)
        case "NotFoundException":
            sys.exit(6)
        case "InvalidTypeException":
            sys.exit(7)
        case "SyntaxException":
            sys.exit(8)
        case "InvalidOperationException":
            sys.exit(9)
        case "InvalidIndexException":
            sys.exit(10)
        case "KeyError":
            sys.exit(12)
        case _:
            sys.exit(11)