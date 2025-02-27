from error import *
class Types:
    def __init__(self, value=None):
        if value["type"] == "none":
            self.type = "null"
            self.value = None
            return
        self.type = value["type"]
        self.value = value["value"]
    
    def __str__(self):
        return f"{self.value}"
    def __repr__(self):
        return str(self)
    
    def list_compare(self, other, op):
        if (type(self.value) == list or type(self.value) == tuple) and (type(other.value) == list or type(other.value) == tuple) and type(self.value) == type(other.value):
            for i in range(min(len(self.value), len(other.value))):
                if self.value[i].type != other.value[i].type:
                    raise InvalidOperationException("Invalid comparison in list or tuple")
                if self.value[i].value > other.value[i].value:
                    if op == ">" or op == ">=":
                        return Types({"type": "bool", "value": True})
                    else:
                        return Types({"type": "bool", "value": False})
                if self.value[i].value < other.value[i].value:
                    if op == "<" or op == "<=":
                        return Types({"type": "bool", "value": True})
                    else:
                        return Types({"type": "bool", "value": False})
            if op == "<" or op == ">" or op == "!=":
                return Types({"type": "bool", "value": False})
            else:
                return Types({"type": "bool", "value": True})
        else:
            raise InvalidOperationException("Invalid comparison between (list or tuple) and non-(list or tuple)")
    def __eq__(self, other):
        if self.type == "list" or self.type == "tuple":
            return self.list_compare(other, "==")
        return Types({"type": "bool", "value": self.value == other.value})
    def __ne__(self, other):
        if self.type == "list" or self.type == "tuple":
            return self.list_compare(other, "!=")
        return Types({"type": "bool", "value": self.value != other.value})
    
    def __lt__(self, other):
        if self.type == "list" or self.type == "tuple":
            return self.list_compare(other, "<")
        return Types({"type": "bool", "value": self.value < other.value})
        
    def __le__(self, other):
        if self.type == "list" or self.type == "tuple":
            return self.list_compare(other, "<=")
        return Types({"type": "bool", "value": self.value <= other.value})
    
    def __gt__(self, other):
        if self.type == "list" or self.type == "tuple":
            return self.list_compare(other, ">")
        return Types({"type": "bool", "value": self.value > other.value})
    
    def __ge__(self, other):
        if self.type == "list" or self.type == "tuple":
            return self.list_compare(other, ">=")
        return Types({"type": "bool", "value": self.value >= other.value})
    
    def __and__(self, other):        
        return Types({"type": "bool", "value": self.value and other.value})
    
    def __or__(self, other):
        return Types({"type": "bool", "value": self.value or other.value})
    
    def __add__(self, other):
        if self.type != other.type and not ((self.type != "bool" and other.type != "int") or (self.type != "int" and other.type != "bool")):
            raise InvalidOperationException(f"Invalid operation '+' between {self.type} and {other.type}")
        return Types({"type": self.type, "value": self.value + other.value})
    
    def __sub__(self, other):
        if self.type != other.type and not ((self.type != "bool" and other.type != "int") or (self.type != "int" and other.type != "bool")):
            raise InvalidOperationException(f"Invalid operation '-' between {self.type} and {other.type}")
        return Types({"type": self.type, "value": self.value - other.value})
    
    def __mul__(self, other):
        if self.type != other.type and not ((self.type != "bool" and other.type != "int") or (self.type != "int" and other.type != "bool")) and ((self.type != "list" and other.type != "int") or (self.type != "int" and other.type != "list")):
            raise InvalidOperationException(f"Invalid operation '*' between {self.type} and {other.type}")
        return Types({"type": self.type, "value": self.value * other.value})
    
    def __truediv__(self, other):
        if other.value == 0:
            raise ZeroDivisionError("Division by zero")
        if self.type != other.type and not ((self.type != "bool" and other.type != "int") or (self.type != "int" and other.type != "bool")):
            raise InvalidOperationException(f"Invalid operation '/' between {self.type} and {other.type}")
        return Types({"type": self.type, "value": self.value // other.value})
    
    def __mod__(self, other):
        if self.type != other.type:
            raise Exception("Invalid operation")
        if self.type != "int":
            raise InvalidOperationException(f"Invalid operation '%' between {self.type} and {other.type}")
        return Types({"type": self.type, "value": self.value % other.value})
    
    def __getitem__(self, key):
        if self.type != "list" and self.type != "tuple":
            raise InvalidOperationException("accessing index of non-list or non-tuple")
        if key.type != "int":
            raise InvalidOperationException("accessing index with non-integer")
        return self.value[key.value]
    
    def __setitem__(self, key, value):
        if self.type != "list":
            raise InvalidOperationException("setting index of non-list")
        if key.type != "int":
            raise InvalidOperationException("setting index with non-integer")
        self.value[key.value] = value
    def __iter__(self):
        if self.type == "generator":
            return self.value["function"](self.value["args"])
        else:
            return iter(self.value)
    def __next__(self):
        if self.type == "generator":
            return next(iter(self))
        else:
            raise InvalidOperationException("next() on non-generator")
    
class PrintList:
    def __init__(self, value):
        self.value = value
    def print_list(self, value):
        string = "["
        for i in value:
            if i.type == "list":
                string += self.print_list(i.value) + ", "
            elif i.type == "string":
                #/!\ This is a hack to print the string with escaped characters
                string += str(bytes(i.value, "utf-8"))[1:] + ", "
            else:
                string += str(i) + ", "
        if len(string) > 1: #handle empty list
            string = string[:-2]
        string += "]"
        return string
    def __str__(self):
        string = ""
        for i in self.value:
            if i.type == "generator":
                string += "<generator object> "
            elif i.type == "list":
                string += self.print_list(i.value) + " "
            else:
                string += str(i) + " "
        return string[:-1]

class Function:
    def __init__(self, name, args, body, interpreter=None):
        self.name = name
        self.args = args
        self.local_vars = {}
        self.body = body
        self.interpreter = interpreter
        self.is_a_yield_function = self.find_yield(body)
    def find_yield(self, body):
        for stmt in body["body"]:
            if stmt["type"] == "while" or stmt["type"] == "for":
                if self.find_yield(stmt["body"]):
                    return True
            if stmt["type"] == "if" or stmt["type"] == "if_else":
                if self.find_yield(stmt["then"]):
                    return True
                if "else" in stmt:
                    if self.find_yield(stmt["else"]):
                        return True
            if stmt["type"] == "yield":
                return True
        else:
            return False
    
    def interpret_yield(self, body):
        for stmt in body["body"]:
            res_stmt = self.interpreter.interpret_statement(stmt, self, False, True)
            if res_stmt:
                for result in res_stmt:
                    yield result
        return Types({"type": "null", "value": None})
    
    def __call__(self, *args):
        if len(args) == 1 and type(args[0]) == list:
            args = args[0]
            if len(args) != len(self.args):
                raise Exception("Invalid number of arguments in function call")
            for i in range(len(args)):
                self.local_vars[self.args[i]] = args[i]
        if self.is_a_yield_function:
            return self.interpret_yield(self.body)
        else:
            for stmt in self.body["body"]:
                result = self.interpreter.interpret_statement(stmt, self)
                if result:
                    return result
            return Types({"type": "null", "value": None})
        
    def copy(self):
        new = Function(self.name, self.args, self.body, self.interpreter)
        new.local_vars = self.local_vars.copy()
        return new