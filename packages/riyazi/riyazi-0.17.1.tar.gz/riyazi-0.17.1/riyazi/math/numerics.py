from ..core.numeric.basic import (_add, _sub, _mul, _div, _sqrt, _square, _power, _table, _fabonaci, _fab, 
                                 _fabs, _factorial, _is_prime, _root, _lerp, _compound_interest, _Heron, _is_triangle,
                                  _factors, _Triangle, _solve_quad, _gcd, _lcm, _sign, _theta, _ceil, _fmod, _exp,
                                   _remainder,_radians,_modf, _degrees ,_expm1, _comb, _perm, _copysign, _dist, _ldexp, _frexp,
                                  _fsum, _isqrt, _trunc, inf, _isfinite, _isinf, nan, _isnan, _erf, _erfc, _successor,
                                  _predecessor, _zeta, _is_complex, _is_real, _transform, _erfi, _product, _isEven, _isOdd,
                                  _isPrime, tau, pi, eta, e, gammas, _gamma, _integrand, _hypot, _norm, _unitvector, _relu,
                                  _sum_of_series, _celsius, _fahrenheit, _gaussian, _sigmoid, _infj, _nanj, _polynomial,
                                  _conj, _conjugate,  _prod,)



def add(**args):
    """
    Addition  program
    >>> add(5,6,7,8)
    >>>  26

    """
    return _add(*args)


def sub(a, b):
    """
    subtraction 
    >>> sub(5,7)
    """
    return _sub(a, b)


def mul(a, b):
    """
    Multiplication 
    >>> mul(4,5)
    """
    return _mul(a, b)


def div(a, b):
    """
    Division program 
    >>> div(a,b)
    
    """
    return _div(a, b)


def sqrt(x):
    """
    Return the square root of x.
    Real and complex arguement 
    
    ``sqrt(x)`` gives the principal square root of `x`, `\sqrt x`.
    or positive real numbers, the principal root is simply the
    positive square root. For arbitrary complex numbers, the principal
    square root is defined to satisfy `\sqrt x = \exp(\log(x)/2)`.
    The function thus has a branch cut along the negative half real axis.

    For all mpmath numbers ``x``, calling ``sqrt(x)`` is equivalent to
    performing ``x**0.5``.

    **Examples**


    >>> from riyazi import* 
    >>> sqrt(4)
    2.0
    >>> sqrt(-4)
    2j
    >>> sqrt(2+3j)
    (1.67414922803554+0.8959774761298382j)
    >>> sqrt(2j+3j)
    (1.5811388300841898+1.5811388300841898j)
    >>> sqrt(-3j) # Result negative some problem

    >>> sqrt(inf)
    inf
    >>> sqrt(-inf)

    Refrence:
    ::
    # Wikipedia
    # --------

    """
    return _sqrt(x)


def square(x):
    """
    Return the square of x. 

    >>> from riyazi import*
    >>> square(2)
    4
    >>> square(2+3j)
    (0.6075666647314784-0.308756018097902j)
    >>> square(2j)
    (0.007927894711475971+0.04248048042515221j)
    >>> square(-2j)
    (0.007927894711475971-0.04248048042515221j)
    >>> square(2j+3j)
    (-7.453816615815512e-05+0.00038098003796102734j)
    >>> square(inf)
    inf
    >>> square(-inf)

    Refrence:
    ::
    # Wikipedia 
    # --------
    """
    return _square(x)


def  power(a, x):
    """
    Return the power of a raised to x . 

    >>> from riyazi import* 
    >>> power(2,3)
    8
    >>> power(-2,3)
    -8
    >>> power(2,-3)
    0.125
    >>> pow(-2,-3)
    -0.125
    >>> power(2j,3j)
    (-0.004374812582252155+0.007846052028917017j)
    >>> power(-2j,-3j)
    (-0.004374812582252155-0.007846052028917017j)
    >>> power(2j,-4)
    (0.0625+0j)
    >>> power(2,-4j)
    (-0.9326870768360711-0.360686590689181j)
    
    Refrence:
    ::
    # Wikipedia
    # ---------
    """
    return _power(a, x)


def table(x,rng=11):
    """
    Return the table of any no. 

    >>> from riyazi import* 
    >>> table (2)
    2 * 1 = 2
    ....
    2 * 10 = 20
    >>> table(-2)
    -2 * 1 = -2
    ....
    -2 * 10 = -20
    >>> table(2j)
    2j * 1 = 2j
    ....
    2j * 10 = 20j
    >>> table(-2j)
    (-0-2j) * 1 = -2j
    ....
    (-0-2j) * 10 = -20j

    Refrence:
    ::
    # Wikipedia

    """
    return _table(x,rng+1)


def fabonaci(n):
    """ 
    >>> rz.math.fabonaci(5)
    0 1 1 2 3
    
    """
    return _fabonaci(n)


def fab(n):
    """ 
    >>> rz.math.fab(10)
    0 1 1 2 3 5 8 
    
    """
    return _fab(n)


def fabs(x):
    """
    Return the absolute value of the float x.

    >>> from riyazi import* 
    >>> fabs(-4)
    4.0
    >>> fabs(2)
    2.0
    >>> fabs(-2j)
    2.0
    >>> fabs(2+3j)
    3.605551275463989
    >>> fabs(2-3j)
    3.605551275463989
    >>> fabs(inf)
    inf
    >>> fabs(-inf)
    inf

    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    """
    return _fabs(x)


def factorial(n):
    """
    Find x!.
    
    Raise a ValueError if x is negative or non-integral.
    
    >>> factorial(0)
    1
    >>> factorial(-1)
    you must enter a non-negative integer
    >>> factorial(2.5) # some error 
    factorial() only accepts integral values

    """
    return _factorial(n)


def is_prime(n):
    """ 
    >>> rz.math.isprime(2)
    True
    >>> rz.math.isprime(4)
    False
    """
    return _is_prime(n)


def root(n, root=2):
    """
    
    ``root(z, n, k=0)`` computes an `n`-th root of `z`, i.e. returns a number
    `r` that (up to possible approximation error) satisfies `r^n = z`.
    (``nthroot`` is available as an alias for ``root``.)

    Every complex number `z \ne 0` has `n` distinct `n`-th roots, which are
    equidistant points on a circle with radius `|z|^{1/n}`, centered around the
    origin. A specific root may be selected using the optional index
    `k`. The roots are indexed counterclockwise, starting with `k = 0` for the root
    closest to the positive real half-axis.

    The `k = 0` root is the so-called principal `n`-th root, often denoted by
    `\sqrt[n]{z}` or `z^{1/n}`, and also given by `\exp(\log(z) / n)`. If `z` is
    a positive real number, the principal root is just the unique positive
    `n`-th root of `z`. Under some circumstances, non-principal real roots exist:
    for positive real `z`, `n` even, there is a negative root given by `k = n/2`;
    for negative real `z`, `n` odd, there is a negative root given by `k = (n-1)/2`.

    To obtain all roots with a simple expression, use
    ``[root(z,n,k) for k in range(n)]``.

    An important special case, ``root(1, n, k)`` returns the `k`-th `n`-th root of
    unity, `\zeta_k = e^{2 \pi i k / n}`. Alternatively, :func:`~mpmath.unitroots`
    provides a slightly more convenient way to obtain the roots of unity,
    including the option to compute only the primitive roots of unity.

    Both `k` and `n` should be integers; `k` outside of ``range(n)`` will be
    reduced modulo `n`. If `n` is negative, `x^{-1/n} = 1/x^{1/n}` (or
    the equivalent reciprocal for a non-principal root with `k \ne 0`) is computed.

    :func:`~mpmath.root` is implemented to use Newton's method for small
    `n`. At high precision, this makes `x^{1/n}` not much more
    expensive than the regular exponentiation, `x^n`. For very large
    `n`, :func:`~mpmath.nthroot` falls back to use the exponential function.

    **Examples**

    find any root like a sqrt(),cbrt() 
    
    >>> from riyazi import * 
    >>> root(8,2)
    2.8284271247461903
    >>> root(8,3) 
    2.0
    >>> root(8,2j)
    2.8284271247461903
    >>> root(8,3j)
    (0.7692389013639722-0.6389612763136348j)

    Refrence:
    ::
    # --------
    
    """
    return _root(n,root)


def lerp(num1, num2, t):
    """ 
    >>> rz.math.lerp(4, 5, 2)
    6
    
    """
    return _lerp(num1, num2, t)


def compound(principal, rate, years):
    """ 
    >>> rz.math.compound(2000, 5, 2)
    2205.0
    
    """
    return _compound_interest(principal, rate, years)


def heron(a, b, c):
    return _Heron(a, b, c)


def is_triangle(a, b, c):
    return _is_triangle(a, b, c)


def factors(a):
    return _factors(a)


def triangle(a, b, c):
    return _Triangle(a, b, c)


def solve_quad(a, b, c):
    return _solve_quad(a, b, c)


def gcd(*integers):
    """
    Greatest Common Divisor.
    
    >>> from riyazi import* 
    >>> gdc(122,12)
    2
    >>> gcd(4,8)
    4
    >>> gcd(2.3,4)
    8.881784197001252e-16
    >>> gcd(2.3,1.2)
    1.1102230246251565e-15
    >>> gcd(-2,4)
    -2
    >>> gcd(-2,-4)
    -2
    >>> gcd(2,-4)
    -2 

    Refrence:
    ::
    # Wikipedia 
    # Wolframe 
    
    """
    return _gcd(*integers)


def lcm(*integers):
    """
     Least Common Multiple.

     >>> from riyazi import * 
     >>> lcm(4,8)
     8
     >>> lcm(2,4,6,8)
     24
     >>> lcm(4,5,2)
     20
     >>> lcm(-2,-4,-8)
     -8
     >>> lcm(-2,4,8)
     8
     >>> lcm(-2,-4,8)
     8

     Refrence:
     ::
     # Wikipedai 
     # Wolframe 
    
    """
    return _lcm(*integers)


def sign(x):
    return _sign(x)


def theta(x):
    return _theta(x)


def ceil(x):
    """
    Return the ceiling of x as an Integral.
    This is the smallest integer >= x.

    >>> from riyazi import* 
    >>> ceil(4.2)
    5
    >>> ceil(3)
    3
    >>> ceil(5.9)
    6
    >>> ceil(-5.9) # error
    >>> ceil(-2.1)
    -1
    >>> ceil(-2.9)
    -2
    >>> ceil(-3.1)
    -2
    >>> ceil(-3.1)
    -2

    Refrence:
    ::
    # Wolframe 
    # Wikipedia

    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    """
    return _ceil(x)


def fmod(x, y, /):
    return _fmod(x, y)


def exp(x):
    """
    Return the e riased  to the power of x. 

    >>> from riyazi import* 
    >>> exp(2)
    7.3890560989306495
    >>> exp(4)
    54.59815003314423
    >>> exp(2j)
    (-0.4161468365471424+0.9092974268256817j)
    >>> exp(-2j)
    (-0.4161468365471424-0.9092974268256817j)
    >>> exp(2+3j)
    (-7.315110094901102+1.0427436562359043j)
    >>> exp(inf)
    inf

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return _exp(x)


def remainder(x, y, /):
    return _remainder(x, y, )


def radians(x):
    """
    Convert angle x from degrees to radians.
    https://en.wikipedia.org/wiki/Radian
    
    >>> from riyazi import* 

    >>> radians(0.3)
    0.005235987755982988
    >>> radians(2)
    0.03490658503988659
    >>> radians(2j)
    0.03490658503988659j
    >>> radians(2+3j)
    (0.03490658503988659+0.05235987755982989j)
    >>> radians(-2j)
    -0.03490658503988659j
    >>> radians(inf)
    inf
    >>> radians(-inf)
    -inf

    Refrence:
    ::
    # Wikipedia
    # Wolframe

    
    """
    return _radians(x)


def modf(x):
    return _modf(x)


def degrees(x, /):
    """
    Convert angle x from radians to degrees.

    >>> degrees(3)
    171.88733853924697
    >>> degrees(pi/2)
    90.0
    >>> degrees(3j)
    171.88733853924697j
    >>> degrees(-3j)
    -171.88733853924697j
    >>> degrees(2+3j)
    (114.59155902616465+171.88733853924697j)
    >>> degrees(inf)
    inf
    >>> degrees(-inf)
    -inf

    Refrence:
    ::

    # Wikipedia
    #  Wolframe 



    """
    return _degrees(x)


def expm1(x,/):
    """
    Return  exp(x)-1.

    This function avoids the loss of precision involved 
    in the direct evaluation of exp(x)-1 for small x.

    >>>from riyazi import*
    >>> expm1(2)

    >>> expm1(pi/2)

    >>> exmp1(2+3j)

    >>> exmp1(2j+3j)

    >>> expm1(-2j)

    >>> expm1(inf)

    >>> exmp1(-inf)

    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    """
  
    return _expm1(x)
    
    
def comb(n,k):
    """
    Number of ways to choose k items from n items without
    repetition and without order.

    Evaluates to n! / (k! * (n - k)!) when k <= n and evaluates
    to zero when k > n.

    Also called the binomial coefficient because it is equivalent
    to the coefficient of k-th term in polynomial expansion of the
    expression (1 + x)**n.

    Raises TypeError if either of the arguments are not integers.
    Raises ValueError if either of the arguments are negative.
    
    ValueError: n must be a non-negative integer
    ValueError: k must be a non-negative integer
    TypeError: 'float' object cannot be interpreted as an integer



    >>> from riyazi import* 
    >>> comb(4,3)
    4.0
    >>> comb(9,2)
    36.0

    Refrence:
    ::
    # Wiki
    # Wolframe

    """
    return _comb(n,k)


def perm(n,k):
    """
    Number of ways to choose k items from n items without 
    repetition and with order.

    Evaluates to n! / (n - k)! when k <= n and evaluates
    to zero when k > n.

    If k is not specified or is None, then k defaults to n
    and the function returns n!.

    Raises TypeError if either of the arguments are not integers.
    Raises ValueError if either of the arguments are negative.
    
    >>> from riyazi import* 
    >>> perm(5,4)
    120.0
    >>> perm(5,2)
    20.0

    Refrence:
    ::
    # Wikipedia
    # Wolframe


    """
    return _perm(n,k)


def copysign(x,y):
    """
    Return a float with the magnitude (absolute value) of x but
    the sign of y.

    >>> from riyazi import*
    >>> copysign(1.0,-0.0)
    -1.0
    >>> copysign(4,3)
    4.0
    >>> copysign(-4,3)
    4.0
    >>> complex number n't handle 

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return _copysign(x,y)


def dist(p,q):
    """
    Return the Euclidean distance between two points p and q.

    The points should be specified as sequences (or iterables) of
    coordinates.  Both inputs must have the same dimension.

    Roughly equivalent to:
    sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    
    >>> from riyazi import* 

    >>> dist([3,4,5].[3,4,2])
    3.0
    >>> dist([3,4,5],[3,4])

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return _dist(p,q)


def ldexp(x,i):
    """
    Return x * (2**i).

    This is essentially the inverse of frexp().
    
    >>> from riyazi import* 
    >>> ldexp(2,2)
    8.0
    >>> ldexp(2,3)
    16.0
    >>> ldexp(2,23)
    16777216.0
    >>> ldexp(2,2.3)
    
    >>> ldexp(2,2j)

    >>> ldexp(2j, 3j)

    >>> ldexp(-2j, 3j)

    >>> ldexp(inf,-inf)

    Refrence:
    ::
    # Wolframe 
    # Wikipedia
     
    
    """
    return _ldexp(x,i)


def frexp(x, /):
    return _frexp(x)


def fsum(seq):
    """
    Return an accurate floating point sum of values in the iterable seq.

    Assumes IEEE-754 floating point arithmetic.
    
    >>> from riyazi  import* 
    >>> fsum([3,4,5])
    12.0
    >>> fsum([3,4,5.4])
    12.4

    Refrence:
    ::
    # Wikipedia
    # Wolframe 
    """
    return _fsum(seq)


def isqrt(x):
    """
    Return the integer part of the square root of the input.

    >>> from riyazi import* 
    >>> isqrt(2)
    1
    >>> isqrt(5)
    2
    >>> isqrt(12)
    3

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return _isqrt(x)


def trunc(x):
    """
    Truncates the Real x to the nearest Integral toward 0.

    Uses the __trunc__ magic method.

    >>> from riyazi import* 
    >>> trunc(24.1)
    24
    >>> trunc(1.9)
    1
    >>> trunc(0.9)
    0

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    
    """
    return _trunc(x)


def isfinite(x):
    """
    Return True if x is neither an infinity nor a NaN,
    and False otherwise.
    >>> from riyazi  import * 
    >>> isifnite(4)
    True
    >>> isfinite(inf)
    False
    >>> isfinite(nan)

    >>> isfinite()


    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    
    """
    return _isfinite(x)


def isinf(x):
    """
    Return True if x is a positive or negative infinity,
     and False otherwise
    
    >>> from riyazi import * 
    >>> isinf(4)
    False
    >>> isinf(inf)
    True
    >>> isinf(nan)
    False 

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    """
    return _isinf(x)


def isnan(x):
    """
    Return True if x is a NaN (not a number), 
    and False otherwise.

    >>> isnan(3)
    False
    >>> isnan(inf)
    False
    >>> isnan(nan)
    True 

    Refrence:
    ::
    # Wikipedia
    # Wolframe 

    
    """
    return _isnan(x)


def erf(z):
    return _erf(z)


def erfc(x):
    return _erfc(x)


def successor(x):
    return _successor(x)


def predecessor(x):
    return _predecessor(x)


def zeta(x):
    return _zeta(x)


def is_complex(_x):
    return _is_complex(_x)


def is_real(x):
    return _is_real(x)


def transform(p):
    return _transform(p)


def erfi(x):
    return _erfi(x)


def product(*args):
    return _product(*args)


def iseven(num):
    return _isEven(num)


def isodd(num):
    return _isOdd(num)


def isprime(num):
    return _isPrime(num)


def gamma(num):
    return _gamma(num)

def integrand(x, z):
    return _integrand(x, z)


def hypot(*coordinates):
    """
    Multidimensional Euclidean distance from the origin to a point.

    Roughly equivalent to:
    sqrt(sum(x**2 for x in coordinates))

    For a two dimensional point (x, y), gives the hypotenuse
    using the Pythagorean theorem:  sqrt(x*x + y*y).

    For example, the hypotenuse of a 3/4/5 right triangle is:

    >>> hypot(3.0, 4.0)
    5.0

    
    """
    return _hypot(*coordinates)


def norm(x):
    return _norm(x)


def unitvector(x):
    """returns a unit vector x/|x|. x needs to be a numpy array."""
    return _unitvector(x)


def relu(vector):
    return _relu(vector)


def sum_of_series(first_term, common_diff, num_of_terms):
    """ 
    
    Find the sum of n terms in an arithmetic progression.

    >>> sum_of_series(1, 1, 10)
    55.0
    >>> sum_of_series(1, 10, 100)
    49600.0
    
    
    """
    return _sum_of_series(first_term, common_diff, num_of_terms)


def celsuis(f):
    return _celsius(f)

def fahrenheit(c):
    return _fahrenheit(c)

def gaussian(x, mu, sigma):
    
    """ 
    Reference: https://en.wikipedia.org/wiki/Gaussian_function
    >>> gaussian(1)
    0.24197072451914337

    >>> gaussian(24)
    3.342714441794458e-126

    >>> gaussian(1, 4, 2)
    0.06475879783294587

    >>> gaussian(1, 5, 3)
    0.05467002489199788

    Supports NumPy Arrays
    Use numpy.meshgrid with this to generate gaussian blur on images.
    >>> import numpy as np
    >>> x = np.arange(15)
    >>> gaussian(x)
    array([3.98942280e-01, 2.41970725e-01, 5.39909665e-02, 4.43184841e-03,
           1.33830226e-04, 1.48671951e-06, 6.07588285e-09, 9.13472041e-12,
           5.05227108e-15, 1.02797736e-18, 7.69459863e-23, 2.11881925e-27,
           2.14638374e-32, 7.99882776e-38, 1.09660656e-43])

    >>> gaussian(15)
    5.530709549844416e-50

    >>> gaussian([1,2, 'string'])
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for -: 'list' and 'float'

    >>> gaussian('hello world')
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for -: 'str' and 'float'

    >>> gaussian(10**234) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    OverflowError: (34, 'Result too large')

    >>> gaussian(10**-326)
    0.3989422804014327

    >>> gaussian(2523, mu=234234, sigma=3425)
    0.0
    """
    return _gaussian(x, mu, sigma)

def sigmoid(u):
    """
    Implements the sigmoid function
    """
    return _sigmoid(u) # 1 / (1 + np.exp(-vector))

def polynomial(coeff, x):
    return _polynomial(coeff, x)

def conj(x):
    return _conj(x)

def conjugate(x):
    return _conjugate(x)

def prod(iterable,/,*,start=1):
    """
    Calculate the product of all the elements in the input iterable.

    The default start value for the product is 1.

    When the iterable is empty, return the start value.  
    This function is
    intended specifically for use with numeric values and may reject
    non-numeric types.
    
    >>> from riyazi import* 
    >>> prod()
    >>> prod()
    
    Refrence:
    ::
    # Wiki
    # Wolframe
    
    """
    return _prod(iterable,start=1)


def abs(num):
    """
    Find the absolute value of a number.

    >>> abs_val(-5.1)
    5.1
    >>> abs_val(-5) == abs_val(5)
    True
    >>> abs_val(0)
    0
    """
    return -num if num < 0 else num

def absolute():
    pass 

def amin(x: list[int]) -> int:
    """
    >>> abs_min([0,5,1,11])
    0
    >>> abs_min([3,-10,-2])
    -2
    >>> abs_min([])
    Traceback (most recent call last):
        ...
    ValueError: abs_min() arg is an empty sequence
    """
    if len(x) == 0:
        raise ValueError("abs_min() arg is an empty sequence")
    j = x[0]
    for i in x:
        if abs(i) < abs(j):
            j = i
    return j

def amax(x: list[int]) -> int:
    """
    >>> abs_max([0,5,1,11])
    11
    >>> abs_max([3,-10,-2])
    -10
    >>> abs_max([])
    Traceback (most recent call last):
        ...
    ValueError: abs_max() arg is an empty sequence
    """
    if len(x) == 0:
        raise ValueError("absmax() arg is an empty sequence")
    j = x[0]
    for i in x:
        if abs(i) > abs(j):
            j = i
    return j

def argmax(x: list[int]) -> int:
    """
    >>> abs_max_sort([0,5,1,11])
    11
    >>> abs_max_sort([3,-10,-2])
    -10
    >>> abs_max_sort([])
    Traceback (most recent call last):
        ...
    ValueError: abs_max_sort() arg is an empty sequence
    """
    if len(x) == 0:
        raise ValueError("absmaxsort() arg is an empty sequence")
    return sorted(x, key=abs)[-1]

def argmin():
    pass 
































































