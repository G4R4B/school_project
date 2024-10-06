"""
Author: Paul Vie
Reviewer: Yanis Lacenne
"""

import random
from circuits import create_min_n, NodeType


class VirtualMachineError(Exception):
    pass


class StackError(Exception):
    pass


class VirtualMachine:

    class Instruction:
        def __init__(self, name, f, args=[]):
            self.name = name
            self.f = f
            self.args = args

        def __call__(self, push):
            if push and (self.name == "pop" or self.name == "pop_quad"):
                raise StackError("Cannot pop own stack")

            self.args = list(self.args)
            for i in range(len(self.args)):
                if isinstance(self.args[i], VirtualMachine.Instruction):
                    self.args[i] = self.args[i](push)
            if len(self.args) == 0:
                return self.f()
            elif len(self.args) == 1:
                return self.f(self.args[0])
            elif len(self.args) == 2:
                return self.f(self.args[0], self.args[1])
            elif len(self.args) == 3:
                return self.f(self.args[0], self.args[1], self.args[2])
            elif len(self.args) == 4:
                return self.f(self.args[0], self.args[1], self.args[2], self.args[3])
            else:
                raise VirtualMachineError("Too many arguments")

    class InstructionCreator:
        def __init__(self, name, f):
            self.name = name
            self.f = f

        def __call__(self, *args):
            return VirtualMachine.Instruction(self.name, self.f, args)

    class Stack:
        def __init__(self):
            self.stack = []
            self.stack_state = False

        def push(self, value):
            if self.stack_state:
                raise StackError("Stack is full")
            self.stack.append(value)
            self.stack_state = True

        def pop(self):
            if not self.stack_state:
                raise StackError("Stack is empty")
            self.stack_state = False
            return self.stack.pop()

    class Program:
        def __init__(self):
            self.program = []

        def add(self, instruction):
            self.program.append(instruction)

        def run(self):
            push = False
            while len(self.program) > 0:
                instruction = self.program[0]
                if instruction.name == "push" or instruction.name == "push_quad":
                    push = True
                instruction(push)
                self.program = self.program[1:]

        class Variable:
            def __init__(self, index):
                self.value = None
                self.index = index

            def set_value(self, value):
                self.value = value

            def get_value(self):
                return self.value

            def get_index(self):  # for debugging
                return self.index

        def localVariable(self, num_nodes, name):
            if name == "Alice":
                self.xA = [self.Variable(i) for i in range(num_nodes + 4)]
                return self.xA
            elif name == "Bob":
                self.xB = [self.Variable(i) for i in range(num_nodes + 2)]
                return self.xB

    def __init__(self):
        self.instructions = {}
        self.stack = VirtualMachine.Stack()
        self.programAlice = VirtualMachine.Program()
        self.programBob = VirtualMachine.Program()
        self.local_variable_alice = None
        self.local_variable_bob = None

    def rnd(self):
        return random.randint(0, 1)

    def xor(self, x, y):
        return x.get_value() ^ y.get_value()

    def and_gate(self, x, y):
        return x.get_value() * y.get_value()

    def not_gate(self, x):
        return 1 - x.get_value()

    def push(self, x):
        self.stack.push(x.get_value())

    def pop(self):
        return self.stack.pop()

    def push_quad(self, x1, x2, x3, x4):
        self.stack.push(
            (x1.get_value(), x2.get_value(), x3.get_value(), x4.get_value())
        )

    def pop_quad(self, y1, y2):
        x1, x2, x3, x4 = self.stack.pop()
        return (
            y1.get_value() * x2
            ^ (1 - y1.get_value()) * x1
            ^ y2.get_value() * x4
            ^ (1 - y2.get_value()) * x3
        )

    def assign(self, x, e):
        if isinstance(e, VirtualMachine.Instruction):
            raise VirtualMachineError("Cannot assign instruction")
        if isinstance(e, int):
            x.set_value(e)
        else:
            x.set_value(e.get_value())

    def compile(self, graph):
        num_nodes = len(graph.vertex)
        xA = self.programAlice.localVariable(num_nodes, "Alice")
        xB = self.programBob.localVariable(num_nodes, "Bob")
        for node in graph.topological_sort():
            if node.type == NodeType.IN and node.name == "A":
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[num_nodes], self.instructions["rnd"]()
                    )
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[num_nodes + 1],
                        self.instructions["xor"](xA[num_nodes], xA[node.index]),
                    )
                )
                self.programAlice.add(self.instructions["push"](xA[num_nodes + 1]))
                self.programAlice.add(
                    self.instructions["assign"](xA[node.index], xA[num_nodes])
                )
                self.programBob.add(
                    self.instructions["assign"](
                        xB[node.index], self.instructions["pop"]()
                    )
                )
            elif node.type == NodeType.IN and node.name == "B":
                self.programBob.add(
                    self.instructions["assign"](
                        xB[num_nodes], self.instructions["rnd"]()
                    )
                )
                self.programBob.add(
                    self.instructions["assign"](
                        xB[num_nodes + 1],
                        self.instructions["xor"](xB[num_nodes], xB[node.index]),
                    )
                )
                self.programBob.add(self.instructions["push"](xB[num_nodes + 1]))
                self.programBob.add(
                    self.instructions["assign"](xB[node.index], xB[num_nodes])
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[node.index], self.instructions["pop"]()
                    )
                )
            elif node.type == NodeType.NOT:
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[node.index],
                        self.instructions["not"](xA[node.ancestors[0].index]),
                    )
                )
                self.programBob.add(
                    self.instructions["assign"](
                        xB[node.index], xB[node.ancestors[0].index]
                    )
                )
            elif node.type == NodeType.AND:
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[num_nodes], self.instructions["rnd"]()
                    )
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[num_nodes + 1], self.instructions["rnd"]()
                    )
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[num_nodes + 2],
                        self.instructions["xor"](
                            xA[num_nodes], xA[node.ancestors[0].index]
                        ),
                    )
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[num_nodes + 3],
                        self.instructions["xor"](
                            xA[num_nodes + 1], xA[node.ancestors[1].index]
                        ),
                    )
                )
                self.programAlice.add(
                    self.instructions["push_quad"](
                        xA[num_nodes],
                        xA[num_nodes + 2],
                        xA[num_nodes + 1],
                        xA[num_nodes + 3],
                    )
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[num_nodes],
                        self.instructions["xor"](xA[num_nodes], xA[num_nodes + 1]),
                    )
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[node.index],
                        self.instructions["and"](
                            xA[node.ancestors[0].index], xA[node.ancestors[1].index]
                        ),
                    )
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[node.index],
                        self.instructions["xor"](xA[node.index], xA[num_nodes]),
                    )
                )

                self.programBob.add(
                    self.instructions["assign"](
                        xB[node.index],
                        self.instructions["pop_quad"](
                            xB[node.ancestors[1].index], xB[node.ancestors[0].index]
                        ),
                    )
                )
                self.programBob.add(
                    self.instructions["assign"](
                        xB[num_nodes],
                        self.instructions["and"](
                            xB[node.ancestors[0].index], xB[node.ancestors[1].index]
                        ),
                    )
                )
                self.programBob.add(
                    self.instructions["assign"](
                        xB[node.index],
                        self.instructions["xor"](xB[node.index], xB[num_nodes]),
                    )
                )
            elif node.type == NodeType.XOR:
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[node.index],
                        self.instructions["xor"](
                            xA[node.ancestors[0].index], xA[node.ancestors[1].index]
                        ),
                    )
                )
                self.programBob.add(
                    self.instructions["assign"](
                        xB[node.index],
                        self.instructions["xor"](
                            xB[node.ancestors[0].index], xB[node.ancestors[1].index]
                        ),
                    )
                )
            elif node.type == NodeType.OUT and node.name == "A":
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[node.index], self.instructions["pop"]()
                    )
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[node.index],
                        self.instructions["xor"](
                            xA[node.index], xA[node.ancestors[0].index]
                        ),
                    )
                )

                self.programBob.add(
                    self.instructions["push"](xB[node.ancestors[0].index])
                )
                self.programBob.add(
                    self.instructions["assign"](
                        xB[node.index], xB[node.ancestors[0].index]
                    )
                )
            elif node.type == NodeType.OUT and node.name == "B":
                self.programBob.add(
                    self.instructions["assign"](
                        xB[node.index], self.instructions["pop"]()
                    )
                )
                self.programBob.add(
                    self.instructions["assign"](
                        xB[node.index],
                        self.instructions["xor"](
                            xB[node.index], xB[node.ancestors[0].index]
                        ),
                    )
                )

                self.programAlice.add(
                    self.instructions["push"](xA[node.ancestors[0].index])
                )
                self.programAlice.add(
                    self.instructions["assign"](
                        xA[node.index], xA[node.ancestors[0].index]
                    )
                )

    def get_program(self):
        return self.programAlice, self.programBob

    def get_local_variable(self):
        return self.local_variable_alice, self.local_variable_bob

    def get_stack(self):
        return self.stack

    def get_instructions(self):
        return self.instructions

    def create_instructions(self):
        self.instructions["rnd"] = VirtualMachine.InstructionCreator("rnd", self.rnd)
        self.instructions["push"] = VirtualMachine.InstructionCreator("push", self.push)
        self.instructions["pop"] = VirtualMachine.InstructionCreator("pop", self.pop)
        self.instructions["push_quad"] = VirtualMachine.InstructionCreator(
            "push_quad", self.push_quad
        )
        self.instructions["pop_quad"] = VirtualMachine.InstructionCreator(
            "pop_quad", self.pop_quad
        )
        self.instructions["assign"] = VirtualMachine.InstructionCreator(
            "assign", self.assign
        )
        self.instructions["xor"] = VirtualMachine.InstructionCreator("xor", self.xor)
        self.instructions["and"] = VirtualMachine.InstructionCreator(
            "and", self.and_gate
        )
        self.instructions["not"] = VirtualMachine.InstructionCreator(
            "not", self.not_gate
        )

    def run(self, programAlice, programBob):
        alice_finished = False
        bob_finished = False
        while not alice_finished or not bob_finished:
            if not alice_finished:
                try:
                    programAlice.run()
                except StackError:
                    pass
                if len(programAlice.program) == 0:
                    alice_finished = True
            if not bob_finished:
                try:
                    programBob.run()
                except StackError:
                    pass
                if len(programBob.program) == 0:
                    bob_finished = True

    def test(self, A_input, B_input, len_bytes, graph):
        self.create_instructions()
        self.compile(graph)
        programAlice, programBob = self.get_program()
        for i in range(len_bytes):
            programAlice.xA[i].set_value(A_input[i])
            programBob.xB[i + len_bytes].set_value(B_input[i])
        self.run(programAlice, programBob)
        returnvalue_a = []
        returnvalue_b = []
        for node in graph.vertex:
            if node.type == NodeType.OUT and node.name == "A":
                returnvalue_a.append(programAlice.xA[node.index].get_value())
            if node.type == NodeType.OUT and node.name == "B":
                returnvalue_b.append(programBob.xB[node.index].get_value())
        return returnvalue_a, returnvalue_b


if __name__ == "__main__":
    vm = VirtualMachine()
    graph = create_min_n(2)[0]
    A = [1, 0]
    B = [0, 1]
    print(vm.test(A, B, 2, graph))
