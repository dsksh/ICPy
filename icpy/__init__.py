# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from copy import deepcopy
from interval import interval, inf, imath
from .csp_parser import CspParser
from .csp_semantics import CspSemantics
from .contractor import Hc4revise

def parse_and_solve(csp):
    parser = CspParser(semantics = CspSemantics())
    vs, box0, (dag, cs) = parser.parse(csp)

    # prepare an initial box
    box = deepcopy(box0)

    contractor = Hc4revise(dag, cs)
    contractor.contract(box)

    return box


def main():
#if __name__ == '__main__':
    csp = open(sys.argv[1]).read()
    print(csp.strip())
    print()

    result = parse_and_solve(csp)
    print(result)
