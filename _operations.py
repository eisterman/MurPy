from abc import ABC, abstractmethod
from collections import OrderedDict
from _internalobjects import StackObj
# TODO: Documentazione


class Operation(ABC):
    """
    Abstract Base Class for all the Operation subclasses.
    The Operations are the core of the transpiler engine, they contain
    all the information of a single "instruction" of the code.
    The Operation is paragonable at a single line of Pseudocode.
    """
    @abstractmethod
    def PreCompile(self, env):  # TODO: Decidere cosa cazzo deve ritornare il precompile
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
    def GetCode(self, env, p):  # TODO: Argomenti speciali per GetCode, magari usando un item EnvState (?)
        """
        Procedure for the generation of the Brainfuck Code by the Environment

        :param env: Environment of operation
        :param p: Pointer of starting for the BFCode generation procedure
        :return: (Code, Pointer): A tuple containing the generated Code and
            the position of the pointer at the termination of the BFCode
        """
        return "", 0


# TODO: Dividere in InNestedOperation e OutNestedOperation o comunque un interfaccia personalizzata
class NestedOperation(ABC):
    def __init__(self):
        self._IREGKEY = None
        self._OREGKEY = None

    def InputRegKey(self, key):
        self._IREGKEY = key

    def OutputRegKey(self):
        return self._OREGKEY


class OperatorOperation(Operation, NestedOperation):
    def __init__(self, name1, name2, nreg, reservebits, exitreg):
        super().__init__()
        self._name1 = name1
        self._name2 = name2
        self._nreg = nreg  # Numero di registri
        self._exitreg = int(exitreg)  # Registro d'uscita (numerazione interna 0,1,2,...)
        self._reservebits = reservebits  # Bit di riserva post operazione
        self._choosedreg = OrderedDict()

    def PreCompile(self, env):  # TODO: Somma Nestata
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


# TODO: creare un sistema per la memorizzazione tipizzata
class NewStaticOp(Operation, NestedOperation):
    def __init__(self, name, value):
        super().__init__()
        self._name = name
        self._value = value

    def PreCompile(self, env):
        if self._name in env.StackObject.keys():
            raise Exception("Duplicated Creation!")
        else:
            env.StackObject[self._name] = StackObj(self._value)

    def GetCode(self, env, p):
        # CASO SPECIALE UN BYTE:
        # TODO: Estensione a multipli Byte
        code = ""
        target = int(list(env.StackObject).index(self._name))
        code += env.MoveP(p, target)
        code += "+" * self._value
        return code, target  # Tuple


class ChangeStaticValueOp(Operation):
    def __init__(self, name, value):
        super().__init__()
        # TODO: Assert the world
        self._name = name  # Id Bersaglio
        self._value = value  # Valore da ficcare nel Berdaglio

    def PreCompile(self, env):
        if self._name not in env.StackObject:  # TODO: Heap support
            raise Exception("Variabile non definita")

    def GetCode(self, env, p):
        code = ""
        target = int(list(env.StackObject).index(self._name))
        env.StackObject[self._name] = StackObj(self._value)  # Per tenere traccia
        if p > target:
            code += "<" * (p - target)
        else:
            code += ">" * (target - p)
        targetval = self._value
        code += '[-]'  # Azzeramento variabile
        code += "+" * targetval
        return code, target


class RegToStackOp(Operation, NestedOperation):  # PROTOCOLLO NESTEDOP
    def __init__(self, stackname):
        super().__init__()
        self._stackname = stackname

    def PreCompile(self, env):
        if self._stackname not in env.StackObject:  # TODO: Heap support & Assert the World
            raise Exception("Variabile non definita")
        env.RegistryColl[self._IREGKEY].ReserveBit = False

    def GetCode(self, env, p):
        code = ""
        start = env.getRegPosition(self._IREGKEY)
        target = int(list(env.StackObject).index(self._stackname))
        code += env.MoveP(p, target)
        code += "[-]"
        code += env.MoveP(target, start)
        code += "[-" + env.MoveP(start, target) + "+" + env.MoveP(target, start) + "]"
        return code, start


class CopyStackToRegOp(Operation, NestedOperation):  # PROTOCOLLO NESTEDOP
    def __init__(self, stackname):
        super().__init__()
        self._stackname = stackname
        self._targetreg = {}

    def PreCompile(self, env):
        if self._stackname not in env.StackObject:
            raise Exception("Variabile non definita")
        reservedreg = self._targetreg
        nreg = 2
        for regKey, regObj in env.RegistryColl.items():
            if not regObj.ReserveBit and len(reservedreg) < nreg:
                reservedreg[regKey] = regObj
            elif len(reservedreg) == nreg:
                break
        while len(reservedreg) < nreg:
            regKey, regObj = env.RequestRegistry()
            reservedreg[regKey] = regObj
        # Ref Power
        vals = list(reservedreg.values())
        vals[0].ReserveBit = True
        vals[1].ReserveBit = False
        self._OREGKEY = tuple(reservedreg.keys())[0]

    def GetCode(self, env, p):
        code = ""
        A = int(list(env.StackObject).index(self._stackname))
        R1 = env.getRegPosition(list(self._targetreg.keys())[0])
        R2 = env.getRegPosition(list(self._targetreg.keys())[1])
        code += env.MoveP(p, R1)
        code += "[-]"
        code += env.MoveP(R1, A)
        code += "[-" + env.MoveP(A, R1) + "+" + env.MoveP(R1, R2) + "+"
        code += env.MoveP(R2, A) + "]"
        code += env.MoveP(A, R2)
        code += "[-" + env.MoveP(R2, A) + "+" + env.MoveP(A, R2) + "]"
        return code, R2


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
