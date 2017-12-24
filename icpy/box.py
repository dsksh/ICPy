# -*- coding: utf-8 -*-

import sys
from copy import copy, deepcopy
from interval import interval
from functools import reduce

class Box:
    """The interface for box implementations.
    """

    def __getitem__(self, vn): # box[varname] operator
        pass

    def __setitem__(self, vn, value): # box[varname] = value
        pass

    def __len__(self):
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

    def __str__(self):
        return "box"+str(self.__value)


class IntervalList(Box):

    def __init__(self, vd, box=None):
        if box is None:
            self.__init_from_dict(vd)
        else:
            self.__scope = vd
            self.__value = box

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
        self.__value[self.__scope[vn]] = value

    def __len__(self):
        return len(self.__value)

    def __str__(self):
        ss = map(lambda vn: "'"+vn+"': "+str(self[vn]), self.__scope)
        return 'box{'+reduce(lambda s1, s2: s1+', '+s2, ss)+'}'

