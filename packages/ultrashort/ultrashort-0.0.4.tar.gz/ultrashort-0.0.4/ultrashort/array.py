"""A toolset for array manipulation"""

import numpy as np
from numpy import asarray, cumsum

def get_left_index_of_val(val, arr):
    _arr, _val = asarray(arr), val
    _below_zero = (_arr - _val) < 0
    _indice_of_true_to_false, = np.nonzero(
        np.logical_xor(_below_zero[:-1], _below_zero[1:]))
    assert _indice_of_true_to_false.size == 1
    _index_of_zero_to_nonzero = _indice_of_true_to_false[0]
    return _index_of_zero_to_nonzero




def equidistanced_arr_with_upper_limit_of_spacing(
        t_start, t_end, upper_bound_of_dt):
    """
    Construct an array of equal spacing `dt` 
    whose upper bound is given by `upper_bound_of_dt`
    """
    assert t_start < t_end and upper_bound_of_dt > 0
    total_duration = t_end - t_start
    Nt = int(total_duration / upper_bound_of_dt + 2)
    t_arr = np.linspace(t_start, t_end, Nt)
    return t_arr


def add_mid_points(arr):
    """Insert middle points to given array"""
    _arr = np.asarray(arr)
    assert _arr.ndim == 1
    _N_aug = _arr.size * 2 - 1
    _arr_aug = np.empty((_N_aug,))
    _arr_aug[::2] = _arr
    _arr_aug[1::2] = 0.5 * (_arr[:-1] + _arr[1:])
    return _arr_aug





def accum_integral(ft, dt=None, t=None):
    """Evaluate accumated integral of given array `ft`
    
    ft : real or complex-valued array, (...,N) with N >= 2.
    dt : float, positive.
    t : array of real numbers at which `ft` is defined.
    """
    _ft = asarray(ft)
    assert _ft.ndim >= 1 and _ft.shape[-1] > 1
    N = _ft.shape[-1]
    _dt = None
    if dt is not None:
        _dt = float(dt)
        assert _dt > 0
    elif t is not None:
        _t = asarray(t)
        assert _t.shape == (N,)
        _dt = np.diff(_t)
    else: raise ValueError("The argument `dt` and `t` cannot be None simultaneouly.")
    assert _dt is not None
    
    _accum_ft = np.empty_like(_ft)
    _accum_ft[...,0] = 0
    _accum_ft[...,1:] = (_ft[...,1:]+_ft[...,:-1])*(0.5*_dt)
    _accum_ft[:] = cumsum(_accum_ft, axis=-1)
    
    return _accum_ft



def is_unitary(U, thres=1e-14):
    """
    # Arguments
    - U : array-like (...,N,N)
    """
    _U = asarray(U)
    assert _U.ndim >= 2
    N = _U.shape[-1]
    assert _U.shape[-2] == N
    _U_dagger = np.einsum('...jk->...kj', _U.conj())
    _U_dagger_U = np.einsum('...jk,...kl->...jl', _U_dagger, _U)
    err_max = np.abs(_U_dagger_U - np.eye(N)).max()
    return err_max < thres


