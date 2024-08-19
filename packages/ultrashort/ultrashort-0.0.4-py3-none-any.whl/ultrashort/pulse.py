"""A collection of pulse shapes"""

from numpy import pi, cos, exp, square, asarray, logical_and
from numba import njit



# from numpy import asarray, logical_and

def pulse_shape_half_cycle_sine_square(t, t1, tau):
    """
    Return a temporal profile of a half cycle sine-square pulse.

    Parameters
    ----------
    t : float or array-like
        The time at which the pulse shape is evaluted
    t1 : float
        The time shift of the pulse
    tau : float
        The pulse duration
    """
    _t, _t1, _tau = asarray(t), t1, tau
    _supp_mask = logical_and((_t1 - 0.5 * _tau <= _t), (_t < _t1 + 0.5 * _tau))
    _f = _supp_mask * ( cos(pi*(_t-_t1)/_tau) )**2
    return _f



# from numpy import exp, square

def pulse_shape_half_cycle_gaussian(t, t1, tau):
    """
    Return a temporal profile of a half-cycle Gaussian shape pulse.
    
    It does not matter whether the arguments t, t1, tau have dimension or not, 
    since the formula for this pulse shape is dependent 
    only on the ratios between t or t1 and tau, the pulse duration.
    In other words, the pulse duration is itself a unit of time.
    
    Parameters
    ----------
    t : float or array-like
        The time at which the pulse shape is evaluted
    t1 : float
        The time shift of the pulse
    tau : float
        The pulse duration
    """
    return exp(-square(t-t1)/tau**2)



import numpy as np
from numpy import log, sqrt, pi, asarray
from scipy.special import erf

def phase_offset_for_half_cycle_gaussian(omega, Omega, tau_d):
    """
    Evaluate phase offset between two time points 
    corresponding to given frequency omega.
    
    The result is valid for a half-cycle Gaussian shaped pulse,
    and for high enough omega compared to omega_0 
    (which is 1 with omega_0 as unit of frequency)
        
    With omega_0 as unit of angular frequency.
    """
    f_max_hcg = max_value_of_half_cycle_gaussian()
    omega_max_hcg = sqrt(1**2 + (2*Omega*f_max_hcg)**2)
    
    assert tau_d > 0
    _omega = asarray(omega)
    assert np.all(_omega < omega_max_hcg)
    
    tau_omega = tau_d * sqrt(log(2*Omega/sqrt(_omega**2 - 1)))
    offset = 2*(2*Omega*tau_d*sqrt(pi)/2*erf(tau_omega/tau_d)-_omega*tau_omega)
    return offset








def max_value_of_half_cycle_gaussian():
    return 1

def max_value_of_single_cycle_gaussian():
    return 1./2**0.5 * exp(-0.5)


# from numpy import exp, square

def pulse_shape_single_cycle_gaussian(t, t1, tau):
    """Evaluate single-cycle Gaussian pulse shape for given time point(s)

    Parameters
    ----------
    t : float or array-like
        The time at which the pulse shape is evaluted
    t1 : float
        The time shift of the pulse
    tau : float
        The pulse duration
    """
    _t_minus_t1_over_tau = (t - t1) / tau
    _f_t = _t_minus_t1_over_tau * exp( - square(_t_minus_t1_over_tau) )
    return _f_t



# from numpy import square, exp, asarray

def pulse_shape_quarter_cycle_gaussian(t, t1, tau):
    """
    Returns the temporal profile of a quarter-cycle Gaussian shape pulse.
    
    The pulse shape is defined as the following:

    For t < t1

    .. math::
       f(t) = e^{-(t-t_{1})^2 / \tau^{2}}

    For t >= t1

    .. math::
       f(t) = f(t1) = 1


    Parameters
    ----------
    t : float or array-like
        The time at which the pulse shape is evaluted
    t1 : float
        The time shift of the pulse
    tau : float
        The duration of pulse modulation
    """
    _t = asarray(t)
    _t_before_t1_mask = _t < t1
    _f_t = exp(-square(_t-t1)/tau**2) * _t_before_t1_mask \
            + ~_t_before_t1_mask
    return _f_t




def one_over_factorial(n):
    assert not (n < 0) and int(n) == n
    return np.prod(1. / np.arange(1,n+1))

def one_over_a_pow_n(a, n):
    assert abs(a) > 1e-14
    assert not (n < 0) and int(n) == n
    return np.prod(np.full((n,), 1/a))

from numpy import pi, sqrt, exp
from scipy.special import hermite

def hg(u, m):
    """
    - u : float or array-like
    - m : int, nonnegative
    """
    Hm = hermite(m)
    one_over_sqrt_2_pow_m = sqrt(one_over_a_pow_n(2,m))
    one_over_sqrt_fact_m = sqrt(one_over_factorial(m))
    return pi**(-1/4.) * one_over_sqrt_2_pow_m * one_over_sqrt_fact_m * Hm(u) * exp(-1/2. * u*u)

@njit
def hg0(u):
    return pi**(-1/4.) * exp(-1/2. * u**2)

@njit
def hg2(u):
    return pi**(-1/4.) * sqrt(2) * (u**2 - 1/2.) * exp(-1/2. * u**2)

@njit
def hg4(u):
    return pi**(-1/4.) * sqrt(2/3.) * (u**4 - 3.*u**2 + 3/4.) * exp(-1/2. * u**2)




