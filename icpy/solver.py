# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from copy import deepcopy
from interval import interval
from .interval_utils import width
from .contractor_hull import HC4
from .contractor_newton import NewtonUni
from .contractor_box import BC3


def extract_stack(b_list):
    return b_list.pop()

def extract_queue(b_list):
    return b_list.popleft()

def extract_sorted(b_lise):
    pass


def select_bb(eps, box, vs, context):
    if 'last' not in context:
        context['last'] = 0
    else:
        context['last'] += 1
        context['last'] %= len(vs)
        
    if 'sp' not in context:
        context['sp'] = context['last']
    elif context['sp'] == context['last']:
        del context['sp']
        return None

    vn = vs[context['last']]
    if width(box[vn]) <= eps:
        return select_bb(eps, box, vs, context)
    else:
        del context['sp']
        return vn

def select_largest(eps, box, vs, context):
    pass


class Solver:
    '''Branch-and-prune solver.
    '''

    def __init__(self, vs, dag, cs, 
            eps=1e-12, 
            ext_fun=extract_stack, sel_fun=select_bb):
        self.__vs = vs
        self.__dag = dag
        self.__cs = cs
        self.__eps = eps
        self.__extract = ext_fun
        self.__select_var = sel_fun

    def __contract(self, box):
        for c in self.__cs:
            for i in range(len(self.__vs)):
                bc = BC3(self.__dag, c, self.__vs[i], i)
                bc.contract(box)
    
        #print('after BC3:')
        #print(box)
        #print()

        if box.is_empty():
            return
    
        #for c in self.__cs:
        #    hc = HC4(self.__dag, c)
        #    hc.contract(box)
    
        #print('after HC4:')
        #print(box)
        #print()


    def __split(self, v, box):
        i = box[v]
        b1 = box
        b1[v] = interval[i[0].inf, i.midpoint]
        b2 = deepcopy(box)
        b2[v] = interval[i.midpoint, i[0].sup]
        return b1, b2


    def __append(self, b_list, elem):
        b_list.append(elem)


    def solve(self, box):

        solutions = []
        undecided = [(box,{})]

        while (len(undecided) > 0):
            box,ctx = self.__extract(undecided)

            self.__contract(box)

            v = self.__select_var(self.__eps, box, self.__vs, ctx)

            if (v is None):
                if (not box.is_empty()):
                    solutions.append(box)
            else:
                b1,b2 = self.__split(v, box)
                self.__append(undecided, (b1,ctx))
                self.__append(undecided, (b2,deepcopy(ctx)))

        return solutions

