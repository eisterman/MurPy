from .. import InterfaceObj, NestedInterfaceObj
from ...core.operations.controlflow import IFConditionOp
from ...core.operations.special import NestedOp
from ...core.operations.memory import CopyStackToRegOp

__all__ = ["IF", "ELSE", "ENDIF"]


class IF(InterfaceObj):
    def __init__(self, condition):
        preludeops = []
        if isinstance(condition, str):
            preludeops.append(CopyStackToRegOp(condition))
        elif isinstance(condition, NestedInterfaceObj):
            preludeops.append(condition.getOp())
        else:
            raise Exception("IF can take only variable or NestedInterfaceObj")
        preludeops.append(IFConditionOp())
        self.BUFFER.TrackIfIndex(len(self.BUFFER.RefBuffer()))
        self.BUFFER.AddPseudoCode(NestedOp(preludeops))
        self.BUFFER.IndentBuffer()


class ELSE(InterfaceObj):
    def __init__(self):
        outif = self.BUFFER.DeIndentBuffer()
        refbuffer = self.BUFFER.RefBuffer()
        refbuffer[self.BUFFER.GetIfIndex()].RefLastOp().SetOpList(outif)
        self.BUFFER.IndentBuffer()


class ENDIF(InterfaceObj):
    def __init__(self):
        outif = self.BUFFER.DeIndentBuffer()
        refbuffer = self.BUFFER.RefBuffer()
        refbuffer[self.BUFFER.PopIfIndex()].RefLastOp().SetOpList(outif)
