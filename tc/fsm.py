#!/usr/bin/python3.2 -tt
# Copyright (c) 2016 ghst659@github.com
# All rights reserved.
import abc
import collections
import threading
##############################################################################
ProcessResult = collections.namedtuple("ProcessResult", ["nexttag", "data"])
                                       
class State(metaclass=abc.ABCMeta):
    """State interface."""
    @abc.abstractmethod
    def tag(self):
        """Returns the tag of this state."""
        raise NotImplementedError("must override tag method.")

    @abc.abstractmethod
    def process(self, *args, **kwargs):
        """Processes inputs, returning next state and result."""
        raise NotImplementedError("must override process method.")

class Context:
    """Performs transitions according to process results."""

    def __init__(self, *states):
        self._lock = threading.RLock()
        self._state_tbl = {} # maps state tag to register State objects
        self._incumbent = None  # current state of the machine
        if states:
            for s in states:
                self.register(s)
            self.current_state = states[0].tag()

    def current(self):
        """The tag of the current machine state."""
        result = None
        with self._lock:
            if self._incumbent:
                result = self._incumbent.tag()
            else:
                raise ValueError("illegal state")
        return result

    def set_current(self, state_tag):
        """Sets current state."""
        with self._lock:
            if state_tag in self._state_tbl:
                self._incumbent = self._state_tbl[state_tag]
            else:
                raise ValueError("illegal next state: %s" % state_tag)

    def register(self, state_obj):
        """Registers a possible state."""
        required_hook = getattr(state_obj, "process")
        if not callable(required_hook):
            raise ValueError("invalid state object")
        tag = state_obj.tag()
        with self._lock:
            self._state_tbl[tag] = state_obj

    def process(self, *args, **kwargs):
        """Dispatch current state to process inputs."""
        process_result = None
        with self._lock:
            if self._incumbent:
                process_result = self._incumbent.process(*args, **kwargs)
                self.set_current(process_result.nexttag)
            else:
                raise ValueError("illegal next state")
        return process_result.data

# Local Variables:
# mode: python
# python-indent: 4
# End:
