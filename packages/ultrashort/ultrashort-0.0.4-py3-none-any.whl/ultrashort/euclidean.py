"""Routines for dealing with Euclidean vectors"""



import numpy as np
from numpy import asarray, arctan2, sqrt, cos, sin
from numpy.linalg import norm



def dim3_unit_vector_of(a):
    _a = asarray(a)
    _ndim = 3
    assert _a.ndim == 1 and _a.size == _ndim
    _theta3 = arctan2(norm(_a[:-1]), _a[-1])
    _phi = arctan2(_a[1], _a[0])
    _ua = np.empty((_ndim,))
    _ua[0] = sin(_theta3)*cos(_phi)
    _ua[1] = sin(_theta3)*sin(_phi)
    _ua[2] = cos(_theta3)
    return _ua



def dim4_unit_vector_of(a):
    _a = asarray(a)
    _ndim = 4
    assert _a.ndim == 1 and _a.size == _ndim
    _theta4 = arctan2(norm(_a[:-1]), _a[-1])
    _theta3 = arctan2(norm(_a[:-2]), _a[-2])
    _phi = arctan2(_a[1], _a[0])
    _ua = np.empty((_ndim,))
    _ua[0] = sin(_theta4)*sin(_theta3)*cos(_phi)
    _ua[1] = sin(_theta4)*sin(_theta3)*sin(_phi)
    _ua[2] = sin(_theta4)*cos(_theta3)
    _ua[3] = cos(_theta4)
    return _ua



def unit_vector_of(a):
    """
    # Arguments
    a : (N,...) array-like
    """
    _a = asarray(a)
    assert _a.ndim >= 1 and _a.shape[0] > 2
    _N = _a.shape[0]
    _N_theta = _N - 2
    _theta_arr = np.empty((_N_theta,)+_a.shape[1:])
    for _j in range(_N_theta):
        _theta_arr[_j,...] = arctan2(norm(_a[:-1-_j,...], axis=0), _a[-1-_j,...])
    _phi = arctan2(_a[1,...], _a[0,...])
    _sin_theta_arr = sin(_theta_arr)
    _ua = np.empty((_N,)+_a.shape[1:])
    _ua[0,...] = cos(_phi)*np.prod(_sin_theta_arr, axis=0)
    _ua[1,...] = sin(_phi)*np.prod(_sin_theta_arr, axis=0)
    for _j in range(_N_theta):
        _ua[2+_j,...] = cos(_theta_arr[-1-_j,...])*np.prod(_sin_theta_arr[:-1-_j,...], axis=0)
    return _ua

