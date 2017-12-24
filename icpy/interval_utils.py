# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from interval import interval, inf, imath

def pow(x, n):
    return imath.exp(n * imath.log(x))

def root(x, n):
    if len(x) == 0: # null interval
        return x
    if x[0].inf == 0 and x[0].sup == 0:
        return interval[0]
    if n == 0:
        return interval[1]
    if n < 0:
        return 1.0/root(x, -n)
    if n==1:
        return x;

    if n%2 == 0:
        return pow(x, interval[1]/n)
    else:
        return pow(x, interval[1]/n) | (-pow(-x, interval[1]/n))

