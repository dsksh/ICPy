# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from .csp_parser import CspParser
import json
from grako.util import asjson
from interval import interval, imath
from .box import IntervalList, IntervalDict
from .dag import merge, append_node, append_diff_node


Box = IntervalList


def calc_rest(value, ast):
    """This function handles split binary expressions.
    """

    if ast.op is None:
        return value
    else:
        dag = merge([value[0], ast.arg[0]])

        k = '('+value[1]+ast.op+ast.arg[1]+')'
        if k not in dag.keys():
            dag[k] = (ast.op, value[1], ast.arg[1])

        dk = tuple(map(
            lambda i: append_diff_node(dag, ast.op, 
                value[1], value[2][i], ast.arg[1], ast.arg[2][i] ), 
            range(len(value[2])) ))

        return calc_rest((dag,k,dk), ast.rest)


class CspSemantics(object):

    def __init__(self):
        self.vs = {}

    def start(self, ast):
        return list(self.vs.keys()), Box(self.vs), ast.cs

    def variables(self, ast):
        if not ast.id is None:
            self.vs[ast.id[1]] = interval[ast.inf, ast.sup]
            #return ast.rest

    def signed_number(self, ast):
        v = ast.value[0][ast.value[1]][1]
        if ast.minus is None:
            return v
        else:
            return -v


    def constraints(self, ast):
        if ast.head is None:
            return {'0': ('C', 0), '1': ('C', 1)}, []
        else:
            dag = merge([ast.head[0], ast.rest[0]])
            #print(str(ast.head[1]))
            return dag, [ast.head[1]] + ast.rest[1]

    def inequality(self, ast):
        dl,kl,dkl = ast.left
        dr,kr,dkr = ast.right
        dag = merge([dl,dr])
        #k = kl+ast.op+kr
        #if k not in d:
        #    d[k] = ast.op, kl, kr
        return dag, (ast.op, (kl,dkl), (kr,dkr))

    def expression(self, ast):
        #print(json.dumps(asjson(ast.rest), indent=2))
        return calc_rest(ast.head, ast.rest)

    def term(self, ast):
        return calc_rest(ast.head, ast.rest)

    def min_expr(self, ast):
        if type(ast) == int:
            assert(False)
            return ast
        elif type(ast) == float:
            assert(False)
            return ast
        elif type(ast) == interval:
            assert(False)
            return ast
        elif type(ast) == tuple:
            return ast
        elif ast.op == "-":
            dag,k,dk = ast.arg
            k_ = '('+str(0)+'-'+k+')'
            if k_ not in dag.keys():
                dag[k_] = '-', '0', k

            dk_ = tuple(map(
                lambda i: append_diff_node(dag, '-', '0', '0', k, dk[i]), 
                range(len(dk)) ))

            return dag, k_, dk_

    def pow_expr(self, ast):
        return calc_rest(ast.base, ast.rest)


    def integer(self, ast):
        v = int(ast)
        n = 'C', v
        k = str(v)
        dk = tuple(map(lambda _: '0', self.vs))
        return {k: n}, k, dk

    def float(self, ast):
        v = float(ast)
        n = 'C', v
        k = str(v)
        dk = tuple(map(lambda _: '0', self.vs))
        return {k: n}, k, dk

    def infinity(self, ast):
        v = float('inf')
        n = 'C', v
        k = str(v)
        dk = tuple(map(lambda _: '0', self.vs))
        return {k: n}, k, dk

    def interval(self, ast):
        n = 'I', ast.inf, ast.sup
        k = str(v)
        dk = tuple(map(lambda _: '0', range(len(self.vs))))
        return {k: n}, k, dk

    def ident(self, ast):
        k = ast
        n = 'V', k
        dk = tuple(map(lambda vn: '1' if vn == k else '0', self.vs.keys()))
        return {k: n}, k, dk

