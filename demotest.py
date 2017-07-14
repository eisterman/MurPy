import unittest

from _environment import Environment
from _interfaceobjects import VAR, SET, ADD, SUB, MUL, IF, ELSE, ENDIF
from BFVM import brainfuck


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.env = Environment()

    def EnvCode(self, fun):
        env = self.env
        env.addRoutine(fun)
        env.Parse()
        env.Precompile()
        env.Compile()
        code = env.BFCode
        tape, runned = brainfuck(code)
        return code, tape, runned

    def test_VARSET(self):
        def main():
            VAR("A", 5)
            VAR("B", 2)
            SET("A", 3)
            VAR("C", 1)
        tape = self.EnvCode(main)[1]
        self.assertEqual(tape, (3, 2, 1))

    def test_ADD(self):
        def main():
            VAR("A", 5)
            VAR("B", 2)
            SET("A", ADD("A", "B"))
            VAR("C", 1)
            VAR("D", ADD("C", "A"))
        tape = self.EnvCode(main)[1]
        # Vi sono ben due registri temporanei
        self.assertEqual(tape, (7, 2, 1, 8, 0, 0))

    def test_SUB(self):
        def main():
            VAR("A", 5)
            VAR("B", 2)
            SET("A", SUB("A", "B"))
            VAR("C", 1)
            VAR("D", SUB("C", "A"))
        tape = self.EnvCode(main)[1]
        self.assertEqual(tape, (3, 2, 1, 254, 0, 0))

    def test_MUL(self):
        def main():
            VAR("A", 5)
            VAR("B", 2)
            SET("A", MUL("A", "B"))
            VAR("C", 1)
            VAR("D", MUL("A", "C"))
            VAR("E", MUL("C", "A"))
            VAR("F", 0)
            VAR("G", MUL("A", "F"))
            VAR("H", MUL("A", "F"))
            VAR("I", 1)
        tape = self.EnvCode(main)[1]
        self.assertEqual(tape, (10, 2, 1, 10, 10, 0, 0, 0, 1, 0, 0, 0, 0))

    def test_DoubleNotNestedIFVar(self):
        def main():
            VAR("A", 5)
            VAR("B", 2)
            IF("A")
            SET("B", 3)
            ENDIF()
            VAR("C", 0)
            IF("C")
            SET("B", 4)
            ENDIF()
            VAR("D", 1)
        tape = self.EnvCode(main)[1]
        self.assertEqual(tape, (5, 3, 0, 1, 0, 0, 0))

    def tearDown(self):
        self.env = None

if __name__ == '__main__':
    unittest.main()
