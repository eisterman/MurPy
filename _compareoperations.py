from _operations import OperatorOperation


# Prima operatione con Cleanup. Preventivamente antecedente
class EqualOp(OperatorOperation):
    def __init__(self, name1, name2):
        super().__init__(name1, name2, 3, [True, False, False], 0)

    def GetCode(self, env, p):
        code = ""
        A = int(list(env.StackObject).index(self._name1))
        B = int(list(env.StackObject).index(self._name2))
        R1, R2, R3 = env.getRegPosition(self._choosedreg.keys())
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
