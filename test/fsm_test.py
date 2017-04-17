#!/usr/bin/env python3
# Copyright (c) 2016 ghst659@github.com
# All rights reserved.
import unittest
import tc.fsm

class TestBase(unittest.TestCase):
    def setUp(self):
        self.fsm = tc.fsm.Context()

    def tearDown(self):
        del self.fsm

class TestOneState(TestBase):
    """Basic tests for the state machine base class."""

    def test_empty(self):
        """Test empty state machine."""
        self.assertTrue(self.fsm.current_state is None)

    def test_illegal_state(self):
        """Test setting an illegal state."""
        self.fsm.register_state(A())
        with self.assertRaises(tc.fsm.IllegalState):
            self.fsm.current_state = "X"
        self.fsm.current_state = "A"
        with self.assertRaises(tc.fsm.IllegalState):
            self.fsm.process()

    def test_cycling_state(self):
        """Test three state rotation."""
        self.fsm.register_state(A())
        self.fsm.register_state(B())
        self.fsm.register_state(C())
        self.fsm.current_state = "A"
        self.assertEqual("A", self.fsm.current_state)
        self.assertEqual("A to B", self.fsm.process())
        self.assertEqual("B", self.fsm.current_state)
        self.assertEqual("B to C", self.fsm.process())
        self.assertEqual("C", self.fsm.current_state)
        self.assertEqual("C to A", self.fsm.process())
        self.assertEqual("A", self.fsm.current_state)

class A(tc.fsm.State):
    """One of three states."""

    def process(self, *args, **kwargs):
        return ("B", "A to B")

class B(tc.fsm.State):
    """One of three states."""

    def process(self, *args, **kwargs):
        return ("C", "B to C")

class C(tc.fsm.State):
    """One of three states."""

    def process(self, *args, **kwargs):
        return ("A", "C to A")

if __name__ == "__main__":
    unittest.main()
