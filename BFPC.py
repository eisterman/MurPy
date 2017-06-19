from abc import ABC

class Operation(ABC): # Operazione eseguibile e compilabile in BF
    pass

class VarOp(Operation): # Operazione di creazione di una nuova istanza STATICA
    pass

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
    pass

class HeapOnbj(MemObj): # Oggetto rappresentante variabile dinamica in Heap
    pass

class Compiler:
    def __init__(self):
        self.PseudoCode = [] # Contenitore delle operazioni da eseguire
        #self.StackObject = {} # Container degli StackObj
        #self.HeapObject = {} # Container degli HeapObj
    def infereStackSize(self): # Calcola dimensione dello stack
        pass
    def infereREGSize(self): # Calcola numero di registri necessari per fare le cose.
        pass
    def insertOp(self,operation): # Inserisce operazione nello PseudoCode
        pass
    def getBFCodeOp(self,operation): # Ottiene il codice BF da un operazione (PRIVATE)
        pass
    def compile(self):
        pass