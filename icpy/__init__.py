# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from copy import deepcopy
from interval import interval, inf, imath
from .csp_parser import CspParser
from .csp_semantics import CspSemantics
from .contractor_hull import HC4
from .contractor_newton import NewtonUni
from .contractor_box import BC3
from .dag import *


def parse_and_solve(csp):
    parser = CspParser(semantics = CspSemantics())
    vs, box0, (dag, cs) = parser.parse(csp)

    # prepare an initial box
    box = deepcopy(box0)

    for c in cs:
        for i in range(len(vs)):
            bc = BC3(dag, c, vs[i], i)
            bc.contract(box)

    print('after BC3:')
    print(box)
    print()

    for c in cs:
        hc = HC4(dag, c)
        hc.contract(box)

    print('after HC4:')
    print(box)
    print()

    hc.contract(box)

    return box


def main():
    csp = open(sys.argv[1]).read()
    print(csp.strip())
    print()

    result = parse_and_solve(csp)
    print('result:')
    print(result)

