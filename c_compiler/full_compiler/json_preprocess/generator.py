from utils import *

class Generator:
    def __init__(self):
        self.rodata_section = []
        self.data_section = []
        self.function_section = []
        self.program = []
        self.ast = []
        self.labels = []
        self.global_vars = {}
        self.current_label = 0
    
    def gen_ast(self):
        for i in self.data:
            self.gen_node(i)
        self.ast.insert(0, {"type": "function_section", "data": self.function_section})
        self.ast.insert(0, {"type": "rodata_section", "data": self.rodata_section})
        self.ast.insert(0, {"type": "data_section", "data": self.data_section})
        self.ast.append({"type": "text", "data": self.program})

    def transform_args(self, args):
        new_args = {}
        stack_index = 8
        for i in args:
            var_type = i["type"]
            if "type" in var_type and var_type["type"] == "pointer":
                if "len" in var_type['of']:
                    var_type['first_len'] = var_type['of']['len']
            new_args[i["name"]] = ({"type": "var", "name": i["name"], "var_type": var_type, "stack_index" : stack_index})
            stack_index += stack_size_of(i["type"])
        return new_args
    
    def varget_context(self, name, func):
        if func != None and name in func["local_vars"]:
            return func["local_vars"][name]
        elif func != None and name in func["args"]:
            return func["args"][name]
        elif name in self.global_vars:
            return self.global_vars[name]
        else:
            raise Exception(f"Variable {name} not found")
        return self.transform_expr(expr, func)
    
    def linearize_deref(self, expr, func, deref=0):
        return self.transform_expr(expr, func, deref+1)
    def transform_expr(self, expr, func, deref=0):
        if expr["type"] == "sizeof":
            if expr['value'] == "int":
                return {"type": "const", "value": {"type": "int", "value": 8}}
            elif expr['value'] == "char":
                return {"type": "const", "value": {"type": "int", "value": 1}}
            elif "type" in expr['value']:
                if expr['value']['type'] == "pointer":
                    return {"type": "const", "value": {"type": "int", "value": 8}}
                elif expr['value']['type'] == "array":
                    return {"type": "const", "value": {"type": "int", "value": stack_size_of(expr['value']['of'])*expr['value']['len']}}
                else:
                    return {"type": "sizeof", "value": self.transform_expr(expr['value'], func)}
            else:
                return {"type": "sizeof", "value": self.transform_expr(expr['value'], func)}
                
        if expr["type"] == "const":
            if expr["value"]["type"] == "int":
                return {"type": "const", "value": {"type": "int", "value": int(expr["value"]["value"])}}
            elif expr["value"]["type"] == "string":
                list_map = list(map(lambda x: x["value"], self.rodata_section))
                if expr["value"]["value"] not in list_map:
                    self.rodata_section.append({"type": "string", "value": expr["value"]["value"]})
                    return {"type": "rodata", "at": (len(self.rodata_section) - 1), "len" : len(expr["value"]["value"])}
                else:
                    return {"type": "rodata", "at": list_map.index(expr["value"]["value"]), "len" : len(expr["value"]["value"])}
            elif expr["value"]["type"] == "char":
                return {"type": "const", "value": {"type": "char", "value": ord(expr["value"]["value"])}}
            else:
                return {"type": "const", "value": expr["value"]}
            
        elif expr["type"] == "binop":
            if expr["lhs"]["type"] != "const":
                expr["lhs"] = self.transform_expr(expr["lhs"], func, deref)
            if expr["rhs"]["type"] != "const":
                expr["rhs"] = self.transform_expr(expr["rhs"], func, deref)
            if expr["lhs"]["type"] == "const" and expr["rhs"]["type"] == "const":
                lhs = expr["lhs"]["value"]
                rhs = expr["rhs"]["value"]
                if lhs["type"] == "int" and rhs["type"] == "int":
                    match expr["op"]:
                        case "+":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) + int(rhs["value"]))}}
                        case "-":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) - int(rhs["value"]))}}
                        case "*":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) * int(rhs["value"]))}}
                        case "/":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) / int(rhs["value"]))}}
                        case "%":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) % int(rhs["value"]))}}
                        case "==":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) == int(rhs["value"]))}}
                        case "!=":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) != int(rhs["value"]))}}
                        case "<":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) < int(rhs["value"]))}}
                        case ">":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) > int(rhs["value"]))}}
                        case "<=":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) <= int(rhs["value"]))}}
                        case ">=":
                            return {"type": "const", "value": {"type": "int", "value": int(int(lhs["value"]) >= int(rhs["value"]))}}
            if expr["lhs"]["type"] == "varget":
                expr["lhs"] = self.varget_context(expr["lhs"]["name"], func)
            if expr["rhs"]["type"] == "varget":
                expr["rhs"] = self.varget_context(expr["rhs"]["name"], func)
            return expr
        elif expr["type"] == "array_get":
            if deref == 1:
                var = self.varget_context(expr["name"], func)
                if "first_len" in var:
                    return {"type": "binop", "lhs": self.varget_context(expr["name"], func), "rhs": {"type": "binop", "lhs": self.transform_expr(expr["index"], func), "rhs": var["first_len"], "op": "*"}, "op": "+"}
            if expr["name"] in self.global_vars:
                return {"type": "array_get", "name": expr["name"], "index": self.transform_expr(expr["index"], func)}
            else:
                return {"type": "array_get", "name": expr["name"], "index": self.transform_expr(expr["index"], func), "stack_index": self.varget_context(expr["name"], func)["stack_index"]}
        elif expr["type"] == "array_get_generic":
            return {"type": "array_get_generic", "name": expr["where"]["name"], "where": self.transform_expr(expr["where"], func), "index": self.transform_expr(expr["index"], func)}
        elif expr["type"] == "unop":
            if expr["op"] == "&":
                if expr["expr"]["type"] == "unop" and expr["expr"]["op"] == "*":
                    return self.transform_expr(expr["expr"]["expr"], func)
            elif expr["op"] == "*":
                if expr["expr"]["type"] == "unop" and expr["expr"]["op"] == "&":
                    return self.transform_expr(expr["expr"]["expr"], func)
                else:
                    if deref == 1: # linearize 2d array access initialize in the stack or in global var to a 1d array access
                        #copy is used to avoid changing the original expr if it don't catch the condition
                        expr_at_linearized = self.linearize_deref(expr["expr"].copy(), func, deref)
                        if expr_at_linearized["type"] == "global_var" or expr_at_linearized["type"] == "var":
                            return expr_at_linearized
                        elif expr_at_linearized["type"] == "binop" and (expr_at_linearized["lhs"]["type"] == "global_var" or expr_at_linearized["rhs"]["type"] == "global_var" or expr_at_linearized["lhs"]["type"] == "var" or expr_at_linearized["rhs"]["type"] == "var"):
                            if expr_at_linearized["lhs"]["type"] == "global_var" or expr_at_linearized["lhs"]["type"] == "var":
                                if "first_len" in expr_at_linearized["lhs"]:
                                    return {"type": "binop", "lhs": expr_at_linearized["lhs"], "rhs": 
                                            {"type": "binop", "lhs": expr_at_linearized["rhs"], "rhs": expr_at_linearized["lhs"]["first_len"], "op": "*"}, "op": expr_at_linearized["op"]}
                                elif "first_len" in expr_at_linearized["lhs"]["var_type"]:
                                    return {"type": "binop", "lhs": expr_at_linearized["lhs"], "rhs":
                                            {"type": "binop", "lhs": expr_at_linearized["rhs"], "rhs": {"type": "const", "value": {"type": "int", "value": expr_at_linearized["lhs"]["var_type"]["first_len"]}}, "op": "*"}, "op": expr_at_linearized["op"]}
                            elif expr_at_linearized["rhs"]["type"] == "global_var" or expr_at_linearized["rhs"]["type"] == "var":
                                if "first_len" in expr_at_linearized["rhs"]:
                                    return {"type": "binop", "lhs": expr_at_linearized["rhs"], "rhs": 
                                            {"type": "binop", "lhs": expr_at_linearized["lhs"], "rhs": expr_at_linearized["rhs"]["first_len"], "op": "*"}, "op": expr_at_linearized["op"]}
                                elif "first_len" in expr_at_linearized["rhs"]["var_type"]:
                                    return {"type": "binop", "lhs": expr_at_linearized["rhs"], "rhs":
                                            {"type": "binop", "lhs": expr_at_linearized["lhs"], "rhs": {"type": "const", "value": {"type": "int", "value": expr_at_linearized["rhs"]["var_type"]["first_len"]}}, "op": "*"}, "op": expr_at_linearized["op"]}
                    return {"type": "unop", "op": expr["op"], "expr": self.linearize_deref(expr["expr"], func, deref)}
            return {"type": "unop", "op": expr["op"], "expr": self.transform_expr(expr["expr"], func)}
        elif expr["type"] == "var":
            if func is not None:
                if expr["name"] in func["local_vars"]:
                    return {"type": "var", "var_type": expr["var_type"], "name": expr["name"], "stack_index": func["local_vars"][expr["name"]]["stack_index"]}
                else:
                    func["local_vars"][expr["name"]] = {"type": "local_var", "name": expr["name"], "var_type": expr["var_type"], "stack_index": func["stack_size"]}
                    func["stack_size"] += stack_size_of(expr["var_type"])
                    return {"type": "var", "var_type": expr["var_type"], "name": expr["name"], "stack_index": func["stack_size"] - stack_size_of(expr["var_type"])}
            else:
                if expr["name"] not in self.global_vars:
                    self.data_section.append({"type": expr["var_type"], "var_type": expr["var_type"], "name": expr["name"]})
                    self.global_vars[expr["name"]] = {"type": "global_var", "name": expr["name"], "var_type": expr["var_type"]}
            return {"type": "var", "var_type": expr["var_type"], "name": expr["name"]}
        elif expr["type"] == "varset":
            if func is not None:
                # if expr["name"] in func["local_vars"]:
                #     print(func["local_vars"])
                #     raise Exception("Variable already defined") Need to handle height level variable shadowing, for now it is allowed
                func["local_vars"][expr["name"]] = {"type": "local_var", "name": expr["name"], "var_type": expr["var_type"], "stack_index": func["stack_size"]}
                func["stack_size"] += stack_size_of(expr["var_type"])
                return {"type": "varset", "var_type": expr["var_type"], "name": expr["name"], "value": self.transform_expr(expr["value"], func), "stack_index": func["local_vars"][expr["name"]]["stack_index"]}
            else:
                if expr["name"] in self.global_vars:
                    list_map = list(map(lambda x: x["name"], self.data_section))
                    get_index = list_map.index(expr["name"])
                    if "value" in self.data_section[get_index]:
                        raise Exception("Variable already defined")
                    self.data_section[get_index]["value"] = self.transform_expr(expr["value"], func)
                else:
                    
                    self.data_section.append({"type": expr["var_type"], "name": expr["name"], "value": self.transform_expr(expr["value"], func)})
                    self.global_vars[expr["name"]] = {"type": "global_var", "name": expr["name"], "var_type": expr["var_type"]}
                if expr["value"]["type"] == "const" and expr["value"]["value"]["type"] == "string":
                    if expr["var_type"] == {"type": "pointer", "of": "char"}:
                        if expr["value"]["value"]["value"] not in self.rodata_section:
                            self.rodata_section.append({"type": "string", "value": expr["value"]["value"]["value"]})
                            return {"type": "varset", "var_type": expr["var_type"], "name": expr["name"], "value": {"type": "rodata", "at": (len(self.rodata_section) - 1)}}

                        else:
                            return {"type": "varset", "var_type": expr["var_type"], "name": expr["name"], "value": {"type": "rodata", "at": self.rodata_section.index(expr["value"]["value"]["value"])}}
                    elif expr["var_type"] == "char":
                        return {"type": "varset", "var_type": expr["var_type"], "name": expr["name"], "value": {"type": "char", "value": ord(expr["value"]["value"]["value"])}}
                else:
                    return {"type": "varset", "var_type": expr["var_type"], "name": expr["name"], "value": self.transform_expr(expr["value"], func)}
                
                
        elif expr["type"] == "varget":
            return self.varget_context(expr["name"], func)
        elif expr["type"] == "unop":
            return {"type": "unop", "op": expr["op"], "expr": self.transform_expr(expr["expr"], func)}
        elif expr["type"] == "array":
            evaluated_expr = {"type": "array", "name": expr["name"], "var_type": {"type": "array", "of" : expr["array_type"]}, "value": {"type": "array", "len": self.transform_expr(expr["len"], func), "Values" : list(map(lambda x: self.transform_expr(x, func), expr["values"]))}}
            if func is None:
                self.data_section.append(evaluated_expr)
                self.global_vars[expr["name"]] = {"type": "global_var", "name": expr["name"], "var_type": {"type": "array", "len": self.transform_expr(expr["len"], func), "of": expr["array_type"]}}
                return evaluated_expr
            else:
                try:
                    len_of_array = self.transform_expr(expr["len"], func)["value"]["value"]
                except:
                    raise Exception("Array length must be a constant")
                func["stack_size"] += stack_size_of(expr["array_type"])*len_of_array
                func["local_vars"][expr["name"]] = {"type": "local_var", "name": expr["name"], "var_type": {"type": "array", "len": self.transform_expr(expr["len"], func), "of": expr["array_type"]}, "stack_index": func["stack_size"] - 8}

                evaluated_expr.update({"stack_index": func["stack_size"] - 8})
                return evaluated_expr
        elif expr["type"] == "2d_array":
            evaluated_expr = {"type": "array",
                               "name": expr["name"],
                                 "var_type": {"type": "array", "of" : {"type": "pointer", "of" : expr["array_type"]}, "first_len": self.transform_expr(expr["len"], func)},
                                   "value": {"type": "array", "len": self.transform_expr({"type": "binop", "lhs": expr["len"], "rhs": expr["len2"], "op": "*"}, func),
                                              "Values" : list(map(lambda x: list(map(lambda y: self.transform_expr(y, func), x)), expr["values"]))}}
            if func is None:
                self.data_section.append(evaluated_expr)
                self.global_vars[expr["name"]] = {"type": "global_var",
                                                  "first_len": self.transform_expr(expr["len"], func),
                                                  "name": expr["name"], "var_type": {"type": "array", "len": self.transform_expr({"type": "binop", "lhs": expr["len"], "rhs": expr["len2"], "op": "*"}, func), "of": {"type": "pointer", "of" : expr["array_type"]}}}
                return evaluated_expr
            else:
                try:
                    len_of_array = self.transform_expr({"type": "binop", "lhs": expr["len"], "rhs": expr["len2"], "op": "*"}, func)["value"]["value"]
                except:
                    raise Exception("Array length must be a constant")
                func["stack_size"] += stack_size_of({"type": "pointer", "of" : expr["array_type"]})*len_of_array
                func["local_vars"][expr["name"]] = {"type": "local_var", "name": expr["name"], "first_len": self.transform_expr(expr["len"], func), "var_type": {"type": "array", "len": self.transform_expr({"type": "binop", "lhs": expr["len"], "rhs": expr["len2"], "op": "*"}, func), "of": {"type": "pointer", "of" : expr["array_type"]}}, "stack_index": func["stack_size"] - 8}

                evaluated_expr.update({"stack_index": func["stack_size"] - 8})
                return evaluated_expr
        elif expr["type"] == "array_set_generic":
            return {"type": "array_set_generic", "where": self.transform_expr(expr["where"], func), "index": self.transform_expr(expr["index"], func), "value": self.transform_expr(expr["value"], func)}
        elif expr["type"] == "array_set":
            return {"type": "array_set", "name": expr["name"], "index": self.transform_expr(expr["index"], func), "value": self.transform_expr(expr["value"], func)}
        elif expr["type"] == "call":
            if expr["name"] == "print_int":
                expr["args"] = [{"type":"const","value":{"type":"string","value":"%d\n"}}] + expr["args"]
                expr["name"] = "printf"
            if expr["name"] == "print_string":
                expr["args"] = [{"type":"const","value":{"type":"string","value":"%s\n"}}] + expr["args"]
                expr["name"] = "printf"

            return {"type": "call", "name": expr["name"], "args": list(map(lambda x: self.transform_expr(x, func), expr["args"]))}
        else:
            print(expr)
            raise Exception("Invalid expression")
        return expr
        

    
    def transform_node(self, node, func=None):
        if "type" not in node:
            raise Exception("Type not found in node")
        if node["type"] == "return":
            if "value" in node:
                evaluated_node = {"type": "return", "value": self.transform_expr(node["value"], func)}
        elif node["type"] == "expr_stmt":
            evaluated_node = self.transform_expr(node["expr"], func)
            if (evaluated_node["type"] == "varset" or evaluated_node["type"] == "var" or evaluated_node["type"] == "array") and func is None:
                evaluated_node =  None
        elif node["type"] == "assign":
            return {"type": "assign", "name": node["name"], "value": self.transform_expr(node["value"], func)}
        elif node["type"] == "assign_deref":
            return {"type": "assign_deref", "where": self.linearize_deref(node["where"], func), "value": self.transform_expr(node["value"], func)}
        elif node["type"] == "if_else":
            try:
                (node["then"]["body"], node["else"]["body"])
            except:
                raise Exception("Body not found (else if not supported)")
            evaluated_node = {"type": "if_else", "cond": self.transform_expr(node["cond"], func), 
                              "then": {"type": "block", "body": self.transform_body(node["then"]['body'], func)},
                                "else": {"type": "block", "body": self.transform_body(node["else"]['body'], func)}}
            if evaluated_node["cond"]["type"] == "const" and evaluated_node["cond"]["value"]["type"] == "int":
                if evaluated_node["cond"]["value"]["value"] == 0:
                    evaluated_node = evaluated_node["else"]
                else:
                    evaluated_node = evaluated_node["then"]
        elif node["type"] == "if":
            evaluated_node = {"type": "if", "cond": self.transform_expr(node["cond"], func), 
                              "then": {"type": "block", "body": self.transform_body(node["then"]['body'], func)}}
            if evaluated_node["cond"]["type"] == "const" and evaluated_node["cond"]["value"]["type"] == "int":
                if evaluated_node["cond"]["value"]["value"] == 0:
                    evaluated_node = None
                else:
                    evaluated_node = evaluated_node["then"]
        elif node["type"] == "do_while" or node["type"] == "while":
            evaluated_node = {"type": "while", "cond": self.transform_expr(node["cond"], func), 
                              "body": {"type": "block", "body": self.transform_body(node["body"]['body'], func)}}
        elif node["type"] == "for":
            evaluated_node = {"type": "for", "init": self.transform_node(node["init"], func), "cond": self.transform_expr(node["cond"], func), "inc": self.transform_node(node["inc"], func),
                              "body": {"type": "block", "body": self.transform_body(node["body"]['body'], func)}}
        elif node["type"] == "block":
            evaluated_node = {"type": "block", "body": self.transform_body(node["body"], func)}
        elif node["type"] == "break":
            evaluated_node = {"type": "break"}
        elif node["type"] == "continue":
            evaluated_node = {"type": "continue"}
        else:
            print(node)
        return evaluated_node

    def transform_body(self, body, func):
        new_body = []
        for i in body:
            new_body.append(self.transform_node(i, func))
        return new_body

    def gen_node(self, node):
        evaluated_node = None
        if "type" not in node:
            raise Exception("Type not found in node")
        if node["type"] == "function":
            self.function_section.append({"type": "function", "name": node["name"], "return_type": node["return_type"]})
            new_func = ({"type": "function", "name": node["name"], "args": self.transform_args(node["params"]), "local_vars": {}})
            if new_func["args"] == {}:
                new_func["stack_size"] = 8
            else:
                new_func["stack_size"] = 8 + max(new_func["args"].values(), key=lambda x: x["stack_index"])["stack_index"]
            new_body = self.transform_body(node["body"], new_func)
            new_func["body"] = new_body
            evaluated_node = new_func
        if node["type"] == "stmt":
            evaluated_node = self.transform_node(node['stmt'])
        if evaluated_node is not None:    
            self.program.append(evaluated_node)
    def gen(self, data):
        self.data = data
        self.ast = []
        self.bytecode = []
        self.labels = []
        self.current_label = 0
        self.gen_ast()
        return self.ast