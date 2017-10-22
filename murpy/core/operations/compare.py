from . import OperatorOperation


# Prima operatione con Cleanup. Preventivamente antecedente
class EqualOp(OperatorOperation):
    def __init__(self, name1, name2):
        super().__init__(name1, name2, 3, [True, False, False], 0)

    def GetCode(self, env, p):
        code = ""
        A, B, (R1, R2, R3) = super().initGetCode(env)
        # Cleanup
        code += env.MoveP(p, R3) + "[-]"
        code += env.MoveP(R3, R2) + "[-]"
        code += env.MoveP(R2, R1) + "[-]"
        # Begin Operation
        code += env.MoveP(R1, A)
        code += "[-" + env.MoveP(A, R2) + "+" + env.MoveP(R2, R1) + "+" + env.MoveP(R1, A) + "]"
        code += env.MoveP(A, R1)
        code += "[-" + env.MoveP(R1, A) + "+" + env.MoveP(A, R1) + "]+"
        code += env.MoveP(R1, B)
        code += "[-" + env.MoveP(B, R3) + "+" + env.MoveP(R3, R2) + "-" + env.MoveP(R2, B) + "]"
        code += env.MoveP(B, R3)
        code += "[-" + env.MoveP(R3, B) + "+" + env.MoveP(B, R3) + "]"
        # Hot Topic
        code += env.MoveP(R3, R2)
        code += "[" + env.MoveP(R2, R1) + "-" + env.MoveP(R1, R2) + "[-]]"
        return code, R2


class NotEqualOp(OperatorOperation):
    def __init__(self, name1, name2):
        super().__init__(name1, name2, 3, [True, False, False], 0)

    def GetCode(self, env, p):
        code = ""
        A, B, (R1, R2, R3) = super().initGetCode(env)
        # Cleanup
        code += env.MoveP(p, R3) + "[-]"
        code += env.MoveP(R3, R2) + "[-]"
        code += env.MoveP(R2, R1) + "[-]"
        # Begin Operation
        code += env.MoveP(R1, A)
        code += "[-" + env.MoveP(A, R2) + "+" + env.MoveP(R2, R1) + "+" + env.MoveP(R1, A) + "]"
        code += env.MoveP(A, R1)
        code += "[-" + env.MoveP(R1, A) + "+" + env.MoveP(A, R1) + "]"
        code += env.MoveP(R1, B)
        code += "[-" + env.MoveP(B, R3) + "+" + env.MoveP(R3, R2) + "-" + env.MoveP(R2, B) + "]"
        code += env.MoveP(B, R3)
        code += "[-" + env.MoveP(R3, B) + "+" + env.MoveP(B, R3) + "]"
        # Hot Topic
        code += env.MoveP(R3, R2)
        code += "[" + env.MoveP(R2, R1) + "+" + env.MoveP(R1, R2) + "[-]]"
        # CLEANUP
        clrcode, ptr = env.ClearRegList(R2, (R2, R3))
        code += clrcode
        return code, ptr


class GreaterOp(OperatorOperation):
    def __init__(self, name1, name2):
        super().__init__(name1, name2, 1, [True], 0)

    def GetCode(self, env, p):
        code = ""
        raise Exception("GR not working.")
        # r1[-] a[b[-a-b]a] (a)[r1+a[-]]
        # p-out: a
        A, B, (R1, ) = super().initGetCode(env)
        # Cleanup
        code += env.MoveP(p, R1) + "[-]"
        # Begin Operation
        #  Reduction
        code += env.MoveP(R1, A) + "[" + env.MoveP(A, B)  # [
        code += "[-" + env.MoveP(B, A) + "-" + env.MoveP(A, B) + "]"  # [ ]
        code += env.MoveP(B, A) + "]"  # ]
        #  Choosing
        code += "[" + env.MoveP(A, R1) + "+" + env.MoveP(R1, A) + "[-]]"  # [ [] ]
        # CLEANUP not required in THIS case
        return code, A
