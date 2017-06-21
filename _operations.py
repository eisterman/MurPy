from abc import ABC,abstractmethod
from _internalobjects import StackObj
from _interfaceobjects import InterfaceObj

class Operation(ABC): # Operazione eseguibile e compilabile in BF
    @abstractmethod
    def preComp(self,env): pass
    @abstractmethod
    def compute(self,env, p): pass

class VarOp(Operation): # Operazione di creazione di una nuova istanza STATICA
    def __init__(self,ID,obj):
        #TODO: Assert the world
        self._id = ID
        self._value = obj.getValue()
        self._byte = obj.getByte()
    def preComp(self, env): #Può modificare lo stato del compilatore!
        if self._id in env.StackObject.keys():
            raise "Duplicated Creation!"
        else:
            env.StackObject[self._id] = StackObj(self._value, self._byte)
    def compute(self,env,p):
        #CASO SPECIALE UN BYTE:
        #TODO: Estensione a multipli Byte
        code = ""
        target = int(list(env.StackObject).index(self._id))
        if p > target:
            code += "<"*(p-target)
        else:
            code += ">"*(target-p)
        code += "+"*self._value
        return (code,target)

class NewOp(Operation): # Operazione di creazione di una nuova istanza DINAMICA
    pass

class MathOp(Operation): # Operazione simil-math (Var1,Var2,MathOperatorLambda) - circa -
    pass

class SumOp(MathOp):
    def __init__(self,target,one,second): # target = $one + $second
        self._neededReg = 2 # TODO: Estendere a più Byte
        self._target = target
        self._one = one
        self._second = second
    def preComp(self,env):
        if not self._target in env.StackObject:
            raise "Variabile bersaglio non in Stack"
        else:
            pass


class MemOp(Operation): # Operazione di memoria (copy,set)(move è comb di copy e set, oppure mov semantic
    pass

class SetOp(MemOp): # Operazione di set
    def __init__(self,ID,obj):
        #TODO: Assert the world
        self._id = ID # Id Bersaglio
        self._obj = obj # Valore da ficcare nel Berdaglio
    def preComp(self, env):
        if not self._id in env.StackObject: #TODO: Heap support
            raise "Variabile non definita"
    def compute(self,env, p: int):
        code = ""
        target = int(list(env.StackObject).index(self._id))
        obj = self._obj
        env.StackObject[self._id] = StackObj(obj.getValue(),obj.getByte()) # Per tenere traccia
        if p > target:
            code += "<" * (p - target)
        else:
            code += ">" * (target - p)
        targetval = self._obj.getValue()
        code += '[-]' #Azzeramento variabile
        code += "+" * targetval
        return (code, target)
