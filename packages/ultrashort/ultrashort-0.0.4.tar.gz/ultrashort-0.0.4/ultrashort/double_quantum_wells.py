"""Routines for one-dimensional double quantum wells system"""

import numpy as np
from numpy import cos, exp

def potential_double_quantum_wells(z, a1=6.6, a2=2000, a3=10):
    """
    Evaluate potential in position space
    
    Parameters
    ----------
    z : float or array-like
        Position at which the potential is evaluated
    """
    for _arg in (a1,a2,a3): assert _arg > 0
    _cos_z = cos(a1 * z)
    _abs_cos_z = np.abs(_cos_z)
    _pot = 1/2. * ( 
            ((_abs_cos_z+_cos_z)/2)**0.25 
            - ((_abs_cos_z-_cos_z)/2)**0.25 + 1 
            ) \
        + (exp(a3*np.abs(z)) - 1) / a2
    return _pot

