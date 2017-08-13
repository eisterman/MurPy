from abc import ABC, abstractmethod
from murpy.core.objects.memory import StackObj, RegObj
# TODO: Documentazione


class Operation(ABC):
    """
    Abstract Base Class for all the Operation subclasses.
    The Operations are the core of the transpiler engine, they contain
    all the information of a single "instruction" of the code.
    The Operation is paragonable at a single line of Pseudocode.
    """
    @abstractmethod
    def PreCompile(self, env):  # TODO: Precompilation Flags
        """
        Procedure for prepare the Environment for the successive compilation.

        Example of operation to do in PreCompile:
        - Check existance of precise objects in Stack
        - Ask for registries to Environment
        - Set ReserveBit for the registries in use
        - Put in and out additional information
        - Everything is needed to prepare the Operation for compiletime

        :param env: Environment of operation
        :return: Nothing
        """
        pass

    @abstractmethod
    def GetCode(self, env, p):  # TODO: Compilation flags, magari usando un item EnvState (?)
        """
        Procedure for the generation of the Brainfuck Code by the Environment

        :param env: Environment of operation
        :param p: Pointer of starting for the BFCode generation procedure
        :return: (Code, Pointer): A tuple containing the generated Code and
            the position of the pointer at the termination of the BFCode
        """
        return "", 0


# TODO: Assert the World
class INestedOperation(ABC):
    def __init__(self):
        self._IMEMOBJ = None

    def InputMemObj(self, obj):
        self._IMEMOBJ = obj


class ONestedOperation(ABC):
    def __init__(self):
        self._OMEMOBJ = None

    def OutputMemObj(self):
        return self._OMEMOBJ


class NestedOperation(INestedOperation, ONestedOperation):
    def __init__(self):
        INestedOperation.__init__(self)
        ONestedOperation.__init__(self)


class OperatorOperation(Operation, NestedOperation):
    def __init__(self, name1, name2, nreg, reservebits, exitreg):
        super().__init__()
        self._name1 = name1
        self._name2 = name2
        self._nreg = nreg  # Numero di registri
        self._exitreg = int(exitreg)  # Registro d'uscita (numerazione interna 0,1,2,...)
        self._reservebits = reservebits  # Bit di riserva post operazione
        self._choosedreg = []

    def PreCompile(self, env):  # TODO: Somma Nestata (uso della IREGKEY)
        if self._name1 is None:
            self._name1 = self._IMEMOBJ[0]
        elif self._name1 not in env.StackObject:
            raise Exception("Variabile non definita")
        if self._name2 is None:
            self._name2 = self._IMEMOBJ[1]
        elif self._name2 not in env.StackObject:
            raise Exception("Variabile non definita")
        # Registry
        choosedreg = self._choosedreg
        nreg = self._nreg
        for regobj in env.RegistryColl.values():
            if not regobj.ReserveBit and len(choosedreg) < nreg:
                choosedreg.append(regobj)
            elif len(choosedreg) == nreg:
                break
        while len(choosedreg) < nreg:
            regobj = env.RequestRegistry()
            choosedreg.append(regobj)
        # Ref Power
        for i, obj in enumerate(choosedreg):
            obj.ReserveBit = self._reservebits[i]
        self._OMEMOBJ = choosedreg[self._exitreg]

    def initGetCode(self, env):
        # TODO: Implement the head of all the GetCode and so use it later.
        # TODO: With automatic pointer extraction!!!!!!!! Now we have String and Memobj
        # TODO: Unire i comportamenti, far parlare a tutti la lingua dei MemObj
        if isinstance(self._name1, str):
            A = int(list(env.StackObject).index(self._name1))
        elif isinstance(self._name1, StackObj):
            A = env.getStackPosition(self._name1)
        elif isinstance(self._name1, RegObj):
            A = env.getRegPosition(self._name1)
        else:
            raise Exception("A is undefinable.")
        if isinstance(self._name2, str):
            B = int(list(env.StackObject).index(self._name2))
        elif isinstance(self._name2, StackObj):
            B = env.getStackPosition(self._name2)
        elif isinstance(self._name2, RegObj):
            B = env.getRegPosition(self._name2)
        else:
            raise Exception("B is undefinable.")
        Registry = env.getRegPosition(self._choosedreg)
        return A, B, Registry

    @abstractmethod
    def GetCode(self, env, p):
        pass
