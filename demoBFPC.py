import BFPC

@BFPC.BFMain
def main():
    BFPC.COMPILETIME.PseudoCode.append(5)
    print(BFPC.COMPILETIME.PseudoCode)

if __name__ == '__main__': main()