from _operations import Operation, NestedOperation


class IFConditionOp(Operation, NestedOperation):
    def __init__(self, condition, oplisttrue, oplistfalse):
        super().__init__()
        if isinstance(condition, NestedOperation):
            pass  # TODO: eseguire lavori per un operazione su registro come condizione
        elif isinstance(condition, str):
            pass  # TODO: eseguire con al posto della condizione un nome
        else:
            raise Exception("IFConditionOp condition parameter error (str or NestedOperation)")

    def PreCompile(self, env):
        pass

    def GetCode(self, env, p):
        pass
