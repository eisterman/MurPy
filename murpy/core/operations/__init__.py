from abc import ABC, abstractmethod
from collections import OrderedDict
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


# TODO: Creare interfacce personalizzate per avere un più valido RegKeyStream tra NestedOperation
# TODO: Dividiere il concetto di NestedOperation da quello di utente del RegKeyStream
class INestedOperation(ABC):
    def __init__(self):
        self._IREGKEY = None

    def InputRegKey(self, key):
        self._IREGKEY = key


class ONestedOperation(ABC):
    def __init__(self):
        self._OREGKEY = None

    def OutputRegKey(self):
        return self._OREGKEY


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
        self._choosedreg = OrderedDict()

    def PreCompile(self, env):  # TODO: Somma Nestata (uso della IREGKEY)
        if self._name1 not in env.StackObject:
            raise Exception("Variabile non definita")
        if self._name2 not in env.StackObject:
            raise Exception("Variabile non definita")
        # Registry
        choosedreg = self._choosedreg
        nreg = self._nreg
        for regKey, regObj in env.RegistryColl.items():
            if not regObj.ReserveBit and len(choosedreg) < nreg:
                choosedreg[regKey] = regObj
            elif len(choosedreg) == nreg:
                break
        while len(choosedreg) < nreg:
            regKey, regObj = env.RequestRegistry()
            choosedreg[regKey] = regObj
        # Ref Power
        for i, obj in enumerate(choosedreg.values()):
            obj.ReserveBit = self._reservebits[i]
        self._OREGKEY = tuple(choosedreg.keys())[self._exitreg]

    @abstractmethod
    def GetCode(self, env, p):
        pass
