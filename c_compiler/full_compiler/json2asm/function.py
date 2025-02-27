from x64 import *
from utils import *
import hashlib

class Function:
    def __init__(self, name, body, args, local_vars, global_vars, declared_functions):
        self.name = name
        self.body = body
        self.args = args
        self.local_vars = local_vars
        self.instructions = []
        #scope
        self.current_accessible_vars = global_vars.copy() 
        for arg in args:
            args[arg].update({"in_args": True})
            self.current_accessible_vars.update({arg: args[arg]})
        self.declared_functions = declared_functions
        self.current_block = 0
        self.height = 0
        self.height_current_block = {0: 0}
        self.previous_loop_height = []
        self.addrneeded = False
    def get_type(self, expr):
        if expr["type"] == "const":
            return "int"
        elif expr["type"] == "global_var" or expr["type"] == "var" or expr["type"] == "local_var":
            if "want_address" in self.current_accessible_vars[expr["name"]]:
                return  {"type": "pointer", "of": self.current_accessible_vars[expr["name"]]["type"]}
            if self.current_accessible_vars[expr["name"]]["type"] == "array":
                return {"type": "array", "of": self.current_accessible_vars[expr["name"]]["var_type"]["of"], "len": self.current_accessible_vars[expr["name"]]["value"]["len"]}
            if "var_type" in self.current_accessible_vars[expr["name"]]:
                return self.current_accessible_vars[expr["name"]]["var_type"]
            return self.current_accessible_vars[expr["name"]]["type"]
        elif expr["type"] == "rodata":
            return "string"
        elif expr["type"] == "binop":
            return self.compare_types(expr["lhs"], expr["rhs"])[0]
        elif expr["type"] == "unop":
            if expr["op"] == "&":
                return {"type": "pointer", "of": self.get_type(expr["expr"])}
            if expr["op"] == "*":
                if 'of' in self.get_type(expr["expr"]):
                    return self.get_type(expr["expr"])['of']
                else:
                    print(expr)
                    raise Exception("Pointer dereference of non pointer type")
            return self.get_type(expr["expr"])
        elif expr["type"] == "array_get":
            if 'of' in self.current_accessible_vars[expr["name"]]['var_type']:
                return (self.current_accessible_vars[expr["name"]]['var_type']['of'])
        elif expr["type"] == "array_get_generic":
            return self.get_type(expr["where"])
        elif expr["type"] == "call":
            return self.declared_functions[expr["name"]]
        elif expr["type"] == "sizeof":
            return "int"
        else:
            print(expr)
        raise Exception("Not handled")
    
    def compare_types(self, lhs, rhs, start = False):
        typeleft =self.get_type(lhs)
        typeright = self.get_type(rhs)
        if type(typeleft) == dict and type(typeright) == dict:
            return typeleft, "both"
        elif type(typeleft) == dict:
            return typeleft, "left"
        elif type(typeright) == dict:
            return typeright, "right"
        else:
            return "int", "both"

        
    
    @staticmethod
    def create(name, body, args, local_vars, global_vars, declared_functions):
        return Function(name, body, args, local_vars, global_vars, declared_functions)
    def eval_expr(self, expr):
        if expr["type"] == "const":
            self.instructions.append(x64_push_const(expr["value"]))
        elif expr["type"] == "global_var" or expr["type"] == "var" or expr["type"] == "local_var":
            if self.addrneeded:
                self.instructions.append(x64_push_adress(self.current_accessible_vars[expr["name"]]))
            else:
                self.instructions.append(x64_push_var(self.current_accessible_vars[expr["name"]]))
        elif expr["type"] == "rodata":
            self.instructions.append(x64_push_rodata(expr["at"]))
        elif expr["type"] == "binop":
            #lazy logic part
            if expr["op"] == "&&":
                unique_id = hashlib.md5(str(expr).encode()).hexdigest()
                self.eval_expr(expr["lhs"])
                self.instructions.append("popq %rax")
                self.instructions.append("cmpq $0, %rax")
                self.instructions.append("setne %al")
                self.instructions.append("movzbq %al, %rax")
                self.instructions.append("pushq %rax")
                self.instructions.append("jz AND_FALSE_"+unique_id)
                self.eval_expr(expr["rhs"])
                self.instructions.append("jmp AND_"+unique_id)
                self.instructions.append("AND_FALSE_"+unique_id+":")
                self.instructions.append("pushq $0")
                self.instructions.append("AND_"+unique_id+":")
                
                
            elif expr["op"] == "||":
                unique_id = hashlib.md5(str(expr).encode()).hexdigest()
                self.eval_expr(expr["lhs"])
                self.instructions.append("popq %rax")
                self.instructions.append("cmpq $0, %rax")
                self.instructions.append("setne %al")
                self.instructions.append("movzbq %al, %rax")
                self.instructions.append("pushq %rax")
                self.instructions.append("jnz OR_TRUE_"+unique_id)
                self.eval_expr(expr["rhs"])
                self.instructions.append("jmp OR_"+unique_id)
                self.instructions.append("OR_TRUE_"+unique_id+":")
                self.instructions.append("pushq $1")
                self.instructions.append("OR_"+unique_id+":")
                
                
            else:
                self.eval_expr(expr["lhs"])
                self.eval_expr(expr["rhs"])
            type_for_scalar, order = self.compare_types(expr["lhs"], expr["rhs"])
            self.instructions.append(f"popq %rbx")
            self.instructions.append(f"popq %rax")
            if expr["op"] == "+":
                if order == "left":
                    self.instructions.append(f"leaq (%rax, %rbx, {size_of_operation(type_for_scalar)}), %rax")
                elif order == "right":
                    self.instructions.append(f"leaq (%rbx, %rax, {size_of_operation(type_for_scalar)}), %rax")
                elif order == "both" and type_for_scalar == "int":
                    self.instructions.append("addq %rbx, %rax")
                else:
                    raise Exception(f'{expr["op"]} not handled for {order} {type_for_scalar}')
            elif expr["op"] == "-":
                if order == "left":
                    self.instructions.append(f"imulq ${size_of_operation(type_for_scalar)}, %rbx")
                    self.instructions.append("subq %rbx, %rax")
                elif order == "right":
                    self.instructions.append(f"imulq ${size_of_operation(type_for_scalar)}, %rax")
                    self.instructions.append("subq %rax, %rbx")
                elif order == "both" and type_for_scalar != "int":
                    self.instructions.append("subq %rbx, %rax")
                    self.instructions.append("cqto")
                    self.instructions.append(f"movq ${size_of_operation(type_for_scalar)}, %rbx")
                    self.instructions.append("idivq %rbx")
                else:
                    self.instructions.append("subq %rbx, %rax")

            elif expr["op"] == "*":
                self.instructions.append("imulq %rbx, %rax")
            elif expr["op"] == "/":
                self.instructions.append("cqto")
                self.instructions.append("idivq %rbx")
            elif expr["op"] == "%":
                self.instructions.append("cqto")
                self.instructions.append("idivq %rbx")
                self.instructions.append("movq %rdx, %rax")
            elif expr["op"] == ">=":
                self.instructions.append(x64_ge())
            elif expr["op"] == "<=":
                self.instructions.append(x64_le())
            elif expr["op"] == ">":
                self.instructions.append(x64_gt())
            elif expr["op"] == "<":
                self.instructions.append(x64_lt())
            elif expr["op"] == "==":
                self.instructions.append(x64_eq())
            elif expr["op"] == "!=":
                self.instructions.append(x64_ne())
            elif expr["op"] == "&&":
                self.instructions.append(x64_and())
            elif expr["op"] == "||":
                self.instructions.append(x64_or())
            else:
                print(expr)
                raise Exception("Binop not handled")
            self.instructions.append("pushq %rax")
        elif expr["type"] == "unop":
            if expr["op"] == "&":
                self.addrneeded = True
                self.eval_expr(expr["expr"])
                self.addrneeded = False
                return
            self.eval_expr(expr["expr"])
            self.instructions.append("popq %rax")
            if expr["op"] == "-":
                self.instructions.append("negq %rax")
            elif expr["op"] == "!":
                self.instructions.append("cmpq $0, %rax")
                self.instructions.append("sete %al")
                self.instructions.append("movzbq %al, %rax")
            elif expr["op"] == "*":
                self.instructions.append("movq (%rax), %rax")
            elif expr["op"] == "++post":
                self.instructions.append("pushq %rax")
                type_for_scalar = self.get_type(expr["expr"])
                if type(type_for_scalar) == dict:
                    self.instructions.append(f"add ${size_of_operation(type_for_scalar)}, %rax")
                else:
                    self.instructions.append("incq %rax")
                self.instructions.append("pushq %rax")
                if "name" in expr["expr"]:
                    self.instructions.append(x64_rax_assign(self.current_accessible_vars[expr["expr"]["name"]]))
                elif expr["expr"]["type"] == "unop" and expr["expr"]["op"] == "*":
                    self.instructions.append(x64_push_var(self.current_accessible_vars[expr["expr"]["expr"]["name"]]))
                    self.instructions.append("popq %rbx")
                    self.instructions.append("popq %rax")
                    self.instructions.append("movq %rax, (%rbx)")
                return
            elif expr["op"] == "++pre":
                type_for_scalar = self.get_type(expr["expr"])
                if type(type_for_scalar) == dict:
                    self.instructions.append(f"add ${size_of_operation(type_for_scalar)}, %rax")
                else:
                    self.instructions.append("incq %rax")
                self.instructions.append("pushq %rax")
                if "name" in expr["expr"]:
                    self.instructions.append(x64_rax_assign(self.current_accessible_vars[expr["expr"]["name"]]))
                elif expr["expr"]["type"] == "unop" and expr["expr"]["op"] == "*":
                    self.instructions.append(x64_push_var(self.current_accessible_vars[expr["expr"]["expr"]["name"]]))
                    self.instructions.append("popq %rbx")
                    self.instructions.append("popq %rax")
                    self.instructions.append("movq %rax, (%rbx)")
            elif expr["op"] == "--pre":
                type_for_scalar = self.get_type(expr["expr"])
                if type(type_for_scalar) == dict:
                    self.instructions.append(f"sub ${size_of_operation(type_for_scalar)}, %rax")
                else:
                    self.instructions.append("decq %rax")
                self.instructions.append("pushq %rax")
                if "name" in expr["expr"]:
                    self.instructions.append(x64_rax_assign(self.current_accessible_vars[expr["expr"]["name"]]))
                elif expr["expr"]["type"] == "unop" and expr["expr"]["op"] == "*":
                    self.instructions.append(x64_push_var(self.current_accessible_vars[expr["expr"]["expr"]["name"]]))
                    self.instructions.append("popq %rbx")
                    self.instructions.append("popq %rax")
                    self.instructions.append("movq %rax, (%rbx)")
            elif expr["op"] == "--post":
                self.instructions.append("pushq %rax")
                type_for_scalar = self.get_type(expr["expr"])
                if type(type_for_scalar) == dict:
                    self.instructions.append(f"sub ${size_of_operation(type_for_scalar)}, %rax")
                else:
                    self.instructions.append("decq %rax")
                self.instructions.append("pushq %rax")
                if "name" in expr["expr"]:
                    self.instructions.append(x64_rax_assign(self.current_accessible_vars[expr["expr"]["name"]]))
                elif expr["expr"]["type"] == "unop" and expr["expr"]["op"] == "*":
                    self.instructions.append(x64_push_var(self.current_accessible_vars[expr["expr"]["expr"]["name"]]))
                    self.instructions.append("popq %rbx")
                    self.instructions.append("popq %rax")
                    self.instructions.append("movq %rax, (%rbx)")
                return
            else:
                print(expr)
                raise Exception("Unary operation not handled")
            self.instructions.append("pushq %rax")
        elif expr["type"] == "array_get" or expr["type"] == "array_get_generic":
            address_needed = self.addrneeded
            self.addrneeded = False
            if "in_args" in self.current_accessible_vars[expr["name"]]:  
                in_args = is_a_array_args(self.current_accessible_vars[expr["name"]])
            else:
                in_args = False # this is if the array is a global variable
            if ((self.current_accessible_vars[expr["name"]]["type"] == "array") or in_args) and expr["type"] == "array_get_generic":
                self.eval_expr(expr["where"]["index"])
                if in_args:
                    self.instructions.append(x64_push_var(self.current_accessible_vars[expr["name"]]))
                else:
                    self.instructions.append(x64_push_adress(self.current_accessible_vars[expr["name"]]))
                self.instructions.append("popq %rax")
                self.instructions.append("popq %rbx")
                if in_args:
                    first_len = int(self.current_accessible_vars[expr["name"]]["var_type"]["first_len"])
                else:
                    first_len = self.current_accessible_vars[expr["name"]]["var_type"]["first_len"]["value"]["value"]
                self.instructions.append(f"imulq ${first_len*size_of_operation(self.current_accessible_vars[expr['name']]['var_type'])}, %rbx")
                self.instructions.append("addq %rbx, %rax")
                self.instructions.append("pushq %rax")
            elif expr["type"] == "array_get_generic":
                self.eval_expr(expr["where"])
            else:
                try:
                    if self.current_accessible_vars[expr["name"]]["var_type"]['type'] == "pointer":
                        self.instructions.append(x64_push_var(self.current_accessible_vars[expr["name"]]))
                    else:
                        self.instructions.append(x64_push_adress(self.current_accessible_vars[expr["name"]]))
                except:
                    raise Exception("Variable not found")
            self.eval_expr(expr["index"])
            if 'of' in self.current_accessible_vars[expr["name"]]['var_type']:
                typeofarray = (self.current_accessible_vars[expr["name"]]['var_type']['of'])
            else:
                raise Exception("Array get on a no pointer or array type")
            self.instructions.append("popq %rbx")
            self.instructions.append("popq %rax")
            self.instructions.append(f"imulq ${sizeof(typeofarray)}, %rbx")
            self.instructions.append("addq %rbx, %rax")
            if address_needed:
                self.instructions.append("pushq %rax")
            else:
                if typeofarray == "char":
                    self.instructions.append("movb (%rax), %al")
                    self.instructions.append("movzbq %al, %rax")
                else:
                    self.instructions.append("movq (%rax), %rax")
                    
                self.instructions.append("pushq %rax")
        elif expr["type"] == "call":
            args_pushed_to_the_stack = self.handle_args(expr["args"])
            self.instructions.append(x64_call(expr["name"], self.declared_functions))
            if args_pushed_to_the_stack > 0:
                self.instructions.append(f"addq ${8*args_pushed_to_the_stack}, %rsp")
            self.instructions.append("pushq %rax")
        elif expr["type"] == "sizeof":
            self.get_type(expr["value"])
            self.instructions.append(f"pushq ${size_of_function(self.get_type(expr['value']))}")
        else:
            print(expr)
            raise Exception("Expr not handled")
    
    def handle_args(self, args):
        for i in range(len(args)-1,-1,-1):
            self.eval_expr(args[i])
        for i in range(len(args)):
            if i < 6:
                self.instructions.append(f"popq %{call_convention[i]}")
        return len(args) - 6

    def parse_instruction(self, instr):
        if instr["type"] == "break":
            i = 1
            previous_loop,previous_loop_type = self.previous_loop_height[-1]
            self.instructions.append(f"jmp .L{self.name}{self.current_block+1}H{previous_loop}")
        elif instr["type"] == "continue":
            i = 1
            previous_loop,previous_loop_type = self.previous_loop_height[-1]
            if previous_loop_type == "for":
                self.instructions.append(f"jmp .L{self.name}{self.current_block}H{previous_loop}INC")
            elif previous_loop_type == "while":
                self.instructions.append(f"jmp .L{self.name}{self.current_block}H{previous_loop}")
            else:
                raise Exception("Continue not in loop")
        elif instr["type"] == "block":
            self.height += 1
            tmp_current_accessible_vars = self.current_accessible_vars.copy()
            if self.height not in self.height_current_block:
                self.height_current_block[self.height] = 0
            for i in instr["body"]:
                self.parse_instruction(i)
            self.current_accessible_vars = tmp_current_accessible_vars
            self.height -= 1
        elif instr["type"] == "var":
            self.current_accessible_vars[instr["name"]] = {"type": instr["type"], "value": 0, "stack_index": instr["stack_index"], "var_type": instr["var_type"], "in_args": False}
            self.instructions.append(x64_set_var_null(self.current_accessible_vars[instr["name"]]))
        elif instr["type"] == "varset":
            self.current_accessible_vars[instr["name"]] = {"type": instr["type"], "value": instr["value"], "stack_index": instr["stack_index"], "var_type": instr["var_type"], "in_args": False}
            if instr["value"]["type"] == "const" or instr["value"]["type"] == "rodata":
                self.instructions.append(x64_set_var_to_const(self.current_accessible_vars[instr["name"]], instr["value"]))
            else:
                self.eval_expr(instr["value"])
                self.instructions.append(x64_rax_assign(self.current_accessible_vars[instr["name"]]))
        elif instr["type"] == "assign":
            self.eval_expr(instr["value"])
            self.instructions.append(x64_rax_assign(self.current_accessible_vars[instr["name"]]))
        elif instr["type"] == "assign_deref":
            self.eval_expr(instr["value"])
            self.eval_expr(instr["where"])
            self.instructions.append("popq %rbx")
            self.instructions.append("popq %rax")
            self.instructions.append("movq %rax, (%rbx)")
        elif instr["type"] == "array_set":
            try:
                var_complete = self.current_accessible_vars[instr["name"]]
                if var_complete["var_type"]['type'] == "pointer":
                    self.instructions.append(x64_push_var(self.current_accessible_vars[instr["name"]]))
                else:
                    self.instructions.append(x64_push_adress(self.current_accessible_vars[instr["name"]]))
            except:
                raise Exception("Variable not found")
            self.eval_expr(instr["index"])
            self.eval_expr(instr["value"])
            if 'of' in self.current_accessible_vars[instr["name"]]['var_type']:
                typeofarray = (self.current_accessible_vars[instr["name"]]['var_type']['of'])
            else:
                raise Exception("Array set on a no pointer or array type")
            self.instructions.append("popq %rcx")
            self.instructions.append("popq %rbx")
            self.instructions.append("popq %rax")
            self.instructions.append(f"imulq ${sizeof(typeofarray)}, %rbx")
            self.instructions.append("addq %rbx, %rax")
            if typeofarray == "char":
                self.instructions.append("movb %cl, (%rax)")
            else:
                self.instructions.append("movq %rcx, (%rax)")
        elif instr["type"] == "array_set_generic":
            name = instr["where"]["name"]
            if "in_args" in self.current_accessible_vars[name]:  
                in_args = (self.current_accessible_vars[name]["in_args"])
            else:
                in_args = False # this is if the array is a global variable
            if ((self.current_accessible_vars[name]["type"] == "array")  or in_args)  and instr["type"] == "array_set_generic":
                self.eval_expr(instr["where"]["index"])
                if in_args:
                    self.instructions.append(x64_push_var(self.current_accessible_vars[name]))
                else:
                    self.instructions.append(x64_push_adress(self.current_accessible_vars[name]))
                self.instructions.append("popq %rax")
                self.instructions.append("popq %rbx")
                if in_args:
                    first_len = int(self.current_accessible_vars[name]["var_type"]["first_len"])
                else:
                    first_len = self.current_accessible_vars[name]["var_type"]["first_len"]["value"]["value"]
                self.instructions.append(f"imulq ${first_len*size_of_operation(self.current_accessible_vars[name]['var_type'])}, %rbx")
                self.instructions.append("addq %rbx, %rax")
                self.instructions.append("pushq %rax")
            else:
                self.eval_expr(instr["where"])
            self.eval_expr(instr["index"])
            self.eval_expr(instr["value"])
            typeofarray = self.get_type(instr["where"])
            self.instructions.append("popq %rcx")
            self.instructions.append("popq %rbx")
            self.instructions.append("popq %rax")
            self.instructions.append(f"imulq ${sizeof(typeofarray)}, %rbx")
            self.instructions.append(f"addq %rbx, %rax")
            self.instructions.append("movq %rcx, (%rax)")
        elif instr["type"] == "array":
            var_type = instr["var_type"]
            self.current_accessible_vars[instr["name"]] = {"type": instr["type"], "value": instr["value"], "stack_index": instr["stack_index"], "var_type": var_type, "in_args": False}
            stack_index = instr["stack_index"]
            values = instr["value"]
            lenarr = values["len"]["value"]["value"]
            of = var_type["of"]
            real_values = values["Values"]
            if len(real_values) == 0:
                return
            elif len(real_values) == 1:
                if real_values[0]["type"] == "const":
                    for i in range(lenarr):
                        self.instructions.append(x64_set_var_to_const({"type": "var", "value": real_values[0], "stack_index": stack_index - i*sizeof(of)}, real_values[0]))
                if real_values[0]["type"] == "rodata":
                    for i in range(real_values[0]["len"]):
                        self.instructions.append(x64_set_rodata_to_char_at(real_values[0]["at"], {"type": "var", "stack_index": stack_index - i*sizeof(of)}, i))
                    self.instructions.append(x64_set_var_to_const({"type": "var", "stack_index": stack_index - real_values[0]["len"]*sizeof(of)}, {"type": "const", "value": {"type": "int", "value": 0}}))
            else:
                for i in range(len(real_values)):
                    self.eval_expr(real_values[i])
                self.instructions.append(x64_set_array_to(stack_index, lenarr, of))
        elif instr["type"] == "return":
            self.eval_expr(instr["value"])
            self.instructions.append(x64_return())
        elif instr["type"] == "call":
            args_pushed_to_the_stack = self.handle_args(instr["args"])
            self.instructions.append(x64_call(instr["name"], self.declared_functions))
            if args_pushed_to_the_stack > 0:
                self.instructions.append(f"addq ${8*args_pushed_to_the_stack}, %rsp")
        elif instr["type"] == "if_else":

            self.eval_expr(instr["cond"])
            self.instructions.append("popq %rax")
            self.instructions.append("cmpq $0, %rax")
            self.instructions.append(f"je .L{self.name}{self.current_block}H{self.height}ELSE{self.height_current_block[self.height]}")
            self.parse_instruction(instr["then"])
            self.instructions.append(f"jmp .L{self.name}{self.current_block+1}H{self.height}FIN{self.height_current_block[self.height]}")
            self.instructions.append(f".L{self.name}{self.current_block}H{self.height}ELSE{self.height_current_block[self.height]}:")
            self.parse_instruction(instr["else"])
            self.instructions.append(f".L{self.name}{self.current_block+1}H{self.height}FIN{self.height_current_block[self.height]}:")
            if self.height == 0:
                self.current_block += 2
            else:
                self.height_current_block[self.height] += 1
        elif instr["type"] == "if":
            self.eval_expr(instr["cond"])
            self.instructions.append("popq %rax")
            self.instructions.append("cmpq $0, %rax")
            self.instructions.append(f"je .L{self.name}{self.current_block}H{self.height}FIN{self.height_current_block[self.height]}")
            self.parse_instruction(instr["then"])
            self.instructions.append(f".L{self.name}{self.current_block}H{self.height}FIN{self.height_current_block[self.height]}:")
            if self.height == 0:
                self.current_block += 1
            else:
                self.height_current_block[self.height] += 1
        elif instr["type"] == "for":
            self.previous_loop_height.append((self.height, "for"))
            self.parse_instruction(instr["init"])
            self.instructions.append(f".L{self.name}{self.current_block}H{self.height}:")
            self.eval_expr(instr["cond"])
            self.instructions.append("\tpopq %rax")
            self.instructions.append("\tcmpq $0, %rax")
            self.instructions.append(f"je .L{self.name}{self.current_block+1}H{self.height}")
            self.parse_instruction(instr["body"])
            self.instructions.append(f".L{self.name}{self.current_block}H{self.height}INC:")
            self.parse_instruction(instr["inc"])
            self.instructions.append(f"jmp .L{self.name}{self.current_block}H{self.height}")
            self.instructions.append(f".L{self.name}{self.current_block+1}H{self.height}:")
            if self.height == 0:
                self.current_block += 2
            self.previous_loop_height.pop()
        elif instr["type"] == "while":
            self.previous_loop_height.append((self.height, "while"))
            self.instructions.append(f".L{self.name}{self.current_block}H{self.height}:")
            self.eval_expr(instr["cond"])
            self.instructions.append("\tpopq %rax")
            self.instructions.append("\tcmpq $0, %rax")
            self.instructions.append(f"je .L{self.name}{self.current_block+1}H{self.height}")
            self.parse_instruction(instr["body"])
            self.instructions.append(f"jmp .L{self.name}{self.current_block}H{self.height}")
            self.instructions.append(f".L{self.name}{self.current_block+1}H{self.height}:")
            if self.height == 0:
                self.current_block += 2
            self.previous_loop_height.pop()
        elif instr["type"] == "unop":
            self.eval_expr(instr)
            self.instructions.append("popq %rax")

        else:
            print(instr)
            raise Exception("Instruction not handled")
        # if instr["type"] == "call":
        #     self.instructions.append(x64_call(instr["name"], instr["args"]))
    def gen(self):
        for i in self.body:
            self.parse_instruction(i)
        return self.instructions
    