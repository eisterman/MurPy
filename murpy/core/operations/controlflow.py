from . import Operation, INestedOperation


class IFConditionOp(Operation, INestedOperation):
    def __init__(self):
        super().__init__()
        self._condregkey = None
        self._oplisttrue = None
        self._oplistfalse = None
        self._choosedreg = {}

    def SetOpList(self, lista):
        # TODO: Proteggi il mondo
        if self._oplisttrue is None:
            self._oplisttrue = lista
        elif self._oplistfalse is None:
            self._oplistfalse = lista
        else:
            raise Exception("Setted OpList of IfConditionOp more than two times.")

    def PreCompile(self, env):
        self._condregkey = self._IREGKEY
        # Registri
        choosedreg = self._choosedreg
        nreg = 2
        for regKey, regObj in env.RegistryColl.items():
            if not regObj.ReserveBit and len(choosedreg) < nreg:
                choosedreg[regKey] = regObj
            elif len(choosedreg) == nreg:
                break
        while len(choosedreg) < nreg:
            regkey, regobj = env.RequestRegistry()
            choosedreg[regkey] = regobj
        # Allocate Registry
        for obj in choosedreg.values():
            obj.ReserveBit = True
        env.RegistryColl[self._condregkey].ReserveBit = True
        # Precompile Nested
        if self._oplisttrue is not None and len(self._oplisttrue) > 0:
            for op in self._oplisttrue:
                op.PreCompile(env)
        if self._oplistfalse is not None and len(self._oplistfalse) > 0:
            for op in self._oplistfalse:
                op.PreCompile(env)
        # Deallocate Registry
        for obj in choosedreg.values():
            obj.ReserveBit = False
        env.RegistryColl[self._condregkey].ReserveBit = False

    def GetCode(self, env, p):
        code = ""
        RCOND = env.getRegPosition(self._condregkey)
        R1, R2 = env.getRegPosition(self._choosedreg.keys())
        # Start Code
        code += env.MoveP(p, R1) + "[-]+" + env.MoveP(R1, R2) + "[-]" + env.MoveP(R2, RCOND)
        code += "["
        pointer = RCOND
        # CODICE UNO
        if self._oplisttrue is not None and len(self._oplisttrue) > 0:
            for op in self._oplisttrue:
                newcode, newpointer = op.GetCode(env, pointer)
                code += newcode
                pointer = newpointer
        # FINE CODICE UNO
        code += env.MoveP(pointer, R1) + "-" + env.MoveP(R1, RCOND)
        code += "[" + env.MoveP(RCOND, R2) + "+" + env.MoveP(R2, RCOND) + "-]]"
        code += env.MoveP(RCOND, R2) + "[" + env.MoveP(R2, RCOND) + "+" + env.MoveP(RCOND, R2)
        code += "-]" + env.MoveP(R2, R1) + "["
        pointer = R1
        # CODICE DUE
        if self._oplistfalse is not None and len(self._oplistfalse) > 0:
            for op in self._oplistfalse:
                newcode, newpointer = op.GetCode(env, pointer)
                code += newcode
                pointer = newpointer
        # FINE CODICE DUE
        code += env.MoveP(pointer, R1) + "-]"
        # CLEANUP
        clrcode, ptr = env.ClearRegList(R1, (RCOND, R1, R2))
        code += clrcode
        return code, ptr
