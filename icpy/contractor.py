# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from interval import interval, inf, imath
from .interval_utils import root

class Contractor:

    def __init__(self, dag):
        self.dag = dag

    PROVED = 0
    UNKNOWN = 1
    NO_SOL = 2

    def contract(self, box):
        """Contracts a given box.

        Returns: PROVED, UNKNOWN or NO_SOL
        """
        pass

