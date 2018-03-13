# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from interval import interval, inf, imath
from .interval_utils import root, is_empty
from .contractor import Contractor


class HC4(Contractor):

    def __init__(self, dag, constr):
        super().__init__(dag)
        self.__constr = constr
        self.__fwd = {}
        self.__bwd = {}

    def __fwd_eval(self, n_id, box):
        n = self.dag[n_id]

        fwd = self.__fwd
        rec = self.__fwd_eval
    
        if n[0] == '+':
            rec(n[1], box)
            rec(n[2], box)
            fwd[n_id] = fwd[n[1]] + fwd[n[2]]
        elif n[0] == '-':
            rec(n[1], box)
            rec(n[2], box)
            fwd[n_id] = fwd[n[1]] - fwd[n[2]]
        elif n[0] == '*':
            rec(n[1], box)
            rec(n[2], box)
            fwd[n_id] = fwd[n[1]] * fwd[n[2]]
        elif n[0] == '/':
            rec(n[1], box)
            rec(n[2], box)
            fwd[n_id] = fwd[n[1]] / fwd[n[2]]
    
        elif n[0] == '^':
            rec(n[1], box)
            i = self.dag[n[2]][1]
            fwd[n_id] = fwd[n[1]] ** i
    
        elif n[0] == 'exp':
            rec(n[1], box)
            fwd[n_id] = imath.exp( fwd[n[1]] )
    
        elif n[0] == 'sqrt':
            rec(n[1], box)
            fwd[n_id] = imath.sqrt( fwd[n[1]] )
    
        elif n[0] == 'sin':
            rec(n[1], box)
            fwd[n_id] = imath.sin( fwd[n[1]] )
    
        elif n[0] == 'cos':
            rec(n[1], box)
            fwd[n_id] = imath.cos( fwd[n[1]] )
    
        elif n[0] == 'C':
            fwd[n_id] = interval[n[1]]
        elif n[0] == 'V':
            fwd[n_id] = box[n[1]]
        else:
            print('unsupported node: '+n)
            assert(False)


    def __bwd_propag(self, n_id, box):
        n = self.dag[n_id]

        fwd = self.__fwd
        bwd = self.__bwd
        rec = self.__bwd_propag

        if n[0] == '+':
            bwd[n[1]] = bwd[n_id] - fwd[n[2]]
            rec(n[1], box)
            bwd[n[2]] = bwd[n_id] - fwd[n[1]]
            rec(n[2], box)
    
        elif n[0] == '-':
            bwd[n[1]] = bwd[n_id] + fwd[n[2]]
            rec(n[1], box)
            bwd[n[2]] = fwd[n[1]] - bwd[n_id]
            rec(n[2], box)

        elif n[0] == '*':
            bwd[n[1]] = bwd[n_id] / fwd[n[2]]
            rec(n[1], box)
            bwd[n[2]] = bwd[n_id] / fwd[n[1]]
            rec(n[2], box)
    
        elif n[0] == '/':
            bwd[n[1]] = bwd[n_id] * fwd[n[2]]
            rec(n[1], box)
            bwd[n[2]] = fwd[n[1]] / bwd[n_id]
            rec(n[2], box)
    
        elif n[0] == '^':
            i = self.dag[n[2]][1]
    
            if i % 2 == 0:
                p = root(bwd[n_id], i)
                pp = p & fwd[n[1]]
                np = (-p) & fwd[n[1]]
                if is_empty(pp) or is_empty(np):
                    bwd[n[1]] = interval()
                else:
                    bwd[n[1]] = interval.hull([pp, np])
            else:
                bwd[n[1]] = root(bwd[n_id], i)
    
            rec(n[1], box)

        elif n[0] == 'sqrt':
            if is_empty(bwd[n_id]) or bwd[n_id][0].sup < 0:
                bwd[n[1]] = interval()
            elif bwd[n_id][0].inf < 0:
                i = interval([0, bwd[n_id][0].sup])
                bwd[n[1]] &= i*i
            else:
                bwd[n[1]] &= bwd[n_id] * bwd[n_id]

            assert(not is_empty(bwd[n[1]]))

        # TODO
        #elif n[0] == 'sin':

        elif n[0] == 'C':
            bwd[n_id] &= n[1]
        elif n[0] == 'V':
            box[n[1]] &= bwd[n_id]
    
        else:
            print('unsupported node: '+str(n))
            assert(False)


    def contract(self, box):
        op,l,r = self.__constr
        l = l[0]
        r = r[0]

        # forward propagation
        self.__fwd_eval(l, box)
        self.__fwd_eval(r, box)

        print('fwd:')
        print(self.__fwd)
        print()

        # backward propagation
        fwd = self.__fwd
        bwd = self.__bwd

        if op == '=':
            v = fwd[l] & fwd[r]
            bwd[l] = v
            self.__bwd_propag(l, box)
            bwd[r] = v
            self.__bwd_propag(r, box)
    
        elif op == '>' or op == '>=':
            v = interval.hull([fwd[r], interval[inf]]) 
            bwd[l] = fwd[l] & v
            self.__bwd_propag(l, box)
            v = interval.hull([interval[-inf], fwd[l]])
            bwd[r] = fwd[r] & v
            self.__bwd_propag(r, box)
    
        elif op == '<' or op == '<=':
            v = interval.hull([interval[-inf], fwd[r]]) 
            bwd[l] = fwd[l] & v
            self.__bwd_propag(l, box)
            v = interval.hull([fwd[l], interval[inf]])
            bwd[r] = fwd[r] & v
            self.__bwd_propag(r, box)
        
        print('bwd:')
        print(self.__bwd)
        print()

