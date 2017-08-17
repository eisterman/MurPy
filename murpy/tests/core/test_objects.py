import unittest
from random import randrange
from copy import copy

from murpy.core.objects.memory import StackObj, RegObj


class StackObjTestCase(unittest.TestCase):
    def setUp(self):
        self.names = ["test{}".format(i) for i in range(10)]

    def test_init(self):
        for name in self.names:
            obj = StackObj(name)
            self.assertEqual(obj.name, name)

    def test_equality(self):
        objs = [StackObj(name) for name in self.names]
        for i, name in enumerate(self.names):
            obj = StackObj(name)
            self.assertEqual(objs.index(obj), i)
            if i != 0:
                self.assertNotEqual(obj, objs[0])


class RegObjTestCase(unittest.TestCase):
    def setUp(self):
        self.skeys = list(range(10))

    def test_init_empty(self):
        try:
            RegObj(None)
        except AssertionError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_init_with_default(self):
        for skey in self.skeys:
            obj = RegObj(skey)
            self.assertEqual(obj.regkey, skey)
            self.assertTrue(obj.ReserveBit)  # Default

    def test_reservebit_get_set(self):
        obj = RegObj(self.skeys[0], False)
        self.assertFalse(obj.ReserveBit)
        obj.ReserveBit = True
        self.assertTrue(obj.ReserveBit)
        obj.ReserveBit = not obj.ReserveBit
        self.assertFalse(obj.ReserveBit)

    def test_wrongreservebit_init(self):
        start = (0, 1, 2, 3, "", "ciao", None)
        aspected = (False, True, True, True, False, True, False)
        for starter, expected in zip(start, aspected):
            obj = RegObj(self.skeys[0], starter)
            self.assertEqual(obj.ReserveBit, expected)

    def test_equality_regkey(self):
        while True:
            key1 = randrange(0, 1000000)
            key2 = randrange(0, 1000000)
            if key1 != key2:
                break
        obj1 = RegObj(key1)
        obj2 = RegObj(key2)
        self.assertNotEqual(obj1, obj2)
        obj3 = RegObj(copy(key1))
        self.assertEqual(obj3, obj1)

    def test_equality_reservebit(self):
        key = randrange(0, 1000000)
        obj1 = RegObj(key, True)
        obj2 = RegObj(key, False)
        self.assertNotEqual(obj1, obj2)
        obj3 = RegObj(key, True)
        self.assertEqual(obj3, obj1)

    def test_equality_all(self):
        while True:
            key1 = randrange(0, 1000000)
            key2 = randrange(0, 1000000)
            if key1 != key2:
                break
        obj1 = [RegObj(key1, True), RegObj(key1, False)]
        obj2 = [RegObj(key2, True), RegObj(key2, False)]
        obj3 = [RegObj(key1, True), RegObj(key1, False)]
        for o1, o2, o3 in zip(obj1, obj2, obj3):
            self.assertNotEqual(o1, o2)
            self.assertEqual(o1, o3)
            self.assertNotEqual(o3, o2)
            self.assertNotEqual(o1, o2)
        for o1, o2, o3 in zip(obj1, reversed(obj2), reversed(obj3)):
            self.assertNotEqual(o1, o2)
            self.assertNotEqual(o1, o3)
            self.assertNotEqual(o3, o2)


if __name__ == '__main__':
    unittest.main()
