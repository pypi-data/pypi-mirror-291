
"""
=================================================
Power Series (:mod:`numpy.polynomial.polynomial`)
=================================================
This module provides a number of objects (mostly functions) useful for
dealing with polynomials, including a `Polynomial` class that
encapsulates the usual arithmetic operations.  (General information
on how this module represents and works with polynomial objects is in
the docstring for its "parent" sub-package, `numpy.polynomial`).
Classes
-------
.. autosummary::
   :toctree: generated/
   Polynomial
Constants
---------
.. autosummary::
   :toctree: generated/
   polydomain
   polyzero
   polyone
   polyx
Arithmetic
----------
.. autosummary::
   :toctree: generated/
   polyadd
   polysub
   polymulx
   polymul
   polydiv
   polypow
   polyval
   polyval2d
   polyval3d
   polygrid2d
   polygrid3d
Calculus
--------
.. autosummary::
   :toctree: generated/
   polyder
   polyint
Misc Functions
--------------
.. autosummary::
   :toctree: generated/
   polyfromroots
   polyroots
   polyvalfromroots
   polyvander
   polyvander2d
   polyvander3d
   polycompanion
   polyfit
   polytrim
   polyline
See Also
--------
`numpy.polynomial`


__all__ = [
    'polyzero', 'polyone', 'polyx', 'polydomain', 'polyline', 'polyadd',
    'polysub', 'polymulx', 'polymul', 'polydiv', 'polypow', 'polyval',
    'polyvalfromroots', 'polyder', 'polyint', 'polyfromroots', 'polyvander',
    'polyfit', 'polytrim', 'polyroots', 'Polynomial', 'polyval2d', 'polyval3d',
    'polygrid2d', 'polygrid3d', 'polyvander2d', 'polyvander3d']
    
"""

__all__ = ['polyadd', 'polysub', 'polymulx', 'polymul', 'polydiv', 'polypow', 'polyval',
           'polyval2d', 'polyval3d', 'polygrid2d', 'polygrid3d']


import numpy as np 
from . import polyutils as pu



def polyadd(c1, c2):
    """
    Add one polynomial to another.
    Returns the sum of two polynomials `c1` + `c2`.  The arguments are
    sequences of coefficients from lowest order term to highest, i.e.,
    [1,2,3] represents the polynomial ``1 + 2*x + 3*x**2``.
    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of polynomial coefficients ordered from low to high.
    Returns
    -------
    out : ndarray
        The coefficient array representing their sum.
    See Also
    --------
    polysub, polymulx, polymul, polydiv, polypow
    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c1 = (1,2,3)
    >>> c2 = (3,2,1)
    >>> sum = P.polyadd(c1,c2); sum
    array([4.,  4.,  4.])
    >>> P.polyval(2, sum) # 4 + 4(2) + 4(2**2)
    28.0
    """
    return pu._add(c1, c2)

def polysub(c1, c2):
    """
    Subtract one polynomial from another.
    Returns the difference of two polynomials `c1` - `c2`.  The arguments
    are sequences of coefficients from lowest order term to highest, i.e.,
    [1,2,3] represents the polynomial ``1 + 2*x + 3*x**2``.
    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of polynomial coefficients ordered from low to
        high.
    Returns
    -------
    out : ndarray
        Of coefficients representing their difference.
    See Also
    --------
    polyadd, polymulx, polymul, polydiv, polypow
    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c1 = (1,2,3)
    >>> c2 = (3,2,1)
    >>> P.polysub(c1,c2)
    array([-2.,  0.,  2.])
    >>> P.polysub(c2,c1) # -P.polysub(c1,c2)
    array([ 2.,  0., -2.])
    """
    return pu._sub(c1, c2)


def polymulx(c):
    """Multiply a polynomial by x.
    Multiply the polynomial `c` by x, where x is the independent
    variable.
    Parameters
    ----------
    c : array_like
        1-D array of polynomial coefficients ordered from low to
        high.
    Returns
    -------
    out : ndarray
        Array representing the result of the multiplication.
    See Also
    --------
    polyadd, polysub, polymul, polydiv, polypow
    Notes
    -----
    .. versionadded:: 1.5.0
    """
    # c is a trimmed copy
    [c] = pu.as_series([c])
    # The zero series needs special treatment
    if len(c) == 1 and c[0] == 0:
        return c

    prd = np.empty(len(c) + 1, dtype=c.dtype)
    prd[0] = c[0]*0
    prd[1:] = c
    return prd



def polymul(c1, c2):
    """
    Multiply one polynomial by another.
    Returns the product of two polynomials `c1` * `c2`.  The arguments are
    sequences of coefficients, from lowest order term to highest, e.g.,
    [1,2,3] represents the polynomial ``1 + 2*x + 3*x**2.``
    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of coefficients representing a polynomial, relative to the
        "standard" basis, and ordered from lowest order term to highest.
    Returns
    -------
    out : ndarray
        Of the coefficients of their product.
    See Also
    --------
    polyadd, polysub, polymulx, polydiv, polypow
    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c1 = (1,2,3)
    >>> c2 = (3,2,1)
    >>> P.polymul(c1,c2)
    array([  3.,   8.,  14.,   8.,   3.])
    """
    # c1, c2 are trimmed copies
    [c1, c2] = pu.as_series([c1, c2])
    ret = np.convolve(c1, c2)
    return pu.trimseq(ret)



def polydiv(c1, c2):
    """
    Divide one polynomial by another.
    Returns the quotient-with-remainder of two polynomials `c1` / `c2`.
    The arguments are sequences of coefficients, from lowest order term
    to highest, e.g., [1,2,3] represents ``1 + 2*x + 3*x**2``.
    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of polynomial coefficients ordered from low to high.
    Returns
    -------
    [quo, rem] : ndarrays
        Of coefficient series representing the quotient and remainder.
    See Also
    --------
    polyadd, polysub, polymulx, polymul, polypow
    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c1 = (1,2,3)
    >>> c2 = (3,2,1)
    >>> P.polydiv(c1,c2)
    (array([3.]), array([-8., -4.]))
    >>> P.polydiv(c2,c1)
    (array([ 0.33333333]), array([ 2.66666667,  1.33333333])) # may vary
    """
    # c1, c2 are trimmed copies
    [c1, c2] = pu.as_series([c1, c2])
    if c2[-1] == 0:
        raise ZeroDivisionError()

    # note: this is more efficient than `pu._div(polymul, c1, c2)`
    lc1 = len(c1)
    lc2 = len(c2)
    if lc1 < lc2:
        return c1[:1]*0, c1
    elif lc2 == 1:
        return c1/c2[-1], c1[:1]*0
    else:
        dlen = lc1 - lc2
        scl = c2[-1]
        c2 = c2[:-1]/scl
        i = dlen
        j = lc1 - 1
        while i >= 0:
            c1[i:j] -= c2*c1[j]
            i -= 1
            j -= 1
        return c1[j+1:]/scl, pu.trimseq(c1[:j+1])



def polypow(c, pow, maxpower=None):
    """Raise a polynomial to a power.
    Returns the polynomial `c` raised to the power `pow`. The argument
    `c` is a sequence of coefficients ordered from low to high. i.e.,
    [1,2,3] is the series  ``1 + 2*x + 3*x**2.``
    Parameters
    ----------
    c : array_like
        1-D array of array of series coefficients ordered from low to
        high degree.
    pow : integer
        Power to which the series will be raised
    maxpower : integer, optional
        Maximum power allowed. This is mainly to limit growth of the series
        to unmanageable size. Default is 16
    Returns
    -------
    coef : ndarray
        Power series of power.
    See Also
    --------
    polyadd, polysub, polymulx, polymul, polydiv
    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> P.polypow([1,2,3], 2)
    array([ 1., 4., 10., 12., 9.])
    """
    # note: this is more efficient than `pu._pow(polymul, c1, c2)`, as it
    # avoids calling `as_series` repeatedly
    return pu._pow(np.convolve, c, pow, maxpower)


def polyval(x, c, tensor=True):
    """
    Evaluate a polynomial at points x.
    If `c` is of length `n + 1`, this function returns the value
    .. math:: p(x) = c_0 + c_1 * x + ... + c_n * x^n
    The parameter `x` is converted to an array only if it is a tuple or a
    list, otherwise it is treated as a scalar. In either case, either `x`
    or its elements must support multiplication and addition both with
    themselves and with the elements of `c`.
    If `c` is a 1-D array, then `p(x)` will have the same shape as `x`.  If
    `c` is multidimensional, then the shape of the result depends on the
    value of `tensor`. If `tensor` is true the shape will be c.shape[1:] +
    x.shape. If `tensor` is false the shape will be c.shape[1:]. Note that
    scalars have shape (,).
    Trailing zeros in the coefficients will be used in the evaluation, so
    they should be avoided if efficiency is a concern.
    Parameters
    ----------
    x : array_like, compatible object
        If `x` is a list or tuple, it is converted to an ndarray, otherwise
        it is left unchanged and treated as a scalar. In either case, `x`
        or its elements must support addition and multiplication with
        with themselves and with the elements of `c`.
    c : array_like
        Array of coefficients ordered so that the coefficients for terms of
        degree n are contained in c[n]. If `c` is multidimensional the
        remaining indices enumerate multiple polynomials. In the two
        dimensional case the coefficients may be thought of as stored in
        the columns of `c`.
    tensor : boolean, optional
        If True, the shape of the coefficient array is extended with ones
        on the right, one for each dimension of `x`. Scalars have dimension 0
        for this action. The result is that every column of coefficients in
        `c` is evaluated for every element of `x`. If False, `x` is broadcast
        over the columns of `c` for the evaluation.  This keyword is useful
        when `c` is multidimensional. The default value is True.
        .. versionadded:: 1.7.0
    Returns
    -------
    values : ndarray, compatible object
        The shape of the returned array is described above.
    See Also
    --------
    polyval2d, polygrid2d, polyval3d, polygrid3d
    Notes
    -----
    The evaluation uses Horner's method.
    Examples
    --------
    >>> from numpy.polynomial.polynomial import polyval
    >>> polyval(1, [1,2,3])
    6.0
    >>> a = np.arange(4).reshape(2,2)
    >>> a
    array([[0, 1],
           [2, 3]])
    >>> polyval(a, [1,2,3])
    array([[ 1.,   6.],
           [17.,  34.]])
    >>> coef = np.arange(4).reshape(2,2) # multidimensional coefficients
    >>> coef
    array([[0, 1],
           [2, 3]])
    >>> polyval([1,2], coef, tensor=True)
    array([[2.,  4.],
           [4.,  7.]])
    >>> polyval([1,2], coef, tensor=False)
    array([2.,  7.])
    """
    c = np.array(c, ndmin=1, copy=False)
    if c.dtype.char in '?bBhHiIlLqQpP':
        # astype fails with NA
        c = c + 0.0
    if isinstance(x, (tuple, list)):
        x = np.asarray(x)
    if isinstance(x, np.ndarray) and tensor:
        c = c.reshape(c.shape + (1,)*x.ndim)

    c0 = c[-1] + x*0
    for i in range(2, len(c) + 1):
        c0 = c[-i] + c0*x
    return c0


def polyval2d(x, y, c):
    """
    Evaluate a 2-D polynomial at points (x, y).
    This function returns the value
    .. math:: p(x,y) = \\sum_{i,j} c_{i,j} * x^i * y^j
    The parameters `x` and `y` are converted to arrays only if they are
    tuples or a lists, otherwise they are treated as a scalars and they
    must have the same shape after conversion. In either case, either `x`
    and `y` or their elements must support multiplication and addition both
    with themselves and with the elements of `c`.
    If `c` has fewer than two dimensions, ones are implicitly appended to
    its shape to make it 2-D. The shape of the result will be c.shape[2:] +
    x.shape.
    Parameters
    ----------
    x, y : array_like, compatible objects
        The two dimensional series is evaluated at the points `(x, y)`,
        where `x` and `y` must have the same shape. If `x` or `y` is a list
        or tuple, it is first converted to an ndarray, otherwise it is left
        unchanged and, if it isn't an ndarray, it is treated as a scalar.
    c : array_like
        Array of coefficients ordered so that the coefficient of the term
        of multi-degree i,j is contained in `c[i,j]`. If `c` has
        dimension greater than two the remaining indices enumerate multiple
        sets of coefficients.
    Returns
    -------
    values : ndarray, compatible object
        The values of the two dimensional polynomial at points formed with
        pairs of corresponding values from `x` and `y`.
    See Also
    --------
    polyval, polygrid2d, polyval3d, polygrid3d
    Notes
    -----
    .. versionadded:: 1.7.0
    """
    return pu._valnd(polyval, c, x, y)


def polyval3d(x, y, z, c):
    """
    Evaluate a 3-D polynomial at points (x, y, z).
    This function returns the values:
    .. math:: p(x,y,z) = \\sum_{i,j,k} c_{i,j,k} * x^i * y^j * z^k
    The parameters `x`, `y`, and `z` are converted to arrays only if
    they are tuples or a lists, otherwise they are treated as a scalars and
    they must have the same shape after conversion. In either case, either
    `x`, `y`, and `z` or their elements must support multiplication and
    addition both with themselves and with the elements of `c`.
    If `c` has fewer than 3 dimensions, ones are implicitly appended to its
    shape to make it 3-D. The shape of the result will be c.shape[3:] +
    x.shape.
    Parameters
    ----------
    x, y, z : array_like, compatible object
        The three dimensional series is evaluated at the points
        `(x, y, z)`, where `x`, `y`, and `z` must have the same shape.  If
        any of `x`, `y`, or `z` is a list or tuple, it is first converted
        to an ndarray, otherwise it is left unchanged and if it isn't an
        ndarray it is  treated as a scalar.
    c : array_like
        Array of coefficients ordered so that the coefficient of the term of
        multi-degree i,j,k is contained in ``c[i,j,k]``. If `c` has dimension
        greater than 3 the remaining indices enumerate multiple sets of
        coefficients.
    Returns
    -------
    values : ndarray, compatible object
        The values of the multidimensional polynomial on points formed with
        triples of corresponding values from `x`, `y`, and `z`.
    See Also
    --------
    polyval, polyval2d, polygrid2d, polygrid3d
    Notes
    -----
    .. versionadded:: 1.7.0
    """
    return pu._valnd(polyval, c, x, y, z)



def polygrid2d(x, y, c):
    """
    Evaluate a 2-D polynomial on the Cartesian product of x and y.
    This function returns the values:
    .. math:: p(a,b) = \\sum_{i,j} c_{i,j} * a^i * b^j
    where the points `(a, b)` consist of all pairs formed by taking
    `a` from `x` and `b` from `y`. The resulting points form a grid with
    `x` in the first dimension and `y` in the second.
    The parameters `x` and `y` are converted to arrays only if they are
    tuples or a lists, otherwise they are treated as a scalars. In either
    case, either `x` and `y` or their elements must support multiplication
    and addition both with themselves and with the elements of `c`.
    If `c` has fewer than two dimensions, ones are implicitly appended to
    its shape to make it 2-D. The shape of the result will be c.shape[2:] +
    x.shape + y.shape.
    Parameters
    ----------
    x, y : array_like, compatible objects
        The two dimensional series is evaluated at the points in the
        Cartesian product of `x` and `y`.  If `x` or `y` is a list or
        tuple, it is first converted to an ndarray, otherwise it is left
        unchanged and, if it isn't an ndarray, it is treated as a scalar.
    c : array_like
        Array of coefficients ordered so that the coefficients for terms of
        degree i,j are contained in ``c[i,j]``. If `c` has dimension
        greater than two the remaining indices enumerate multiple sets of
        coefficients.
    Returns
    -------
    values : ndarray, compatible object
        The values of the two dimensional polynomial at points in the Cartesian
        product of `x` and `y`.
    See Also
    --------
    polyval, polyval2d, polyval3d, polygrid3d
    Notes
    -----
    .. versionadded:: 1.7.0
    """
    return pu._gridnd(polyval, c, x, y)


def polygrid3d(x, y, z, c):
    """
    Evaluate a 3-D polynomial on the Cartesian product of x, y and z.
    This function returns the values:
    .. math:: p(a,b,c) = \\sum_{i,j,k} c_{i,j,k} * a^i * b^j * c^k
    where the points `(a, b, c)` consist of all triples formed by taking
    `a` from `x`, `b` from `y`, and `c` from `z`. The resulting points form
    a grid with `x` in the first dimension, `y` in the second, and `z` in
    the third.
    The parameters `x`, `y`, and `z` are converted to arrays only if they
    are tuples or a lists, otherwise they are treated as a scalars. In
    either case, either `x`, `y`, and `z` or their elements must support
    multiplication and addition both with themselves and with the elements
    of `c`.
    If `c` has fewer than three dimensions, ones are implicitly appended to
    its shape to make it 3-D. The shape of the result will be c.shape[3:] +
    x.shape + y.shape + z.shape.
    Parameters
    ----------
    x, y, z : array_like, compatible objects
        The three dimensional series is evaluated at the points in the
        Cartesian product of `x`, `y`, and `z`.  If `x`,`y`, or `z` is a
        list or tuple, it is first converted to an ndarray, otherwise it is
        left unchanged and, if it isn't an ndarray, it is treated as a
        scalar.
    c : array_like
        Array of coefficients ordered so that the coefficients for terms of
        degree i,j are contained in ``c[i,j]``. If `c` has dimension
        greater than two the remaining indices enumerate multiple sets of
        coefficients.
    Returns
    -------
    values : ndarray, compatible object
        The values of the two dimensional polynomial at points in the Cartesian
        product of `x` and `y`.
    See Also
    --------
    polyval, polyval2d, polygrid2d, polyval3d
    Notes
    -----
    .. versionadded:: 1.7.0
    """
    return pu._gridnd(polyval, c, x, y, z)


