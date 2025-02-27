import json
import sys

import ast2asm

if len(sys.argv) != 2:
    print("Usage: python main.py <json_file>")
    sys.exit(1)
json_file = sys.argv[1]
with open(json_file) as f:
    data = json.load(f)


  
  
compiler = ast2asm.Compiler()

try:
    result = compiler.gen(data)
    with open(json_file.replace("_preprocess.json", "") + ".s", "w") as f:
        f.write("\n".join(result))
except Exception as e:
    print(type(e).__name__ + ": " + str(e))