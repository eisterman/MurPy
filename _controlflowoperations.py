from _operations import Operation, NestedOperation


class IFConditionOp(Operation, NestedOperation):
    def __init__(self, condregkey, oplisttrue, oplistfalse):
        super().__init__()

    def PreCompile(self, env):
        pass

    def GetCode(self, env, p):
        pass
