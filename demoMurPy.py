from MurPy import Environment,OperationManager,Compiler,Byte
from MurPy import newEnvironment
from _interfaceobjects import protovar,protoset

def testmain():
    executor = Environment()
    helper = OperationManager(executor)
    helper.newStatic("ciao",Byte(5))
    helper.newStatic("ciao2",Byte(2))
    helper.newStatic("ciao3",Byte(1))
    helper.setTo("ciao",Byte(3))
    executor.preCompile()
    comp = Compiler(executor)
    code = comp.compile()
    print(code)

def main():
    protovar("ciao",5)
    protovar("ciao2",2)
    protovar("ciao3",1)
    protoset("ciao",3)

if __name__ == '__main__':
    #testmain()
    env = newEnvironment()
    env.addRoutine(main)
    env.Parse()
    env.Precompile()
    env.Compile()
    print(env.Code)
