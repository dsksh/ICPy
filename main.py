from __future__ import print_function
import sys
from copy import deepcopy
from interval import interval, inf, imath
from csp_parser import CspParser
from csp_semantics import CspSemantics

def root(x, n):
    if len(x) == 0:
        return x
    if x[0].inf == 0 and x[0].sup == 0:
        return interval[0]
    if n == 0:
        return interval[1]
    if n < 0:
        return 1.0/root(x, -n)
    if n==1:
        return x;

    # TODO: interval pow function
    #if n%2 == 0:
    #    return pow(x, interval[1]/n)
    #else:
    #    return pow(x, interval[1]/n) | (-pow(-x, interval[1]/n))

    # FIXME
    return x

###

def fwd_eval(dictio, constr, box, fwd):
    n = dictio[constr]

    if n[0] == '+':
        fwd_eval(dictio, n[1], box, fwd)
        fwd_eval(dictio, n[2], box, fwd)
        fwd[constr] = fwd[n[1]] + fwd[n[2]]
    elif n[0] == '-':
        fwd_eval(dictio, n[1], box, fwd)
        fwd_eval(dictio, n[2], box, fwd)
        fwd[constr] = fwd[n[1]] - fwd[n[2]]
    elif n[0] == '*':
        fwd_eval(dictio, n[1], box, fwd)
        fwd_eval(dictio, n[2], box, fwd)
        fwd[constr] = fwd[n[1]] * fwd[n[2]]
    elif n[0] == '/':
        fwd_eval(dictio, n[1], box, fwd)
        fwd_eval(dictio, n[2], box, fwd)
        fwd[constr] = fwd[n[1]] / fwd[n[2]]

    elif n[0] == '^':
        fwd_eval(dictio, n[1], box, fwd)
        i = dictio[n[2]][1]
        fwd[constr] = fwd[n[1]] ** i

    elif n[0] == 'C':
        fwd[constr] = interval[n[1]]
    elif n[0] == 'V':
        fwd[constr] = box[n[1]]
    else:
        print('unsupported node: '+n)
        assert(False)

def bwd_propag(dictio, constr, box, fwd, bwd):
    n = dictio[constr]
    if n[0] == '==':
        v = fwd[n[1]] & fwd[n[2]]
        bwd[n[1]] = v
        bwd_propag(dictio, n[1], box, fwd, bwd)
        bwd[n[2]] = v
        bwd_propag(dictio, n[2], box, fwd, bwd)

    elif n[0] == '>' or n[0] == '>=':
        v = interval.hull([interval[-inf], fwd[n[1]]]) 
        v &= interval.hull([fwd[n[2]], interval[inf]])
        bwd[n[1]] = fwd[n[1]] & v
        bwd_propag(dictio, n[1], box, fwd, bwd)
        bwd[n[2]] = fwd[n[2]] & v
        bwd_propag(dictio, n[2], box, fwd, bwd)

    elif n[0] == '<' or n[0] == '<=':
        v = interval.hull([fwd[n[1]], interval[inf]]) 
        v &= interval.hull([interval[-inf], fwd[n[2]]])
        bwd[n[1]] = fwd[n[1]] & v
        bwd_propag(dictio, n[1], box, fwd, bwd)
        bwd[n[2]] = fwd[n[1]] & v
        bwd_propag(dictio, n[2], box, fwd, bwd)

    elif n[0] == '+':
        bwd[n[1]] = bwd[constr] - fwd[n[2]]
        bwd_propag(dictio, n[1], box, fwd, bwd)
        bwd[n[2]] = bwd[constr] - fwd[n[1]]
        bwd_propag(dictio, n[2], box, fwd, bwd)

    elif n[0] == '-':
        bwd[n[1]] = bwd[constr] + fwd[n[2]]
        bwd_propag(dictio, n[1], box, fwd, bwd)
        bwd[n[2]] = fwd[n[1]] - bwd[constr] 
        bwd_propag(dictio, n[2], box, fwd, bwd)

    elif n[0] == '*':
        bwd[n[1]] = bwd[constr] / fwd[n[2]]
        bwd_propag(dictio, n[1], box, fwd, bwd)
        bwd[n[2]] = bwd[constr] / fwd[n[1]]
        bwd_propag(dictio, n[2], box, fwd, bwd)

    elif n[0] == '/':
        bwd[n[1]] = bwd[constr] * fwd[n[2]]
        bwd_propag(dictio, n[1], box, fwd, bwd)
        bwd[n[2]] = fwd[n[1]] / bwd[constr]
        bwd_propag(dictio, n[2], box, fwd, bwd)

    elif n[0] == '^':
        i = dictio[n[2]][1]

        if i % 2 == 0:
            # TODO
            #p = fwd[n[1]].newton(lambda x: x**i, lambda x: i*x**(i-1))
            p = root(bwd[constr], i)
            pp = p & fwd[n[1]]
            np = (-p) & fwd[n[1]]
            bwd[n[1]] = interval.hull([pp, np])
        else:
            #bwd[n[1]] = fwd[n[1]].newton(lambda x: x**i, lambda x: i* x**(i-1))
            bwd[n[1]] = root(bwd[constr], i)
        print(bwd[n[1]])

        bwd_propag(dictio, n[1], box, fwd, bwd)

    elif n[0] == 'C':
        bwd[constr] &= n[1]
    elif n[0] == 'V':
        bwd[constr] &= n[2]
        box[n[1]] = bwd[constr]

    else:
        print('unsupported node: '+str(n))
        assert(False)

def hc4revise(dictio, constr, box):
    fwd = {}
    n = dictio[constr]
    fwd_eval(dictio, n[1], box, fwd)
    fwd_eval(dictio, n[2], box, fwd)
    #print('fwd:')
    #print(fwd)
    #print()
    
    bwd = {}
    bwd_propag(dictio, constr, box, fwd, bwd)
    #print('bwd:')
    #print(bwd)
    #print()
    
def parse_and_solve(csp):
    parser = CspParser(semantics = CspSemantics())
    vs, (cd, cs) = parser.parse(csp)

    # set variable nodes
    for v in vs.keys():
        cd[v] = vs[v]

    box = {}
    for v in vs.keys():
        box[v] = vs[v][2]

    for c in cs:
        hc4revise(cd, c, box)

    return box


if __name__ == '__main__':
    csp = open(sys.argv[1]).read()
    print(csp.strip())
    print()

    result = parse_and_solve(csp)
    print(result)
    #print(result[1])
    #print(result[2])

