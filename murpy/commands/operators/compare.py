from .. import InterfaceObj, NestedInterfaceObj
from ...core.operations.compare import EqualOp, NotEqualOp, GreaterOp


class EQ(InterfaceObj, NestedInterfaceObj):
    # TODO: DOCUMENTAZIONE EQ
    def __init__(self, name1, name2):
        super().__init__()
        self._OPERATION = EqualOp(name1, name2)


class NEQ(InterfaceObj, NestedInterfaceObj):
    # TODO: DOCUMENTAZIONE NEQ
    def __init__(self, name1, name2):
        super().__init__()
        self._OPERATION = NotEqualOp(name1, name2)


class GR(InterfaceObj, NestedInterfaceObj):
    # TODO: DOCUMENTAZIONE GR
    def __init__(self, name1, name2):
        super().__init__()
        self._OPERATION = GreaterOp(name1, name2)
