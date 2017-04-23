#!/usr/bin/python3.2 -tt
# Copyright (c) 2016 ghst659@github.com
# All rights reserved.
import collections
import threading
##############################################################################
ProcessResult = collections.namedtuple("ProcessResult", ["next", "data"])
                                       
class State:
    """Base class for a state in the state machine."""
    
    @property
    def name(self):
        """Returns the name of this state."""
        return self.__class__.__name__

    def process(self, *args, **kwargs):
        """Responds to *ARGS and **KWARGS, returning next state and result."""
        next_state_tag = self.name
        process_result = None
        return ProcessResult(next=next_state_tag, data=process_result)

class Context:
    """The state machine state engine."""

    def __init__(self, *states):
        """Initiailses the state machine."""
        self._lock = threading.RLock()
        self._state_tbl = {}    # maps state name to register State objects
        self._current = None    # current state of the machine
        self._strict = True    # raise ValueError on illegal state
        if states:
            for s in states:
                self.register_state(s)
            self.current_state = states[0].name

    @property
    def strict(self):
        """Return the state of the strict flag."""
        return self._strict

    @strict.setter
    def strict(self, strictness):
        """Sets the strict property to STRICTNESS."""
        self._strict = strictness

    @property
    def current_state(self):
        """The name of the current machine state."""
        result = None
        with self._lock:
            if self._current is not None:
                result = self._current.name
            elif self._strict:
                raise ValueError("illegal state")
            else:
                pass
        return result

    @current_state.setter
    def current_state(self, state_tag):
        """Sets current state to the state named STATE_TAG."""
        with self._lock:
            if state_tag in self._state_tbl:
                self._current = self._state_tbl[state_tag]
            elif self._strict:
                raise ValueError("illegal next state: %s" % state_tag)
            else:
                pass

    def register_state(self, state_obj, name=None):
        """Registers STATE_OBJECT as a possible state."""
        required_hook = getattr(state_obj, "process")
        if not callable(required_hook):
            raise ValueError("invalid state object")
        tag = name if name else state_obj.name
        with self._lock:
            self._state_tbl[tag] = state_obj
        return tag

    def process(self, *args, **kwargs):
        """Dispatch current state to process *ARGS and **KWARGS."""
        process_result = None
        with self._lock:
            if self._current is not None:
                next_state, process_result = self._current.process(*args, **kwargs)
                self.current_state = next_state
            elif self._strict:
                raise ValueError("illegal state")
            else:
                pass
        return process_result

# Local Variables:
# mode: python
# python-indent: 4
# End:
