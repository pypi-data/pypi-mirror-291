"""Trigonometric functions over a power of x"""

import numpy as np
from numpy import asarray, sin, sinc, pi, square, cos
from scipy.special import factorial


def sinc_handmade(x,delta=1e-3,N=1e2):
    
    _x = asarray(x)
    _x_near_zero_mask = np.abs(_x) < delta
    _x_else_mask = ~_x_near_zero_mask
    _sinc = np.empty_like(_x, dtype=np.float)
    
    _x_else = _x[_x_else_mask]
    _sinc[_x_else_mask] = sin(_x_else) / _x_else
    
    _x_near_zero = _x[_x_near_zero_mask]
    _n = np.arange(N)
    _x_near_zero_mesh, _2n_mesh = np.meshgrid(_x_near_zero, 2*_n, indexing='ij')
    _sinc[_x_near_zero_mask] = np.sum(
            (_x_near_zero_mesh ** _2n_mesh) * ((-1)**_n / factorial(2*_n+1)), 
            axis=-1 )
    
    return _sinc



def two_mul_one_minus_sinc_over_x_sq_handmade(x,delta=1e-3,N=1e2):
    
    _x = asarray(x)
    _x_near_zero_mask = np.abs(_x) < delta
    _x_else_mask = ~_x_near_zero_mask
    _result = np.empty_like(_x, dtype=np.float)
    
    _x_else = _x[_x_else_mask]
    _result[_x_else_mask] = 2 * (1-sinc(_x_else/pi)) / square(_x_else)
    
    _x_near_zero = _x[_x_near_zero_mask]
    _n = np.arange(N)
    _x_near_zero_mesh, _2n_mesh = np.meshgrid(_x_near_zero, 2*_n, indexing='ij')
    _result[_x_near_zero_mask] = 2 * np.sum( 
            (_x_near_zero_mesh ** _2n_mesh) * ((-1)**_n / factorial(2*_n+3)), 
            axis=-1 )
    
    return _result




def one_minus_cos_over_x_sq_handmade(x,delta=1e-3,N=1e2):
    
    _x = asarray(x)
    _x_near_zero_mask = np.abs(_x) < delta
    _x_else_mask = ~_x_near_zero_mask
    _result = np.empty_like(_x, dtype=np.float)
    
    _x_else = _x[_x_else_mask]
    _result[_x_else_mask] = (1-cos(_x_else)) / square(_x_else)
    
    _x_near_zero = _x[_x_near_zero_mask]
    _n = np.arange(N)
    _x_near_zero_mesh, _2n_mesh = np.meshgrid(_x_near_zero, 2*_n, indexing='ij')
    _result[_x_near_zero_mask] = np.sum( 
            (_x_near_zero_mesh ** _2n_mesh) * ((-1)**_n / factorial(2*_n+2)), 
            axis=-1 )
    
    return _result

