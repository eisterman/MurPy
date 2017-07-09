from _environment import Environment
from _interfaceobjects import VAR, SET, ADD, SUB, MUL, EQ, NEQ
from BFVM import brainfuck


def main_old():
    VAR("A", 5)
    VAR("B", 2)
    VAR("C", 1)
    SET("A", 3)
    SET("C", ADD("A", "B"))
    VAR("D", 2)
    VAR("E", 5)
    SET("D", SUB("C", "B"))
    SET("E", SUB("B", "C"))
    # 3 2 5 3 253


def main():
    VAR("A", 5)
    VAR("B", 2)
    VAR("C", ADD("A", "B"))
    VAR("D", 2)
    VAR("E", MUL("A", "B"))
    VAR("OUT1", NEQ("B", "C"))
    VAR("OUT2", NEQ("B", "D"))
    VAR("OUT3", EQ("B", "C"))
    VAR("OUT4", EQ("B", "D"))
    # 5 2 7 2 10 | 0 1 0 1

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
