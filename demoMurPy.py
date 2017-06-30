from MurPy import Environment
from _interfaceobjects import var, put


def main():
    var("ciao", 5)
    var("ciao2", 2)
    var("ciao3", 1)
    put("ciao", 3)

if __name__ == '__main__':
    env = Environment()
    env.addRoutine(main)
    env.Parse()
    env.Precompile()
    env.Compile()
    print(env.Code)
