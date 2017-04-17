#!/usr/bin/python3.2 -tt
##############################################################################
class IllegalState(Exception):
    """Signifies that an illegal state has been encountered."""
    pass

class FSMContext:
    """The state machine state engine."""

    def __init__(self):
        """Initiailses the state machine."""
        self._state_tbl = {}    # maps state name to register State objects
        self._current = None    # current state of the machine

    @property
    def current_state(self):
        """The name of the current machine state."""
        result = None
        if self._current is not None:
            result = self._current.name
        return result

    @current_state.setter
    def current_state(self, state_tag):
        """Sets current state to the state named STATE_TAG."""
        result = None
        if state_tag in self._state_tbl:
            self._current = self._state_tbl[state_tag]
            result = state_tag
        else:
            raise IllegalState("invalid state: %s" % state_tag)
        return result

    def register_state(self, state_obj):
        """Registers STATE_OBJECT as a possible state."""
        tag = state_obj.name
        self._state_tbl[tag] = state_obj
        return tag

    def process(self, *args, **kwargs):
        """Dispatch current state to process *ARGS and **KWARGS."""
        if self._current is not None:
            next_state_tag = self._current.process(*args, **kwargs)
            self.current_state = next_state_tag

class State:
    """Base class for a state in the state machine."""
    
    @property
    def name(self):
        """Returns the name of this state."""
        return self.__class__.__name__

    def process(self, *args, **kwargs):
        """Responds to *ARGS and **KWARGS, returning next state name"""
        next_state_tag = self.name
        return next_state_tag

# Local Variables:
# mode: python
# python-indent: 4
# End:
