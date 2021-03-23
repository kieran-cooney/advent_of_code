import re
import sys
import numpy as np

# Match string like "a OR b"
BINARY_OP_PATTERN = re.compile(r"^(\w+)\s(OR|AND|XOR|LSHIFT|RSHIFT)\s(\w+)$")
# Match string like "NOT a"
UNARY_OP_PATTERN = re.compile(r"^(NOT)\s(\w+)$")
# Match string like "a" or "123"
VAL_PATTERN = re.compile(r"^(\w+)$")

NUM_BITS = 16
MAX_VAL = 2**NUM_BITS

from operator import and_, or_, xor

class Wire:
    """
    Class designed to emulate unsigned 16 bit integer.
    Underlying data structure is a boolean array.
    """
    def __init__(self, i):
        if isinstance(i, int):
            sub_i = i % MAX_VAL
            bin_sub_i = bin(sub_i)[2:][::-1]
            a = np.zeros(NUM_BITS, dtype=bool)
            for index, s in enumerate(bin_sub_i):
                a[index] = (s == '1')
            self.vals = a
        elif isinstance(i, str):
            self.__init__(int(i))
        else:
            try:
                self.vals = np.array(i)
                assert (self.vals.shape == (NUM_BITS, ))
            except:
                raise ValueError(f"Incorrect value {i} type passed to Wire")

    def __iter__(self):
        return (x for x in self.vals)

    def __repr__(self):
        return str(sum(2**i for i, b in enumerate(self.vals) if b))
    
    def __lshift__(self, other):
        res = np.zeros(NUM_BITS, dtype=bool)
        res[other:] = self.vals[:-other]
        return Wire(res)

    def __rshift__(self, other):
        res = np.zeros(NUM_BITS, dtype=bool)
        res[:-other] = self.vals[other:]
        return Wire(res)

    def __and__(self, other):
        return Wire(self.vals & other.vals)

    def __or__(self, other):
        return Wire(self.vals | other.vals)

    def __xor__(self, other):
        return Wire(self.vals ^ other.vals)
    
    def __invert__(self):
        return Wire(~self.vals)


class Board:
    """
    Class representing board of wires. Will lazily evaluate instructions
    as required. Example:

    b = Board(path_to_instructions.txt)
    b['a']
    """
    def _parse_line(self, l):
        instruction, label = l.strip().split(" -> ")
        binary_op_regex_result = BINARY_OP_PATTERN.match(instruction)
        if binary_op_regex_result:
            arg1, op, arg2 = binary_op_regex_result.groups()
            op_args_pair = (op, [arg1, arg2])
        else:
            unary_op_regex_result = UNARY_OP_PATTERN.match(instruction)
            if unary_op_regex_result:
                op, arg = unary_op_regex_result.groups()
                op_args_pair = (op, [arg, ])
            else:
                val_regex_result = VAL_PATTERN.match(instruction)
                if val_regex_result:
                    op_args_pair = ("VAL", list(val_regex_result.groups()))
                else:
                    raise ValueError("Bad instruction string {}".format(instruction))

        return (label, op_args_pair)


    def __init__(self, filepath):
        self.instructions = dict()
        self.values = dict()
        with open(filepath) as f:
            for line in f:
                label, op_args_pair = self._parse_line(line)
                self.instructions[label] = op_args_pair

    def _parse_val(self, string):
        try:
            val = Wire(int(string))
        except ValueError:
            val = self.__getitem__(string)
        return val

    def _parse_vals(self, strings):
        return [self._parse_val(s) for s in strings]

    def __getitem__(self, key):
        if key in self.values:
            val = self.values[key]
        else:
            op, args = self.instructions[key]
            if op == 'VAL':
                val = self._parse_val(*args)
            elif op == 'NOT':
                val = ~(self._parse_val(*args))
            elif op == 'OR':
                val = or_(*self._parse_vals(args))
            elif op == 'AND':
                val = and_(*self._parse_vals(args))
            elif op == 'XOR':
                val = xor(*self._parse_vals(args))
            elif op == 'LSHIFT':
                arg1, arg2 = args
                val = self._parse_val(arg1) << int(arg2)
            elif op == 'RSHIFT':
                arg1, arg2 = args
                val = self._parse_val(arg1) >> int(arg2)
            self.values[key] = val

        return val

def main(filepath):
    board = Board(filepath)

    ans_1 = board['a']
    print("Answer for part 1: {}".format(ans_1))

    board.values = dict()
    board.values['b'] = ans_1

    print("Answer for part 2: {}".format(board['a']))


if __name__=='__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'input.txt'
    main(filepath)
