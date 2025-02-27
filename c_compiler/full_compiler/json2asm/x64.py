from utils import sizeof

call_convention = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']

def convert_type_to_x64_type(type):
    match type:
        case "int":
            return "quad"
        case "char":
            return "byte"
        case "void":
            return "void"
        case "string":
            return "string"
        case ptr:
            if "type" in ptr and ptr["type"] == "pointer":
                return "quad"
            else:
                print(ptr)
                raise Exception("Invalid type")
def convert_type_to_x64_array(type, value):
    text = ""
    type = value["var_type"]["of"]
    list_of_values = value["values"]
    if list_of_values == []:
        return f"  .zero {value['len']*sizeof(type)}\n"
    else:
        for i in range(value["len"]):
            text += f"  .{convert_type_to_x64_type(type)} {list_of_values[i]}\n"
        return text

def data_add(name, type, value):
    if type == "array":
        return f'''{name}:\n{convert_type_to_x64_array(type, value)}'''
    else:
        return f'''{name}:
    .{convert_type_to_x64_type(type)} {value}'''


def x64_set_var_null(var):
    if "stack_index" in var:
        return f"movq $0, -{var['stack_index']}(%rbp)"
    else:
        return f"movq $0, {var['name']}(%rip)"
    

def x64_set_var_to_const(var, value):
    if value["type"] == "const":
        value = value["value"]
        if value["type"] == "int":
            if "stack_index" in var:
                return f"movq ${value['value']}, -{var['stack_index']}(%rbp)"
            else:
                return f"movq ${value['value']}, {var['name']}(%rip)"
        if value["type"] == "char":
            if "stack_index" in var:
                return f"movb ${value['value']}, -{var['stack_index']}(%rbp)"
            else:
                return f"movb ${value['value']}, {var['name']}(%rip)"
    elif value["type"] == "rodata":
        if "stack_index" in var:
            return f"lea .LC{value['at']}(%rip), %rax\n\tmovq %rax, -{var['stack_index']}(%rbp)"
        else:
            return f"lea .LC{value['at']}(%rip), %rax\n\tmovq %rax, {var['name']}(%rip)"
    else:
        raise Exception("Set var to const error")

def x64_set_array_to(stack_index, len, of):
    text = ""
    for i in range(len-1, -1, -1):
        text += "\tpopq %rax\n"
        text += f"\tmovq %rax, -{stack_index-i*sizeof(of)}(%rbp)\n"
    return text



def x64_push_const(value):
    if value["type"] == "int":
        return f"pushq ${value['value']}"
    elif value["type"] == "char":
        return f"pushq ${value['value']}"
    else:
        raise Exception("Push const error")
    #todo: add support for other types
def x64_rax_assign(var):
    text = "popq %rax\n"
    if "stack_index" in var:
        return text+f"\tmovq %rax, -{var['stack_index']}(%rbp)"
    else:
        return text+f"\tmovq %rax, {var['name']}(%rip)"
    
def x64_push_var(var):
    if var["type"] == "array":
        return x64_push_adress(var)
    if "stack_index" in var:
        return f"pushq -{var['stack_index']}(%rbp)"
    else:
        return f"pushq {var['name']}(%rip)"

def x64_push_rodata(at):
    return f"lea .LC{at}(%rip), %rax\n\tpushq %rax"

def x64_set_rodata_to_char_at(at, var, index):
    text = f"lea .LC{at}(%rip), %rax\n"
    text += f"\tmovb {index}(%rax), %al\n"
    if "stack_index" in var:
        return text + f"\tmovb %al, -{var['stack_index']}(%rbp)"
    else:
        return text + f"\tmovq %al, {var['name']}(%rip)"

def x64_call(name, decl):
    #add stack alignment
    if name in decl:
        text = "call "+name+"\n"
        return text
    else:
        text = "pushq %rbp\n"
        text += "\tmovq %rsp, %rbp\n"
        text += "\tandq $-16, %rsp\n"
        text += "\tcall "+name+"\n"
        text += "\tmovq %rbp, %rsp\n"
        text += "\tpopq %rbp"
        return text


def x64_push_adress(var):
    if "stack_index" in var:
        return f"lea -{var['stack_index']}(%rbp), %rax\n\tpushq %rax"
    else:
        return f"lea {var['name']}(%rip), %rax\n\tpushq %rax"
    
def x64_return():
    text = "popq %rax\n"
    return text+f"\tleave\n\tret"

def x64_mov(dest, src, tab=0):
    return "\t"*tab+f"movq {src}, {dest}"

def x64_ge():
    text = "cmpq %rbx, %rax\n"
    text += "\tsetge %al\n"
    text += "\tmovzbq %al, %rax\n"
    return text

def x64_le():
    text = "cmpq %rbx, %rax\n"
    text += "\tsetle %al\n"
    text += "\tmovzbq %al, %rax\n"
    return text

def x64_gt():
    text = "cmpq %rbx, %rax\n"
    text += "\tsetg %al\n"
    text += "\tmovzbq %al, %rax\n"
    return text

def x64_lt():
    text = "cmpq %rbx, %rax\n"
    text += "\tsetl %al\n"
    text += "\tmovzbq %al, %rax\n"
    return text

def x64_eq():
    text = "cmpq %rbx, %rax\n"
    text += "\tsete %al\n"
    text += "\tmovzbq %al, %rax\n"
    return text

def x64_ne():
    text = "cmpq %rbx, %rax\n"
    text += "\tsetne %al\n"
    text += "\tmovzbq %al, %rax\n"
    return text

def x64_convert_to_bool_rax():
    text = "cmpq $0, %rax\n"
    text += "\tsetne %al\n"
    text += "\tmovzbq %al, %rax\n"
    return text

def x64_convert_to_bool_rbx():
    text = "cmpq $0, %rbx\n"
    text += "\tsetne %bl\n"
    text += "\tmovzbq %bl, %rbx\n"
    return text

def x64_and():
    text = x64_convert_to_bool_rax()
    text += x64_convert_to_bool_rbx()
    text += "andq %rbx, %rax\n"
    return text

def x64_or():
    text = x64_convert_to_bool_rax()
    text += x64_convert_to_bool_rbx()
    text += "orq %rbx, %rax\n"
    return text
