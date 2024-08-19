"""Routines for fourier transform"""

import numpy as np
from numpy import pi, exp, arange, asarray
# from numpy.fft import rfft, rfftfreq
from scipy.fft import rfft, rfftfreq, irfft
from numbers import Integral, Real



def number_of_freq_for_real_func_fourier_transform(Nt):
    """
    Return the number of frequencies that the fourier transform 
    of a real function with the number of temporal points `Nt` would have.

    Parameters
    ----------
    Nt : positive integer
    """
    assert isinstance(Nt, Integral)
    _N = Nt
    # _N_nonneg = (_N+(_N % 2)) // 2 + ((_N+1) % 2)
    _N_nonneg = _N//2 + 1
    return _N_nonneg


def ang_freq_array_for_fourier_transform_of_real_func(Nt, dt):
    """
    Return an array of angular frequencies for a discrete Fourier transform of 
    an array of real-valued function values defined on a discrete time values.

    Parameters
    ----------
    Nt : positive integer
        the number of sample points
    dt : positive float
        sampling interval
    """
    assert isinstance(Nt, Integral) and Nt > 0
    assert isinstance(dt, Real) and dt > 0
    _N, _dt = Nt, dt
    _omega_arr = 2.* pi * rfftfreq(_N, _dt)
    return _omega_arr



def real_ft_to_fomega(ft, t0, dt, with_omega_arr=False):
    """Evaluate a discrete Fourier transform of a real input."""

    _ft = asarray(ft)
    _N = _ft.size
    assert isinstance(t0, Real) and isinstance(dt, Real)
    assert _N > 1 and dt > 0.

    _N_nonneg = number_of_freq_for_real_func_fourier_transform(_N)
    _delta_omega = 2.*pi/(_N*dt)
    _fomega = rfft(_ft) * exp((-1.j *_delta_omega *t0) *arange(_N_nonneg)) *dt

    if with_omega_arr:
        _omega_arr = ang_freq_array_for_fourier_transform_of_real_func(_N, dt)
        return _fomega, _omega_arr
    else:
        return _fomega




# from scipy.fft import irfft
# from numpy import asarray, arange, pi, exp

def fomega_to_real_ft(fomega, t0, dt, Nt):
    """
    Inverse discrete Fourier transform into real function 
    with `scipy.fft.irfft`
    """
    
    _fomega = asarray(fomega)
    assert _fomega.ndim == 1
    _t0, _dt, _Nt = float(t0), float(dt), int(Nt)
    assert _t0 == t0 and _dt == dt and _Nt == Nt
    
    _Nomega = _fomega.size
    _domega = 2.*pi/(_Nt*_dt)
    _phase = exp(1.j*arange(_Nomega)*_domega*_t0)
    _ft = 1/_dt * irfft(fomega * _phase, n=_Nt)
    
    return _ft





#from numpy import exp, asarray

def _fourier_transform_of_sine_decaying_from_t0(
        omega, t0, f_at_t0, dtdf_at_t0, decay_const):
    """
    Evaluate a Fourier transform of a sine function, 
    decaying from time t0 and before which was zero.
    
    Notes
    -----
    This routine was designed for evaluating the Fourier transform
    of a signal interval-by-interval which has this decaying sine signal 
    starting from a time point to positive infinity.
    
    Parameter
    ---------
    omega: float or (N,) array-like
    t0: float
    f_at_t0: float
    dtdf_at_t0: float
    decay_const: float, positive
    """
    _omega = asarray(omega)
    assert decay_const > 0
    _f_omega = exp(-1.j*_omega*t0) \
    * ( (decay_const + 1.j*_omega)*f_at_t0 + dtdf_at_t0 ) \
    / ( decay_const**2 - (_omega-1)*(_omega+1) + 2.j*decay_const*_omega )
    return _f_omega





# from numpy import asarray

def fourier_transform_part_by_part_for_short_signal_with_decaying_sine(
    ft, t0, dt, ti_near, tf_near, decay_const, return_each_part=False, 
    zero_rtol=1e-5, zero_atol=1e-4):
    """
    Evaluate a Fourier transform part-by-part of a short signal with following 
    sine function extended to infinity with its tail decaying to zero.
    
    Parameters
    ----------
    ...
    ti_near: float
    tf_near: float
        ti_near and tf_near are replaced by nearest time points, 
        which are consistent with given `t0` and `dt`
    """
    assert dt > 0 and t0 < ti_near and ti_near < tf_near and decay_const > 0
    _dt, _t0 = float(dt), float(t0)
    _ti_near, _tf_near = float(ti_near), float(tf_near)
    _decay_const = float(decay_const)
    _ft = asarray(ft)
    assert _ft.ndim == 1
    
    ########## Devide the whole timeline into three parts
    
    _ti_index,_tf_index = (int((_tt -_t0) / dt) for _tt in [_ti_near,_tf_near])
    _ti, _tf = (_t0 + _index * _dt for _index in [_ti_index, _tf_index])
    
    _ft_part1 = _ft[:_ti_index]
    _ft_part2 = _ft[_ti_index:_tf_index]
    _ft_part3 = _ft[_tf_index:]
    
    ########## Check whether the part 1 indeed almost zero
    
    assert np.allclose(_ft_part1, 0, rtol=zero_rtol, atol=zero_atol)

    ########## Fourier transform of part 2 using the Fast Fourier Transform
    
    _fomega_part2, _nonneg_omega_arr = real_ft_to_fomega(
        _ft_part2, _ti, _dt, with_omega_arr=True)
    
    ########## Fourier transform of part 3 using analytical expression
    
    _f_at_tf = _ft[_tf_index]
    # second-order finite difference approximation
    _dtdf_at_tf = (_ft[_tf_index+1] - _ft[_tf_index-1]) / (2*_dt)  

    _fomega_part3 = _fourier_transform_of_sine_decaying_from_t0(
        _nonneg_omega_arr, _tf, _f_at_tf, _dtdf_at_tf, _decay_const)
    
    ########## Fourier transform of total signal

    _fomega = _fomega_part2 + _fomega_part3
    
    ########## Return results

    if return_each_part:
        return _fomega, _nonneg_omega_arr, _fomega_part2, _fomega_part3
    else: return _fomega, _nonneg_omega_arr




from numpy import exp, asarray, pi
from ultrashort.fourier import real_ft_to_fomega
from ultrashort.fourier import ang_freq_array_for_fourier_transform_of_real_func

def husimi_fft(w, t0, dt, f_t, sigma):
    _sig = sigma
    _f = asarray(f_t)
    _Nt = _f.size
    _dt = dt
    _win_tot = exp(-(np.arange(-(_Nt-1), _Nt) * _dt / (2**0.5 * _sig) )**2) \
            * (1./(2*pi*_sig)**0.5)
    _t0 = t0
    
    _w_arr = ang_freq_array_for_fourier_transform_of_real_func(_Nt, _dt)
    _Nw = _w_arr.size
    _husimi_t_w = np.empty((_Nt,_Nw), dtype=np.complex)
    
#     _t = _t0 + np.arange(_Nt) * _dt
    for _it in range(_Nt):
        _win = _win_tot[_Nt-1-_it:2*_Nt-1-_it]
        
        _t = _t0 + _it * _dt
        _husimi_t_w[_it,:] = real_ft_to_fomega(
                _win * _f, _t0, _dt, with_omega_arr=False)
    
    return _husimi_t_w, _w_arr



def husimi(w, t0, dt, f_t, sigma, Nt_eval_interval=1):
    _sig = sigma
    _f = asarray(f_t)
    _Nt = _f.size

    _Ntau = int((_Nt + (Nt_eval_interval-1)) / Nt_eval_interval)
    _dt = dt
    _win_tot = exp(-(np.arange(-(_Nt-1), _Nt) * _dt / (2**0.5 * _sig) )**2) \
            * (1./(2*pi*_sig)**0.5)
    _t0 = t0
    
    _w = asarray(w)
    _Nw = _w.size
    _husimi_t_w = np.empty((_Ntau,_Nw), dtype=np.complex)
    
    _t = _t0 + np.arange(_Nt) * _dt
    for _itau in range(_Ntau):
        _tau = _t0 + _itau * (_dt * Nt_eval_interval)
        _it = _itau * Nt_eval_interval
        for _iw in range(_Nw):
            _win = _win_tot[_Nt-1-_it:2*_Nt-1-_it]
            _integrand = _win * _f * exp(-1.j*_w[_iw]*(_t - _tau))
            _husimi_t_w[_itau,_iw] = np.trapz(_integrand, dx=_dt)
    
    return _husimi_t_w



