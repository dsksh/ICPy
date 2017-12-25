# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from copy import deepcopy
from interval import interval, inf, imath
from .csp_parser import CspParser
from .csp_semantics import CspSemantics
from .contractor import Hc4revise
from .contractor_newton import NewtonUni
from .dag import merge, append_node, append_diff_node


def cons_fun(dag, op, nl, nr):
    #if op == '==':
    #elif op == '>' or op == '>=':
    #elif op == '<' or op == '<=':

    n_id = append_node(dag, '-', nl[0], nr[0])
    d_ids = tuple(map(
        lambda i: append_diff_node(dag, '-', 
            nl[0], nl[1][i], nr[0], nr[1][i] ), 
        range(len(nl[1])) ))
    return n_id, d_ids


def parse_and_solve(csp):
    parser = CspParser(semantics = CspSemantics())
    vs, box0, (dag, cs) = parser.parse(csp)

    # prepare an initial box
    box = deepcopy(box0)

    c1 = Hc4revise(dag, cs)
    c1.contract(box)

    print('after Hc4revise:')
    print(box)
    print()

    op,l,r = cs[0]
    n,ds = cons_fun(dag, op, l, r)
    c2 = NewtonUni(dag, n, ds, vs[0], 0)
    c2.contract(box)

    return box


def main():
    csp = open(sys.argv[1]).read()
    print(csp.strip())
    print()

    result = parse_and_solve(csp)
    print('result:')
    print(result)

