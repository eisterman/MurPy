from .. import InterfaceObj, NestedInterfaceObj
from ...core.operations.math import AdditionOp, SubtractionOp, MultiplicationOp


class ADD(InterfaceObj, NestedInterfaceObj):
    """
    This command will sum two variable using a Registry as output.
    This command is a NestedInterfaceObj.
    """
    def __init__(self, name1, name2):
        """
        This command will sum two variable using a Registry as output.
        This command is a NestedInterfaceObj.
        :param name1: First member
        :param name2: Second member
        """
        super().__init__()
        self._OPERATION = AdditionOp(name1, name2)


class SUB(InterfaceObj, NestedInterfaceObj):
    """
    This command will subtract two variable using a Registry as output.
    The algorithm is classical progressive subtraction.
    This command is a NestedInterfaceObj.
    """
    def __init__(self, name1, name2):
        """
        This command will sum two variable using a Registry as output.
        This command is a NestedInterfaceObj.
        :param name1: First member
        :param name2: Second member
        """
        super().__init__()
        self._OPERATION = SubtractionOp(name1, name2)


class MUL(InterfaceObj, NestedInterfaceObj):
    """
    This command will multiply two variable using a Registry as output.
    The algorithm use heavily the registry for the operations.
    This command is a NestedInterfaceObj.
    """
    def __init__(self, name1, name2):
        """
        This command will multiply two variable using a Registry as output.
        The algorithm use heavily the registry for the operations.
        This command is a NestedInterfaceObj.
        :param name1: First member
        :param name2: Second member
        """
        super().__init__()
        self._OPERATION = MultiplicationOp(name1, name2)
