from collections import OrderedDict

from _interfaceobjects import InterfaceObj


class Environment:
    def __init__(self):
        self._code = None
        self.PseudoCode = []  # Contenitore delle operazioni da eseguire
        self.StackObject = OrderedDict()  # Container degli StackObj
        self.RoutineDict = {}

    def addRoutine(self, func):
        self.RoutineDict[func.__name__] = func

    def Parse(self):
        # MODELLO PER UNA SOLA FUNZIONE MAIN
        self.RoutineDict["main"]()
        self.PseudoCode = InterfaceObj.GetBuffer()

    def Precompile(self):
        for op in self.PseudoCode:
            op.PreCompile(self)

    def Compile(self):
        self._code = ""
        pointer = 0
        for op in self.PseudoCode:
            code, newpointer = op.GetCode(self, pointer)
            self._code += code
            pointer = newpointer
        return self._code

    @property
    def Code(self):
        return self._code
