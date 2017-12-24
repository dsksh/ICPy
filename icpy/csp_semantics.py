# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from .csp_parser import CspParser
import json
from grako.util import asjson
from interval import interval, imath
from .box import IntervalList, IntervalDict

def merge(ds):
    return {k: v for d in ds for k,v in d.items()}

def calc_rest(value, ast):
    if ast.op is None:
        return value
    else:
        d = merge([value[0], ast.arg[0]])
        k = '('+value[1]+ast.op+ast.arg[1]+')'
        if k not in d.keys():
            d[k] = (ast.op, value[1], ast.arg[1])
        return calc_rest((d,k), ast.rest)


class CspSemantics(object):

    def __init__(self):
        self.vs = {}

    def start(self, ast):
        return self.vs.keys(), IntervalDict(self.vs), ast.cs

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
            return {}, []
        else:
            d = merge([ast.head[0], ast.rest[0]])
            return d, [ast.head[1]] + ast.rest[1]

    def inequality(self, ast):
        dl,kl = ast.left
        dr,kr = ast.right
        d = merge([dl,dr])
        k = kl+ast.op+kr
        if k not in d:
            d[k] = ast.op, kl, kr
        return d, k

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
            d,k = ast.arg
            k = '('+str(0)+'-'+k+')'
            if k not in d.keys():
                d[k] = '-', str(0), k
            return d, k
            #return '-', ('C', 0), ast.arg

    def pow_expr(self, ast):
        return calc_rest(ast.base, ast.rest)


    def integer(self, ast):
        v = int(ast)
        n = 'C', v
        k = str(v)
        return {k: n}, k

    def float(self, ast):
        v = float(ast)
        n = 'C', v
        k = str(v)
        return {k: n}, k

    def infinity(self, ast):
        v = float('inf')
        n = 'C', v
        k = str(v)
        return {k: n}, k

    def interval(self, ast):
        n = 'I', ast.inf, ast.sup
        k = str(v)
        return {k: n}, k

    def ident(self, ast):
        k = ast
        n = 'V', k
        return {k: n}, k

