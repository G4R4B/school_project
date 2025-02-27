def stack_size_of(type):
    match type:
        case "int":
            return 8
        case "char":
            return 1
        case "void":
            return 0
        case ptr:
            if ptr["type"] == "pointer":
                return 8
            else:
                raise Exception("Invalid type")