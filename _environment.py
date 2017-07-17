from collections import OrderedDict, Iterable
from _internalobjects import RegObj
from _interfaceobjects import InterfaceObj


class Environment:
    """
    Environment Object used for the MurPy operations.
    """
    def __init__(self):
        """Create a new Environment indipendent instance."""
        self._code = None
        self.PseudoCode = []  # Contenitore delle operazioni da eseguire
        self.StackObject = OrderedDict()  # Container degli StackObj
        self.RegistryColl = OrderedDict()  # Container dei RegObj
        self.RoutineDict = {}

    def RequestRegistry(self):
        """
        Request a new registry slot.
        :return: regkey = Identity Key of the new Reg, item = the new Reg Object.
        """
        regkey = len(self.RegistryColl)
        item = RegObj()
        self.RegistryColl[regkey] = item
        return regkey, item

    def getRegPosition(self, regkey):
        """
        Given a regkey return the Tape Position of the associated registry.
        :param regkey: Identity Key fo the registry or a list of it.
        :return: Tape Position of the registry or a tuple of it.
        """
        keys = list(self.RegistryColl.keys())
        if not isinstance(regkey, Iterable):
            work = int(regkey)
            return len(self.StackObject) + keys.index(work)
        else:
            work = tuple(regkey)
            return tuple((len(self.StackObject) + keys.index(rkey)) for rkey in work)

    @staticmethod
    def MoveP(start: int, end: int):
        """
        Autogenerate the BFCode for the pointer moving from a
        position to another.
        :param start: Position of start.
        :param end: Position of end.
        :return: The BFCode of the movement.
        """
        if start > end:
            return "<" * (start - end)
        else:
            return ">" * (end - start)

    @staticmethod
    def ClearRegList(startpos: int, reglist: tuple):
        code = ""
        pointer = int(startpos)
        for reg in reglist:
            code += Environment.MoveP(pointer, reg) + "[-]"
            pointer = reg
        return code, pointer

    def clear(self):
        self.__init__()

    def addRoutine(self, func):
        """
        Introduce in the Routine Dictionary the specified routine.
        :param func: The Routine to put in the Routine Dictionary.
        """
        # TODO: Assert func as Function Type
        self.RoutineDict[func.__name__] = func

    def Parse(self):
        """
        Do on the data previously provided the Parsing process.
        After that all the PseudoCode will be generated into the Environment.
        """
        # MODELLO PER UNA SOLA FUNZIONE MAIN
        # TODO: Le IF interfaccia sono separate bla bla, ma in OP sono un unica op a buffer diverso
        self.RoutineDict["main"]()
        # Proteggo il BUFFER da import non voluti
        self.PseudoCode = InterfaceObj.BUFFER.GetMainBuffer()

    def Precompile(self):
        """
        Do the Precompilation process.
        After that all the Operation in the PseudoCode will have already
        executed his PreCompile method on the Environment for tuning it.
        """
        for op in self.PseudoCode:
            op.PreCompile(self)

    def Compile(self):
        """
        Do the Compilation process.
        After the Precompilation and the tuning of the Environment with this
        method the Environment will compute the final BFCode.
        :return: The BFCode compiled.
        """
        self._code = ""
        pointer = 0
        for op in self.PseudoCode:
            code, newpointer = op.GetCode(self, pointer)
            self._code += code
            pointer = newpointer
        return self._code

    @property
    def BFCode(self):
        """Get the BFCode if already generated."""
        return self._code
