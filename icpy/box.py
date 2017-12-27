# -*- coding: utf-8 -*-

import sys
from copy import copy, deepcopy
from interval import interval
from functools import reduce
from .interval_utils import is_empty, width

class Box:
    """The interface for box implementations.
    """

    def __getitem__(self, vn): # box[varname] operator
        pass

    def __setitem__(self, vn, value): # box[varname] = value
        pass

    def __len__(self):
        pass

    def width(self):
        pass

    def is_empty(self):
        pass


class IntervalDict(Box):

    def __init__(self, vd):
        self.__value = vd

    def __copy__(self):
        return IntervalDict(self.__value)

    def __deepcopy__(self, memo):
        vd = deepcopy(self.__value, memo)
        return IntervalDict(vd)

    def __getitem__(self, vn):
        return self.__value[vn]

    def __setitem__(self, vn, value):
        self.__value[vn] = value

    def __len__(self):
        return len(self.__value)

    def width(self):
        w = 0
        for i in self.__value.values():
            w_ = width(i)
            if w_ > w:
                w = w_
        return w

    def __str__(self):
        return "box"+str(self.__value)

    def is_empty(self):
        if len(self) == 0:
            return True
        for i in self.__value.values():
            if is_empty(i):
                return True
        return False


class IntervalList(Box):

    def __init__(self, vd, ilist=None):
        if ilist is None:
            self.__init_from_dict(vd)
        else:
            self.__scope = vd
            self.__value = ilist

    def __init_from_dict(self, vd):
        # create a map from a vn to an index
        self.__scope = {}
        for i in range(len(vd.keys())):
            self.__scope[list(vd.keys())[i]] = i

        # value is a list of intervals
        self.__value = list(vd.values())

    def __copy__(self):
        return IntervalList(self.__scope, self.__value)

    def __deepcopy__(self, memo):
        box = deepcopy(self.__value, memo)
        # scope is shared
        return IntervalList(self.__scope, box)

    def __getitem__(self, vn):
        return self.__value[self.__scope[vn]]

    def __setitem__(self, vn, value):
        if vn not in self.__scope:
            self.__scope[vn] = len(self.__scope)
            self.__value.append(value)
        else:
            self.__value[self.__scope[vn]] = value

    def __len__(self):
        return len(self.__value)

    def width(self):
        w = 0
        for i in self.__value:
            w_ = width(i)
            if w_ > w:
                w = w_
        return w

    def __str__(self):
        ss = list(map(lambda vn: "'"+vn+"': "+str(self[vn]), self.__scope))
        s = ''
        if len(ss) >= 1:
            s = reduce(lambda s1, s2: s1+', '+s2, ss[1:], ss[0])
        return 'box{'+s+'}'

    def is_empty(self):
        if len(self) == 0:
            return True
        for i in self.__value:
            if is_empty(i):
                return True
        return False
