from .. import InterfaceObj, NestedInterfaceObj
from ...core.operations.compare import EqualOp, NotEqualOp


class EQ(InterfaceObj, NestedInterfaceObj):
    # TODO: DOCUMENTAZIONE EQ
    def __init__(self, name1, name2):
        super().__init__()
        self._OPERATION = EqualOp(name1, name2)


class NEQ(InterfaceObj, NestedInterfaceObj):
    # TODO: DoCUMENTAZIONE NEQ
    def __init__(self, name1, name2):
        super().__init__()
        self._OPERATION = NotEqualOp(name1, name2)
