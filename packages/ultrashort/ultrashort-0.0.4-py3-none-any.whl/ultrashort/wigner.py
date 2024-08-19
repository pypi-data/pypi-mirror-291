"""Calculation of the Wigner function for a scalar function"""

import numpy as np
from numpy import asarray, pi, trapz, cos, empty, exp

def wigner(Nt, dt, w_arr, E_t):
    """Evaluate the Wigner function for real function `E_t`"""
    
    _Nt, _dt = Nt, dt
    _w_arr = asarray(w_arr)
    _Nw = _w_arr.size
    _E_t = asarray(E_t)
    
    _ds = 2 * _dt
    
    _Wigner_t_w = empty((_Nt,_Nw), dtype=np.float)

    for _iw in range(_Nw):
        _w = _w_arr[_iw]
        for _n in range(_Nt):
            _l_n = min([_n-0, (_Nt-1)-_n])
            _m_arr, = np.indices((_l_n,))
            _integrand = np.real(
                    np.conj(_E_t[_n+_m_arr]) * _E_t[_n-_m_arr] 
                    * exp(1.j*(_m_arr * _ds * _w))
                    )
            _Wigner_t_w[_n,_iw] = (1./pi) * trapz(_integrand, dx=_ds)
            
    return _Wigner_t_w




def wigner_EE(Nt, dt, Et, return_s_arr=False):
    """
    Evaluate E^*(t+s/2) E(t-s/2), 
    a part of integrand of the Wigner function for real valued function
    """
    
    _Nt, _dt = int(Nt), float(dt)
    assert _Nt == Nt and _dt == dt
    _Et = np.asarray(Et)
    assert _Et.ndim == 1
    
    _Ns = _Nt // 2 + _Nt % 2
    _ds = 2 * _dt

    _s_arr = np.arange(_Ns) * _ds
    
    # Assumes fEt is zero outside range of t_arr
    _EE = np.zeros((_Nt,_Ns), dtype=np.float) # `np.float` type for real signal
    
    for _it in range(_Nt):
        _Ns_it = min([_it,(_Nt-1)-_it]) + 1
        _idx_s_arr, = np.indices((_Ns_it,))
        _EE[_it,_idx_s_arr] = np.conj(_Et)[_it-_idx_s_arr] * _Et[_it+_idx_s_arr]    
        
    _out = (_EE, _s_arr) if return_s_arr else _EE
    return _out




def wigner_dist_for_real_func(Nt, dt, Et, omega_arr):
    """
    Evaluate Wigner function for real function
    """
    
    #### Process input parameters
    _Nt, _dt = int(Nt), float(dt)
    assert _Nt == Nt and _dt == dt
    _Et = np.asarray(Et)
    assert _Et.ndim == 1
    _omega_arr = np.asarray(omega_arr)
    assert _omega_arr.ndim == 1
    _Nomega = _omega_arr.shape[-1]
    
    
    #### Evaluate integrand (except exp(iws))
    _EE, _s_arr = wigner_EE(_Nt, _dt, _Et, return_s_arr=True)
    
    
    #### Evaluate Wigner distribution function
    _ds = 2 * dt
    assert _ds == (_s_arr[1] - _s_arr[0])
    
    _wd = np.empty((_Nt, _Nomega), dtype=np.float)
    for _i_omega, _omega in enumerate(_omega_arr):
         _wd[:,_i_omega] = (1./pi) * np.trapz(
                 _EE * np.cos(_omega * _s_arr), dx=_ds, axis=-1)
    
    return _wd



