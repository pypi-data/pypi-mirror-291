"""A set of 'special' functions"""

import numpy as np
from numpy import exp, asarray, pi
from scipy.special import hyp1f1

def sinhc(x):
    _x = asarray(x)
    return exp(-_x)*hyp1f1(1,2,2*_x)

def sinc(x):
    return np.sinc(x / pi)
