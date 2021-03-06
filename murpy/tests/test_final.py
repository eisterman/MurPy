import unittest

from BFVM import brainfuck

from murpy.commands.memory.stack import VAR, SET
from murpy.commands.operators.math import ADD, SUB, MUL
from murpy.commands.controlflow.IF import IF, ELSE, ENDIF

from murpy.compiletools import Environment


class FinalTestCase(unittest.TestCase):
    def setUp(self):
        self.env = Environment()

    def EnvCode(self, fun):
        self.env.addRoutine(fun)
        self.env.Parse()
        self.env.Precompile()
        self.env.Compile()
        code = self.env.BFCode
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
        self.assertEqual(tape[:-2], (7, 2, 1, 8))

    def test_SUB(self):
        def main():
            VAR("A", 5)
            VAR("B", 2)
            SET("A", SUB("A", "B"))
            VAR("C", 1)
            VAR("D", SUB("C", "A"))
        tape = self.EnvCode(main)[1]
        self.assertEqual(tape[:-2], (3, 2, 1, 254))

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
        self.assertEqual(tape[:-4], (10, 2, 1, 10, 10, 0, 0, 0, 1))

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
        self.assertEqual(tape[:-3], (5, 3, 0, 1))

    def test_DoubleIFELSEVar(self):
        def main():
            VAR("A", 5)
            VAR("B", 0)
            IF("A")
            IF("B")
            SET("B", 4)
            ELSE()
            SET("A", 1)
            ENDIF()
            ELSE()
            SET("B", 1)
            ENDIF()
            VAR("C", 3)
        tape = self.EnvCode(main)[1]
        self.assertEqual(tape[:-6], (1, 0, 3))
        # TODO: Controllare quantità di registri alloccati almeno una volta

    # TODO: MORE TEST!!!!!!!

    def tearDown(self):
        self.env = None

if __name__ == '__main__':
    unittest.main()
