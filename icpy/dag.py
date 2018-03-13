# -*- coding: utf-8 -*-

from __future__ import print_function
import sys


def merge(ds):
    """This function merges a set of DAGs into a DAG.
    """

    return {k: v for d in ds for k,v in d.items()}


def append_node_bin(dag, op, arg1, arg2):
    """This function generates and appends a node, which corresponds to a binary operator application, to the DAG.

    Returns: the node key.
    """
    k = '('+arg1+op+arg2+')'
    if k not in dag.keys():
        dag[k] = (op, arg1, arg2)

    return k


def append_node_un(dag, op, arg):
    k = '('+op+arg+')'
    if k not in dag.keys():
        dag[k] = (op, arg)

    return k


def append_diff_node_bin(dag, op, v1, d1, v2, d2):
    """This function appends a node representing the differentiated expression of a given expression.

    Returns: the node key.
    """

    if op == '+':
        if d1 == '0':
            return d2
        elif d2 == '0':
            return d1
        else:
            return append_node_bin(dag, '+', d1, d2)

    elif op == '-':
        if d1 == '0':
            return append_node_bin(dag, '-', '0', d2)
        elif d2 == '0':
            return d1
        else:
            return append_node_bin(dag, '-', d1, d2)

    elif op == '*':
        if d1 == '0':
            return append_node_bin(dag, '*', v1, d2)
        elif d2 == '0':
            return append_node_bin(dag, '*', v2, d1)
        else:
            # a.v*b.d + b.v*a.d
            k1 = append_node_bin(dag, '*', v1, d2)
            k2 = append_node_bin(dag, '*', v2, d1)
            return append_node_bin(dag, '+', k1, k2)

    elif op == '/':
        if d1 == '0':
            # b.d * (- a.v/(b.v*b.v))
            k1 = append_node_bin(dag, '*', v2, v2)
            k2 = append_node_bin(dag, '/', v1, k1)
            k3 = append_node_bin(dag, '-', '0', k2)
            return append_node_bin(dag, '*', d2, k3)
        elif d2 == '0':
            return append_node_bin(dag, '/', d1, v2)
        else:
            # a.d / b.v + b.d * (- a.v/(b.v*b.v))
            k1 = append_node_bin(dag, '/', d1, v2)

            k2 = append_node_bin(dag, '*', v2, v2)
            k3 = append_node_bin(dag, '/', v1, k2)
            k4 = append_node_bin(dag, '-', '0', k3)
            k5 = append_node_bin(dag, '*', d2, k4)

            return append_node_bin(dag, '+', k1, k5)

    elif op == '^':
        # (n * a.v^(n-1)) * a.d
        n_ = dag[v2][1] - 1 # v2 should be an integer
        dag[str(n_)] = 'C', n_
        k1 = append_node_bin(dag, '^', v1, str(n_))
        k2 = append_node_bin(dag, '*', v2, k1)
        return append_node_bin(dag, '*', k2, d1)

    else:
        print("unsupported op: "+op)
        assert(False)


def append_diff_node_un(dag, op, v, d):
    if op == 'exp':
        # exp(v) * d
        k1 = append_node_un(dag, 'exp', v)
        return append_node_bin(dag, '*', k1, d)

    if op == 'log':
        # d / v
        return append_node_bin(dag, '/', d, v)

    if op == 'sqrt':
        # d / (2 * sqrt(v))
        k1 = append_node_un(dag, 'sqrt', v)
        k2 = append_node_bin(dag, '*', '2', k1)
        return append_node_bin(dag, '/', d, k2)

    elif op == 'sin':
        # cos(v) * d
        k1 = append_node_un(dag, 'cos', v)
        return append_node_bin(dag, '*', k1, d)

    elif op == 'cos':
        # -sin(v) * d
        k1 = append_node_un(dag, 'sin', v)
        k2 = append_node_bin(dag, '-', '0', k1)
        return append_node_bin(dag, '*', k2, d)

    elif op == 'tan':
        # d / (cos(v)*cos(v)
        k1 = append_node_un(dag, 'cos', v)
        k2 = append_node_bin(dag, '*', k1, k1)
        return append_node_bin(dag, '/', d, k2)

    elif op == 'asin':
        # d / sqrt( 1 - v*v )
        k1 = append_node_bin(dag, '*', v, v)
        k2 = append_node_bin(dag, '-', '1', k1)
        k3 = append_node_un(dag, 'sqrt', k2)
        return append_node_bin(dag, '/', d, k3)

    elif op == 'acos':
        # -d / sqrt( 1 - v*v )
        k1 = append_node_bin(dag, '-', '0', d)
        k2 = append_node_bin(dag, '*', v, v)
        k3 = append_node_bin(dag, '-', '1', k2)
        k4 = append_node_un(dag, 'sqrt', k3)
        return append_node_bin(dag, '/', k3, k4)

    elif op == 'atan':
        # d / sqrt( 1 + v*v )
        k1 = append_node_bin(dag, '*', v, v)
        k2 = append_node_bin(dag, '+', '1', k1)
        k3 = append_node_un(dag, 'sqrt', k2)
        return append_node_bin(dag, '/', d, k3)

    elif op == 'sinh':
        # cosh(v) * d
        k1 = append_node_un(dag, 'cosh', v)
        return append_node_bin(dag, '*', k1, d)

    elif op == 'cosh':
        # sinh(v) * d
        k1 = append_node_un(dag, 'sinh', v)
        return append_node_bin(dag, '*', k1, d)

    elif op == 'tanh':
        # d / (cosh(v)*cosh(v)
        k1 = append_node_un(dag, 'cosh', v)
        k2 = append_node_bin(dag, '*', k1, k1)
        return append_node_bin(dag, '/', d, k2)

    else:
        print("unsupported op: "+op)
        assert(False)


def cons_fun(dag, op, nl, nr):
    #if op == '==':
    #elif op == '>' or op == '>=':
    #elif op == '<' or op == '<=':

    n_id = append_node_bin(dag, '-', nl[0], nr[0])
    d_ids = tuple(map(
        lambda i: append_diff_node_bin(dag, '-', 
            nl[0], nl[1][i], nr[0], nr[1][i] ), 
        range(len(nl[1])) ))
    return n_id, d_ids

