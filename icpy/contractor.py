from __future__ import print_function
import sys
from interval import interval, inf, imath
from .interval_utils import root

class Contractor:

    def __init__(self, dag, c_ids):
        self.dag = dag
        self.c_ids = c_ids

    def contract(box):
        pass


class Hc4revise(Contractor):

    def __init__(self, dag, c_ids):
        super().__init__(dag, c_ids)
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

        if n[0] == '==':
            v = fwd[n[1]] & fwd[n[2]]
            bwd[n[1]] = v
            rec(n[1], box)
            bwd[n[2]] = v
            rec(n[2], box)
    
        elif n[0] == '>' or n[0] == '>=':
            v = interval.hull([interval[-inf], fwd[n[1]]]) 
            v &= interval.hull([fwd[n[2]], interval[inf]])
            bwd[n[1]] = fwd[n[1]] & v
            rec(n[1], box)
            bwd[n[2]] = fwd[n[2]] & v
            rec(n[2], box)
    
        elif n[0] == '<' or n[0] == '<=':
            v = interval.hull([fwd[n[1]], interval[inf]]) 
            v &= interval.hull([interval[-inf], fwd[n[2]]])
            bwd[n[1]] = fwd[n[1]] & v
            rec(n[1], box)
            bwd[n[2]] = fwd[n[1]] & v
            rec(n[2], box)
    
        elif n[0] == '+':
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
                bwd[n[1]] = interval.hull([pp, np])
            else:
                bwd[n[1]] = root(bwd[n_id], i)
    
            rec(n[1], box)
    
        elif n[0] == 'C':
            bwd[n_id] &= n[1]
        elif n[0] == 'V':
            box[n[1]] &= bwd[n_id]
    
        else:
            print('unsupported node: '+str(n))
            assert(False)


    def contract(self, box):
        for c in self.c_ids:
            n = self.dag[c]
            self.__fwd_eval(n[1], box)
            self.__fwd_eval(n[2], box)
            print('fwd:')
            print(self.__fwd)
            print()
            
            self.__bwd_propag(c, box)
            print('bwd:')
            print(self.__bwd)
            print()

