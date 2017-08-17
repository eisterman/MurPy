import unittest
from collections import OrderedDict
from copy import deepcopy

from murpy.compiletools import Environment, RegObj


class EnvState:
    def __init__(self, bfcode=None, pcode=[], stackobjs=OrderedDict(),
                 regobjs=OrderedDict(), functions={}):
        # Copy of the default value with list() and dict() here
        self._code = bfcode
        self.PseudoCode = list(pcode)  # Contenitore delle operazioni da eseguire
        self.StackObject = stackobjs  # Container degli StackObj
        self.RegistryColl = regobjs  # Container dei RegObj
        self.RoutineDict = dict(functions)

    def __eq__(self, other):
        return self._code == other._code and self.PseudoCode == other.PseudoCode and \
            self.StackObject == other.StackObject and self.RegistryColl == \
            other.RegistryColl and self.RoutineDict == other.RoutineDict

    @property
    def params(self):
        return self._code, self.PseudoCode, self.StackObject, self.RegistryColl, \
            self.RoutineDict

    @staticmethod
    def getState(env: Environment):
        """Used for storing the Env state without copying all the Environment"""
        return EnvState(*(deepcopy(x) for x in (env._code, env.PseudoCode, env.StackObject,
                                                env.RegistryColl, env.RoutineDict)))

    def __repr__(self):
        return "Env(code={},Pcode={},Stack={},Registry={},Routine={})".format(
            self._code, self.PseudoCode, self.StackObject, self.RegistryColl,
            self.RoutineDict )


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.env = Environment()

    def test_RequestRegistry(self):
        state0 = EnvState.getState(self.env)
        regobj = self.env.RequestRegistry()
        state1 = EnvState.getState(self.env)
        for i in (0, 1, 2, 4):
            self.assertEqual(state0.params[i],state1.params[i])
        self.assertNotEqual(state0.params[3], state1.params[3])
        self.assertEqual([x for x in state1.params[3].values() \
                          if x not in state0.params[3].values()], [regobj])

    # TODO: Continue Unittesting

if __name__ == '__main__':
    unittest.main()
