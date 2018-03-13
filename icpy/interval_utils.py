# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from interval import interval, inf, imath


def is_empty(x):
    return len(x) == 0

def width(x):
    if is_empty(x):
        return 0
    else:
        return x[0].sup - x[0].inf

def is_superset(x, v):
    return x[0].inf <= v and v <= x[0].sup

def is_strict_superset(x, v):
    return x[0].inf < v and v < x[0].sup


def ext_div(x, y):
    if is_strict_superset(y, 0):
        if x[0].inf > 0:
            xl = interval[x[0].inf]
            yl = interval[y[0].inf]
            yu = interval[y[0].sup]
            xl_yl = xl / yl
            xl_yu = xl / yu
            r1 = interval[-inf, xl_yl[0].sup]
            r2 = interval[xl_yu[0].inf, inf]
            return r1, r2

        elif x[0].sup < 0:
            xu = interval[x[0].sup]
            yl = interval[y[0].inf]
            yu = interval[y[0].sup]
            xu_yl = xu / yl
            xu_yu = xu / yu
            r1 = interval[-inf, xu_yu[0].sup]
            r2 = interval[xu_yl[0].inf, inf]
            return r1, r2

        else:
            return interval[-inf, inf], interval()

    else:
        return x / y, interval()

  
def pow(x, n):
    return imath.exp(n * imath.log(x))

def root(x, n):
    if is_empty(x):
        return x
    elif x[0].inf == 0 and x[0].sup == 0:
        return interval[0]
    elif n == 0:
        return interval[1]
    elif n < 0:
        return 1.0/root(x, -n)
    elif n == 1:
        return x;

    elif n%2 == 0:
        return pow(x, interval[1]/n)
    else:
        return pow(x, interval[1]/n) | (-pow(-x, interval[1]/n))


def slice_lower(x, eps=1e-8):
    if is_empty(x) or width(x) <= eps:
        return x

    b = max([-sys.float_info.max, x[0].inf]) + eps

    if not is_superset(x, b):
        return x
    else:
        return interval[x[0].inf, b]

def slice_upper(x, eps=1e-8):
    if is_empty(x) or width(x) <= eps:
        return x

    b = min([sys.float_info.max, x[0].sup]) - eps

    if not is_superset(x, b):
        return x
    else:
        return interval[b, x[0].sup]


