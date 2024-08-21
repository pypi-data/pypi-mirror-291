
"""
# Utility functions

**Conversion and printing**
- mpmathify() / convert()
- nstr()

**Arithmetic operations**
- fadd()
- fsub()
- fneg()
- fmul()
- fdiv()
- fmod()
- fsum()
- fprod()
- fdot()

**Complex components**
- fabs()
- sign()
- re()
- im()
- arg()
- conj()
- polar()
- rect()

**Integer and fractional parts**
- floor()
- ceil()
- nint()
- frac()

**Tolerances and approximate comparisons
- chop()
- almosteq()

**Properties of numbers
- isinf()
- isnan()
- isnormal()
- isfinite()
- isint()
- ldexp()
- frexp()
- mag()
- nint_distance()

**Number generation**
- fraction()
- rand()
- arange()
- linspace()

*Precision management**
- autoprec()
- workprec()
- workdps()
- extraprec()
- extradps()

**Performanance and debugging**
- memoize()
- maxcalls()
- monitor()
- timing()
"""
def _fix_real_lt_zero(x):
    """Convert `x` to complex if it has real, negative components.

    Otherwise, output is just the array version of the input (via asarray).

    Parameters
    ----------
    x : array_like

    Returns
    -------
    array

    Examples
    --------
    >>> np.lib.scimath._fix_real_lt_zero([1,2])
    array([1, 2])

    >>> np.lib.scimath._fix_real_lt_zero([-1,2])
    array([-1.+0.j,  2.+0.j])

    """
    x = asarray(x)
    if any(isreal(x) & (x < 0)):
        x = _tocomplex(x)
    return x

def _tocomplex(arr):
    """Convert its input `arr` to a complex array.

    The input is returned as a complex array of the smallest type that will fit
    the original data: types like single, byte, short, etc. become csingle,
    while others become cdouble.

    A copy of the input is always made.

    Parameters
    ----------
    arr : array

    Returns
    -------
    array
        An array with the same input data as the input but in complex form.

    Examples
    --------

    First, consider an input of type short:

    >>> a = np.array([1,2,3],np.short)

    >>> ac = np.lib.scimath._tocomplex(a); ac
    array([1.+0.j, 2.+0.j, 3.+0.j], dtype=complex64)

    >>> ac.dtype
    dtype('complex64')

    If the input is of type double, the output is correspondingly of the
    complex double type as well:

    >>> b = np.array([1,2,3],np.double)

    >>> bc = np.lib.scimath._tocomplex(b); bc
    array([1.+0.j, 2.+0.j, 3.+0.j])

    >>> bc.dtype
    dtype('complex128')

    Note that even if the input was complex to begin with, a copy is still
    made, since the astype() method always copies:

    >>> c = np.array([1,2,3],np.csingle)

    >>> cc = np.lib.scimath._tocomplex(c); cc
    array([1.+0.j,  2.+0.j,  3.+0.j], dtype=complex64)

    >>> c *= 2; c
    array([2.+0.j,  4.+0.j,  6.+0.j], dtype=complex64)

    >>> cc
    array([1.+0.j,  2.+0.j,  3.+0.j], dtype=complex64)
    """
    if issubclass(arr.dtype.type, (nt.single, nt.byte, nt.short, nt.ubyte,
                                   nt.ushort, nt.csingle)):
        return arr.astype(nt.csingle)
    else:
        return arr.astype(nt.cdouble)


def _fix_int_lt_zero(x):
    """Convert `x` to double if it has real, negative components.

    Otherwise, output is just the array version of the input (via asarray).

    Parameters
    ----------
    x : array_like

    Returns
    -------
    array

    Examples
    --------
    >>> np.lib.scimath._fix_int_lt_zero([1,2])
    array([1, 2])

    >>> np.lib.scimath._fix_int_lt_zero([-1,2])
    array([-1.,  2.])
    """
    x = asarray(x)
    if any(isreal(x) & (x < 0)):
        x = x * 1.0
    return x


def _fix_real_abs_gt_1(x):
    """Convert `x` to complex if it has real components x_i with abs(x_i)>1.

    Otherwise, output is just the array version of the input (via asarray).

    Parameters
    ----------
    x : array_like

    Returns
    -------
    array

    Examples
    --------
    >>> np.lib.scimath._fix_real_abs_gt_1([0,1])
    array([0, 1])

    >>> np.lib.scimath._fix_real_abs_gt_1([0,2])
    array([0.+0.j, 2.+0.j])
    """
    x = asarray(x)
    if any(isreal(x) & (abs(x) > 1)):
        x = _tocomplex(x)
    return x