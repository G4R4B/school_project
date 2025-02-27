from x64 import *
 
class Optimizer:
    def __init__(self, passes, instructions):
        self.instructions = self.parse_instructions(instructions)
        self.new_instructions = []
        self.passes = passes

    def parse_instructions(self, instructions):
        new_instructions = []
        for i in instructions:
            new_instructions += i.split("\n")
        return new_instructions

    def optimize(self):
        if self.passes == 0:
            self.new_instructions = self.instructions
            return
        i = 0
        while i < len(self.instructions)-1:
            if "pushq" in self.instructions[i] and "popq" in self.instructions[i+1]:
                # Optimizing pushq/popq
                self.new_instructions.append(x64_mov(self.instructions[i+1].split(" ")[-1], self.instructions[i].split(" ")[-1], tab=self.instructions[i].split(" ")[0].count("\t")))
                i += 2
            elif "movq" in self.instructions[i]:
                #check for movq not useful
                regs = self.instructions[i].split("movq ")[-1]
                src_mov, dst_mov = regs.split(", ")
                if dst_mov == src_mov:
                    i += 1
                    continue
                else:
                    self.new_instructions.append(self.instructions[i])
                    i += 1
                    
            elif "pushq" in self.instructions[i]:
                j = i
                self.new_instructions.append(self.instructions[i])
                index_of_push_new_instruction = len(self.new_instructions) - 1
                while j < len(self.instructions):
                    j += 1
                    if "movq" in self.instructions[j]:
                        self.new_instructions.append(self.instructions[j])
                        continue
                    elif "pushq" in self.instructions[j]:
                        i = j
                        self.new_instructions.append(self.instructions[j])
                        index_of_push_new_instruction = len(self.new_instructions) - 1
                        continue
                    else:
                        break
                if "popq" in self.instructions[j]:
                    self.new_instructions.pop(index_of_push_new_instruction)
                    self.new_instructions.append(x64_mov(self.instructions[j].split(" ")[-1], self.instructions[i].split(" ")[-1], tab=self.instructions[i].split(" ")[0].count("\t")))
                    i = j + 1
                else:
                    self.new_instructions.append(self.instructions[j])
                    i = j + 1
                
            else:
                self.new_instructions.append(self.instructions[i])
                i += 1

        self.new_instructions.append(self.instructions[-1])
        if self.passes > 1:
            self.instructions = self.new_instructions
            self.new_instructions = []
            self.passes -= 1
            self.optimize()
        