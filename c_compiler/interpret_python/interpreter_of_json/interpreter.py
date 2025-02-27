from type import *
from error import *
        
class Interpreter:
    def print_out(self, *args):
        print(PrintList(*args))
        
    def type_out(self, *args):
        args = args[0]
        if len(args) == 1:
            return Types({"type": "string", "value": '<class \'' + args[0].type + '\'>'})
        else:
            raise CallException("Invalid number of arguments in function call")
    
    def str_out(self, *args):
        args = args[0]
        if len(args) == 1:
            return Types({"type": "string", "value": str(args[0].value)})
        else:
            raise CallException("Invalid number of arguments in function call")
        
    def len_out(self, *args):
        args = args[0]
        if len(args) == 1:
            return Types({"type": "int", "value": len(args[0].value)})
        else:
            raise CallException("Invalid number of arguments in function call")
    
    def range_gen(self, args):
        for i in range(*args):
            yield Types({"type": "int", "value": i})
    def range_out(self, *args):
        args = list(map(lambda x: x.value, args[0]))
        if len(args) > 3:
            raise CallException("Invalid number of arguments in function call")
        return Types({"type": "generator", "value": 
            {   
                "function": self.range_gen,
                "args": args
            }
        })
    
    def list_out(self, *args):
        args = args[0]
        if len(args) == 1 and args[0].type == "generator":
            return Types({"type": "list", "value": list(iter(args[0]))})
        else:
            return Types({"type": "list", "value": args})
        
    def reversed_out(self, *args):
        args = args[0]
        if len(args) == 1 and args[0].type == "list":
            return Types({"type": "generator", "value": 
                {
                    "function": reversed,
                    "args": args[0].value
                }
            })
        elif len(args) == 1 and args[0].type == "generator":
            return Types({"type": "generator", "value": 
                {
                    "function": reversed,
                    "args": list(iter(args[0]))
                }
            })
        else:
            raise CallException("Invalid number of arguments in function call")
    
    def iter_out(self, *args):
        args = args[0]
        if len(args) == 1:
            return iter(args[0])
        else:
            raise CallException("Invalid number of arguments in function call")

    def __init__(self):
        self.global_vars = {}
        self.basic_functions = {
            "print": self.print_out,
            "type": self.type_out,
            "len": self.len_out,
            "range": self.range_out,
            "list": self.list_out,
            "reversed": self.reversed_out,
            "iter": self.iter_out,
            "str": self.str_out
        }
        self.functions_table = {}
    
    def add_function(self, name, args, body, interpreter):
        self.functions_table[name] = Function(name, args, body, interpreter)
        
    def eval_binop(self, value, function):
        left = self.eval_expr(value["v1"], function)
        right = self.eval_expr(value["v2"], function)
        if type(left) == dict:
            left = Types(left)
        if type(right) == dict:
            right = Types(right)
        match value["binop"]:
            case "Add":
                return left + right
            case "Sub":
                return left - right
            case "Mul":
                return left * right
            case "Div":
                return left / right
            case "Mod":
                return left % right
            case "<":
                return left < right
            case "<=":
                return left <= right
            case ">":
                return left > right
            case ">=":
                return left >= right
            case "==":
                return left == right
            case "!=":
                return left != right
            case "&&":
                return left & right
            case "||":
                return left | right
            case _:
                raise InvalidOperationException("Invalid binary operation")
            
    def eval_list(self, value, function):
        return Types({"type": "list", "value": list(map(lambda x: self.eval_expr(x, function), value["content"]))})
    def eval_tuple(self, value, function):
        return Types({"type": "tuple", "value": tuple(map(lambda x: self.eval_expr(x, function), value["content"]))})
    
    def eval_list_for(self, value, function):
        content = []
        varname = value["varname"]
        in_set = self.eval_expr(value["in_set"], function)
        for i in in_set:
            if function:
                function.local_vars[varname] = i
            else:
                self.global_vars[varname] = i
            content.append(self.eval_expr(value["content"], function))
        if function:
            function.local_vars.pop(varname, None)
        else:
            self.global_vars.pop(varname, None)
        return Types({"type": "list", "value": content})
            
        
        
    
    def array_access(self, value, function):
        if value["array"]["type"] == "var":
            array = self.variable_access(value["array"], function)
        if value["array"]["type"] == "array access":
            array = self.array_access(value["array"], function)
        index = self.eval_expr(value["index"], function)
        return array[index]
    
    def variable_access(self, value, function):
        name = value["name"]
        if function is not None:
            if name in function.local_vars:
                return function.local_vars[name]
        if name in self.global_vars:
            return self.global_vars[name]
        else:
            raise NotFoundException("Variable not found")
        
    def eval_expr(self, value, function=None):
        if value["type"] == "const":
            return Types(value["value"])
        if value["type"] == "call":
            if value["funname"] in self.basic_functions:
                return self.basic_functions[value["funname"]]((list(map(lambda x: self.eval_expr(x, function), value["args"]))))
            elif value["funname"] in self.functions_table:
                if self.functions_table[value["funname"]].is_a_yield_function:
                    return Types({"type": "generator", "value": 
                        {
                            "function": self.functions_table[value["funname"]].copy(),
                            "args": list(map(lambda x: self.eval_expr(x, function), value["args"]))
                        }
                    })
                else:
                    return self.functions_table[value["funname"]].copy()((list(map(lambda x: self.eval_expr(x, function), value["args"]))))
            else:
                raise NotFoundException("Function not found")
        if value["type"] == "left_value":
            if value["value"]["type"] == "var":
                return self.variable_access(value["value"], function)
            if value["value"]["type"] == "array access":
                return self.array_access(value["value"], function)
        if value["type"] == "binop":
            return self.eval_binop(value, function)
        if value["type"] == "moins":
            return Types({"type": "int", "value": -self.eval_expr(value["value"], function).value})
        if value["type"] == "not":
            return Types({"type": "bool", "value": not self.eval_expr(value["value"], function).value})
        if value["type"] == "list":
            return self.eval_list(value, function)
        if value["type"] == "tuple":
            return self.eval_tuple(value, function)
        if value["type"] == "list for":
            return self.eval_list_for(value, function)
    def variable_setter(self, stmt, function):
        name = stmt["left_value"]["name"]
        new_var = self.eval_expr(stmt['value'], function)
        if stmt['left_value']['type'] == "var":
            if function:
                function.local_vars[name] = new_var
            else:
                self.global_vars[name] = new_var
        else:
            raise InvalidTypeException("Invalid variable type")
    
    def array_setter(self, stmt, function):
        array = stmt["left_value"]["array"]
        index = self.eval_expr(stmt["left_value"]["index"], function)
        new_var = self.eval_expr(stmt["value"], function)
        if array["type"] == "var":
            array = self.variable_access(array, function)
        elif array["type"] == "array access":
            array = self.array_access(array, function)
        array[index] = new_var
        
    def for_loop_return(self, stmt, function, in_set, varname, body):
        breakFlag = False
        continueFlag = False
        for i in in_set:
            if function:
                function.local_vars[varname] = i
            else:
                self.global_vars[varname] = i
            for stmt in body["body"]:
                result = self.interpret_statement(stmt, function, True)
                if result:
                    if type(result) == Types:
                        return result
                    elif result == "break":
                        breakFlag = True
                        break
                    elif result == "continue":
                        continueFlag = True
                        break
            if breakFlag:
                breakFlag = False
                break
            if continueFlag:
                continueFlag = False
                continue
    
    def for_loop_yield(self, stmt, function, in_set, varname, body):
        breakFlag = False
        continueFlag = False
        for i in in_set:
            if function:
                function.local_vars[varname] = i
            else:
                self.global_vars[varname] = i
            for stmt in body["body"]:
                result = self.interpret_statement(stmt, function, True)
                if result:
                    if type(result) == Types:
                        yield result
                    elif result == "break":
                        breakFlag = True
                        break
                    elif result == "continue":
                        continueFlag = True
                        break
            if breakFlag:
                breakFlag = False
                break
            if continueFlag:
                continueFlag = False
                continue
            
    def for_loop(self, stmt, function,in_yield):
        varname = stmt["varname"]
        in_set = self.eval_expr(stmt["in_set"], function)
        body = stmt["body"]
        if in_set.type == "string":
            in_set = Types({"type": "list", "value": list(map(lambda x: Types({"type": "string", "value": x}), in_set.value))})
        if in_yield:
            return self.for_loop_yield(stmt, function, in_set, varname, body)
        else:
            return self.for_loop_return(stmt, function, in_set, varname, body)
        
    
    def while_loop_return(self, stmt, function):
        breakFlag = False
        continueFlag = False
        while self.eval_expr(stmt["cond"], function).value:
            for stmtbody in stmt["body"]["body"]:
                result = self.interpret_statement(stmtbody, function, True)
                if result:
                    if type(result) == Types:
                        return result
                    elif result == "break":
                        breakFlag = True
                        break
                    elif result == "continue":
                        continueFlag = True
                        break
            if breakFlag:
                breakFlag = False
                break
            if continueFlag:
                continueFlag = False
                continue
    def while_loop_yield(self, stmt, function):
        breakFlag = False
        continueFlag = False
        while self.eval_expr(stmt["cond"], function).value:
            for stmtbody in stmt["body"]["body"]:
                result = self.interpret_statement(stmtbody, function, True)
                if result:
                    if type(result) == Types:
                        yield result
                    elif result == "break":
                        breakFlag = True
                        break
                    elif result == "continue":
                        continueFlag = True
                        break
            if breakFlag:
                breakFlag = False
                break
            if continueFlag:
                continueFlag = False
                continue
            
    def yield_return(self, stmt, function):
        yield self.eval_expr(stmt["value"], function)
    def interpret_statement(self, stmt, function=None, in_loop=False, in_yield=False):
        if stmt["type"] == "return":
            return self.eval_expr(stmt["value"], function)
        if stmt["type"] == "yield":
            if in_yield:
                return self.yield_return(stmt, function)
            else:
                return self.eval_expr(stmt["value"], function)
        if (stmt["type"] == "break" or stmt["type"] == "continue"):
            if not in_loop:
                raise SyntaxException("Syntax error")
            else:
                return stmt["type"]
        if stmt["type"] == "for":
            return self.for_loop(stmt, function, in_yield)
        if stmt["type"] == "if_else":
            for stmtin in stmt["then" if self.eval_expr(stmt["cond"], function).value else "else"]["body"]:
                result = self.interpret_statement(stmtin, function, in_loop, in_yield)
                if result:
                    return result
        if stmt["type"] == "if":
            if self.eval_expr(stmt["cond"], function).value:
                for stmtin in stmt["then"]["body"]:
                    result = self.interpret_statement(stmtin, function, in_loop, in_yield)
                    if result:
                        return result
        if stmt["type"] == "while":
            if in_yield:
                return self.while_loop_yield(stmt, function)
            else:
                return self.while_loop_return(stmt, function)
        if stmt["type"] == "varset":
            if stmt["left_value"]["type"] == "var":
                self.variable_setter(stmt, function)
            if stmt["left_value"]["type"] == "array access":
                self.array_setter(stmt, function)
        if stmt["type"] == "expr":
            self.eval_expr(stmt["value"], function)
            
    def interpret(self, data):
        for line in data:
            if line["type"] == "fundef":
                self.add_function(line["name"], line["args"], line["body"], self)
            if line["type"] == "stmt":
                self.interpret_statement(line["stmt"])