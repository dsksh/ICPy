# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from interval import interval, inf, imath
from .contractor import Contractor
from .contractor_newton import NewtonUni, sample_inf, sample_sup
from .interval_utils import *
from .dag import cons_fun


class BC3(Contractor):

    def __init__(self, dag, constr, v_name, v_id):
        super().__init__(dag)
        self.__v_name = v_name
        self.__v_id = v_id

        op,l,r = constr 

        n,ds = cons_fun(dag, op, l, r)
        self.__newton = NewtonUni(dag, n, ds, v_name, v_id)
        self.__fun = self.__newton.fun

        self.__proj = interval()
        if op == '=':
            self.__proj = interval[0]
        elif op == '>' or op == '>=':
            self.__proj = interval[0, inf]
        elif op == '<' or op == '<=':
            self.__proj = interval[-inf, 0]


    def __is_consistent(self, box):
        #print('f: '+str(self.__fun.eval(box)))
        return not is_empty(self.__fun.eval(box) & self.__proj)

    def __is_consistent_l(self, box):
        # save
        dom = box[self.__v_name]

        l = slice_lower(dom)
        box[self.__v_name] = l
        res = self.__is_consistent(box)
        #print(str(res)+' at '+str(l))

        # restore
        box[self.__v_name] = dom
        return res

    def __is_consistent_u(self, box):
        dom = box[self.__v_name]
        u = slice_upper(dom)
        box[self.__v_name] = u
        res = self.__is_consistent(box)
        #print(str(res)+' at '+str(u))
        box[self.__v_name] = dom
        return res


    def __shrink_lower(self, box):
        self.__newton.sample_fun = sample_inf

        vn = self.__v_name
        old = box[vn]

        while True:
            self.__newton.contract(box)
            #print(box)

            if self.__is_consistent_l(box) or is_empty(box[vn]):
                # restore the ub
                box[vn] = interval.hull([box[vn], interval[old[0].sup]])
                return
            else:
                dom = box[vn]
                box[vn] = interval[dom[0].inf, dom.midpoint]

    def __shrink_upper(self, box):
        self.__newton.sample_fun = sample_sup

        vn = self.__v_name
        old = box[vn]

        while True:
            self.__newton.contract(box)
            #print(box)

            if self.__is_consistent_u(box) or is_empty(box[vn]):
                # restore the lb
                box[vn] = interval.hull([interval[old[0].inf, box[vn]]])
                return
            else:
                dom = box[vn]
                box[vn] = interval[dom.midpoint, dom[0].inf]


    def contract(self, box):
        vn = self.__v_name

        if not self.__is_consistent(box):
            box[vn] = interval()
            return 

        # shrink the lower bound
        if not self.__is_consistent_l(box):
            self.__shrink_lower(box)

        #print('after sl: '+str(box))

        if is_empty(box[vn]):
            return

        lb = box[vn][0].inf

        # shrink the upper bound
        if not self.__is_consistent_u(box):
            self.__shrink_upper(box)

        #print('after su: '+str(box))

