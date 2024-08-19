"""Matrices for SU(3) group"""

from itertools import combinations, combinations_with_replacement

import numpy as np
from numpy import asarray, einsum
from scipy.integrate import solve_ivp
import sympy as sp
from sympy import tensorcontraction, tensorproduct, Rational

from .euclidean import unit_vector_of
from .special import sinhc


N_su_dim = 3

lambs = np.array(
    [
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ],
        [
            [0, -1j, 0],
            [1j, 0, 0],
            [0, 0, 0]
        ],
        [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 0]
        ],
        [
            [0, 0, 1],
            [0, 0, 0],
            [1, 0, 0]
        ],
        [
            [0, 0, -1j],
            [0, 0, 0],
            [1j, 0, 0]
        ],
        [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [0, 0, -1j],
            [0, 1j, 0]
        ],
        [
            [1./3**0.5, 0, 0],
            [0, 1./3**0.5, 0],
            [0, 0, -2./3**0.5]
        ]
    ], dtype=np.complex
)









lambs_sym = sp.Array(
    [
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ],
        [
            [0, -sp.I, 0],
            [sp.I, 0, 0],
            [0, 0, 0]
        ],
        [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 0]
        ],
        [
            [0, 0, 1],
            [0, 0, 0],
            [1, 0, 0]
        ],
        [
            [0, 0, -sp.I],
            [0, 0, 0],
            [sp.I, 0, 0]
        ],
        [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [0, 0, -sp.I],
            [0, sp.I, 0]
        ],
        [
            [1/sp.sqrt(3), 0, 0],
            [0, 1/sp.sqrt(3), 0],
            [0, 0, -2/sp.sqrt(3)]
        ]
    ]
)









def magnitude_of_bloch_vector(N, tr_rho_sq):
    """
    Evaluate magnitude of bloch vector defined in SU(N) group 
    for given trace of density operator squared
    """
    assert int(N) == N and N > 0
    _N = N
    
    assert float(tr_rho_sq) == tr_rho_sq
    assert (1./N <= tr_rho_sq) and (tr_rho_sq <= 1)
    _tr_rho_sq = tr_rho_sq
    
    _magnitude = (2*(_tr_rho_sq-1/_N))**0.5
    return _magnitude



# from numpy import asarray, einsum
# from ultrashort.su3 import lambs

def hilbert_space_vector_to_SU3_bloch_vector(state_vec, with_norm=False):
    global N_su_dim
    _state_vec = asarray(state_vec)
    assert _state_vec.ndim > 0 and _state_vec.shape[-1] == N_su_dim
    _bloch_vec = einsum(
            '...m,jmn,...n->...j',np.conj(_state_vec),lambs,_state_vec)
    _initial_index = 0 if with_norm else 1
    return np.real(_bloch_vec[...,_initial_index:])




def dimension_of_SU_N_bloch_vector(N):
    _N = int(N)
    assert _N == N
    return _N**2 - 1




# from numpy import asarray

def time_evolve_three_levels(t_arr, state_t0, sys_args, pulse_args, 
        rtol=1e-7, atol=1e-9, full_output=False):
    """
    # Arguments
    sys_args = (Delta, Omega12, Omega13, Omega23)
    pulse_args = (pulse_shape_func, t1, tau_d)
    
    # Returns
    state_t : (Nt,3) if full_output == False
    """
    
    _t_arr = asarray(t_arr)
    assert _t_arr.ndim == 1 and _t_arr.size >= 2
    
    _state_t0 = asarray(state_t0)
    assert _state_t0.ndim == 1 and _state_t0.size == 3
    
    _Delta, _Omega12, _Omega13, _Omega23 = sys_args
    _pulse_shape_func, _t1, _tau_d = pulse_args
    
    _H0 = - 1./2. * lambs[3] \
        + (1./2. + _Delta) * 1./3. * (lambs[0] - 3**0.5 * lambs[8])

    _V0 = - _Omega12 * lambs[1] - _Omega13 * lambs[4] - _Omega23 * lambs[6]

    def _dydt(_t, _y, _H0, _V0, _pulse_shape, _t1, _tau_d):
        _f_t = _pulse_shape(_t, _t1, _tau_d)
        _H = _H0 + _f_t * _V0
        return -1.j * _H @ _y
    
    _dydt_args = (_H0, _V0, _pulse_shape_func, _t1, _tau_d)

    _sol = solve_ivp(_dydt, _t_arr[[0,-1]], y0=_state_t0, method='RK45', 
            t_eval=_t_arr, args=_dydt_args, rtol=rtol, atol=atol)
    
    _output = _sol if full_output else np.transpose(_sol.y)
    return _output




# from numpy import asarray
# from ultrashort.su3 import lambs
# from scipy.integrate import solve_ivp

def time_evolve_three_levels_omega0(t_arr, state_t0, sys_args, pulse_args,
        rtol=1e-7, atol=1e-9, full_output=False):
    """
    The unit of frequency:
    omega0 = sqrt(omega01^2 + omega12^2)
    
    # Arguments
    sys_args = (theta0_over_pi, Omega01, Omega02, Omega12)
    pulse_args = (pulse_shape_func, t1, tau_d)

    # Returns
    state_t : (Nt,3) if full_output == False
    """
    
    global lambs
    
    _t_arr = asarray(t_arr)
    assert _t_arr.ndim == 1 and _t_arr.size >= 2

    _state_t0 = asarray(state_t0)
    assert _state_t0.ndim == 1 and _state_t0.size == 3

    _theta0_over_pi, _Omega01, _Omega02, _Omega12 = sys_args
    _pulse_shape_func, _t1, _tau_d = pulse_args
    
    _theta0 = _theta0_over_pi * np.pi
    # with time unit of 1/omega0
    # and omega0 = sqrt(omega01^2 + omega12^2)
    _omega01, _omega12 = np.cos(_theta0), np.sin(_theta0)
    
    _H03 = - _omega01
    _H08 = (-2./(3**0.5)) * (0.5*_omega01 + _omega12)
    _H0 = (_H03 / 2.) * lambs[3] + (_H08 / 2.) * lambs[8]
    
    _V0 = - _Omega01 * lambs[1] - _Omega02 * lambs[4] - _Omega12 * lambs[6]

    def _dydt(_t, _y, _H0, _V0, _pulse_shape, _t1, _tau_d):
        _f_t = _pulse_shape(_t, _t1, _tau_d)
        _H = _H0 + _f_t * _V0
        return (-1.j) * _H @ _y

    _dydt_args = (_H0, _V0, _pulse_shape_func, _t1, _tau_d)
    
    _sol = solve_ivp(_dydt, _t_arr[[0,-1]], y0=_state_t0, method='RK45',
                     t_eval=_t_arr, args=_dydt_args, rtol=rtol, atol=atol)

    _output = _sol if full_output else np.transpose(_sol.y)
    return _output







# import sympy as sp

def eval_f_ijk():
    """Return antisymmetric tensor for a set of SU(3) generators"""

    Ngen = 8

    nonzeros = [
        [1,2,3,sp.Number('1')],
        [4,5,8,sp.sqrt(3)/2],
        [6,7,8,sp.sqrt(3)/2],
        [1,4,7,sp.Rational('1/2')],
        [2,4,6,sp.Rational('1/2')],
        [2,5,7,sp.Rational('1/2')],
        [3,4,5,sp.Rational('1/2')],
        [1,5,6,sp.Rational('-1/2')],
        [3,6,7,sp.Rational('-1/2')],
    ]

    f = sp.MutableSparseNDimArray.zeros(Ngen, Ngen, Ngen)

    for i,j,k,val_ijk in nonzeros:
        ijk = np.array([i,j,k], dtype=np.int)
        py_ijk = ijk - 1
        
        for offset in range(3):

            indices = np.mod(np.array([0,1,2], dtype=int) + offset, 3)
            indices_negative = np.mod(np.array([0,2,1], dtype=int) + offset, 3)

            f[py_ijk[indices]] = val_ijk
            f[py_ijk[indices_negative]] = - val_ijk
    return f




# import sympy as sp
# import numpy as np
# from ultrashort.su3 import lambs_sym
# from itertools import combinations

def eval_f_from_scratch():
    Ngen = 8
    f = sp.tensor.array.MutableDenseNDimArray.zeros(Ngen,Ngen,Ngen)
    
    ind_stat = np.array([0,1,2], dtype=int)
    ind_stat_neg = np.flip(ind_stat)
    for indices in combinations(range(1,Ngen+1), 3):
        lj, lk, ll = (lambs_sym[i].tomatrix() for i in indices)
        ind_py = np.array(indices,dtype=int) - 1
        val = ((lj*lk - lk*lj)*ll).trace() / (sp.S(4)*sp.I)
        if val == 0: continue
        for offset in range(3):
            ind_ind = np.mod(ind_stat+offset, 3)
            ind_ind_neg = np.mod(ind_stat_neg+offset, 3)
            f[ind_py[ind_ind]] = val
            f[ind_py[ind_ind_neg]] = - val
    return f




# import sympy as sp
# import numpy as np
# from ultrashort.su3 import lambs_sym
# from itertools import combinations_with_replacement

def eval_d_from_scratch():
    """Evaluate the totally symmetric tensor d_jkl for 3-by-3 Hermition matrices"""
    
    Ngen = 8
    d = sp.tensor.array.MutableDenseNDimArray.zeros(Ngen,Ngen,Ngen)

    ind_stat = np.array([0,1,2], dtype=int)
    ind_stat_neg = np.flip(ind_stat)
    for indices in combinations_with_replacement(range(1,Ngen+1), 3):
        lj, lk, ll = (lambs_sym[i].tomatrix() for i in indices)
        ind_py = np.array(indices,dtype=int) - 1
        val = ((lj*lk + lk*lj)*ll).trace() / sp.S(4)
        if val == 0: continue
        for offset in range(3):
            ind_ind = np.mod(ind_stat+offset, 3)
            ind_ind_neg = np.mod(ind_stat_neg+offset, 3)
            d[ind_py[ind_ind]] = val
            d[ind_py[ind_ind_neg]] = val
    return d







# import sympy as sp

# from ultrashort.su3 import eval_f_ijk

def commutator(c1, c2):
    """
    Evaluate commutator of the form :
    [c1_{j} \hat{\lambda}_{j}/2, c2_{k} \hat{\lambda}_{k}/2]
    
    # Arguments
    c1, c2 : (8,)
        Coefficients arrays
    """
    _c1, _c2 = sp.Array(c1), sp.Array(c2)
    assert _c1.shape == (8,) and _c2.shape == (8,)
    _f = eval_f_ijk()
    # [NOTE] Want to get f_jkl c1_j c2_k with contraction of j and k
    _f_c1 = sp.tensorcontraction(sp.tensorproduct(_f,_c1), (0,3))
    # [NOTE] Now, the indices of _f_c1 is kl
    # [NOTE] We are going to perform : _f_c1_kl c2_k
    _f_c1_c2 = sp.tensorcontraction(sp.tensorproduct(_f_c1, _c2), (0,2))
    # [NOTE] Now, we have _f_c1_c2 of index l
    return sp.I * _f_c1_c2


def su3_vec_with_identity_to_matrix(vec):
    """
    Return a 3-by-3 matrix corresponding to the input su(3) vector.
    mat = vec[0] * I/3 + sum_{j=1}^{9-1} vec[j] * lambda[j] / 2

    # Argument
    vec : (9,)

    # Returns
    mat : (3,3)
    """
    dim = 3
#    mat = sp.MutableDenseNDimArray.zeros(dim,dim)
    mat = vec[0] * sp.MutableDenseNDimArray(sp.eye(3)) / 3
    for j in range(1,dim*dim):
        mat += vec[j] * lambs_sym[j] / 2
    return mat

def su3_vec_to_matrix(vec):
    """
    Return a 3-by-3 matrix corresponding to the input su(3) vector.
    mat = sum_{j=1}^{9-1} vec[j] * lambda[j] / 2

    # Argument
    vec : (8,)

    # Returns
    mat : (3,3)
    """
    dim = 3
    assert len(vec) == 8
    su3_vec_with_identity = sp.MutableDenseNDimArray.zeros(dim*dim)
    for j in range(1,dim*dim):
        su3_vec_with_identity[j] = vec[j-1]
    mat = su3_vec_with_identity_to_matrix(su3_vec_with_identity)
    return mat



def multiply_su3_vec(A,B):
    """
    Evaluate Cj for j in {0,1,2,...,8} such that
    \hat{C} = \hat{A}\hat{B} = C0 / 3 * \hat{1} + Cj * \hat{\lambda}_{j} / 2
    for
    \hat{A} = A0 / 3 * \hat{1} + Aj * \hat{\lambda}_j / 2
    \hat{B} = B0 / 3 * \hat{1} + Bj * \hat{\lambda}_j / 2
    
    # Arguments
    A, B: (9,) array-like
        Arrays of coefficients of Hermitian operators \hat{A} and \hat{B}.
    """
    _A, _B = sp.Array(A), sp.Array(B)
    assert _A.shape == (9,) and _B.shape == (9,)
    _f = eval_f_ijk()
    _d = eval_d_from_scratch()
    
    _C = sp.tensor.array.MutableDenseNDimArray.zeros(9)
    _A_trless_dot_B_trless = tensorcontraction(
	tensorproduct(_A[1:],_B[1:]), (0,1))
    _C[[0]] = sp.S(1)/sp.S(3)*_A[0]*_B[0] \
	+ sp.S(1)/sp.S(2)*_A_trless_dot_B_trless

    _d_if = _d + sp.I * _f
    # Evaluate _Bk * _d_if_jkl = _B_d_if_jl
    _B_d_if_jl = tensorcontraction(tensorproduct(_B[1:],_d_if), (0,2))
    # Evaluate _Aj * _B_d_if_jl = _A_B_d_if_l
    _A_B_d_if_l = tensorcontraction(tensorproduct(_A[1:],_B_d_if_jl), (0,1))
    _Cj = Rational(1,3)*(_A[0]*_B[1:]+_B[0]*_A[1:]) + Rational(1,2)*_A_B_d_if_l

    for j in range(1,9): _C[[j]] = _Cj[j-1]

    return _C




def coef_of_su3_hermitian_sym(H):
    _H = sp.Matrix(H)
    global lambs_sym
    _vH = sp.Array([(_H * lambs_sym[j].tomatrix()).trace() for j in range(9)])
    return _vH




# import sympy as sp
# import numpy as np

# from ultrashort.su3 import lambs_sym, lambs
# from ultrashort.euclidean import unit_vector_of
# from ultrashort.special import sinhc

def _eval_gamma_and_eigvals_for_U2_exponent(alpha2_nonzero_vec):
    """
    Evaluate $\gamma$ and $\a_n$ for $n \in \{-1,0,1\}$
    where $U_2 = \exp{\gamma \tilde{X}_{2}}$ 
    and $a_n$ are eigvenvalues of \tilde{X}_{2}}

    # Argument
    alpha2_nonzero_vec: (5,...) array-like
    """
    
    #### Evalaute expressions for `p` and `q`, 
    #### the coefficients of the characteristic polynomials 
    #### for the eigenvalues of exponent of U2
    a_indices = np.array([2,3,4,7,8], dtype=int)
    a_arr = sp.symbols(' '.join(["alpha{:d}".format(j) for j in a_indices]), real=True)
    alpha2_vec = sp.MutableDenseNDimArray.zeros(9)
    for j in range(a_indices.size): alpha2_vec[[a_indices[j]]] = a_arr[j]
    alp_dot_lamb = sp.tensorcontraction(sp.tensorproduct(alpha2_vec, lambs_sym), (0,1)).tomatrix()
    alp_dot_lamb_charpoly = alp_dot_lamb.charpoly(x='x')
    q_expr = alp_dot_lamb_charpoly.subs('x',0)
    p_expr = alp_dot_lamb_charpoly.diff().subs('x',0)
    p_func = sp.lambdify(a_arr, p_expr, 'numpy')
    q_func = sp.lambdify(a_arr, q_expr, 'numpy')
    
    #### Evaluate p and q
    a_arr_nu = np.asarray(alpha2_nonzero_vec)
    assert a_arr_nu.shape[0] == 5
    p_nu = p_func(*a_arr_nu)
    q_nu = q_func(*a_arr_nu)
    
    #### Evaluate eigenvalues of X2_tilde
    A_cos_theta_nu = -q_nu/2.
    A_sin_theta_sq_nu = -(q_nu**2 / 4. + p_nu**3 / 27.)
    assert np.all(A_sin_theta_sq_nu > -1e-14)
    A_sin_theta_nu = np.sqrt(np.abs(A_sin_theta_sq_nu))
    theta_nu = np.arctan2(A_sin_theta_nu, A_cos_theta_nu)
    n = np.arange(-1,2)
    an = np.cos(np.add.outer(2.*np.pi/3.*n, theta_nu/3.))
    alpha_nu = np.linalg.norm(a_arr_nu, axis=0)
    gamma = alpha_nu / (1.j * 3**0.5)
    
    #### Evaluate X2_tilde
    unit_a_arr_nu = unit_vector_of(alpha2_nonzero_vec)
    unit_alpha2_vec_nu = np.zeros((9,)+a_arr_nu.shape[1:], dtype=float)
    unit_alpha2_vec_nu[a_indices] = unit_a_arr_nu
    unit_alpha2_vec_dot_lamb_nu = np.einsum('i...,ijk->jk...',unit_alpha2_vec_nu,lambs)
    X2_tilde = (3**0.5 / 2.) * unit_alpha2_vec_dot_lamb_nu
    
    return gamma, an, X2_tilde


def eval_U2_all_distinct(alpha2_nonzero_vec):
    """
    Evaluate U2 unitary for given nonzero elements of alpha2 vector
    
    The form of $U_2$ assumes $U_2 = exp{X_2}$
    for $X2 \equiv {\gamma}\tilde{X}_{2}$
    where
    $\gamma \equiv alpha / (i \sqrt{3})$ and $\alpha \equiv |\vec{\alpha}_{2}|$
    The $\vec{\alpha}_{2}$ has three zero elements: 
    1st, 5th, 6th (out of 1st ~ 8th elements)
    Thus, only five elements are needed for computing $U_2$
    They are given as the argument of this function `alpha2_nonzero_vec`
    as an ordered 5-tuple : (a2, a3, a4, a7, a8)
    The $U_2 = \exp{X_2}$ is evaluated based on:
    $X2 \equiv \vec{\alpha}_{2} \cdot \hat{\vec{\lambda}} / (2i)$
    where $\hat{\vec{\lambda}}$ is the vector of the SU(3) generators.
    
    # Arguments
    alpha2_nonzero_vec : (5,...) array-like
    """
        
    gamma, an, X2_tilde = _eval_gamma_and_eigvals_for_U2_exponent(alpha2_nonzero_vec)
    D_an = (an[0] - an[1]) * (an[0] - an[2]) * (an[1] - an[2])
    
    X2_tilde_sq_term = 0
    X2_tilde_term = 0
    I_term = 0

    for j in range(3):
        j0,j1,j2 = np.mod(np.arange(3)+j,3)
        X2_tilde_sq_term += np.exp(gamma*an[j0])*(an[j1]-an[j2])
        X2_tilde_term += np.exp(gamma*an[j0])*(an[j1]**2 - an[j2]**2)
        I_term += np.exp(gamma*an[j0])*an[j1]*an[j2]*(an[j1]-an[j2])

    # [NOTE] Be sure to have the minus sign for the X2_tilde term, 
    # which is different from "More Explicit ..."
    U2_is_exp_gamma_X2_tilde = (1./D_an) * ( 
        X2_tilde_sq_term * (X2_tilde @ X2_tilde) 
        - X2_tilde_term * X2_tilde + I_term * np.eye(3) )
    
    return U2_is_exp_gamma_X2_tilde



def _g1(lam,nu,gamma):
    _g1_val = gamma * np.exp((lam+nu)/2.*gamma) * sinhc((lam-nu)/2.*gamma)
    return _g1_val

def _g2(lam,mu,nu,gamma):
    _g2_val = 1./(lam-mu)*(_g1(lam,nu,gamma) - _g1(mu,nu,gamma))
    return _g2_val


def eval_U2_two_can_be_close(alpha2_nonzero_vec):
    """
    For description of this funciton, refer to the docstring of 
    `eval_U2_all_distinct`.
    The valid shape of the argument is more general than that of `eval_U2_all_distinct`
    
    # Arguments
    alpha2_nonzero_vec : (5,...)
    """
    
    gamma, an, X2_tilde = _eval_gamma_and_eigvals_for_U2_exponent(alpha2_nonzero_vec)
#    print(gamma.shape, an.shape, X2_tilde.shape)
    dim = 3
    i_nu = np.argmax([np.abs(an[(iv+1) % dim,...] - an[(iv+2) % dim,...]) for iv in range(3)], axis=0)
#    print(i_nu.shape)
#    nu, lam, mu = an[np.mod(np.add.outer(np.arange(dim),i_nu), dim)]
    nu, lam, mu = np.take_along_axis(an, np.mod(np.add.outer(np.arange(dim),i_nu), dim), axis=0)
#    print(np.add.outer(np.arange(dim),i_nu).shape)
#    print(np.mod(np.add.outer(np.arange(dim),i_nu), dim).shape)
#    print(np.mod(np.add.outer(np.arange(dim),i_nu), dim))
#    print(an[np.mod(np.add.outer(np.arange(dim),i_nu), dim)].shape)
#    print(nu.shape, lam.shape, mu.shape)
    
    g2_lam_mu_nu_gamma = _g2(lam,mu,nu,gamma)
    g1_mu_nu_gamma = _g1(mu,nu,gamma)
    X2_tilde_sq_term = g2_lam_mu_nu_gamma
    X2_tilde_term = (mu+nu)*g2_lam_mu_nu_gamma - g1_mu_nu_gamma
    I_term = np.exp(nu*gamma) - nu*g1_mu_nu_gamma + mu*nu*g2_lam_mu_nu_gamma

    X2_tilde_sq = np.einsum("jk...,kl...->jl...", X2_tilde, X2_tilde)
    
    # [NOTE] Be sure to have the minus sign for the X2_tilde term, 
    # which is different from "More Explicit ..."
    U2_is_exp_gamma_X2_tilde = X2_tilde_sq_term * X2_tilde_sq \
        - X2_tilde_term * X2_tilde + np.multiply.outer(np.eye(3), I_term)
    
    return U2_is_exp_gamma_X2_tilde


