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
        super().__init__(name1, name2, 6, [False, False, False, False, False, True], 5, True)

    def GetCode(self, env, p):
        code = ""
        # R1=0 R2=1 R3=0 R4=A R5=B R6=out(0)
        # >+>>++>+++ +<+ [->-[>]<<] <[->>>>+<<<<] <[-<]
        # out-p = R1
        A, B, Regs = super().initGetCode(env)
        R1, R2, R3, R4, R5, R6 = Regs
        # Cleanup
        clrcode, ptr = env.ClearRegList(p, Regs)
        code += clrcode
        # Begin Operation
        #  Introduction
        code += env.MoveP(ptr, R2) + "+" + env.MoveP(R2, A)
        code += "[-" + env.MoveP(A, R3) + "+" + env.MoveP(R3, R4) + "+" + env.MoveP(R4, A) + "]"
        code += env.MoveP(A, R3) + "[-" + env.MoveP(R3, A) + "+" + env.MoveP(A, R3) + "]"
        code += env.MoveP(R3, B) + "[-" + env.MoveP(B, R3) + "+" + env.MoveP(R3, R5) + "+" + env.MoveP(R5, B) + "]"
        code += env.MoveP(B, R3) + "[-" + env.MoveP(R3, B) + "+" + env.MoveP(B, R3) + "]"
        code += env.MoveP(R3, R5) + "+" + env.MoveP(R5, R4) + "+"
        #  Magic Loop
        code += "[->-[>]<<]"
        # Output and Syncronization
        code += "<[->>>>+<<<<]<[-<]"
        # CLEANUP
        clrcode, ptr = env.ClearRegList(R1, (R1, R2, R3, R4, R5))
        code += clrcode
        return code, ptr
