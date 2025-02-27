from x64 import *
from function import Function
from optimizer import Optimizer
class Compiler:
    def __init__(self):
        self.instructions = []
        self.global_funct = []
        self.current_function = None
        self.data = []
        self.rodata = []
        self.globalvar = {}
        self.declared_functions = {} # for function calls
    def end(self):
        final = []
        final.append(".text")
        final += self.data
        final += self.rodata
        final.append(".text")
        final += self.global_funct
        final += self.instructions
        final.append(".section .note.GNU-stack,\"\",@progbits")
        final.append("")
        # Optimizing with 6 passes
        optimize = Optimizer(6, final)
        optimize.optimize()
        final = optimize.new_instructions
        return final

    def evaluate_expr_data(self, expr, type, var_type=None):
        if expr["type"] == "const":
            if expr["value"]["type"] == "int" or expr["value"]["type"] == "char":
                return expr["value"]["value"]
        if expr["type"] == "rodata":
            return ".LC" + str(expr["at"])
        if expr["type"] == "unop":
            if expr["op"] == "-":
                return -self.evaluate_expr_data(expr["expr"], type)
            elif expr["op"] == "&":
                return self.evaluate_expr_data(expr["expr"], type)
        if expr["type"] == "global_var":
            return expr["name"]
        if expr["type"] == "array":
            return {"type": "array", "var_type" : var_type, "values": [self.evaluate_expr_data(i, var_type["of"]) for i in expr["Values"]], "len": self.evaluate_expr_data(expr["len"], "int")}
    
    def gen_data(self, node):
        self.data.append(".data")
        for i in node["data"]:
            if "value" not in i:
                if "var_type" in i:
                    self.globalvar[i["name"]] = ({"type": i["type"], "var_type": i["var_type"], "name": i["name"], "value": 0})
                    self.data.append(data_add(i["name"], i["type"], 0))
                else:
                    self.globalvar[i["name"]] = ({"type": i["type"], "name": i["name"], "value": 0})
                    self.data.append(data_add(i["name"], i["type"], 0))
            else:
                if "var_type" in i:
                    self.globalvar[i["name"]] = ({"type": i["type"], "var_type": i["var_type"], "name": i["name"], "value": self.evaluate_expr_data(i["value"], i["type"], i["var_type"])})
                    self.data.append(data_add(i["name"], i["type"], self.evaluate_expr_data(i["value"], i["type"], i["var_type"])))
                else:
                    self.globalvar[i["name"]] = ({"type": i["type"], "name": i["name"], "value": self.evaluate_expr_data(i["value"], i["type"])})
                    self.data.append(data_add(i["name"], i["type"], self.evaluate_expr_data(i["value"], i["type"])))
    
    def gen_rodata(self, node):
        idx = 0
        for i in node["data"]:
            self.rodata.append(data_add('.LC' + str(idx), i["type"], '"'+str(bytes(i["value"], "utf-8"))[2:-1]+'"' ))
            idx += 1
    def gen_function(self, node):
        for i in node["data"]:
            self.declared_functions[i["name"]] = i["return_type"]
            self.global_funct.append(f".globl {i['name']}")

    def parse_instruction(self, instr):
        if instr["type"] == "function":
            self.instructions.append(f"{instr['name']}:")
            self.current_function = instr["name"]
            self.instructions.append("\tpushq %rbp")
            self.instructions.append("\tmovq %rsp, %rbp")
            self.instructions.append(f"\tsubq ${instr['stack_size']}, %rsp")
            for i in range(len(instr["args"])):
                if i < 6:
                    self.instructions.append(f"\tmovq %{call_convention[i]}, -{8*(i+1)}(%rbp)")
                else:
                    self.instructions.append(f"\tmovq {8*(i-4)}(%rbp), %rax")
                    self.instructions.append(f"\tmovq %rax, -{8*(i+1)}(%rbp)")
            new_func = Function.create(instr["name"], instr["body"], instr["args"], instr["local_vars"], self.globalvar, self.declared_functions)
            try:
                self.instructions += list(map(lambda x: ("\t" + x), new_func.gen()))
            except Exception as e:
                raise Exception(f"Error in function {instr['name']}: {e}")
            if self.instructions[-1] != "ret":
                #handle no return functions
                self.instructions.append(f"\tleave")
                self.instructions.append(f"\tret")


    def gen_text(self, data):
        for i in data:
            self.parse_instruction(i)
    
    def gen_node(self, node):
        if node["type"] == "rodata_section":
            self.gen_rodata(node)
        elif node["type"] == "data_section":
            self.gen_data(node)
        elif node["type"] == "function_section":
            self.gen_function(node)
        elif node["type"] == "text":
            self.gen_text(node["data"])
        else:
            return
    

    def gen_instructions(self, ast_to_parse):
        for i in ast_to_parse:
            self.gen_node(i)
    def gen(self, data):
        self.gen_instructions(data)
        return self.end()