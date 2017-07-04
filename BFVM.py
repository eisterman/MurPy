#!/usr/bin/python
import sys
from collections import defaultdict


# TODO: Ricostruire te a manina bellina
def brainfuck (source):
    source = str(source)
    # TODO: Controllo contenuto nel Source
    loop_ptrs = {}
    loop_stack = []
    for ptr, opcode in enumerate(source):
        if opcode == '[': loop_stack.append(ptr)
        if opcode == ']':
            if not loop_stack:
                source = source[:ptr]
                break
            sptr = loop_stack.pop()
            loop_ptrs[ptr], loop_ptrs[sptr] = sptr, ptr
    if loop_stack:
        raise SyntaxError ("unclosed loops at {}".format(loop_stack))
    tape = defaultdict(int)
    cell = 0
    ptr = 0
    runned = 0
    while ptr < len(source):
        opcode = source[ptr]
        if   opcode == '>': cell += 1
        elif opcode == '<': cell -= 1
        elif opcode == '+': tape[cell] = (tape[cell] + 1) % 256
        elif opcode == '-': tape[cell] = (tape[cell] - 1) % 256
        elif opcode == ',': tape[cell] = ord(sys.stdin.read(1))
        elif opcode == '.': sys.stdout.write(chr(tape[cell]))
        elif (opcode == '[' and not tape[cell]) or \
             (opcode == ']' and tape[cell]): ptr = loop_ptrs[ptr]
        ptr += 1
        runned += 1
    # Output
    buffer = tuple( tape[i] for i in range(len(tape)) )
    return buffer, runned
