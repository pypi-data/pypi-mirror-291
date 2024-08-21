
""" 
# Factorials and gamma functions
# Gamma and related functions


### Regularized lower incomplete gamma function. -> gammainc()

https://en.wikipedia.org/wiki/Incomplete_gamma_function#Properties

http://www.ece.northwestern.edu/local-apps/matlabhelp/techdoc/ref/gamma.html

https://rosettacode.org/wiki/Gamma_function#Python

https://www.sciencedirect.com/topics/mathematics/incomplete-gamma-function


"""
__all__ = [ 'factorial', 'fac', 'factorial2', 'fac2', 'factorialk', 'binom', 'binomial', 
           'gamma', 'rgamma', 'gammaprod', 'loggamma', 'rf', 'ff', 'beta', 'betainc', 
           'superfac', 'hyperfac', 'barnesg', 'psi', 'digamma', 'harmonic', 'gammaln', 'gammasgn',
           'gammainc', 'gammaincinv', 'gammaincc', 'gammainccinv', 'betaln' , 'betaincinv',
           'polygamma', 'multigammaln', 'poch', 'subfactorial']

from math import factorial as _factorial
from math import log 
import math


def factorial(n):
    return _factorial(n)


def fac(n):
    return _factorial(n)



def factorial2(num: int) -> int:
    if not isinstance(num, int):
        raise ValueError("double_factorial() only accepts integral values")
    if num < 0:
        raise ValueError("double_factorial() not defined for negative values")
    value = 1
    for i in range(num, 0, -2):
        value *= i
    return value


def fac2(n):
    """
    Computes the double factorial `x!!`, defined for integers
    `x > 0` by
    """
    if(n == 0 or n == 1):
        return 1.0
    return n*fac2(n-2)


def factorialk(n, k, exact=True):
    
    if exact:
        if n < 1-k:
            return 0
        if n <= 0:
            return 1
        val = 1
        for j in range(n, 0, -k):
            val = val*j
        return val
    else:
        raise NotImplementedError


def binom(n, k):
    v = 1
    for i in range(k):
        v *= (n - i) / (i + 1)
    return v


def binomial(n, k):

    if k>n:
        raise ValueError('Invalid Inputs, ensure that n >= k')
        #function is only defined for n>=k
    if k == 0 or n == k:
        #C(n,0) = C(n,n) = 1, so this is our base case.
        return 1
    if k > n/2:
        #C(n,k) = C(n,n-k), so if n/2 is sufficiently small, we can reduce the problem size.
        return binomial(n,n-k)
    else:
        #else, we know C(n,k) = (n/k)C(n-1,k-1), so we can use this to reduce our problem size.
        return ((n/k)*binomial(n-1,k-1))
    
    
    
    
def gamma(x):
    return factorial(x-1)

def rgamma(x):
    return 1/gamma(x)

# Work with list 
def gammaprod(a,b):
    return gamma(a)/ gamma(b)

def loggamma(x):
    return math.log(gamma(x))



def rf(x,n):
    #return x**gamma(n)
    return gamma(x+n)/ gamma(x)

def ff(x,n):
    return gamma(x+1)/ gamma(x-n+1)


def beta(x,y):
    """
    Computes the beta function,
    `B(x,y) = \Gamma(x) \Gamma(y) / \Gamma(x+y)`.
    The beta function is also commonly defined by the integral
    representation
    """
    return (gamma(x) * gamma(y)) / gamma(x+y)


def betainc(a,b,x1=0,x2=1, regularized=False):
    return beta(a,b)


def superfac(n):
    """
    Computes the superfactorial, defined as the product of
    consecutive factorials
    1.http://oeis.org/A000178
    """
    x = 1
    for i in range(1,n+1):
        x *= factorial(i)
    return float(x) 


def hyperfac(n):
    val = 1
    for i in range(1,n+1):
        val = val* pow(i,i)
    return float(val) 


def barnesg(x):
    """
    Evaluates the Barnes G-function
    """
    return superfac(x-2)



def psi(m,z):
    pass

def digamma(x):
    if x == 0:
        return float("inf")
    if x == float("inf"):
        return 0
    if x < 0:
        return digamma(1-x) - (1/x) - (1/(x+1)) + 1
    result = 0
    while x < 8:
        result -= 1/x
        x += 1
    x = x + 1/2 - 1/2*(3-1/(9*x))**0.5
    return result + math.log(x) - 1/(2*x) - 1/(12*x**2)

# Last number not correct 
def harmonic(n):
    i = 1
    s = 0.0
    for i in range(1,n+1):
        s = s + 1/i
    return s 


# Gamma and related functions
def gammaln(x):
    return math.log(math.gamma(x))


def gammasgn(x):
    if x >= 0:
        return 1.0
    else:
        return -1

def gammainc(z, a=0, b=None, regularized=False):
    return float(math.factorial(z-1))

def gammaincinv(a,y):
    pass 

def gammaincc(a,x):
    pass 

def gammainccinv(a,y):
    pass


def betaln(a,b):
    return log(abs(beta(a,b)))


def betaincinv():
    pass 



def polygamma():
    pass

def multigammaln():
    pass

def poch(z,m):
    return gamma(z+m)/gamma(z)


def subfactorial(n):
    res = 0
    fact = 1
    count = 0
    for i in range(1, n+1):
        fact = fact*i
        if (count % 2 == 0):
            res = res - (1/fact)
        else:
            res = res+ (1/fact)
            
        count += 1
    return fact*(1+res)



# Additional algorithms

from numpy import inf
from scipy.integrate import quad


def _gamma(num: float) -> float:
    """
    https://en.wikipedia.org/wiki/Gamma_function
    In mathematics, the gamma function is one commonly
    used extension of the factorial function to complex numbers.
    The gamma function is defined for all complex numbers except the non-positive
    integers
    >>> gamma(-1)
    Traceback (most recent call last):
        ...
    ValueError: math domain error
    >>> gamma(0)
    Traceback (most recent call last):
        ...
    ValueError: math domain error
    >>> gamma(9)
    40320.0
    >>> from math import gamma as math_gamma
    >>> all(.99999999 < gamma(i) / math_gamma(i) <= 1.000000001
    ...     for i in range(1, 50))
    True
    >>> from math import gamma as math_gamma
    >>> gamma(-1)/math_gamma(-1) <= 1.000000001
    Traceback (most recent call last):
        ...
    ValueError: math domain error
    >>> from math import gamma as math_gamma
    >>> gamma(3.3) - math_gamma(3.3) <= 0.00000001
    True
    """

    if num <= 0:
        raise ValueError("math domain error")

    return quad(integrand, 0, inf, args=(num))[0]


def integrand(x: float, z: float) -> float:
    return math.pow(x, z - 1) * math.exp(-x)

from scipy.special import gamma, gammaincc, exp1
def _gammainc(a, x):
    return exp1(x) if a == 0 else gamma(a)*gammaincc(a, x)
