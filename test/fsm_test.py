#!/usr/bin/env python3
# Copyright (c) 2016 ghst659@github.com
# All rights reserved.
import unittest
import tc.fsm

class TestBase(unittest.TestCase):
    def setUp(self):
        self.mut = tc.fsm.Context()

    def tearDown(self):
        del self.mut

class TestMachine(TestBase):
    """Basic tests for the state machine base class."""

    def test_empty(self):
        with self.assertRaises(ValueError):
            x = self.mut.current()

    def test_registration(self):
        with self.assertRaises(TypeError):
            self.mut.register(Z())

    def test_illegal_state(self):
        self.mut.register(A())
        with self.assertRaises(ValueError):
            self.mut.set_current("X")
        self.mut.set_current("A")
        with self.assertRaises(ValueError):
            self.mut.process()

    def test_cycling_state(self):
        """Test three state rotation."""
        self.mut.register(A())
        self.mut.register(B())
        self.mut.register(C())
        self.mut.set_current("A")
        self.assertEqual("A", self.mut.current())
        self.assertEqual("A to B", self.mut.process())
        self.assertEqual("B", self.mut.current())
        self.assertEqual("B to C", self.mut.process())
        self.assertEqual("C", self.mut.current())
        self.assertEqual("C to A", self.mut.process())
        self.assertEqual("A", self.mut.current())

class Z(tc.fsm.State):
    def tag(self):
        return self.__class__.__name__

class A(Z):
    def process(self, *args, **kwargs):
        return tc.fsm.ProcessResult("B", "A to B")

class B(Z):
    def process(self, *args, **kwargs):
        return tc.fsm.ProcessResult("C", "B to C")

class C(Z):
    def process(self, *args, **kwargs):
        return tc.fsm.ProcessResult("A", "C to A")

if __name__ == "__main__":
    unittest.main()
