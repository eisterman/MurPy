from .. import InterfaceObj, NestedInterfaceObj
from ...core.operations.memory import NewStaticOp, RegToStackOp, ChangeStaticValueOp
from ...core.operations.special import NestedOp


class VAR(InterfaceObj):
    """
    This command will create a new variable in the stack.
    This command can take as value a NestedInterfaceObj SubClass.
    """
    def __init__(self, name, value=0):  # TODO: Typecoding
        """
        This command will create a new variable in the stack.
        :param name: Name of the new variable
        :param value: Value assigned at the variable
        """
        # PER ORA SOLO VALORI NUMERICI PURI
        if isinstance(value, NestedInterfaceObj):
            oplist = [NewStaticOp(name, 0), value.getOp(), RegToStackOp(name)]
            op = NestedOp(oplist)
        else:
            op = NewStaticOp(name, value)
        self.BUFFER.AddPseudoCode(op)


class SET(InterfaceObj):
    """
    This command will edit the value into a already existing variable
    in the stack.
    This command can take as value a NestedInterfaceObj SubClass.
    """
    def __init__(self, name, value=0):
        """
        This command will edit the value into a already existing variable
        in the stack.
        This command can take as value a NestedInterfaceObj SubClass.
        :param name: Name of the variable to be changed.
        :param value: Value or NestedInterfaceObj to be inserted in the variable.
        """
        if isinstance(value, NestedInterfaceObj):
            oplist = [value.getOp(), RegToStackOp(name)]
            op = NestedOp(oplist)
        else:
            op = ChangeStaticValueOp(name, value)
        self.BUFFER.AddPseudoCode(op)
