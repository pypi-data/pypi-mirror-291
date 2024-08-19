"""ODE solver such as Runge-Kutta method"""

import numpy as np
from numpy import empty, asarray
from numba import njit

@njit
def rk4_complex(t0, y0, f, h, Nt, args=()):
    """
    # Arguments
    - f : callable
      f(t, y, *args) -> number
    - h : float or array of floats (Nt-1,), positive
      The temporal length per step.
    - Nt : int, > 1
      The number of time points.
      This routine propagate Nt-1 steps.
    """
    _y0 = asarray(y0, dtype=np.complex128)
    assert _y0.ndim >= 1

    h_arr = np.empty((Nt-1,), dtype=np.float64)
    h_arr[:] = h
    
    dim = _y0.shape[-1]
    t = empty((Nt,), dtype=np.float64)
    t[0] = t0
    y_shape = (Nt,) + _y0.shape
    y = empty(y_shape, dtype=np.complex128)
    y[0] = y0
    b_n = np.array([1/6,1/3,1/3,1/6], dtype=np.float64)
    k_mn_shape = _y0.shape + (b_n.size,)
    k_mn = np.empty(k_mn_shape, dtype=np.complex128)
    for it in range(Nt-1):
        _h = h_arr[it]
        k_mn[...,0] = f(t[it],y[it], *args)
        k_mn[...,1] = f(t[it]+0.5*_h, y[it]+0.5*_h*k_mn[...,0], *args)
        k_mn[...,2] = f(t[it]+0.5*_h, y[it]+0.5*_h*k_mn[...,1], *args)
        k_mn[...,3] = f(t[it]+_h, y[it]+_h*k_mn[...,2], *args)
        y[it+1] = y[it] + _h * np.sum(b_n * k_mn, axis=-1)
        t[it+1] = t[it] + _h
    return t, y
