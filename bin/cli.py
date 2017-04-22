#!/usr/bin/env python3
from __future__ import print_function
import sys                      # access to basic things like sys.argv
import os                       # access pathname utilities
import argparse                 # for command-line options parsing
import fileinput
import tc.fsm
##############################################################################
class ParseState:
    def __init__(self, shared):
        self._accum = shared
    def clear(self):
        self._accum.clear()
    def close(self):
        result = list(x.rstrip() for x in self._accum)
        self.clear()
        return result
    def add(self, line):
        self._accum.append(line)

class Outside(ParseState):
    def process(self, line):
        # print("outside: %s" % line, file=sys.stderr)
        next_state = self.name
        result = None
        if line.strip() != "":
            self.add(line)
            next_state = "Inside"
            return next_state, result

class Inside(ParseState):
    def process(self, line):
        # print("inside: %s" % line, file=sys.stderr)
        next_state = self.name
        if line.strip() == "":
            result = self.close()
            next_state = "Outside"
        else:
            result = None
            self.add(line)
        return next_state, result


class LineParser:
    def __init__(self):
        self._buffer = []
        self._fsm = tc.fsm.Context()
        self._fsm.register_state(Outside(self._buffer))
        self._fsm.register_state(Inside(self._buffer))
        self._fsm.current_state = "Outside"
        self._cleanup = ParseState(self._buffer)

    def run(self, stream):
        for line in stream:
            # print("run: %s" % line, file=sys.stderr)
            result = self._fsm.process(line)
            if result:
                yield result
        conclusion = self._cleanup.close()
        if conclusion:
            yield conclusion
##############################################################################
def main(argv):
    """
    Example command-line entrypoint
    """
    exit_code = 0
    global me; me = os.path.basename(argv[0]) # name of this program
    global mydir; mydir = os.path.dirname(os.path.abspath(__file__))
    ################################
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-v","--verbose",
                        dest='verbose', action="store_true",
                        help="run verbosely")
    parser.add_argument("targets",
                        metavar="TARGET_FILE", nargs="*",
                        help="target files to process, nargs=* means 0 or more")
    args = parser.parse_args(args=argv[1:])  # will exit on parse error
    ################################################################
    if exit_code == 0:
        buf = []
        o = Outside(buf)
        i = Inside(buf)
        print("o.name = %s, i.name = %s" % (o.name, i.name))
        lp = LineParser()
        for stanza in lp.run(fileinput.input(args.targets)):
            print("\n".join(stanza))
            print("-" * 80)
    ################################################################
    return exit_code

##############################################################################
# The following code calls main only if this program is invoked standalone
if __name__ == "__main__":
    sys.exit(main(sys.argv))
##############################################################################
# Text Editor Settings to help retain formatting; last line is for vi/vim
# Local Variables:
# mode: python
# python-indent: 4
# End:
# vim: set expandtab:
