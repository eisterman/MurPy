from MurPy import Environment,OperationManager,Compiler,Byte

def main():
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

if __name__ == '__main__': main()