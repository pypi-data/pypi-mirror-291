from __future__ import annotations
import numpy as np
import numpy.typing as npt
from .. import Criteria
from dataclasses import dataclass


@dataclass
class Bounded(Criteria):
    """The bounded criteria downgrades for regions outside of bounds.
    A single downgrade is applied for each group of values outside the bounds.
    The ids correspond to the middle value in each group.
    The downgrade is the average distance from the bound multiplied by the ratio
    of the group width to the total width and by the average visibility of the group.
    """

    bound: float | list[float] = 0

    def get_errors(self, ids: npt.NDArray, data: npt.NDArray):
        raise Exception("Method not available in base class")

    def __call__(self, vs: npt.NDArray, limits=True):
        """each downgrade corresponds to a group of values outside the bounds, ids
        correspond to the last value in each case"""
        #sample = self.prepare(vs)
        ids = np.linspace(0, len(vs) - 1, len(vs)).astype(int)
        groups = np.concatenate([[0], np.diff(vs != 0).cumsum()])

        dgids = np.array(
            [
                ids[groups == grp][int(len(ids[groups == grp]) / 2)]
                for grp in set(groups)
            ]
        )
        errors = np.array([
            np.mean(vs[groups == grp]) * len(vs[groups == grp]) / len(vs)
            for grp in set(groups)
        ])
        dgs = self.lookup(errors, limits)

        return errors, dgs, dgids


@dataclass
class MaxBound(Bounded):
    """Downgrade values above the bound."""

    def prepare(self, data: npt.NDArray):
        oarr = np.zeros_like(data)
        oarr[data > self.bound] = data[data > self.bound] - self.bound
        return oarr


@dataclass
class MinBound(Bounded):
    """Downgrade values below the bound."""

    def prepare(self, data: npt.NDArray):
        oarr = np.zeros_like(data)
        oarr[data < self.bound] = self.bound - data[data < self.bound]
        return oarr


@dataclass
class OutsideBound(Bounded):
    """Downgrade values inside the bound."""

    def prepare(self, data: npt.NDArray):
        midbound = np.mean(self.bound)
        oarr = np.zeros_like(data)
        b1fail = (data >= midbound) & (data < self.bound[1])
        b0fail = (data < midbound) & (data > self.bound[0])
        oarr[b1fail] = self.bound[1] - data[b1fail]
        oarr[b0fail] = data[b0fail] - self.bound[0]
        return oarr


@dataclass
class InsideBound(Bounded):
    """Downgrade values outside the bound."""

    def prepare(self, data: npt.NDArray):
        oarr = np.zeros_like(data)
        oarr[data > self.bound[1]] = data[data > self.bound[1]] - self.bound[1]
        oarr[data < self.bound[0]] = self.bound[0] - data[data < self.bound[0]]
        return oarr
