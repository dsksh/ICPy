# -*- coding: utf-8 -*-

#from __future__ import print_function
import sys
import argparse
from copy import deepcopy
from interval import interval
from .csp_parser import CspParser
from .csp_semantics import CspSemantics
from .contractor_hull import HC4
from .contractor_box import BC3
from .solver import Solver


def parse_and_solve(eps, csp):
    parser = CspParser(semantics = CspSemantics())
    vs, box0, (dag, cs) = parser.parse(csp)

    # prepare an initial box
    box = deepcopy(box0)

    print(dag)

#    # demonstration of the contractors
#    for c in cs:
#        for i in range(len(vs)):
#            bc = BC3(dag, c, vs[i], i)
#            bc.contract(box)
#
#    print('after BC3:')
#    print(box)
#    print()
#
#    for c in cs:
#        hc = HC4(dag, c)
#        hc.contract(box)
#
#    print('after HC4:')
#    print(box)
#    print()
#
#    # one more contraction
#    hc.contract(box)
#
#    return box


    # branch and prune solving
    solver = Solver(vs, dag, cs, eps)
    ss = solver.solve(box)

    return ss


def main():
    parser = argparse.ArgumentParser(description='Solve a numerical CSP.')
    parser.add_argument('csp_fn', metavar='example.bch', type=str,
            help='a filename of a CSP description')
    parser.add_argument('-e', '--eps', metavar='<e>', type=float, default=0.1,
            help='a precition of the solving process')
    args = parser.parse_args()
    
    csp = open(args.csp_fn).read()

    print('[input model]')
    print(csp.strip())
    print()

    result = parse_and_solve(args.eps, csp)
    print('[result]')
    #print(result)
    for i in range(len(result)):
        print('solution %d:' % i)
        print(result[i])
        print()

