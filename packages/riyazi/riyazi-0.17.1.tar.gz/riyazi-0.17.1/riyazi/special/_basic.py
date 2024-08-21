
"""
convenience 
combinatorics
other special function 
"""

import numpy as np 
from math import pi, sin, log, sqrt
from math import perm,comb
import math
from scipy.integrate import quad 
from itertools import count, islice
from .factorials import binom

def exp(x):
    return math.e**x

def factorial(n):
    if n < 1 :
        return 1
    else:
        return n* factorial(n-1)
    
def combination(m, k):
    if k <=m :
        return factorial(m)/ (factorial(k)* factorial(m-k))
    else:
        return 0


__all__ =['cbrt', 'exp10', 'exp2','radian','cosdg','sindg','tandg','cotdg','log1p','expm1','cosm1', 'powm1',
'around','xlogy','xlog1py','logsumexp','exprel','sinc','perm', 'comb', 'agm','bernoulli', 'diric', 'euler',
'expn', 'exp1', 'expi', 'shichi', 'sici', 'softmax', 'log_softmax', 'spence', 'zeta', 'zetac']

def cbrt(x):
    """ 
    Element-wise cube root of x.
    
    """
    if x<0:
        return (pow(abs(x),1/3)*(-1))
    else:
        return (pow(x,1/3))


def exp10(x):  # *args, **kwargs
    """ 
    	
    Compute 10**x element-wise.
    
    """
    return pow(10,x)

def exp2(x):
    """ 
    Compute 2**x element-wise.
    
    """
    return pow(2,x)


def radian(d,m,s):
    """ 
    	
    Convert from degrees to radians.
     

    Returns the angle given in (d)egrees, (m)inutes, and (s)econds in
    radians.
    
    Parameters
    ----------
    d : 
    Degrees, can be real-valued and imag-valued.
    m : 
    Minutes, can be real-valued and imag-valued.
    s :
    Seconds, can be real-valued and img-valued.
    
    
    
    """
    return (pi)* ((d+(m/60)+(s/3600))/180)


def cosdg(x):
    """ 
    
    Cosine of the angle x given in degrees.
    
    """
    if x == 90:
        return 0.0
    
    x = math.radians(x)
  
    if x is x.real:
        return ((exp(x * 1j) + exp(x * -1j)) / 2).real 
    else:
        return ((exp(x * 1j) + exp(x * -1j)) / 2)

def sindg(x):
    """ 
    Sine of the angle x given in degrees.
    
    """
    x = math.radians(x)
    if x is x.real:
        return ((exp(x*1j) - exp(x*(-1j))) / 2j).real
    else:
        return ((exp(x*1j) - exp(x*(-1j))) / 2j)

def tandg(x):
    """ 
    
    Tangent of angle x given in degrees.
    
    """
    if x == 90:
        return math.inf
    return (sindg(x) / cosdg(x))


def cotdg(x):
    """ 
    
    otangent of the angle x given in degrees.
    
    """
    if x == 90:
        return 0.0
    return 1 / ((sindg(x)/cosdg(x)))

def log1p(x):
    """ 
    Calculates log(1 + x) for use when x is near zero.
    """
    return (math.log(1+x))

def expm1(x):
    """ 
    Compute exp(x) - 1.
    """
    return exp(x)-1

def cosm1(x):
    """ 
    cos(x) - 1 for use when x is near zero.
    """
    return math.cos(x) - 1

def powm1(x,y):
    """
    Computes x**y-1
    
    """
    return pow(x,y)-1


def around(x):
    """ 
    Round to the nearest integer
    """
    return round(x)

def xlogy(x,y):
    """ 
    Compute x*log(y) so that the result is 0 if x = 0.
    """
    return x*math.log(y)

def xlog1py(x,y):
    """ 
    Compute x*log1p(y) so that the result is 0 if x = 0.
    """
    return x*log1p(y)

def logsumexp(x):
    """ 
    Compute the log of the sum of exponentials of input elements.
    """
   
    return np.log(np.sum(np.exp(x)))

def exprel(x):
    """ 
    Relative error exponential, (exp(x) - 1)/x.
    """
    return (exp(x)-1)/x


def sinc(x, method='normalized'):
    """
    Methods:
    1. normalized
    2. unnormalized
    
    """
    if (method == 'normalized'):
        return (sin(pi*x)/(pi*x))
    elif(method =='unnormalized'):
        return (sin(x)/x)
    else:
        return ValueError('method 1 and 2 ')
    
    
# https://en.wikipedia.org/wiki/Arithmetic%E2%80%93geometric_mean

def agm(a, b, tolerance=1e-10):
    """ 
    calculating the arithmetic geometric mean of two number
    
    tolerance the tolerance for the converged
              value of the agm default (value = 1e-10)
    
    """
    an, gn = (a+b)/ 2.0, sqrt(a*b)
    while abs(an - gn) > tolerance:
        an, gn = (an+gn)/2.0, sqrt(an*gn)
    return an 


# https://en.wikipedia.org/wiki/Bernoulli_number

def bernoulli(m):
    if m ==0 :
        return 1
    else:
        t = 0
        for k in range(0, m): 
            t += combination(m,k )*bernoulli(k)/  (m-k +1)
        return 1-t

def diric(x, n) :
    """ 
    Periodic sinc function, also called the Dirichlet function.

    The Dirichlet function is defined as::

    diric(x, n) = sin(x * n/2) / (n * sin(x / 2)),

    where `n` is a positive integer.

    Parameters
    ----------
    x : array_like
    Input data
    n : int
    Integer defining the periodicity.

    Returns
    -------
    diric : ndarray

    Examples
    --------
     """
    return sin(x * n/2) / (n * sin(x / 2))



def euler(n):
    return 0.57721566490153287 



# https://en.wikipedia.org/wiki/List_of_integrals_of_exponential_functions

def expn():
    pass


def exp1(z):
    pass


def expi(x, minfloat=1e-7, maxfloat=10000):
    """Ei integral function."""
    minfloat = min(np.abs(x), minfloat)
    maxfloat = max(np.abs(x), maxfloat)
    def f(t):
        return np.exp(t) / t
    if x > 0:
        return (quad(f, -maxfloat, -minfloat)[0] + quad(f, minfloat, x)[0])
    else:
        return quad(f, -maxfloat, x)[0]


def shichi(x):
    pass


def sici(x):
    pass


def softmax(x):
    return np.exp(x)/sum(np.exp(x))


def log_softmax(x):
    return log(softmax(x))


def spence(z):
    pass



def zeta(s, t=100):
    if s == 1: return complex("inf")
    term = (1 / 2 ** (n + 1) * sum((-1) ** k * binom(n, k) * (k + 1) ** -s 
                                   for k in range(n + 1)) for n in count(0))
    return sum(islice(term, t)) / (1 - 2 ** (1 - s))


def zetac(x):
    return zeta(x)-1

