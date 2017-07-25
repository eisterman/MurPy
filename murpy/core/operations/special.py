from . import Operation, INestedOperation, ONestedOperation


class NestedOp(Operation):  # Risolutore e contenitore di operazioni multiple (per ora protocollo RegKey)
    def __init__(self, oplist):
        self._oplist = oplist

    def RefLastOp(self):
        return self._oplist[-1]

    def PreCompile(self, env):
        MObuffer = None
        for op in self._oplist:
            if isinstance(op, INestedOperation):
                op.InputMemObj(MObuffer)
            op.PreCompile(env)
            if isinstance(op, ONestedOperation):
                MObuffer = op.OutputMemObj()

    def GetCode(self, env, p):
        code = ""
        pointer = int(p)
        for op in self._oplist:
            newcode, newpointer = op.GetCode(env, pointer)
            code += newcode
            pointer = newpointer
        return code, pointer
