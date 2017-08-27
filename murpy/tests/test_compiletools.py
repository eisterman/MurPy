import unittest
from collections import OrderedDict
from copy import deepcopy

from murpy.compiletools import Environment, StackObj


# noinspection PyProtectedMember
class EnvState:
    def __init__(self, bfcode=None, pcode=None, stackobjs=OrderedDict(),
                 regobjs=OrderedDict(), functions=None):
        # Copy of the default value with list() and dict() here
        if pcode is None:
            pcode = []
        if functions is None:
            functions = {}
        self._code = bfcode
        self.PseudoCode = list(pcode)  # Contenitore delle operazioni da eseguire
        self._StackColl = stackobjs  # Container degli StackObj
        self._RegistryColl = regobjs  # Container dei RegObj
        self.RoutineDict = dict(functions)

    def __eq__(self, other):
        return self._code == other._code and self.PseudoCode == other.PseudoCode and \
               self._StackColl == other._StackColl and \
               self._RegistryColl == other._RegistryColl and self.RoutineDict == other.RoutineDict

    @property
    def params(self):
        return self._code, self.PseudoCode, self._StackColl, self._RegistryColl, \
               self.RoutineDict

    @staticmethod
    def getState(env: Environment):
        """Used for storing the Env state without copying all the Environment"""
        return EnvState(*(deepcopy(x) for x in (env._code, env.PseudoCode, env._StackColl,
                                                env._RegistryColl, env.RoutineDict)))

    def __repr__(self):
        return "Env(code={},Pcode={},Stack={},Registry={},Routine={})".format(
            self._code, self.PseudoCode, self._StackColl, self._RegistryColl,
            self.RoutineDict)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.env = Environment()

    def test_RequestRegistry(self):
        state0 = EnvState.getState(self.env)
        regobj = self.env.RequestRegistry()
        state1 = EnvState.getState(self.env)
        for i in (0, 1, 2, 4):
            self.assertEqual(state0.params[i], state1.params[i])
        self.assertNotEqual(state0.params[3], state1.params[3])
        self.assertEqual([x for x in state1.params[3].values()
                          if x not in state0.params[3].values()], [regobj])

    def test_RequestStackName(self):
        state0 = EnvState.getState(self.env)
        name1 = "test1"
        name2 = "tester2"
        stackobj1 = self.env.RequestStackName(name1)
        state1 = EnvState.getState(self.env)
        stackobj2 = self.env.RequestStackName(name2)
        state2 = EnvState.getState(self.env)
        for i in (0, 1, 3, 4):
            self.assertEqual(state0.params[i], state1.params[i])
            self.assertEqual(state1.params[i], state2.params[i])
        self.assertNotEqual(state0.params[2], state1.params[2])
        self.assertNotEqual(state1.params[2], state2.params[2])
        # Manual build
        target1 = StackObj(name1)
        target2 = StackObj(name2)
        self.assertEqual(target1, stackobj1)
        self.assertEqual(target2, stackobj2)
        self.assertEqual([tuple(pair) for pair in state1.params[2].items()
                          if pair not in state0.params[2].items()], [(name1, target1)])
        self.assertEqual([tuple(pair) for pair in state2.params[2].items()
                          if pair not in state0.params[2].items()], [(name1, target1), (name2, target2)])

    def test_ExistStackName(self):
        name = "demotest_ExistStackName"
        self.assertFalse(self.env.ExistStackName(name))
        # noinspection PyUnusedLocal
        stackobj = self.env.RequestStackName(name)
        self.assertTrue(self.env.ExistStackName(name))
        self.assertFalse(self.env.ExistStackName("randomtest"))

    def test_getStackObjByName(self):
        name = "demotest_getStackObjByName"
        stackobj = self.env.RequestStackName(name)
        stackobj_env = self.env.getStackObjByName(name)
        self.assertIs(stackobj, stackobj_env)
        with self.assertRaises(Exception):
            self.env.getStackObjByName(name + "42_broken")

    def test_getStackPosition_single(self):
        aspected = len(self.env._StackColl)
        name = "demotest_getStackPosition_single"
        stackobj = self.env.RequestStackName(name)
        self.assertEqual(aspected, self.env.getStackPosition(stackobj))

    # TODO
    def test_getStackPosition_iterable(self):
        pass

        # TODO: Continue Unittesting from getRegPosition


if __name__ == '__main__':
    unittest.main()
