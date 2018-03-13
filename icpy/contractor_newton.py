# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from interval import interval, inf, imath
from .contractor import Contractor
from .interval_utils import is_empty, is_superset, ext_div


class Function():

    def __init__(self, dag, n_id, d_ids):
        self.__dag = dag
        self.__n_id = n_id
        self.__d_ids = d_ids


    def __eval(self, n_id, box):
        n = self.__dag[n_id]

        rec = self.__eval
    
        if n[0] == '+':
            v1 = rec(n[1], box)
            v2 = rec(n[2], box)
            return v1 + v2
        elif n[0] == '-':
            v1 = rec(n[1], box)
            v2 = rec(n[2], box)
            return v1 - v2
        elif n[0] == '*':
            v1 = rec(n[1], box)
            v2 = rec(n[2], box)
            return v1 * v2
        elif n[0] == '/':
            v1 = rec(n[1], box)
            v2 = rec(n[2], box)
            return v1 / v2
   
        elif n[0] == '^':
            v = rec(n[1], box)
            i = self.__dag[n[2]][1]
            return v ** i
    
        elif n[0] == 'exp':
            v = rec(n[1], box)
            return imath.exp(v)
    
        elif n[0] == 'log':
            v = rec(n[1], box)
            return imath.log(v)
    
        elif n[0] == 'sqrt':
            v = rec(n[1], box)
            return imath.sqrt(v)
    
        elif n[0] == 'sin':
            v = rec(n[1], box)
            return imath.sin(v)
    
        elif n[0] == 'cos':
            v = rec(n[1], box)
            return imath.cos(v)
    
        elif n[0] == 'tan':
            v = rec(n[1], box)
            return imath.tan(v)
    
        elif n[0] == 'asin':
            v = rec(n[1], box)
            return imath.asin(v)
    
        elif n[0] == 'acos':
            v = rec(n[1], box)
            return imath.acos(v)
    
        elif n[0] == 'atan':
            v = rec(n[1], box)
            return imath.atan(v)
    
        elif n[0] == 'sinh':
            v = rec(n[1], box)
            return imath.sinh(v)
    
        elif n[0] == 'cosh':
            v = rec(n[1], box)
            return imath.cosh(v)
    
        elif n[0] == 'tanh':
            v = rec(n[1], box)
            return imath.tanh(v)
    
        elif n[0] == 'C':
            return interval[n[1]]
        elif n[0] == 'V':
            return box[n[1]]
        else:
            print('unsupported node: '+str(n))
            assert(False)


    def eval(self, box):
        return self.__eval(self.__n_id, box)

    def d_eval(self, v_id, box):
        #print('d_eval: '+str(self.__dag))
        #print('d w/ '+str(v_id)+', '+self.__d_ids[v_id])
        return self.__eval(self.__d_ids[v_id], box)


def sample_mp(x):
    return x.midpoint

def sample_inf(x):
    return max([x[0].inf, -inf])

def sample_sup(x):
    return min([x[0].sup, inf])


class NewtonUni(Contractor):

    def __init__(self, dag, n_id, d_ids, v_name, v_id, sample_fun=sample_mp):
        super().__init__(dag)
        self.fun = Function(dag, n_id, d_ids)
        self.__v_name = v_name
        self.__v_id = v_id
        self.sample_fun = sample_fun


    def __step(self, box):

        dom = box[self.__v_name]

        f = self.fun.eval(box)
        #print('f: '+str(f))
        if is_empty(f) or not is_superset(f, 0):
            return interval()

        df = self.fun.d_eval(self.__v_id, box)
        #print('df: '+str(df))
        if is_empty(df):
            return interval()

        c = self.sample_fun(box[self.__v_name])
        # TODO
        box[self.__v_name] = interval[c]
        fc = self.fun.eval(box)
        #print('fc: '+str(fc))
        box[self.__v_name] = dom
        
        l,r = ext_div(fc, df)
        #print('l: '+str(l)+', r: '+str(r))
        l = c - l
        r = c - r
        l &= dom
        r &= dom

        if is_empty(l):
            return r
        else:
            return interval.hull([l, r])


    def contract(self, box):

        vn = self.__v_name

        while True:
            old = box[vn]
            box[vn] = self.__step(box)
            if box[vn] == old or box.is_empty():
                break

