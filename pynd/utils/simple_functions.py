from functools import reduce
import inspect
import numpy as np
import operator as op


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))

CHOOSE_CACHE = {}


def choose_using_cache(n, r):
    if n not in CHOOSE_CACHE:
        CHOOSE_CACHE[n] = {}
    if r not in CHOOSE_CACHE[n]:
        CHOOSE_CACHE[n][r] = choose(n, r, use_cache=False)
    return CHOOSE_CACHE[n][r]


def choose(n, r, use_cache=True):
    if use_cache:
        return choose_using_cache(n, r)
    if n < r:
        return 0
    if r == 0:
        return 1
    denom = reduce(op.mul, range(1, r + 1), 1)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    return numer // denom


def get_num_args(function):
    return len(get_parameters(function))


def get_parameters(function):
    return inspect.signature(function).parameters


def clip_in_place(array, min_val=None, max_val=None):
    if max_val is not None:
        array[array > max_val] = max_val
    if min_val is not None:
        array[array < min_val] = min_val
    return array


def fdiv(a, b, zero_over_zero_value=None):
    if zero_over_zero_value is not None:
        out = np.full_like(a, zero_over_zero_value)
        where = np.logical_or(a != 0, b != 0)
    else:
        out = None
        where = None

    return np.true_divide(a, b, out=out, where=where)


def binary_search(function,
                  target,
                  lower_bound,
                  upper_bound,
                  tolerance=1e-4):
    lh = lower_bound
    rh = upper_bound
    while abs(rh - lh) > tolerance:
        mh = np.mean([lh, rh])
        lx, mx, rx = [function(h) for h in (lh, mh, rh)]
        if lx == target:
            return lx
        if rx == target:
            return rx

        if lx <= target <= rx:
            if mx > target:
                rh = mh
            else:
                lh = mh
        elif lx > target > rx:
            lh, rh = rh, lh
        else:
            return None
    return mh


def remap(array, min_val, max_val):
    return [(((item - min(array) * (max_val - min_val)) / (max(array) - min(array)) + min_val for item in array]
