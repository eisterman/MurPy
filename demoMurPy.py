from BFVM import brainfuck

from murpy.commands.memory.stack import VAR, SET
from murpy.commands.operators.math import ADD, SUB, MUL
from murpy.commands.controlflow.IF import IF, ELSE, ENDIF
from murpy.commands.operators.compare import GR, EQ

from murpy.compiletools import Environment


def main_old():
    VAR("A", 5)
    VAR("B", 2)
    VAR("C", ADD("A", "B"))
    VAR("D", SUB("A", "B"))
    VAR("E", MUL("A", "B"))
    # 5 2 3 2 10 (reg 0 0 0 2)


def main_oldino():
    VAR("A", 5)
    VAR("B", 0)
    IF("A")
    IF("B")
    SET("B", 4)
    ELSE()
    SET("A", 1)
    ENDIF()
    ELSE()
    SET("B", 1)
    ENDIF()
    VAR("C", 3)
    # 1 0 3 | reg


def main():
    VAR("A", 5)
    VAR("B", 3)
    VAR("C", 1)
    VAR("D", 1)
    VAR("out1", 0)
    VAR("out2", 10)
    SET("out1", GR("A", "B"))
    SET("out2", GR("C", "B"))
    # 5 3 1 1 | 1 0 | reg
    IF(GR("A", "B"))
    SET("C", 10)
    ELSE()
    SET("C", 3)
    ENDIF()
    IF(GR("B", "A"))
    SET("D", 10)
    ELSE()
    SET("D", 3)
    ENDIF()
    VAR("out3", 2)
    # 5 3 10 3 | 1 0 2 | reg


if __name__ == '__main__':
    env = Environment()
    env.addRoutine(main)
    env.Parse()
    env.Precompile()
    env.Compile()
    print("Code: {}".format(env.BFCode))
    with open('out.bf', 'w') as file:
        file.write(env.BFCode)
    tape, runned = brainfuck(env.BFCode)
    print("Tape: {}".format(tape))
    print("Number of instruction: {}".format(len(env.BFCode)))
    print("Number of cycles: {}".format(runned))
