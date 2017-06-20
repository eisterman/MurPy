from BFPC import Environment,OperationManager,Byte,Compiler

def main():
    executor = Environment()
    helper = OperationManager(executor)
    helper.newStatic("ciao",Byte(5))
    executor.preCompile()
    comp = Compiler(executor)
    code = comp.compile()
    print(code)

if __name__ == '__main__': main()