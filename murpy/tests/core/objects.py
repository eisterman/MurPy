import unittest

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
        self.skeys = ["test{}".format(i) for i in range(5)] + list(range(5))

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
        for test, yeah in zip(start, aspected):
            obj = RegObj(self.skeys[0], test)
            self.assertEqual(obj.ReserveBit, yeah)

if __name__ == '__main__':
    unittest.main()
