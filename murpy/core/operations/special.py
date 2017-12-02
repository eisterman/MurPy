from . import Operation, INestedOperation, ONestedOperation, NestedOperation


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


# TODO: Unittest & Integrationtest
class ClosureOp(Operation, NestedOperation):
    def __init__(self, oplist):
        super().__init__()
        self._oplist = oplist

    def PreCompile(self, env):
        regkeys = []
        if self._IMEMOBJ is not None:
            regkeys.append(self._IMEMOBJ)
        for op in self._oplist:
            if isinstance(op, INestedOperation):
                op.InputMemObj(self._IMEMOBJ)
            op.PreCompile(env)
            regkeys.append(op.OutputMemObj())
        self._OMEMOBJ = tuple(regkeys)

    def GetCode(self, env, p):
        code = ""
        pointer = int(p)
        for op in self._oplist:
            newcode, newpointer = op.GetCode(env, pointer)
            code += newcode
            pointer = newpointer
        return code, pointer
