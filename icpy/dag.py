# -*- coding: utf-8 -*-

from __future__ import print_function
import sys


def merge(ds):
    """This function merges a set of DAGs into a DAG.
    """

    return {k: v for d in ds for k,v in d.items()}


def append_node(dag, op, arg1, arg2):
    """This function generates and appends a node, which corresponds to a binary operator application, to the DAG.

    Returns: the node key.
    """
    k = '('+arg1+op+arg2+')'
    if k not in dag.keys():
        dag[k] = (op, arg1, arg2)

    return k


def append_diff_node(dag, op, v1, d1, v2, d2):
    """This function appends a node representing the differentiated expression of a given expression.

    Returns: the node key.
    """

    if op == '+':
        if d1 == '0':
            return d2
        elif d2 == '0':
            return d1
        else:
            return append_node(dag, '+', d1, d2)

    elif op == '-':
        if d1 == '0':
            return append_node(dag, '-', '0', d2)
        elif d2 == '0':
            return d1
        else:
            return append_node(dag, '-', d1, d2)

    elif op == '*':
        if d1 == '0':
            return append_node(dag, '*', v1, d2)
        elif d2 == '0':
            return append_node(dag, '*', v2, d1)
        else:
            # a.v*b.d + b.v*a.d
            k1 = append_node(dag, '*', v1, d2)
            k2 = append_node(dag, '*', v2, d1)
            return append_node(dag, '+', k1, k2)

    elif op == '/':
        if d1 == '0':
            # b.d * (- a.v/(b.v*b.v))
            k1 = append_node(dag, '*', v2, v2)
            k2 = append_node(dag, '/', v1, k1)
            k3 = append_node(dag, '-', '0', k2)
            return append_node(dag, '*', d2, k3)
        elif d2 == '0':
            return append_node(dag, '/', d1, v2)
        else:
            # a.d / b.v + b.d * (- a.v/(b.v*b.v))
            k1 = append_node(dag, '/', d1, v2)

            k2 = append_node(dag, '*', v2, v2)
            k3 = append_node(dag, '/', v1, k2)
            k4 = append_node(dag, '-', '0', k3)
            k5 = append_node(dag, '*', d2, k4)

            return append_node(dag, '+', k1, k5)

    elif op == '^':
        # (n * a.v^(n-1)) * a.d
        n_ = dag[v2][1] - 1 # v2 should be an integer
        dag[str(n_)] = 'C', n_
        k1 = append_node(dag, '^', v1, str(n_))
        k2 = append_node(dag, '*', v2, k1)
        return append_node(dag, '*', k2, d1)

    else:
        print("unsupported op: "+op)
        assert(False)

