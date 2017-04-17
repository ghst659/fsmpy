#!/usr/bin/python3.2 -tt
import threading
##############################################################################
class IllegalState(Exception):
    """Signifies that an illegal state has been encountered."""
    pass

class Context:
    """The state machine state engine."""

    def __init__(self):
        """Initiailses the state machine."""
        self._lock = threading.RLock()
        self._state_tbl = {}    # maps state name to register State objects
        self._current = None    # current state of the machine

    @property
    def current_state(self):
        """The name of the current machine state."""
        result = None
        with self._lock:
            if self._current is not None:
                result = self._current.name
        return result

    @current_state.setter
    def current_state(self, state_tag):
        """Sets current state to the state named STATE_TAG."""
        with self._lock:
            if state_tag in self._state_tbl:
                self._current = self._state_tbl[state_tag]
            else:
                raise IllegalState("invalid state: %s" % state_tag)

    def register_state(self, state_obj):
        """Registers STATE_OBJECT as a possible state."""
        tag = state_obj.name
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
        return process_result


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
        return (next_state_tag, process_result)

# Local Variables:
# mode: python
# python-indent: 4
# End:
