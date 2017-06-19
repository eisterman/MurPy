from abc import ABC
from functools import wraps

### IL DECORATORE USERA' PER LE FUNZIONI COMPILATORE 'COMPILETIME'

def BFMain(func): # Potrebbe subire modifiche quando verrà aggiunto il supporto a multiple cose
    global COMPILETIME
    COMPILETIME = Compiler()
    return func

class Operation(ABC): # Operazione eseguibile e compilabile in BF
    pass

class VarOp(Operation): # Operazione di creazione di una nuova istanza STATICA
    def __init__(self,Value):
        self._value = Value
        self._byte = 1 #TODO: Use for automatic stack creation

class NewOp(Operation): # Operazione di creazione di una nuova istanza DINAMICA
    pass

class MathOp(Operation): # Operazione simil-math (Var1,Var2,MathOperatorLambda) - circa -
    def __init__(self, Var1, Var2):
        assert isinstance(Var1,MemObj)
        self._var1 = Var1
        self._var2 = type(Var1)(Var2)
        #Casta Var2 al tipo di Var1 - Se non c'è nello Stack, usa Registro oppure prendi Val e se possibile, esegui.

class SumOp(MathOp):
    pass

class MemOp(Operation): # Operazione di memoria (copy,set)(move è comb di copy e set, oppure mov semantic
    pass

class MemObj(ABC): # Oggetto rappresentante una cella di memoria
    pass

class StackObj(MemObj): # Oggetto rappresentate variabile statica in Stack
    pass

class HeapOnbj(MemObj): # Oggetto rappresentante variabile dinamica in Heap
    pass

class ByteX(StackObj): # TEST per un oggetto Byte statico
    def __init__(self,val):
        self._val = int(val)
        assert self._val >= 0 and self.val <=255 #byte limitation
        Compiler.insertOp()
    def __add__(self, other):
        COMPILETIME.insertOp(MathOp())

class Compiler:
    def __init__(self):
        self.PseudoCode = [] # Contenitore delle operazioni da eseguire
        self.StackObject = {} # Container degli StackObj
        self.HeapObject = {} # Container degli HeapObj
    def infereStackSize(self): # Calcola dimensione dello stack
        #TODO: Utilizzare inferenza dinamica o intelligente
        i = 0
        for obj in self.PseudoCode:
            if isinstance(obj,VarOp): i += 1
        return i
    def infereREGSize(self): # Calcola numero di registri necessari per fare le cose.
        pass
    def insertOp(self,operation): # Inserisce operazione nello PseudoCode
        pass
    def getBFCodeOp(self,operation): # Ottiene il codice BF da un operazione (PRIVATE)
        pass
    def compile(self):
        pass