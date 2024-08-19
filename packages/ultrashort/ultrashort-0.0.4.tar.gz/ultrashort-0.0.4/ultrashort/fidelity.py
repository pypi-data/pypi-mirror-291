"""Fidelity"""

import numpy as np

def gate_fidelity(U_target, U, thres=1e-14):
    U_target = np.asarray(U_target)
    assert U_target.ndim >= 2
    dim1, dim0 = U_target.shape[-2:]
    assert dim1 == dim0 and U.shape[-2:] == (dim0, dim0)
    tr_one = dim0
    U_target_dagger = np.einsum('...ij->...ji', np.conj(U_target))
    assert np.abs(np.einsum('...ij,...jk->...ik', U_target_dagger, U_target) - np.eye(dim0)).max() < thres
    fidel = (1/2.) * (1. + (1/tr_one) * np.real(np.einsum('...ij,...ji->...', U_target_dagger, U)))
    assert fidel.max() - 1 < thres
    fidel[fidel > 1] = 1.
    return fidel

def fidel_trace_qudit(U1, U2):
    _U1, _U2 = (np.asarray(U) for U in (U1, U2))
    assert _U1.shape[-2:] == _U2.shape[-2:]
    tr_I = _U1.shape[-1]
    fidel_tr = np.einsum('...ji,...ji->...', _U1.conj(), _U2).real / tr_I
    return fidel_tr

def avg_gate_fidel_qudit(U1, U2):
    _U1, _U2 = (np.asarray(U) for U in (U1, U2))
    assert _U1.shape[-2:] == _U2.shape[-2:]
    d = _U1.shape[-1]
    tr_U1_dagger_U2_over_tr_I = fidel_trace_qudit(_U1, _U2)
    fidel = 1 / (d+1) + d / (d+1) * (tr_U1_dagger_U2_over_tr_I)**2
    return fidel

