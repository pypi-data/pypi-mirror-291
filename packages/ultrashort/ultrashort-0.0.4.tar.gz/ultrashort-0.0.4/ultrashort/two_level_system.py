"""Routines for two-level system"""

from sys import stderr
from numbers import Real

import numpy as np
from numpy import (
    asarray, isclose, square, conjugate, cos, sin, sqrt, arctan2, exp, pi, e
)
from scipy.optimize import brentq
import sympy as sp
from sympy.simplify.fu import TR10
from numba import njit

from .pulse import (
        max_value_of_half_cycle_gaussian, 
        max_value_of_single_cycle_gaussian,
        phase_offset_for_half_cycle_gaussian 
)
from .su2 import sigma_1, sigma_2, sigma_3
from .ode import rk4_complex
from .fidelity import fidel_trace_qudit, avg_gate_fidel_qudit

def rotation_matrix_SU2(angle, n_vec):

    _angle = asarray(angle)
    assert _angle.ndim <= 1
    _N = _angle.size
    assert _N >= 1
    _result_shape = (2,2) if _N == 1 else (_N,2,2)
    _result = np.empty(_result_shape, dtype=np.complex)

    _n = asarray(n_vec)
    assert _n.shape in [(3,), (_N,3)]
    assert np.all(isclose(square(_n).sum(axis=-1), 1, rtol=1e-10, atol=1e-11))
    _nx, _ny, _nz = _n.transpose()
    
    _a = cos(_angle/2.) - 1.j * sin(_angle/2.) * _nz
    _b = -1.j * sin(_angle/2.) * (_nx - 1.j*_ny)
    
    _result[...,0,0] = _a
    _result[...,0,1] = _b
    _result[...,1,0] = - _b.conj()
    _result[...,1,1] = _a.conj()
    
    return _result


from numpy import asarray, arctan2, real, imag
def c2_to_bloch_angles(c2_vec):
    _c0, _c1 = asarray(c2_vec)
    _bloch_theta = 2. * arctan2(abs(_c0), abs(_c1))
    _bloch_phi = arctan2(imag(_c1), real(_c1)) - arctan2(imag(_c0), real(_c0))
    return _bloch_theta, _bloch_phi


# from numpy import cos, sin
def spherical_angles_to_unit_r3_vector(theta, phi):
    _theta, _phi = asarray(theta), asarray(phi)
    assert _theta.shape == _phi.shape
    assert _theta.ndim <= 1
    _N = _theta.size
    _result_shape = (3,) if _N == 1 else (_N,3)
    _result = np.empty(_result_shape, dtype=np.float)
    
    _sin_theta = sin(_theta)
    _x = _sin_theta * cos(_phi)
    _y = _sin_theta * sin(_phi)
    _z = cos(_theta)
    
    _result[...,0] = _x
    _result[...,1] = _y
    _result[...,2] = _z
    return _result




# from sys import stderr

def map_state_vec_on_bloch_sphere(state_vec):
    """Return Cartesian coordinates on the Bloch sphere for given state vector
    
    Parameters
    ----------
    state_vec: (2,) or (N,2) array-like
        An array of C2 (complex-2) state vectors
    """

    print(
            "This method may have a different convention "
            "of the definition of Bloch vector. "
            "Consider expectation values of pauli matrices.", file=stderr)

    _theta_bloch, _phi_bloch = c2_to_bloch_angles(state_vec.transpose())
    _bloch_vec = spherical_angles_to_unit_r3_vector(_theta_bloch, _phi_bloch)
    _bloch_vec_x, _bloch_vec_y, _bloch_vec_z = _bloch_vec.transpose()
    return _bloch_vec_x, _bloch_vec_y, _bloch_vec_z




# from numpy import asarray, conjugate

def pauli_matrices_expectation_values(state_vec):
    """
    Evaluate expectation values of Pauli matrices for given state vector

    # Argument
    state_vec: (...,2), array-like
        The state vector in the basis ${|0\rangle, |1\rangle}$.

    # Returns
    bloch_vec: (3,...), numpy.ndarray
        The expectation values of Pauli matrices.
    """
    _state_vec = asarray(state_vec)
    assert _state_vec.shape[-1] == 2
    _c1, _c2 = _state_vec[...,0], _state_vec[...,1]
    _c1_c2_conj = _c1 * conjugate(_c2)
    
    _sigma_vec = np.empty((3,) + _state_vec.shape[:-1], dtype=np.float)
    _sigma_vec[0] = 2. * np.real(_c1_c2_conj)  # sigma_x
    _sigma_vec[1] = (- 2.) * np.imag(_c1_c2_conj)  # sigma_y
    _sigma_vec[2] = np.real(_c1*conjugate(_c1) - _c2*conjugate(_c2))  # sigma_z
    
    return _sigma_vec




# from numpy import asarray, cos, sin, sqrt, arctan2, exp

def bloch_to_su2(bloch_vec):
    """
    Convert Bloch vector to SU(2) vector
    
    # Argument
    bloch_vec : (...,3)
        Real-valued array-like
        
    # Return
    su2_vec : (...,2)
        Complex-valued Numpy ndarray
    """
    
    _bloch_dim = 3
    _bloch = asarray(bloch_vec)
    assert _bloch.shape[-1] == _bloch_dim
    
    _sigma1, _sigma2, _sigma3 = (_bloch[...,i] for i in range(_bloch_dim))
    _cos_theta_half = sqrt((1+_sigma3)/2)
    _sin_theta_half = sqrt((1-_sigma3)/2)
    _phi = arctan2(_sigma2, _sigma1)
    _exp_i_phi_half = exp(1.j*_phi/2)
    
    _su2_arr_shape = _bloch.shape[:-1]+(2,)
    _su2 = np.empty(_su2_arr_shape, dtype=np.complex)
    _su2[...,0] = _exp_i_phi_half.conj() * _cos_theta_half
    _su2[...,1] = _exp_i_phi_half * _sin_theta_half
    
    return _su2



from numpy import asarray, cos, sin
def rotate_SU2(state_vec, n_vec, angle):
    _state, _n = (asarray(_arr) for _arr in (state_vec, n_vec))
    _angle = float(angle)
    assert abs(np.dot(_n,_n) - 1.) < 1e-10
    assert _n.shape == (3,)
    _nx, _ny, _nz = _n
    assert _state.shape == (2,)
    
    _a = cos(_angle/2.) - 1.j * sin(_angle/2.) * _nz
    _b = -1.j * sin(_angle/2.) * (_nx - 1.j*_ny)
    
    _Omega = np.array([[_a, _b], [_b.conj(), _a.conj()]], dtype=np.complex)
    _rotated_state = _Omega @ _state
    return _rotated_state








# import numpy as np
# from numpy import asarray

def _check_dt_xor_t_arr_and_get_interval(arg_dt, arg_t_arr):
    """
    Check only one of arg_dt and arg_t_arr is None.
    Return corresponding dt for equidistanced array or an array of intervals
    
    Several other things are also checked 
    which may be useful of these kind of arguments set.
    """
    _dt_tilde_not_given = arg_dt == None
    _t_tilde_arr_not_given = arg_t_arr == None
    if not ((_dt_tilde_not_given) ^ (_t_tilde_arr_not_given)):
        raise ValueError("Either `dt_tilde` or `t_tilde_arr` should be None")
    else: 
        _dt_tilde_is_given = _t_tilde_arr_not_given
        _t_tilde_arr_is_given = _dt_tilde_not_given
    
    _dt_tilde = None
    if _dt_tilde_is_given:
        assert arg_dt > 0
        _dt_tilde = arg_dt
    elif _t_tilde_arr_is_given:
        _t_tilde_arr = asarray(arg_t_arr)
        assert _t_tilde_arr.size >= 2 and _t_tilde_arr.ndim == 1
        _dt_tilde = np.diff(_t_tilde_arr)
    assert _dt_tilde is not None
    
    return _dt_tilde



# import numpy as np
# from numpy import asarray

def tau_tilde_times_s1_t_tilde(
        f_t_tilde_arr, delta_t_tilde=None, t_tilde_arr=None):

    _dt_tilde = _check_dt_xor_t_arr_and_get_interval(delta_t_tilde,t_tilde_arr)
    
    _f_t_tilde_arr = asarray(f_t_tilde_arr)
    assert _f_t_tilde_arr.size >= 2 and _f_t_tilde_arr.ndim == 1

    _tau_tilde_s1_t_tilde = np.empty_like(_f_t_tilde_arr)
    _tau_tilde_s1_t_tilde[0] = 0.
    _tau_tilde_s1_t_tilde[1:] = 0.5 * _dt_tilde \
            * (_f_t_tilde_arr[:-1] + _f_t_tilde_arr[1:])
    np.cumsum(_tau_tilde_s1_t_tilde, out=_tau_tilde_s1_t_tilde)
    
    return _tau_tilde_s1_t_tilde


# from numbers import Real
# from numpy import asarray

def eval_A_over_v_tilde_and_B_over_v_tilde(
    f_t_tilde_arr, t_tilde_arr, v_tilde, t1_tilde, return_tau_s1=False):
    """
    Evaluate integrals, A(t)/v_tilde and B(t)/v_tilde for obtaining
    the time evolution operator in the Short-but-Strong approximation scheme.
    
    Parameters
    ----------
    f_t_tilde_arr: (Nt,) array-like
        an array of field shape values along time
    """
    ########## Check input arguments
    
    _t_tilde_arr = asarray(t_tilde_arr)
    _dt_tilde = np.diff(_t_tilde_arr)
    
    assert v_tilde >= 0 and isinstance(v_tilde, Real)
    _v_tilde = float(v_tilde)
    
    _t1_tilde = float(t1_tilde)
    
    _f_t_tilde_arr = asarray(f_t_tilde_arr)
    assert _f_t_tilde_arr.shape == (_t_tilde_arr.size,)

    
    ########## Evaluate `tau_tilde_s1_t_tilde`
    
    _tau_tilde_s1_t_tilde_arr = np.empty_like(_f_t_tilde_arr)
    _tau_tilde_s1_t_tilde_arr[0] = 0.
    _tau_tilde_s1_t_tilde_arr[1:] = 0.5 * _dt_tilde \
            * (_f_t_tilde_arr[:-1] + _f_t_tilde_arr[1:])
    np.cumsum(_tau_tilde_s1_t_tilde_arr, out=_tau_tilde_s1_t_tilde_arr)
    
    
    ########## Evaluate `_A_over_v_tilde` and `_B_over_v_tilde`
    
    _two_v_tilde_tau_tilde_s1_t_tilde = 2.*_v_tilde *_tau_tilde_s1_t_tilde_arr

    _A_over_v_tilde = np.empty_like(_f_t_tilde_arr)
    _A_over_v_tilde[0] = 0.
    _integrand_A = (_t_tilde_arr - _t1_tilde) * _f_t_tilde_arr \
            * sin(_two_v_tilde_tau_tilde_s1_t_tilde)
    _A_over_v_tilde[1:] = (_integrand_A[1:] +_integrand_A[:-1]) *_dt_tilde *0.5
    _A_over_v_tilde[:] = np.cumsum(_A_over_v_tilde)

    _B_over_v_tilde = np.empty_like(_f_t_tilde_arr)
    _B_over_v_tilde[0] = 0.
    _integrand_B = (_t_tilde_arr - _t1_tilde) * _f_t_tilde_arr \
            * cos(_two_v_tilde_tau_tilde_s1_t_tilde)
    _B_over_v_tilde[1:] = (_integrand_B[1:] +_integrand_B[:-1]) *_dt_tilde *0.5
    _B_over_v_tilde[:] = np.cumsum(_B_over_v_tilde)
    
    _results = (_A_over_v_tilde, _B_over_v_tilde)
    if return_tau_s1: _results += (_tau_tilde_s1_t_tilde_arr,)
    return _results





# from numpy import arctan2, cos, sin, sqrt, asarray
# from ultrashort.two_level_system import eval_A_over_v_tilde_and_B_over_v_tilde

def eval_U1_and_U2_for_SU2(t_arr, Omega, f_t_func, t1, tau_d):
    """
    # Corresponding Hamiltonian
    H(t) = H0 + f(t)V0
    H0 = hbar omega_0 / 2 * sigma_3
    V0 = - hbar Omega sigma_1
    where omgea_0 is unit of frequency (thus 1/omega_0 is the unit of time).
    Note the signs of H0 and V0.
    """
    
    _t_arr = asarray(t_arr)
    _Omega, _t1, _tau_d = float(Omega), float(t1), float(tau_d)
    assert callable(f_t_func)
    _f_t_func = f_t_func
    
    _f_t_arr = _f_t_func(_t_arr, _t1, _tau_d)
    _A_over_Omega, _B_over_Omega, _tau_d_s1_arr = \
            eval_A_over_v_tilde_and_B_over_v_tilde(
                    _f_t_arr, _t_arr, _Omega, _t1, return_tau_s1=True)

    _U1_t = rotation_matrix_SU2(- 2. * _Omega * _tau_d_s1_arr, n_vec=[1,0,0])
    
    _zy_angle_t = arctan2(_B_over_Omega, _A_over_Omega)
    _n_vec_t = asarray([
        np.zeros_like(_t_arr), sin(_zy_angle_t), cos(_zy_angle_t)]).transpose()
    _rot_angle_t = 2. * _Omega * sqrt(_A_over_Omega**2 + _B_over_Omega**2)
    
    _U2_t = rotation_matrix_SU2(_rot_angle_t, _n_vec_t)
    
    return _U1_t, _U2_t





# import sympy as sp
# from sympy.simplify.fu import TR10
# from .su2 import sigma_1, sigma_2, sigma_3

def eval_expr_sigma_1_t_from_ground_state_IA_and_SAS():
    
    _tau, _t1 = sp.symbols('tau, t1', real=True)
    _Omega = sp.symbols('Omega', real=True, positive=True)

    _alpha1, _alpha2 = sp.symbols(r'alpha1 alpha2', real=True)
    _phi2 = sp.symbols(r'phi2', real=True)
    
    _SU_dim = 2
    _one_mat = sp.Matrix.eye(_SU_dim)
    
    _U0_t1_0 = sp.cos(_t1/2) * _one_mat - sp.I * sigma_3 * sp.sin(_t1/2)
    _U2_t = sp.cos(_alpha2/2) * _one_mat - sp.I * \
            (sp.sin(_phi2)*sigma_2 + sp.cos(_phi2)*sigma_3) * sp.sin(_alpha2/2)
    _U1_t = sp.cos(_alpha1/2) * _one_mat - sp.I * sigma_1 * sp.sin(_alpha1/2)
    _U0_t_t1 = sp.cos(_tau/2) * _one_mat - sp.I * sigma_3 * sp.sin(_tau/2)
    
    _su2_vec_0 = sp.Matrix([0, 1])
    
    _U_IA_t_0 = _U0_t_t1 * _U1_t * _U0_t1_0
    _su2_IA_vec_t = sp.simplify(_U_IA_t_0 * _su2_vec_0)
    _sigma_1_IA_t = sp.simplify(
            sp.re((_su2_IA_vec_t.conjugate().T * sigma_1 *_su2_IA_vec_t)[0]))
    _sigma_1_IA_t = TR10(_sigma_1_IA_t)
    
    _U_SAS_t_0 = _U0_t_t1 * _U1_t * _U2_t * _U0_t1_0
    _su2_SAS_vec_t = sp.simplify(_U_SAS_t_0 * _su2_vec_0)
    _sigma_1_SAS_t = sp.simplify(
            sp.re((_su2_SAS_vec_t.conjugate().T * sigma_1 *_su2_SAS_vec_t)[0]))
    
    _vars = (_tau, _Omega, _alpha1, _alpha2, _phi2)
    
    return _sigma_1_IA_t, _sigma_1_SAS_t, _vars



# from .two_level_system import eval_A_over_v_tilde_and_B_over_v_tilde

def eval_numer_sigma_1_t_from_ground_state_IA_and_SAS(
        t_arr, Omega, f_t_func, t1_val, tau_d_val):

    _Omega_arr = asarray(Omega)
    assert _Omega_arr.ndim <= 1
#    _Omega_arr = np.array([_Omega]) if _Omega.ndim == 0 else _Omega

    _t_arr = asarray(t_arr)
    assert _t_arr.ndim <= 1
    _sigma_1_t_arr_shape = _Omega_arr.shape + _t_arr.shape
    _sigma_1_IA_t_arr_stack = np.empty(_sigma_1_t_arr_shape, dtype=np.float)
    _sigma_1_SAS_t_arr_stack = np.empty(_sigma_1_t_arr_shape, dtype=np.float)

    _sigma_1_IA_t, _sigma_1_SAS_t, _sym_vars = \
            eval_expr_sigma_1_t_from_ground_state_IA_and_SAS()
    _tau, _Omega, _alpha1, _alpha2, _phi2 = _sym_vars

    _t_minus_t1_arr = _t_arr - t1_val
    
    _f_t_arr = f_t_func(_t_arr, t1_val, tau_d_val)

    
    for _i_Omega in range(_Omega_arr.size):
        _indices = (Ellipsis,) if (_Omega_arr.size == 1) else _i_Omega
        _Omega_val = float(_Omega_arr[_indices])

        _A_over_Omega_arr, _B_over_Omega_arr, _tau_d_s1_arr = \
                eval_A_over_v_tilde_and_B_over_v_tilde(
                        _f_t_arr, _t_arr, _Omega_val, t1_val, return_tau_s1=True)
        _alpha1_val_arr = - 2. * _Omega_val * _tau_d_s1_arr
        _alpha2_val_arr = 2. * _Omega_val \
                * np.sqrt(_A_over_Omega_arr**2 + _B_over_Omega_arr**2)
        _phi2_val_arr = np.arctan2(_B_over_Omega_arr, _A_over_Omega_arr)
        
        _sigma_1_IA_t_lambda = sp.lambdify((_tau, _alpha1), _sigma_1_IA_t)
        _sigma_1_IA_t_arr_stack[_indices] = _sigma_1_IA_t_lambda(
                _t_minus_t1_arr, _alpha1_val_arr)
        
        _sigma_1_SAS_t_lambda = sp.lambdify(
                (_tau, _alpha1, _alpha2, _phi2), _sigma_1_SAS_t)
        _sigma_1_SAS_t_arr_stack[_indices] = _sigma_1_SAS_t_lambda(
                _t_minus_t1_arr, _alpha1_val_arr, _alpha2_val_arr, _phi2_val_arr)
    
    return _sigma_1_IA_t_arr_stack, _sigma_1_SAS_t_arr_stack








############# NUMERICAL METHODS ############# 

def eval_Crank_Nicolson_time_evol_operator_per_step(
        t_tilde, dt_tilde, v_tilde, f_t_tilde, t1_tilde, tau_tilde):
    assert v_tilde >= 0
    _a = dt_tilde / 2. * (1./1.j) * (-1./2.)
    _b = dt_tilde / 2. * (1./1.j) * v_tilde \
            * f_t_tilde(t_tilde+0.5*dt_tilde, t1_tilde, tau_tilde)
    _a_sq, _b_sq = _a*_a, _b*_b
    _U = np.array([
        [_b_sq+(1.+_a)**2, -2.*_b],
        [-2.*_b, _b_sq + (1.-_a)**2] ], dtype=np.complex)
    _U *= 1./(1-_a_sq-_b_sq)
    return _U



# from numpy import asarray

def eval_Crank_Nicolson_time_evol_operator_at_once(
        t_tilde_arr, f_t_tilde, v_tilde, t1_tilde, tau_tilde):
    """
    Evaluate the Crank-Nicolson time evolution operator 
    for a field-driven two-level system

    H(t) = H0 + f(t)V0

    where

    H0 = + 1/2 hbar omega_0 sigma_3
    V0 = - v sigma_1

    Note, the signs in front of H0 and V0.
    
    Parameters
    ----------
    t_tilde_arr: (Nt,), Nt>=2, array-like
        an array of time points, multiplied by system oscillation frequency, 
        at which state vectors are of interest
    f_t_tilde: callable
        a function which returns field values for given array of time points
    v_tilde: nonnegative float
        the field strength 
        in unit of the energy separation of this two-level system
    t1_tilde: float
        an appropriate time point for the given field shape
    tau_tilde: positive float
        the duration of the field, multiplied by system oscillation frequency
    
    Returns
    -------
    U_CN: (2, 2) or (Nt-1, 2, 2) array-like
        resulting time evolution operators for 'Nt-1' timesteps 
        given by given Nt timepoints

    Notes
    -----
    It would be useful in conjugation with this routine 
    if one have a routine for the accumulative multiplication.
    """
    
    ############ Check function arguments
    _t_tilde_arr = asarray(t_tilde_arr)
    _dt_tilde = np.diff(_t_tilde_arr)
    _t_mid_tilde_arr = 0.5 * (_t_tilde_arr[1:] + _t_tilde_arr[:-1])
    assert _t_tilde_arr.size >= 2 and _t_tilde_arr.ndim == 1
    _Nt = _t_tilde_arr.size
    _N_timesteps = _Nt - 1
    assert v_tilde >= 0
    
    
    ############ Evaluate the time evolution operators
    _a = _dt_tilde / 2. * (1./1.j) * (-1./2.)
    _b = _dt_tilde / 2. * (1./1.j) * (v_tilde) \
            * f_t_tilde(_t_mid_tilde_arr, t1_tilde, tau_tilde)
    _a_sq, _b_sq = _a*_a, _b*_b
    
    _U_shape_per_time = (2, 2)
    _U_shape = (_N_timesteps,) + _U_shape_per_time
    _U = np.empty(_U_shape, dtype=np.complex)
    
    _global_factor = 1./(1.-(_a_sq+_b_sq))
    _Uoffdiag = _global_factor * (2.*(-_b))
    
    _U[...,0,0] = _global_factor * (_b_sq + (1.-_a)**2)
    _U[...,0,1] = _Uoffdiag
    _U[...,1,0] = _Uoffdiag
    _U[...,1,1] = _global_factor * (_b_sq + (1.+_a)**2)
    
    return _U



def propagate_state_by_CN(state_t0, t, f_t, v, t1, tau_d):
    """
    Propagate the given state vector.

    Let $\omega_{0}$ be the transition frequency between the two states.
    The unit of time is $1/\omega_{0}$.

    # Arguments
    state_t0: (2,), array-like
        The initial state vector.
        The basis is ${|1\rangle, |0\rangle}$, 
        where $|1\rangle$ is the excited state vector 
        and $|0\rangle$ is the ground state vector.
    t_tilde_arr: (N,), array-like
        An array of time points.
    f_t_tilde: callable
        The temporal shape function.
    v_tilde: float
        The driving strength.
    t1_tilde: float
        The pulse center in time domain.
    tau_tilde: float, positive
        The pulse duration.
    """
    
    t_tilde_arr, f_t_tilde, v_tilde, t1_tilde, tau_tilde = t, f_t, v, t1, tau_d

    Ndim = 2
    _state_t0 = asarray(state_t0, dtype=np.complex)
    assert _state_t0.shape == (Ndim,)
    assert callable(f_t_tilde)
#    assert tau_tilde > 0

    _U_numerics_t_tilde_arr_arr = eval_Crank_Nicolson_time_evol_operator_at_once(
        t_tilde_arr, f_t_tilde, v_tilde, t1_tilde, tau_tilde)

    _state_t_arr = np.empty((t_tilde_arr.size, Ndim), dtype=np.complex)
    _state_t_arr[0] = _state_t0
    for t_idx in range(t_tilde_arr.size-1):
        _Umat = _U_numerics_t_tilde_arr_arr[t_idx]
        _state_t_arr[t_idx+1] = _Umat @ _state_t_arr[t_idx]
    
    return _state_t_arr





from numpy import pi
# from scipy.optimize import brentq
from .pulse import (
        max_value_of_half_cycle_gaussian, 
        phase_offset_for_half_cycle_gaussian 
)

def dips_and_hills_freq_for_hcg(tau_d, Omega):
    
    _tau_d, _Omega = float(tau_d), float(Omega)
    
    _s1inf = pi**0.5
    _total_area_of_f_t_hcg = _tau_d * _s1inf
    _phi_max = 2*_Omega*_total_area_of_f_t_hcg
    
    _f_max_hcg = max_value_of_half_cycle_gaussian()
    _omega_max_hcg = sqrt(1**2 + (2*_Omega*_f_max_hcg)**2)
    _omega0 = 1. # unit of angular frequency
    
    _phi0_arr = pi/2. + pi*np.arange( int( (_phi_max))/pi - 1)
    
    def _phase_offset_eq(omega, Omega, tau_d, phi0):
        return phase_offset_for_half_cycle_gaussian(omega,Omega,tau_d) - phi0
    
    _omega_phi_n_arr = np.empty_like(_phi0_arr)

    _omega_a, _omega_b = _omega0+1e-5, _omega_max_hcg-1e-5
    for _i_phi, _phi0 in enumerate(_phi0_arr):
        _omega_phi_n_arr[_i_phi] = brentq(_phase_offset_eq, 
                _omega_a, _omega_b, args=(_Omega,_tau_d,_phi0))
        
    return _omega_phi_n_arr




# from numpy import exp, sqrt
# from scipy.optimize import brentq

def z_omega_1_and_2_scg(omega, Omega):
    def _eq(_z, _omega, _Omega):
        return _z*exp(-_z**2) - sqrt(_omega**2 - 1) / (2*_Omega)
    _zp = 1/2**0.5
    _z_omega_1 = brentq(_eq, 0, _zp, args=(omega, Omega))
    _z_omega_2 = brentq(_eq, _zp, 100*_zp, args=(omega, Omega))
    return _z_omega_1, _z_omega_2


def phi_omega_scg(omega, Omega, tau_d):
    _z_omega_1, _z_omega_2 = z_omega_1_and_2_scg(omega, Omega)
    _phi_omega = omega * tau_d * (
            0.5 * (1/_z_omega_1 - 1/_z_omega_2) - (_z_omega_2 - _z_omega_1)
            )
#    _phi_omega += exp(1)/(2*2**0.5 * Omega) * tau_d * (_z_omega_2-_z_omega_1)
    return _phi_omega


def omega_of_phi_scg(phi_over_pi, Omega, tau_d):
    
    if phi_over_pi > Omega*tau_d/pi: return None
    
    def _eq_phi_omega(_omega, _Omega, _tau_d, _phi_over_pi):
        return phi_omega_scg(_omega, _Omega, _tau_d) - _phi_over_pi * pi
    
    _omega_0 = 1.
    _f_peak = max_value_of_single_cycle_gaussian()
    _omega_cutoff = (_omega_0**2 + (2*Omega*_f_peak)**2)**0.5
    _omega_min, _omega_max = 1+1e-10, _omega_cutoff-1e-10
    _omega_of_phi = brentq(
            _eq_phi_omega, _omega_min, _omega_max, 
            args=(Omega, tau_d, phi_over_pi))

    return _omega_of_phi


def get_maybe_all_intra_half_cycle_dips_freq_scg(Omega, tau_d):
    """
    Evalaute frequencies $\{\omega\}$ at which area 
    enclosed by time-dependent radiation frequency $\omega(t)$ 
    and horizontal lines passing those $\{\omega\}$ 
    are $3/2\pi$, $2\pi$, $2\pi$, $2\pi$ and so on.
    This routine is intended to be valid for spectra 
    from system driven by single-cycle Gaussian pulse shape.

    # Argument
    Omega : float
        Rabi frequency corresponding to dipole interaction
    tau_d : float
        pulse duration

    # Returns
    omega_dips_arr : ndarray (N_dips,)
        an array of freqeuncies at which dips structure 
        in frequency spectrum are formed 
        by intra-half-cycle interference (not yet confirmed enough)
    """
    _n_max = int((Omega*tau_d - 3/2*pi)/ (2*pi))
    _N_dips = _n_max + 1
    _omega_dips_arr = np.empty((_N_dips,), dtype=np.float)
    _phi_n_over_pi_arr = 3/2 + 2*np.arange(_N_dips)
    for _n, _phi_n_over_pi in enumerate(_phi_n_over_pi_arr):
        _omega_dips_arr[_n] = omega_of_phi_scg(_phi_n_over_pi, Omega, tau_d)
    return _omega_dips_arr






def phi_omega_inter_half_cycle_scg(omega, Omega, tau_d):
    """
    Approximate phase difference between radiation time points 
    of given frequency omega, between left of first and second half-cycle.

    The pulse shape considered here is single-cycle Gaussian.
    """
    _z_omega_1, _z_omega_2 = z_omega_1_and_2_scg(omega, Omega)
    _phi_omega = 2*Omega*tau_d * (
            1 - 0.5*(exp(-_z_omega_1**2) + exp(-_z_omega_2**2))
            ) \
            - omega*tau_d*(_z_omega_1+_z_omega_2)    
    return _phi_omega



def omega_of_phi_inter_half_cycle_scg(phi_over_pi, Omega, tau_d):
    """
    Evaluate frequency at which phase inter-half-cycle difference 
    is given value `phi_over_pi`
    """

    if phi_over_pi > Omega*tau_d/pi: return None

    def _eq_phi_omega(_omega, _Omega, _tau_d, _phi_over_pi):
        _phi_omega = phi_omega_inter_half_cycle_scg(_omega, _Omega, _tau_d)
        return _phi_omega - _phi_over_pi * pi

    _omega_0 = 1.
    _f_peak = max_value_of_single_cycle_gaussian()
    _omega_cutoff = (_omega_0**2 + (2*Omega*_f_peak)**2)**0.5
    _omega_min, _omega_max = 1+1e-10, _omega_cutoff-1e-10
    _omega_of_phi = brentq(
            _eq_phi_omega, _omega_min, _omega_max,
            args=(Omega, tau_d, phi_over_pi))

    return _omega_of_phi



def get_maybe_all_inter_half_cycle_dips_freq_scg(Omega, tau_d):
    """
    (MAYNOTBETRUE! - does not seem to match with numerical results)
    Evaluate dips frequencies formed by interference
    between radiations coming from time points at different half-cycles
    """
    print("This routine seems incorrect. Please do not use this.", file=stderr)
    _Omega, _tau_d = float(Omega), float(tau_d)
    
    _phi_inter_min = - 2 * _Omega * _tau_d * (2/e**0.5 - 1)
    _phi_inter_max = _Omega * _tau_d

    _n_min = max([0, np.ceil(1+_phi_inter_min/(2*pi))])
    _n_max = int(1+_phi_inter_max/(2*pi))

    _phi_dips_over_pi_arr = 2 * (np.arange(_n_min,_n_max+1) - 1)
    
    _omega_dips_inter_arr = np.empty(
            (_phi_dips_over_pi_arr.size,), dtype=np.float)
    
    for _i, _phi_over_pi in enumerate(_phi_dips_over_pi_arr):
        _omega_dips_inter_arr[_i] = omega_of_phi_inter_half_cycle_scg(
                _phi_over_pi, _Omega, _tau_d)
    
    return _omega_dips_inter_arr




def mag_and_dir(vec):
    """
    # Arguments
    - vec : (...,3)
    """
    vec = np.asarray(vec)
    assert vec.ndim >= 1
    assert vec.shape[-1] == 3
    mag = np.sqrt((np.abs(vec)**2).sum(axis=-1))
    theta = np.arctan2(np.sqrt(vec[...,0]**2 + vec[...,1]**2), vec[...,2])
    sin_theta = sin(theta)
    cos_theta = cos(theta)
    phi = np.arctan2(vec[...,1], vec[...,0])
    dirvec = np.empty_like(vec, dtype=np.float64)
    dirvec[...,0] = sin_theta*cos(phi)
    dirvec[...,1] = sin_theta*sin(phi)
    dirvec[...,2] = cos_theta
    return mag, dirvec



@njit
def dpsidu_beta10(u, psi, Omega_tau_d, omega_tau_d, f, fargs):
    fu = f(u, *fargs)
    sigx_beta10 = np.array([[0,1],[1,0]], dtype=np.complex128)
    sigy_beta10 = np.array([[0,-1.j],[1.j,0]], dtype=np.complex128)
    H = (Omega_tau_d * fu) * (cos(omega_tau_d*u) * sigx_beta10 - sin(omega_tau_d*u) * sigy_beta10)
    dpsidu_ = np.empty(psi.shape, dtype=np.complex128)
    
    for j in range(2):
        dpsidu_[j,...] = -1.j * (H[j,0] * psi[0,...] + H[j,1] * psi[1,...])
    
    return dpsidu_




def infidel_params(params, U_target, f, alpha, U_t, du, Nu, u_min, fargs=(),
                   params_list=None, norm_thres=1e-13, infidel_thres=1e-14):
    """
    The signature of `f` is
    ```
    f(t, *fargs_total) -> float
    ```
    where, `fargs_total = tuple(params[1:]) + tuple(fargs)`.
    """

    if params_list is not None:
        params_list.append(params)
    
    #### Process input parameters
    Omega_tau_d = params[0]
    fargs = tuple(params[1:]) + tuple(fargs)
    omega0_tau_d = alpha * 2 * pi
    
    U_0 = np.eye(2)
    args = (Omega_tau_d, omega0_tau_d, f, fargs)
    u_arr_, U_t[:] = rk4_complex(u_min, U_0, dpsidu_beta10, du, Nu, args=args)
    
    #### Check norm
    norm_tr_t = fidel_trace_qudit(U_t, U_t)
    norm_tr_t_abserr_max = np.abs(norm_tr_t - 1).max()
    if not (norm_tr_t_abserr_max < norm_thres):
        print(f"[alpha={alpha:.3g}] norm_tr_t_abserr_max = {norm_tr_t_abserr_max:.3g}", file=stderr)

    #### Evaluate the trace fideliy and the state fidelity
    fidel_tr_alpha = avg_gate_fidel_qudit(U_target, U_t[-1])
    infidel_tr_alpha = 1 - fidel_tr_alpha
    if infidel_tr_alpha < 0:
        if infidel_tr_alpha < -infidel_thres:
            print(f"[alpha={alpha:.3g}] 1 - fidel_tr_alpha = {infidel_tr_alpha:.3g} < 0", file=stderr)
        infidel_tr_alpha = 0.
    
    return infidel_tr_alpha

