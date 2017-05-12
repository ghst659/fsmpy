#!/usr/bin/python3.2 -tt
# Copyright (c) 2016 ghst659@github.com
# All rights reserved.
import abc
import collections
import threading
##############################################################################
ProcessResult = collections.namedtuple("ProcessResult", ["next", "data"])
                                       
class State(metaclass=abc.ABCMeta):
    """State interface."""
    @abc.abstractmethod
    def name(self):
        """Returns the name of this state."""
        raise NotImplementedError("must override name method.")

    @abc.abstractmethod
    def process(self, *args, **kwargs):
        """Responds to *ARGS and **KWARGS, returning next state and result."""
        raise NotImplementedError("must override process method.")

class Context:
    """The state machine state engine."""
    def __init__(self, *states):
        """Initiailses the state machine."""
        self._lock = threading.RLock()
        self._state_tbl = {}    # maps state name to register State objects
        self._current = None    # current state of the machine
        for s in states:
            self.register_state(s)
        if states:
            self.current_state = states[0].name()


    def current_state(self):
        """The name of the current machine state."""
        result = None
        with self._lock:
            if self._current is not None:
                result = self._current.name()
            else:
                raise ValueError("illegal state")
        return result

    def set_current_state(self, state_tag):
        """Sets current state to the state named STATE_TAG."""
        with self._lock:
            if state_tag in self._state_tbl:
                self._current = self._state_tbl[state_tag]
            else:
                raise ValueError("illegal next state: %s" % state_tag)

    def register_state(self, state_obj):
        """Registers STATE_OBJECT as a possible state."""
        required_hook = getattr(state_obj, "process")
        if not callable(required_hook):
            raise ValueError("invalid state object")
        tag = state_obj.name()
        with self._lock:
            self._state_tbl[tag] = state_obj

    def process(self, *args, **kwargs):
        """Dispatch current state to process *ARGS and **KWARGS."""
        process_result = None
        with self._lock:
            if self._current:
                process_result = self._current.process(*args, **kwargs)
                self.set_current_state(process_result.next)
            else:
                raise ValueError("illegal next state")
        return process_result.data

# Local Variables:
# mode: python
# python-indent: 4
# End:
