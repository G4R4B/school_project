call_convention = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']

def sizeof(type):
    match type:
        case "int":
            return 8
        case "char":
            return 1
        case ptr:
            if ptr["type"] == "pointer":
                return 8
            elif ptr["type"] == "array":
                return 8
                raise Exception("Invalid type")
def size_of_function(typeof):
    if typeof == "int":
        return 8
    if typeof == "char":
        return 1
    if typeof["type"] == "pointer":
        return 8
    if typeof["type"] == "array":
        if type(typeof["len"]) == dict:
            return sizeof(typeof["of"])*typeof["len"]["value"]["value"]
        return sizeof(typeof["of"])*typeof["len"]
            
def size_of_operation(type):
    if type == "int":
        return 1
    if type["type"] == "pointer":
        return 8
    if type["type"] == "array":
        return sizeof(type["of"])
    
def not_two_memory_references(src, dst):
    if src[0] == "%" or dst[0] == "%":
        return True
    return False

def is_a_array_args(arg):
    if arg["in_args"]:
        var_type = arg["var_type"]
        if "type" in var_type["of"]:
            if var_type["of"]["type"] == "array":
                return True
    return False