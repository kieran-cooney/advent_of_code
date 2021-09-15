import re
import sys
from collections import defaultdict, namedtuple
from math import floor

Instruction = namedtuple('Instruction', ['func', 'register', 'inc'])

def parse_input(line):
    inst, *rest = line.replace(',', '').replace('+', '').split()
    if inst in ['hlf', 'tpl', 'inc']:
        return Instruction(inst, rest[0], 0)
    elif inst == 'jmp':
        return Instruction(inst, '', int(rest[0]))
    elif inst in ['jie', 'jio']:
        return Instruction(inst, rest[0], int(rest[1]))
    else:
        raise ValueError("Invalid instruction {} input".format(inst))


class Computer():
    def __init__(self, filepath):
        self.registers = defaultdict(int)
        self.instruction_num = 0

        self.instructions = list()
        self.halt = False
        
        with open(filepath, 'r') as f:
            for line in f:
                self.instructions.append(parse_input(line))

    def hlf(self, register):
        self.registers[register] = self.registers[register]//2
        self.instruction_num += 1
    
    def tpl(self, register):
        self.registers[register] = self.registers[register]*3
        self.instruction_num += 1

    def inc(self, register):
        self.registers[register] += 1
        self.instruction_num += 1

    def jmp(self, offset):
        self.instruction_num += offset

    def jie(self, register, offset):
        if self.registers[register] %2 == 0:
            self.jmp(offset)
        else:
            self.instruction_num += 1

    def jio(self, register, offset):
        if self.registers[register] == 1:
            self.jmp(offset)
        else:
            self.instruction_num += 1

    def step(self):
        assert not self.halt
        if self.instruction_num not in range(len(self.instructions)):
            self.halt = True
        else:
            inst, reg, inc = self.instructions[self.instruction_num]
            print(inst, reg, inc)
            # Case matching would be so nice here
            if inst == 'hlf':
                self.hlf(reg)
            elif inst == 'tpl':
                self.tpl(reg)
            elif inst == 'inc':
                self.inc(reg)
            elif inst == 'jmp':
                self.jmp(inc)
            elif inst == 'jie':
                self.jie(reg, inc)
            elif inst == 'jio':
                self.jio(reg, inc)
            else:
                raise ValueError("Invalid instruction {} passed".format(inst))
    
    def run(self):
        while not self.halt:
            self.step()
        
    
    def __repr__(self):
        return "Compute({})".format(self.registers)


def main(filepath):
    comp1 = Computer(filepath)
    comp1.run()

    print(comp1)

    comp2 = Computer(filepath)
    comp2.registers['a'] = 1
    comp2.run()

    print(comp2)


if __name__=='__main__':
    if len(sys.argv) > 1:
          filepath = sys.argv[1]
    else:
          filepath = "input.txt"
    main(filepath)
