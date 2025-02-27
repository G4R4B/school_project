import json
import sys

import generator

if len(sys.argv) != 2:
    print("Usage: python main.py <json_file>")
    sys.exit(1)
json_file = sys.argv[1]
with open(json_file) as f:
    data = json.load(f)


  
  
generator = generator.Generator()

try:
    new_ast = generator.gen(data)
    with open(json_file.replace(".json", "") + "_preprocess" + ".json", "w") as f:
        f.write(json.dumps(new_ast, indent=4))
except Exception as e:
    print(type(e).__name__ + ": " + str(e))