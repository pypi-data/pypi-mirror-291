"""Routines for plotting"""

import numpy as np
from numpy import meshgrid, asarray

def color_meshes_from_arrays(xarr, yarr, indexing='ij'):
    """
    Create meshes for matplotlib pcolormesh() 
    from two one-dimensional arrays
    """

    _xarr, _yarr = (asarray(_arr) for _arr in [xarr, yarr])
    _x_color_arr, _y_color_arr = (
            np.empty((_arr.size + 1,), dtype=_arr.dtype) 
            for _arr in [_xarr, _yarr])
    _x_color_arr[1:-1], _y_color_arr[1:-1] = (
            0.5 * (_arr[1:] + _arr[:-1]) for _arr in [_xarr, _yarr])
    _x_color_arr[[0,-1]], _y_color_arr[[0,-1]] = (
            _arr[[0,-1]] for _arr in [_xarr, _yarr])
    _x_color_mesh, _y_color_mesh = meshgrid(_x_color_arr, _y_color_arr)

    return _x_color_mesh, _y_color_mesh

