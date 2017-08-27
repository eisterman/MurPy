from functools import wraps

from collections import OrderedDict, Iterable
from ..commands import InterfaceObj
from ..core.objects.memory import StackObj, RegObj


def BeforeParse(f):
    @wraps(f)
    def wrapper(inst, *args, **kwargs):
        # noinspection PyProtectedMember
        if inst._parsed is True:
            raise Exception("Only before Parse")  # TODO: Create Environment Exception
        return f(inst, *args, **kwargs)

    return wrapper


def BeforePrecompile(f):
    @wraps(f)
    def wrapper(inst, *args, **kwargs):
        # noinspection PyProtectedMember
        if inst._precompiled is True:
            raise Exception("Only before Precompile")  # TODO: Create Environment Exception
        return f(inst, *args, **kwargs)

    return wrapper


def BeforeCompile(f):
    @wraps(f)
    def wrapper(inst, *args, **kwargs):
        # noinspection PyProtectedMember
        if inst._compiled is True:
            raise Exception("Only before Compile")  # TODO: Create Environment Exception
        return f(inst, *args, **kwargs)

    return wrapper


class Environment:
    """
    Environment Object used for the MurPy operations.
    """
    def __init__(self):
        """Create a new Environment indipendent instance."""
        self._code = None
        self.PseudoCode = []  # Contenitore delle operazioni da eseguire
        # TODO: Refactor StackObject to a StackCollection/StackColl
        self.StackObject = OrderedDict()  # Container degli StackObj
        self.RegistryColl = OrderedDict()  # Container dei RegObj
        self.RoutineDict = {}
        self._parsed = False
        self._precompiled = False
        self._compiled = False

    @BeforePrecompile
    def ExistStackName(self, name):
        return name in self.StackObject.keys()

    @BeforePrecompile
    def RequestStackName(self, name):
        if self.ExistStackName(name):
            raise Exception("Required insertion of duplicated Stack name!")
        else:
            tmp = StackObj(name)
            self.StackObject[name] = tmp
            return tmp

    @BeforeCompile
    def RequestRegistry(self):
        """
        Request a new registry slot.
        :return: the new Reg Object.
        """
        regkey = len(self.RegistryColl)
        item = RegObj(regkey)
        self.RegistryColl[regkey] = item
        return item

    @BeforeCompile
    def getStackObjByName(self, name):
        if not self.ExistStackName(name):
            raise Exception("Variabile non definita")
        return self.StackObject[name]

    @BeforeCompile
    def getStackPosition(self, stackobjs):
        # TODO: Migliorare impacchettamento (*args)
        """
        Given a StackObject return the Tape Position of the associated registry.
        :param stackobjs: Identity Object for the stack variable or a list of it.
        :return: Tape Position of the registry or a tuple of it.
        """
        names = list(self.StackObject)
        # int(list(env.StackObject).index(self._name1))
        if not isinstance(stackobjs, Iterable):
            work = str(stackobjs.name)
            return int(names.index(work))
        else:
            work = tuple(stackobjs)
            return tuple(int(names.index(obj)) for obj in work)

    @BeforeCompile
    def getRegPosition(self, regobjs):
        """
        Given a RegObject return the Tape Position of the associated registry.
        :param regobjs: Identity Object for the registry or a list of it.
        :return: Tape Position of the registry or a tuple of it.
        """
        keys = list(self.RegistryColl.keys())
        if not isinstance(regobjs, Iterable):
            work = int(regobjs.regkey)
            return len(self.StackObject) + keys.index(work)
        else:
            work = tuple(regobjs)
            return tuple((len(self.StackObject) + keys.index(robj.regkey)) for robj in work)

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

    @BeforeParse
    def addRoutine(self, func):
        """
        Introduce in the Routine Dictionary the specified routine.
        :param func: The Routine to put in the Routine Dictionary.
        """
        # Per essere certi che l'input sia una funzione
        assert callable(func)
        assert hasattr(func, "__name__")
        self.RoutineDict[func.__name__] = func

    @BeforeParse
    def Parse(self):
        """
        Do on the data previously provided the Parsing process.
        After that all the PseudoCode will be generated into the Environment.
        """
        # MODELLO PER UNA SOLA FUNZIONE MAIN
        # TODO: Estendere il parser in modo dinamica a casi multifunzione
        self.RoutineDict["main"]()
        self.PseudoCode = InterfaceObj.BUFFER.GetMainBuffer()
        self._parsed = True

    @BeforePrecompile
    def Precompile(self):
        """
        Do the Precompilation process.
        After that all the Operation in the PseudoCode will have already
        executed his PreCompile method on the Environment for tuning it.
        """
        for op in self.PseudoCode:
            op.PreCompile(self)
        self._precompiled = True

    @BeforeCompile
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
        self._compiled = True
        return self._code

    @property
    def BFCode(self):
        """Get the BFCode if already generated."""
        return self._code

del BeforeParse, BeforePrecompile, BeforeCompile
