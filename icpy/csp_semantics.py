# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from .csp_parser import CspParser
import json
from grako.util import asjson
from interval import interval, imath
from .box import IntervalList, IntervalDict
from .dag import merge, append_diff_node_bin, append_diff_node_un


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
            lambda i: append_diff_node_bin(dag, ast.op, 
                value[1], value[2][i], ast.arg[1], ast.arg[2][i] ), 
            range(len(value[2])) ))

        return calc_rest((dag,k,dk), ast.rest)


class CspSemantics(object):

    def __init__(self):
        self.cs = {}
        self.vs = {}

    def start(self, ast):
        return list(self.vs.keys()), Box(self.vs), ast.constrs

    def constants(self, ast):
        if not ast.id is None:
            if ast.minus is None:
                self.cs[ast.id] = ast.v
            else:
                self.cs[ast.id] = -interval[ast.inf, ast.sup]


    def variables(self, ast):
        if not ast.id is None:
            if ast.ind < 0:
                self.vs[ast.id] = ast.dom
            else:
                assert(ast.ind >= 2)
                for i in range(ast.ind):
                    self.vs[ast.id+'['+str(i)+']'] = ast.dom


    def var_index(self, ast):
        if not ast.n is None:
            return ast.n
        else: 
            return -1


    def interval(self, ast):
        return interval[ast.inf, ast.sup]

    def signed_number(self, ast):
        v = ast.value
        if ast.minus is None:
            return v
        else:
            return -v


    def constraints(self, ast):
        if ast.head is None:
            return {'0': ('C', 0), '1': ('C', 1), '2': ('C', 2)}, []
        else:
            dag = merge([ast.head[0], ast.rest[0]])
            #print(str(ast.head[1]))
            return dag, [ast.head[1]] + ast.rest[1]

    def inequality(self, ast):
        dl,n_id_l,d_ids_l = ast.left
        dr,n_id_r,d_ids_r = ast.right
        dag = merge([dl,dr])
        return dag, (ast.op, (n_id_l,d_ids_l), (n_id_r,d_ids_r))

    def expression(self, ast):
        #print(json.dumps(asjson(ast.rest), indent=2))
        return calc_rest(ast.head, ast.rest)

    def term(self, ast):
        return calc_rest(ast.head, ast.rest)

    def min_expr(self, ast):
        if type(ast) == tuple:
            return ast
        elif ast.op == "-":
            dag,n_id,d_ids = ast.arg
            n_id_ = '('+str(0)+'-'+n_id+')'
            if n_id_ not in dag.keys():
                dag[n_id_] = '-', '0', n_id

            d_ids_ = tuple(map(
                lambda i: append_diff_node_bin(dag, '-', '0', '0', n_id, d_ids[i]), 
                range(len(d_ids)) ))

            return dag, n_id_, d_ids_

    def pow_expr(self, ast):
        # check the type of the exponent
        if not ast.rest.op is None:
            arg = ast.rest.arg
            dag = arg[0]
            assert(type(dag[arg[1]][1]) is int)

        return calc_rest(ast.base, ast.rest)

    def unary_fun(self, ast):
        dag = ast.arg[0]

        k = ast.name+'('+ast.arg[1]+')'
        if k not in dag.keys():
            dag[k] = (ast.name, ast.arg[1])

        dk = tuple(map(
            lambda i: append_diff_node_un(dag, ast.name, 
                ast.arg[1], ast.arg[2][i] ), 
            range(len(ast.arg[2])) ))

        return dag, k, dk

    def ident_ref(self, ast):
        n_id = ast.id
        if n_id in self.cs.keys():
            assert(ast.ind < 0)
            v = self.cs[n_id]
            n = 'C', v
            n_id = str(v)
            d_ids = tuple(map(lambda _: '0', self.vs))
            return {n_id: n}, n_id, d_ids
        else:
            if ast.ind >= 0:
                n_id = n_id+'['+str(ast.ind)+']'
            n = 'V', n_id
            d_ids = tuple(map(lambda vn: '1' if vn == n_id else '0', self.vs.keys()))
            return {n_id: n}, n_id, d_ids


    def const(self, ast):
        v = ast
        n = 'C', v
        n_id = str(v)
        d_ids = tuple(map(lambda _: '0', self.vs))
        return {n_id: n}, n_id, d_ids

    def integer(self, ast):
        return int(ast)

    def float(self, ast):
        return float(ast)

    def infinity(self, ast):
        return float('inf')

