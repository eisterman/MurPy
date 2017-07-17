from _environment import Environment
from _commands import VAR, SET, ADD, SUB, MUL, IF, ELSE, ENDIF
from BFVM import brainfuck


def main_old():
    VAR("A", 5)
    VAR("B", 2)
    VAR("C", ADD("A", "B"))
    VAR("D", SUB("A", "B"))
    VAR("E", MUL("A", "B"))
    # 5 2 3 2 10 (reg 0 0 0 2)


def main():
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

if __name__ == '__main__':
    env = Environment()
    env.addRoutine(main)
    env.Parse()
    env.Precompile()
    env.Compile()
    with open('out.bf', 'w') as file:
        file.write(env.BFCode)
    tape, runned = brainfuck(env.BFCode)
    print(f"Tape: {tape}")
    print("Number of instruction: {}".format(len(env.BFCode)))
    print(f"Number of cycles: {runned}")
