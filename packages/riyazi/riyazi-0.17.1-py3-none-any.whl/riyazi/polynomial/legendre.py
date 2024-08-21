
__all__ = ['legadd', 'legsub', 'legmulx', 'legmul', 'legdiv', 'legpow', 'legval', 'legval2d', 
           'legval3d', 'leggrid2d', 'leggrid3d']

import numpy as np 
from . import polyutils as pu

def legadd(c1, c2):
    """
    Add one Legendre series to another.
    Returns the sum of two Legendre series `c1` + `c2`.  The arguments
    are sequences of coefficients ordered from lowest order term to
    highest, i.e., [1,2,3] represents the series ``P_0 + 2*P_1 + 3*P_2``.
    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of Legendre series coefficients ordered from low to
        high.
    Returns
    -------
    out : ndarray
        Array representing the Legendre series of their sum.
    See Also
    --------
    legsub, legmulx, legmul, legdiv, legpow
    Notes
    -----
    Unlike multiplication, division, etc., the sum of two Legendre series
    is a Legendre series (without having to "reproject" the result onto
    the basis set) so addition, just like that of "standard" polynomials,
    is simply "component-wise."
    Examples
    --------
    >>> from numpy.polynomial import legendre as L
    >>> c1 = (1,2,3)
    >>> c2 = (3,2,1)
    >>> L.legadd(c1,c2)
    array([4.,  4.,  4.])
    """
    return pu._add(c1, c2)


def legsub(c1, c2):
    """
    Subtract one Legendre series from another.
    Returns the difference of two Legendre series `c1` - `c2`.  The
    sequences of coefficients are from lowest order term to highest, i.e.,
    [1,2,3] represents the series ``P_0 + 2*P_1 + 3*P_2``.
    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of Legendre series coefficients ordered from low to
        high.
    Returns
    -------
    out : ndarray
        Of Legendre series coefficients representing their difference.
    See Also
    --------
    legadd, legmulx, legmul, legdiv, legpow
    Notes
    -----
    Unlike multiplication, division, etc., the difference of two Legendre
    series is a Legendre series (without having to "reproject" the result
    onto the basis set) so subtraction, just like that of "standard"
    polynomials, is simply "component-wise."
    Examples
    --------
    >>> from numpy.polynomial import legendre as L
    >>> c1 = (1,2,3)
    >>> c2 = (3,2,1)
    >>> L.legsub(c1,c2)
    array([-2.,  0.,  2.])
    >>> L.legsub(c2,c1) # -C.legsub(c1,c2)
    array([ 2.,  0., -2.])
    """
    return pu._sub(c1, c2)


def legmulx(c):
    """Multiply a Legendre series by x.
    Multiply the Legendre series `c` by x, where x is the independent
    variable.
    Parameters
    ----------
    c : array_like
        1-D array of Legendre series coefficients ordered from low to
        high.
    Returns
    -------
    out : ndarray
        Array representing the result of the multiplication.
    See Also
    --------
    legadd, legmul, legdiv, legpow
    Notes
    -----
    The multiplication uses the recursion relationship for Legendre
    polynomials in the form
    .. math::
      xP_i(x) = ((i + 1)*P_{i + 1}(x) + i*P_{i - 1}(x))/(2i + 1)
    Examples
    --------
    >>> from numpy.polynomial import legendre as L
    >>> L.legmulx([1,2,3])
    array([ 0.66666667, 2.2, 1.33333333, 1.8]) # may vary
    """
    # c is a trimmed copy
    [c] = pu.as_series([c])
    # The zero series needs special treatment
    if len(c) == 1 and c[0] == 0:
        return c

    prd = np.empty(len(c) + 1, dtype=c.dtype)
    prd[0] = c[0]*0
    prd[1] = c[0]
    for i in range(1, len(c)):
        j = i + 1
        k = i - 1
        s = i + j
        prd[j] = (c[i]*j)/s
        prd[k] += (c[i]*i)/s
    return prd


def legmul(c1, c2):
    """
    Multiply one Legendre series by another.
    Returns the product of two Legendre series `c1` * `c2`.  The arguments
    are sequences of coefficients, from lowest order "term" to highest,
    e.g., [1,2,3] represents the series ``P_0 + 2*P_1 + 3*P_2``.
    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of Legendre series coefficients ordered from low to
        high.
    Returns
    -------
    out : ndarray
        Of Legendre series coefficients representing their product.
    See Also
    --------
    legadd, legsub, legmulx, legdiv, legpow
    Notes
    -----
    In general, the (polynomial) product of two C-series results in terms
    that are not in the Legendre polynomial basis set.  Thus, to express
    the product as a Legendre series, it is necessary to "reproject" the
    product onto said basis set, which may produce "unintuitive" (but
    correct) results; see Examples section below.
    Examples
    --------
    >>> from numpy.polynomial import legendre as L
    >>> c1 = (1,2,3)
    >>> c2 = (3,2)
    >>> L.legmul(c1,c2) # multiplication requires "reprojection"
    array([  4.33333333,  10.4       ,  11.66666667,   3.6       ]) # may vary
    """
    # s1, s2 are trimmed copies
    [c1, c2] = pu.as_series([c1, c2])

    if len(c1) > len(c2):
        c = c2
        xs = c1
    else:
        c = c1
        xs = c2

    if len(c) == 1:
        c0 = c[0]*xs
        c1 = 0
    elif len(c) == 2:
        c0 = c[0]*xs
        c1 = c[1]*xs
    else:
        nd = len(c)
        c0 = c[-2]*xs
        c1 = c[-1]*xs
        for i in range(3, len(c) + 1):
            tmp = c0
            nd = nd - 1
            c0 = legsub(c[-i]*xs, (c1*(nd - 1))/nd)
            c1 = legadd(tmp, (legmulx(c1)*(2*nd - 1))/nd)
    return legadd(c0, legmulx(c1))


def legdiv(c1, c2):
    """
    Divide one Legendre series by another.
    Returns the quotient-with-remainder of two Legendre series
    `c1` / `c2`.  The arguments are sequences of coefficients from lowest
    order "term" to highest, e.g., [1,2,3] represents the series
    ``P_0 + 2*P_1 + 3*P_2``.
    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of Legendre series coefficients ordered from low to
        high.
    Returns
    -------
    quo, rem : ndarrays
        Of Legendre series coefficients representing the quotient and
        remainder.
    See Also
    --------
    legadd, legsub, legmulx, legmul, legpow
    Notes
    -----
    In general, the (polynomial) division of one Legendre series by another
    results in quotient and remainder terms that are not in the Legendre
    polynomial basis set.  Thus, to express these results as a Legendre
    series, it is necessary to "reproject" the results onto the Legendre
    basis set, which may produce "unintuitive" (but correct) results; see
    Examples section below.
    Examples
    --------
    >>> from numpy.polynomial import legendre as L
    >>> c1 = (1,2,3)
    >>> c2 = (3,2,1)
    >>> L.legdiv(c1,c2) # quotient "intuitive," remainder not
    (array([3.]), array([-8., -4.]))
    >>> c2 = (0,1,2,3)
    >>> L.legdiv(c2,c1) # neither "intuitive"
    (array([-0.07407407,  1.66666667]), array([-1.03703704, -2.51851852])) # may vary
    """
    return pu._div(legmul, c1, c2)


def legpow(c, pow, maxpower=16):
    """Raise a Legendre series to a power.
    Returns the Legendre series `c` raised to the power `pow`. The
    argument `c` is a sequence of coefficients ordered from low to high.
    i.e., [1,2,3] is the series  ``P_0 + 2*P_1 + 3*P_2.``
    Parameters
    ----------
    c : array_like
        1-D array of Legendre series coefficients ordered from low to
        high.
    pow : integer
        Power to which the series will be raised
    maxpower : integer, optional
        Maximum power allowed. This is mainly to limit growth of the series
        to unmanageable size. Default is 16
    Returns
    -------
    coef : ndarray
        Legendre series of power.
    See Also
    --------
    legadd, legsub, legmulx, legmul, legdiv
    """
    return pu._pow(legmul, c, pow, maxpower)

def legval(x, c, tensor=True):
    """
    Evaluate a Legendre series at points x.
    If `c` is of length `n + 1`, this function returns the value:
    .. math:: p(x) = c_0 * L_0(x) + c_1 * L_1(x) + ... + c_n * L_n(x)
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
        themselves and with the elements of `c`.
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
    values : ndarray, algebra_like
        The shape of the return value is described above.
    See Also
    --------
    legval2d, leggrid2d, legval3d, leggrid3d
    Notes
    -----
    The evaluation uses Clenshaw recursion, aka synthetic division.
    """
    c = np.array(c, ndmin=1, copy=False)
    if c.dtype.char in '?bBhHiIlLqQpP':
        c = c.astype(np.double)
    if isinstance(x, (tuple, list)):
        x = np.asarray(x)
    if isinstance(x, np.ndarray) and tensor:
        c = c.reshape(c.shape + (1,)*x.ndim)

    if len(c) == 1:
        c0 = c[0]
        c1 = 0
    elif len(c) == 2:
        c0 = c[0]
        c1 = c[1]
    else:
        nd = len(c)
        c0 = c[-2]
        c1 = c[-1]
        for i in range(3, len(c) + 1):
            tmp = c0
            nd = nd - 1
            c0 = c[-i] - (c1*(nd - 1))/nd
            c1 = tmp + (c1*x*(2*nd - 1))/nd
    return c0 + c1*x


def legval2d(x, y, c):
    """
    Evaluate a 2-D Legendre series at points (x, y).
    This function returns the values:
    .. math:: p(x,y) = \\sum_{i,j} c_{i,j} * L_i(x) * L_j(y)
    The parameters `x` and `y` are converted to arrays only if they are
    tuples or a lists, otherwise they are treated as a scalars and they
    must have the same shape after conversion. In either case, either `x`
    and `y` or their elements must support multiplication and addition both
    with themselves and with the elements of `c`.
    If `c` is a 1-D array a one is implicitly appended to its shape to make
    it 2-D. The shape of the result will be c.shape[2:] + x.shape.
    Parameters
    ----------
    x, y : array_like, compatible objects
        The two dimensional series is evaluated at the points `(x, y)`,
        where `x` and `y` must have the same shape. If `x` or `y` is a list
        or tuple, it is first converted to an ndarray, otherwise it is left
        unchanged and if it isn't an ndarray it is treated as a scalar.
    c : array_like
        Array of coefficients ordered so that the coefficient of the term
        of multi-degree i,j is contained in ``c[i,j]``. If `c` has
        dimension greater than two the remaining indices enumerate multiple
        sets of coefficients.
    Returns
    -------
    values : ndarray, compatible object
        The values of the two dimensional Legendre series at points formed
        from pairs of corresponding values from `x` and `y`.
    See Also
    --------
    legval, leggrid2d, legval3d, leggrid3d
    Notes
    -----
    .. versionadded:: 1.7.0
    """
    return pu._valnd(legval, c, x, y)


def leggrid2d(x, y, c):
    """
    Evaluate a 2-D Legendre series on the Cartesian product of x and y.
    This function returns the values:
    .. math:: p(a,b) = \\sum_{i,j} c_{i,j} * L_i(a) * L_j(b)
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
        Array of coefficients ordered so that the coefficient of the term of
        multi-degree i,j is contained in `c[i,j]`. If `c` has dimension
        greater than two the remaining indices enumerate multiple sets of
        coefficients.
    Returns
    -------
    values : ndarray, compatible object
        The values of the two dimensional Chebyshev series at points in the
        Cartesian product of `x` and `y`.
    See Also
    --------
    legval, legval2d, legval3d, leggrid3d
    Notes
    -----
    .. versionadded:: 1.7.0
    """
    return pu._gridnd(legval, c, x, y)


def legval3d(x, y, z, c):
    """
    Evaluate a 3-D Legendre series at points (x, y, z).
    This function returns the values:
    .. math:: p(x,y,z) = \\sum_{i,j,k} c_{i,j,k} * L_i(x) * L_j(y) * L_k(z)
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
    legval, legval2d, leggrid2d, leggrid3d
    Notes
    -----
    .. versionadded:: 1.7.0
    """
    return pu._valnd(legval, c, x, y, z)


def leggrid3d(x, y, z, c):
    """
    Evaluate a 3-D Legendre series on the Cartesian product of x, y, and z.
    This function returns the values:
    .. math:: p(a,b,c) = \\sum_{i,j,k} c_{i,j,k} * L_i(a) * L_j(b) * L_k(c)
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
    legval, legval2d, leggrid2d, legval3d
    Notes
    -----
    .. versionadded:: 1.7.0
    """
    return pu._gridnd(legval, c, x, y, z)
