#!/usr/bin/env python3
from __future__ import print_function
import sys                      # access to basic things like sys.argv
import os                       # access pathname utilities
import argparse                 # for command-line options parsing
import concurrent.futures
import random
import threading
import time
import tc.fsm
##############################################################################
class S0(tc.fsm.State):
    def process(self, v):
        next_state = "S1"
        result = self.name + " " + v
        return next_state, result

class S1(tc.fsm.State):
    def process(self, v):
        next_state = "S2"
        result = self.name + " " + v
        return next_state, result

class S2(tc.fsm.State):
    def process(self, v):
        next_state = "S3"
        result = self.name + " " + v
        return next_state, result

class S3(tc.fsm.State):
    def process(self, v):
        next_state = "S4"
        result = self.name + " " + v
        return next_state, result

class S4(tc.fsm.State):
    def process(self, v):
        next_state = "S5"
        result = self.name + " " + v
        return next_state, result

class S5(tc.fsm.State):
    def process(self, v):
        next_state = "S6"
        result = self.name + " " + v
        return next_state, result

class S6(tc.fsm.State):
    def process(self, v):
        next_state = "S7"
        result = self.name + " " + v
        return next_state, result

class S7(tc.fsm.State):
    def process(self, v):
        next_state = "S0"
        result = self.name + " " + v
        return next_state, result

def client_requests(service, limit):
    skein = threading.current_thread().name
    for i in range(limit):
        message = "{}:{}".format(skein, i)
        response = service.process(message)
        print(response, file=sys.stderr)
        time.sleep(0.5 * random.random())
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
    parser.add_argument("-t","--threads", metavar="THREADS", type=int, default=4,
                        dest="threads",
                        help="number of threads.")
    parser.add_argument("-n","--number", metavar="NUM", type=int, default=8,
                        dest="limit",
                        help="iterations per thread.")
    parser.add_argument("-v","--verbose",
                        dest="verbose", action="store_true",
                        help="run verbosely")
    parser.add_argument("targets",
                        metavar="TARGET_FILE", nargs="*",
                        help="target files to process, nargs=* means 0 or more")
    args = parser.parse_args(args=argv[1:])  # will exit on parse error
    ################################################################
    if exit_code == 0:
        service = tc.fsm.Context(S0(), S1(), S2(), S3(), S4(), S5(), S6(), S7())
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as pool:
            for t in range(args.threads):
                pool.submit(client_requests, service, args.limit)
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
