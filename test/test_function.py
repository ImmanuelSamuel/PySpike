""" test_function.py

Tests the PieceWiseConst and PieceWiseLinear functions

Copyright 2014, Mario Mulansky <mario.mulansky@gmx.net>

Distributed under the MIT License (MIT)
"""

from __future__ import print_function
import numpy as np
from copy import copy
from numpy.testing import assert_equal, assert_almost_equal, \
    assert_array_almost_equal

import pyspike as spk

def test_pwc():
    # some random data
    x = [0.0, 1.0, 2.0, 2.5, 4.0]
    y = [1.0, -0.5, 1.5, 0.75]
    f = spk.PieceWiseConstFunc(x, y)
    xp, yp = f.get_plottable_data()
    
    xp_expected = [0.0, 1.0, 1.0, 2.0, 2.0, 2.5, 2.5, 4.0]
    yp_expected = [1.0, 1.0, -0.5, -0.5, 1.5, 1.5, 0.75, 0.75]
    assert_array_almost_equal(xp, xp_expected, decimal=16)
    assert_array_almost_equal(yp, yp_expected, decimal=16)

    assert_almost_equal(f.avrg(), (1.0-0.5+0.5*1.5+1.5*0.75)/4.0, decimal=16)
    assert_almost_equal(f.abs_avrg(), (1.0+0.5+0.5*1.5+1.5*0.75)/4.0,
                        decimal=16)


def test_pwc_add():
    # some random data
    x = [0.0, 1.0, 2.0, 2.5, 4.0]
    y = [1.0, -0.5, 1.5, 0.75]
    f = spk.PieceWiseConstFunc(x, y)

    f1 = copy(f)
    x = [0.0, 0.75, 2.0, 2.5, 2.7, 4.0]
    y = [0.5, 1.0, -0.25, 0.0, 1.5]
    f2 = spk.PieceWiseConstFunc(x, y)
    f1.add(f2)
    x_expected = [0.0, 0.75, 1.0, 2.0, 2.5, 2.7, 4.0]
    y_expected = [1.5, 2.0, 0.5, 1.25, 0.75, 2.25]
    assert_array_almost_equal(f1.x, x_expected, decimal=16)
    assert_array_almost_equal(f1.y, y_expected, decimal=16)

    f2.add(f)
    assert_array_almost_equal(f2.x, x_expected, decimal=16)
    assert_array_almost_equal(f2.y, y_expected, decimal=16)
    
    f1.add(f2)
    # same x, but y doubled
    assert_array_almost_equal(f1.x, f2.x, decimal=16)
    assert_array_almost_equal(f1.y, 2*f2.y, decimal=16)

def test_pwc_mul():
    x = [0.0, 1.0, 2.0, 2.5, 4.0]
    y = [1.0, -0.5, 1.5, 0.75]
    f = spk.PieceWiseConstFunc(x, y)
    
    f.mul_scalar(1.5)
    assert_array_almost_equal(f.x, x, decimal=16)
    assert_array_almost_equal(f.y, 1.5*np.array(y), decimal=16)
    f.mul_scalar(1.0/5.0)
    assert_array_almost_equal(f.y, 1.5/5.0*np.array(y), decimal=16)


def test_pwl():
    x = [0.0, 1.0, 2.0, 2.5, 4.0]
    y1 = [1.0, -0.5, 1.5, 0.75]
    y2 = [1.5, -0.4, 1.5, 0.25]
    f = spk.PieceWiseLinFunc(x, y1, y2)
    xp, yp = f.get_plottable_data()
    
    xp_expected = [0.0, 1.0, 1.0, 2.0, 2.0, 2.5, 2.5, 4.0]
    yp_expected = [1.0, 1.5, -0.5, -0.4, 1.5, 1.5, 0.75, 0.25]
    assert_array_almost_equal(xp, xp_expected, decimal=16)
    assert_array_almost_equal(yp, yp_expected, decimal=16)
    
    avrg_expected = (1.25 - 0.45 + 0.75 + 1.5*0.5) / 4.0
    assert_almost_equal(f.avrg(), avrg_expected, decimal=16)
    
    abs_avrg_expected = (1.25 + 0.45 + 0.75 + 1.5*0.5) / 4.0
    assert_almost_equal(f.abs_avrg(), abs_avrg_expected, decimal=16)


def test_pwl_add():
    x = [0.0, 1.0, 2.0, 2.5, 4.0]
    y1 = [1.0, -0.5, 1.5, 0.75]
    y2 = [1.5, -0.4, 1.5, 0.25]
    f = spk.PieceWiseLinFunc(x, y1, y2)

    f1 = copy(f)
    x = [0.0, 0.75, 2.0, 2.5, 2.7, 4.0]
    y1 = [0.5, 1.0, -0.25, 0.0, 1.5]
    y2 = [0.8, 0.2, -1.0, 0.0, 2.0]
    f2 = spk.PieceWiseLinFunc(x, y1, y2)
    f1.add(f2)
    x_expected = [0.0, 0.75, 1.0, 2.0, 2.5, 2.7, 4.0]
    y1_expected = [1.5, 1.0+1.0+0.5*0.75, -0.5+1.0-0.8*0.25/1.25, 1.5-0.25,
                   0.75, 1.5+0.75-0.5*0.2/1.5]
    y2_expected = [0.8+1.0+0.5*0.75, 1.5+1.0-0.8*0.25/1.25, -0.4+0.2, 1.5-1.0,
                   0.75-0.5*0.2/1.5, 2.25]
    assert_array_almost_equal(f1.x, x_expected, decimal=16)
    assert_array_almost_equal(f1.y1, y1_expected, decimal=16)
    assert_array_almost_equal(f1.y2, y2_expected, decimal=16)

    f2.add(f)
    assert_array_almost_equal(f2.x, x_expected, decimal=16)
    assert_array_almost_equal(f2.y1, y1_expected, decimal=16)
    assert_array_almost_equal(f2.y2, y2_expected, decimal=16)
    
    f1.add(f2)
    # same x, but y doubled
    assert_array_almost_equal(f1.x, f2.x, decimal=16)
    assert_array_almost_equal(f1.y1, 2*f2.y1, decimal=16)
    assert_array_almost_equal(f1.y2, 2*f2.y2, decimal=16)


def test_pwc_mul():
    x = [0.0, 1.0, 2.0, 2.5, 4.0]
    y1 = [1.0, -0.5, 1.5, 0.75]
    y2 = [1.5, -0.4, 1.5, 0.25]
    f = spk.PieceWiseLinFunc(x, y1, y2)
    
    f.mul_scalar(1.5)
    assert_array_almost_equal(f.x, x, decimal=16)
    assert_array_almost_equal(f.y1, 1.5*np.array(y1), decimal=16)
    assert_array_almost_equal(f.y2, 1.5*np.array(y2), decimal=16)
    f.mul_scalar(1.0/5.0)
    assert_array_almost_equal(f.y1, 1.5/5.0*np.array(y1), decimal=16)
    assert_array_almost_equal(f.y2, 1.5/5.0*np.array(y2), decimal=16)

if __name__ == "__main__":
    test_pwc()