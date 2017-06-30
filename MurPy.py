from abc import ABC,abstractmethod
from collections import OrderedDict
from _interfaceobjects import Byte
from _operations import VarOp, SetOp

from _interfaceobjects import newInterfaceObj
#TODO: Index for variable name
class Environment:
    def __init__(self):
        self.PseudoCode = [] # Contenitore delle operazioni da eseguire
        self.StackObject = OrderedDict() # Container degli StackObj
        self.HeapObject = {} # Container degli HeapObj
        self.MaxREGNumber = 0
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

class OperationManager:
    def __init__(self,comp):
        assert isinstance(comp, Environment)
        self._compiler = comp
    def newStatic(self,name,obj):
        op = VarOp(name,obj)
        self._compiler.insertOp(op)
    def setTo(self,name,obj):
        op = SetOp(name,obj)
        self._compiler.insertOp(op)
    def getOpBF(self):
        pass

# New Environment
class newEnvironment:
    def __init__(self):
        self._code = None
        self.PseudoCode = [] # Contenitore delle operazioni da eseguire
        self.StackObject = OrderedDict()  # Container degli StackObj
        self.RoutineDict = {}
    def addRoutine(self,func):
        self.RoutineDict[func.__name__] = func
    def Parse(self):
        # MODELLO PER UNA SOLA FUNZIONE MAIN
        self.RoutineDict["main"]()
        self.PseudoCode = newInterfaceObj.getBuffer()
    def Precompile(self):
        for op in self.PseudoCode:
            op.PreCompile(self)
        # Measure Stack Size
        ssize = 0
        for obs in self.StackObject.values():
            ssize += obs._byte
        self.StackSize = ssize
        # TODO: Measure REG Size
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