from . import Operation


class NestedOp(Operation):  # Risolutore e contenitore di operazioni multiple (per ora protocollo RegKey)
    def __init__(self, oplist):
        self._oplist = oplist

    def RefLastOp(self):
        return self._oplist[-1]

    def PreCompile(self, env):
        regbuffer = None
        for op in self._oplist:
            op.InputRegKey(regbuffer)
            op.PreCompile(env)
            regbuffer = op.OutputRegKey()

    def GetCode(self, env, p):
        code = ""
        pointer = int(p)
        for op in self._oplist:
            newcode, newpointer = op.GetCode(env, pointer)
            code += newcode
            pointer = newpointer
        return code, pointer
