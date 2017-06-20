from abc import ABC,abstractmethod
from collections import OrderedDict


class Environment:
    def __init__(self):
        self.PseudoCode = [] # Contenitore delle operazioni da eseguire
        self.StackObject = OrderedDict() # Container degli StackObj
        self.HeapObject = {} # Container degli HeapObj
    def insertOp(self,operation): # Inserisce operazione nello PseudoCode
        self.PseudoCode.append(operation)
    # Quando si va in compilazione si usa la posizione in StackObject e HeapObject per avere la cella
    def preCompile(self):
        for op in self.PseudoCode:
            op.preComp(self)
        #Measure Stack Size
        ssize = 0
        for obs in self.StackObject.values():
            ssize += obs._byte
        self.StackSize = ssize
        #TODO: Measure REG Size
        #TODO: Measure Heap Size ma attenzione che vengono trattati dinamicamente quindi in compile time

class Compiler:
    def __init__(self,env:Environment):
        self._env = env
        self._code = ""
    def compile(self):
        self._code = ""
        pointer = 0
        for op in self._env.PseudoCode:
            code,newpointer = op.compute(self._env,pointer)
            self._code += code
            pointer = newpointer
        return self._code

class Operation(ABC): # Operazione eseguibile e compilabile in BF
    pass

class VarOp(Operation): # Operazione di creazione di una nuova istanza STATICA
    def __init__(self,ID,obj):
        #TODO: Assert the world
        self._id = ID
        self._value = obj.getValue()
        self._byte = obj.getByte()
    def preComp(self, comp : Environment): #Può modificare lo stato del compilatore!
        if self._id in comp.StackObject.keys():
            raise "Duplicated Creation!"
        else:
            comp.StackObject[self._id] = StackObj(self._value,self._byte)
    def compute(self,env : Environment,p : int):
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
    pass

class MemOp(Operation): # Operazione di memoria (copy,set)(move è comb di copy e set, oppure mov semantic
    pass

class MemObj(ABC): # Oggetto rappresentante una cella di memoria
    pass

class StackObj(MemObj): # Oggetto rappresentate variabile statica in Stack
    def __init__(self,value,byte):
        self._value = value
        self._byte = byte
        #TODO: Error handling
    #TODO: Property

class RegObj(MemObj): # Oggetto rappresentante i registri temporanei
    pass #Forse non serve neanche sta classe

class HeapOnbj(MemObj): # Oggetto rappresentante variabile dinamica in Heap
    pass

class InterfaceObj(ABC): # Oggetti di interfaccia con l'esterno
    @abstractmethod
    def getValue(self):
        pass
    @abstractmethod
    def getByte(self):
        pass

class Byte(InterfaceObj):
    def __init__(self,value):
        self._val = int(value)
        self._byte = 1
        #TODO: Value Handling
    def getByte(self):
        return self._byte
    def getValue(self):
        return self._val

class OperationManager:
    def __init__(self,comp):
        assert isinstance(comp, Environment)
        self._compiler = comp
    def newStatic(self,name,obj):
        op = VarOp(name,obj)
        self._compiler.insertOp(op)
    def getOpBF(self):
        pass
