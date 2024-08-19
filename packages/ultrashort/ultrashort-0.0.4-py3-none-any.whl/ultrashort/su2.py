"""Routines for SU(2)-related operations"""

import sympy as sp
import numpy as np
from numpy import asarray, pi, sinc, cos, sin


sigma_1 = sp.Matrix([[0, 1], [1, 0]])
sigma_2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sigma_3 = sp.Matrix([[1, 0], [0, -1]])


sigvec = np.array([
    [
        [0, 1],
        [1, 0]
    ],
    [
        [0, -1.j],
        [1.j, 0]
    ],
    [
        [1, 0],
        [0, -1]
    ]
])



def eval_exp_alpha_dot_sigma_over_2i(alpha_vec):
    
    _alpha_vec = asarray(alpha_vec)
    _len_three_axis_index = 0
    assert _alpha_vec.shape[_len_three_axis_index] == 3
    _alpha = np.linalg.norm(_alpha_vec, axis=_len_three_axis_index)
    
    _eye = np.eye(2)
    _sigmas = np.empty((3,2,2), dtype=np.complex)
    _sigmas[0] = np.array([[0,1],[1,0]], dtype=np.complex)
    _sigmas[1] = np.array([[0,-1j],[1j,0]], dtype=np.complex)
    _sigmas[2] = np.array([[1,0],[0,-1]], dtype=np.complex)
        
    _alpha_dot_sigma = np.einsum('i...,ijk->...jk', _alpha_vec, _sigmas)

    _exp_alpha_dot_sigma_over_2i = np.multiply.outer(cos(_alpha/2.),_eye) \
        + np.einsum('...jk,...->...jk',
                _alpha_dot_sigma/(2.j),sinc(_alpha/(2.*pi)))
    
    return _exp_alpha_dot_sigma_over_2i


