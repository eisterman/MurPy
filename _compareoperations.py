from abc import abstractmethod
from _operations import Operation, NestedOperation


# TODO: Write init and precompile
class CompareOp(Operation, NestedOperation):
    def __init__(self):
        super().__init__()

    def PreCompile(self, env):
        pass

    @abstractmethod
    def GetCode(self, env, p):
        pass
