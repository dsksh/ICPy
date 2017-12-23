from __future__ import print_function
import sys
from copy import deepcopy
from interval import interval, inf, imath
from .csp_parser import CspParser
from .csp_semantics import CspSemantics
from .contractor import Hc4revise

def parse_and_solve(csp):
    parser = CspParser(semantics = CspSemantics())
    vs, (cd, cs) = parser.parse(csp)

    # set variable nodes
    for v in vs.keys():
        cd[v] = vs[v]

    # prepare an initial box
    box = {}
    for v in vs.keys():
        box[v] = vs[v][2]

    contractor = Hc4revise(cd, cs)
    contractor.contract(box)

    return box


def main():
#if __name__ == '__main__':
    csp = open(sys.argv[1]).read()
    print(csp.strip())
    print()

    result = parse_and_solve(csp)
    print(result)
    #print(result[1])
    #print(result[2])
