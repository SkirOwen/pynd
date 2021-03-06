from functools import reduce
import copy
import itertools as it
import operator as op
import os
import random
import sys

import numpy as np

import pynd.constants as consts
from pynd.constants import *
from pynd.container.container import Container
from pynd.utils.iterables import list_update
from pynd.utils.iterables import remove_list_redundancies
from pynd.utils.simple_functions import get_parameters


class Dobject(Container):
    CONFIG = {
        "name": None,
    }

    def __init__(self, **kwargs):
        Container.__init__(self, **kwargs)
        self.subdobjects = []
        if self.name is None:
            self.name = self.__class__.__name__

    def __str__(self):
        return str(self.name)

    def add(self, *dobjects):
        if self in dobjects:
            raise Exception("Dobject cannot contain self")
        self.subdobjects = list_update(self.subdobjects, dobjects)
        return self

    def add_to_back(self, *dobjects):
        self.remove(*dobjects)
        self.subdobjects = list(dobjects) + self.subdobjects
        return self

    def remove(self, *dobjects):
        for dobject in dobjects:
            if dobject in self.subdobjects:
                self.subdobjects.remove(dobject)
        return self

    def digest_dobject_attrs(self):
        """
        Ensures all attributes which are dobjects are included
        in the subdobjects list.
        """
        dobject_attrs = [x for x in list(self.__dict__.values()) if isinstance(x, Dobject)]
        self.subdobjects = list_update(self.subdobjects, dobject_attrs)
        return self

    # # Display
    #
    # def copy(self):
    #     # TODO, either justify reason for shallow copy, or
    #     # remove this redundancy everywhere
    #     # return self.deepcopy()
    #
    #     # TODO: Change for dobject
    #
    #     copy_mobject = copy.copy(self)
    #     copy_mobject.points = np.array(self.points)
    #     copy_mobject.submobjects = [
    #         submob.copy() for submob in self.submobjects
    #     ]
    #     copy_mobject.updaters = list(self.updaters)
    #     family = self.get_family()
    #     for attr, value in list(self.__dict__.items()):
    #         if isinstance(value, Dobject) and value in family and value is not self:
    #             setattr(copy_mobject, attr, value.copy())
    #         if isinstance(value, np.ndarray):
    #             setattr(copy_mobject, attr, np.array(value))
    #     return copy_mobject
    #
    # def deepcopy(self):
    #     return copy.deepcopy(self)
    #
    # ##
    #
    # def save_state(self, use_deepcopy=False):
    #     if hasattr(self, "saved_state"):
    #         # Prevent exponential growth of data
    #         self.save_state = None
    #     if use_deepcopy:
    #         self.save_state = self.deepcopy()
    #     else:
    #         self.save_state = self.copy()
    #     return self
    #
    # def restore(self):
    #     if not hasattr(self, "saved_state") or self.save_state is None:
    #         raise Exception("Trying to restore without having saved")
    #     self.become(self.saved_state)
    #     return self
    #
    # ##
    #
    # def become(self):
    #     pass


class Group(Dobject):
    def __init__(self, *dobjects, **kwargs):
        if not all([isinstance(d, Dobject) for d in dobjects]):
            raise Exception("All subdojects must be of type Dobject")
        Dobject.__init__(self, **kwargs)
        self.add(*dobjects)
