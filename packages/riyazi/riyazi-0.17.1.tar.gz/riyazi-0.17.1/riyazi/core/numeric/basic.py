__all__ = ['_add', '_sub', '_mul', '_div', '_sqrt', '_square', '_power', '_table', '_fabonaci', '_fab', 
  '_fabs', '_factorial', '_is_prime', '_root', '_lerp', '_compound_interest', '_Heron', '_is_triangle',
  '_factors', '_Triangle', '_solve_quad', '_gcd', '_lcm', '_sign', '_theta', '_ceil', '_fmod', '_exp',
  '_remainder','_radians','_modf','_degrees','_expm1','_comb','_perm','_copysign','_dist','_ldexp', '_frexp',
  '_fsum','_isqrt','_trunc','inf','_isfinite','_isinf','nan','_isnan','_erf','_erfc','_successor',
  '_predecessor','_zeta','_is_complex','_is_real','_transform','_erfi','_product','_isEven','_isOdd',
  '_isPrime','tau','pi','eta','e','gammas','gamma','_integrand','_hypot','_norm','_unitvector','_relu',
  '_sum_of_series','_celsius','_fahrenheit','_gaussian','_sigmoid','_infj','_nanj','_polynomial' ]  
    

"""  

def sqrt(x):
    # complex number handle 
    if(type(x) == complex):
        return  (pow(-x,0.5j)*1j)
    # negative number handle 
    if x is x.real:
        if ( x <= 0  ):
            return abs(x**0.5)* 1j
        else:
            return pow(x,0.5) # non-negative number handle 


"""
def hcf():
    pass

inf = type(float('inf'))
nan = (float('nan'))
_infj = complex('infj')
_nanj = complex('nanj')

# Constants
tau = 6.28318530717958647
pi = 3.1415926535897932
eta = pi / 2
e = 2.71828182845904523
gammas = 0.57721566490153286

from scipy.integrate import quad
from math import e 
from math import gamma # , sqrt
import math 
from math import inf 
from math import sqrt
from cmath import tau #sqrt as csqrt, tau 
import numpy as np
from numpy import exp, pi , sqrt

def _conjugate(x):
    return complex(x.real, -x.imag)

def _conj(x):
    return complex(x.real,-x.imag)

def _prod(iterable,/,*,start=1):
    prod =1.0 
    for num in iterable:
        prod *=num
    return prod*start 







# Addition program
def _add(*args):
    sum = 0
    for x in args:
        sum +=x 
    return sum 

# Subtraction program
def _sub(a,b):
    return a-b

# Multiplication program
def _mul(a,b):
    return a*b

# Division program 
def _div(a,b):
    return a/b

# square root of x 
def _sqrt(x):
    if(type(x) == complex):
        return (-1*x)**0.5*1j
    if x is x.real:
        if ( x <= 0  ):
            return abs(x**0.5)* 1j
        else:
            return x**0.5


# Find Out Square  of x.
def _square(x):
    return pow(x,x)


# Find Out Power of a raised to the power x. 
def  _power(a,x):
    return pow(a,x)


# print the table of any numbers. 
def _table(x, rng ):
    for i in range(1,rng):
        n = x*i
        print(x, "*",i, "=", n)
        

# print the Fibonaci series 
def _fabonaci(n):
    a,b = 0,1
    while a<n:
        print(a, end=' ')
        a,b = b, a+b
        
# Fibonaci 
def _fab(n):
    return _fabonaci(n)

# Floating absolute 
def _fabs(x,/):
    return float(abs(x))


# Find factorial of n!
def _factorial(n):
    if n<0:
        raise ValueError('you must enter a non-negative integer')
    factorial=1
    for i in range(2,n+1):
        factorial *=i
    return factorial

def _is_prime(n):
    if n==2:
        return 1
    if n<2 or n%2==0:
        return 0
    i=3
    while i*i<=n:
        if n%i==0:
            return 0
        i+=2
    return 1

def _root(n, root=2):
    return pow(n,1/root)

def _lerp(num1, num2, t):
    return num1 + ((num2 -num1)*t)

def _compound_interest(principal,rate,years):
    amount=principal*(1+rate/100)**years
    return amount


def _Heron(a,b,c):
    s=(a+b+c)/2.0
    A=_sqrt(s*(s-a)*(s-b)*(s-c))
    return A

def _is_triangle(a,b,c):
    if(a+b>c and a+c>b and b+c>a):
        return True
    else:
        return False


def _factors(a):
    for i in range(1, a+1):
        if a % i == 0:
            lists = ( print(i))
    return lists 

def _Triangle(a,b,c):
    if(a+b>c and a+c>b and b+c>a):
        if(a==b and b==c):
            print("Equalteral triangle")
        elif (a==b or b==c or a==c):
            print("Isoceles triangle")
        else:
            print("scalene triangle")
    else:
        print("Not a triangle")
        

def _solve_quad(a,b,c):
    if(a==b):
        if(b!=0):
            x1= -c/b
            print(f"it has only one root, x1 ={x1}")
        else:
            print("it has no root")
    else:
        d=b**2-4*a*c
        if(d>0):
            print('Roots are real')
            x1=(-b+sqrt(b**2-4*a*c))/(2*a)
            x2=(-b-sqrt(b**2-4*a*c))/(2*a)
            print(f'The roots of are {x1} and {x2}')
        
def _gcd(*integers):
    if len(integers) <= 1:
        return integers[0]
    n, k, *others = integers
    if k > n:
        n, k = k, n
    while k != 0:
        k, n = n % k, k
    return _gcd(n, *others)



def _lcm(*integers):
    """Least Common Multiple."""
    args_max = max(integers)
    n = 1
    while True:
        for k in integers:
            if args_max * n % k != 0:
                n += 1
                break
        else:
            return args_max * n

def _sign(x):
    return x / -x

def _theta(x):
    if 0 < x:
        return 1
    else:
        return 0
    
    
def _ceil(x,/):
    if (int == type(x)):
        return x 
    elif (float == type(x)):
        i= int(x)
        if(x == i):
            return i
        else:
            
            return (i+1)

def _fmod(x,y,/):
    z =float (x%y) 
    return z 


def _exp(x,/):
    if x is x.imag:
        return pow(e,2+0j)
    else:
        x = pow(e,x)
        return x 
    
def _remainder(x,y,/):
    r = x%y
    c = int (-1 * (y/r))
    print("(remainder, Difference closest integer multiply of y.)")
    return r,c

def _radians(x,/):
    r= 0.017453292519943295
    return (x*r)  # degree / (180 / pi)


def _modf(x):
    a = int(x)
    b = (x%a)
    x = float(a)
    decimal_places='%.1f'
    b = float(decimal_places %b)
    return  b, x

def _degrees(x,/):
    dv = 57.29577951308232
    return (x*dv)


def _expm1(x,/):
    x = _exp(x)-1
    return x 

def _comb(n,k):
    if (n >= k):
        minus = (n-k)
        n = _factorial(n)
        k = _factorial(k)* _factorial(minus)
        return ((n/k))
    else:
        return 0


def _perm(n,k):
    if(n >= k):
        minus = (n-k)
        n = _factorial(n)
        k = _factorial(minus)
        return (n/k)
    else:
        return 0.0
    

def _copysign(x,y):
    if(y<=0):
        return (abs(x)*(-1))
    else:
        return float(abs(x))   

def _dist(p,q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))     


def _ldexp(x,i,/):
    return (float (x*(2**i)))

def _frexp(x,/):
    pass



def _fsum(seq):
    return float(sum(seq))


def _isqrt(x):
    return int(pow(x,0.5))

def _trunc(x):
    return int(x)


def _isfinite(x,/):
    if(x == inf):
        return False 
    else:
        return True 
 
        
def _isinf(x,/):
    if(x == inf):
        return True 
    else:
        return False


def _isnan(x,/):
    if (x != x):
        return True
    else:
        return False


def _erf(z):
    t = 1.0 / (1.0 + 0.5 * abs(z))
        # use Horner's method
    ans = 1 - t * math.exp( -z*z -  1.26551223 +
                            t * ( 1.00002368 +
                            t * ( 0.37409196 + 
                            t * ( 0.09678418 + 
                            t * (-0.18628806 + 
                            t * ( 0.27886807 + 
                            t * (-1.13520398 + 
                            t * ( 1.48851587 + 
                            t * (-0.82215223 + 
                            t * ( 0.17087277))))))))))
    if z >= 0.0:
        return ans
    else:
        return -ans


def _erfc(x):
    return 1 - math.erf(x)


def _successor(x):
    x = x+1 
    return x 

def _predecessor(x):
    x = x-1
    return x 

def _zeta(x):
    """
    "zeta(x)" returns the value of ζx.
    """
    if x == 1:
        return inf
    a = [0.5 / (1 - (2 ** (1 - x)))]
    b = [a[0]]
    for n in range(1, 200):
        for k in range(n):
            a[k] = a[k] * n / (n - k) / 2
        a += [-(n / (n + 1)) ** x * a[-1] / n]
        b += [sum(a)]
        if 1.0e+4 < abs(b[-1]) < 1.0e-6:
             break           
    return sum(b)

def _is_complex(_x):
    """
    "complex(x)" returns whether x is a complex number.
    """
    try:
        a = _x.imag
        if a == 0:
            return False
        else:
            return True
    except:
        return True



def _is_real(x):
    try:
        a =x.real
        if a == 0:
            return False
        else:
            return True
    except:
        return True


def _transform(p):
    x,y  = p
    x1 = y + 1.0 - 1.4*x**2
    y1 = 0.3*x

    return x1, y1

def _erfi(x : float) -> float:
    """Calculates  the imaginary error function at a specific point"""
    MULTIPLIER = 2 / math.sqrt(math.pi)
    total = 0
    for n in range(100):
        denominator = math.factorial(n) * (2*n+1)
        nominator = pow(x,2*n+1)
        total += nominator / denominator
    return MULTIPLIER * total

def _product(*args):
    """Returns the product of float or ints
        product(3,4,5) -> 60
        product(*[3,4,5]) -> 60
    """
    prod = 1
    for num in args:
        prod*=num
    return prod

def _isEven(num : int) -> bool:
    """Returns True if a number can be divded by 2"""
    return num%2==0

def _isOdd(num : int) -> bool:
    """Returns True if a number cannot be divded by 2"""
    return not _isEven(num)


def _isPrime(num : int) -> bool:
    """Returns True if a number can divide num in the \n
       ** range(2,int(1+num**(1/2))) **
       """
    if num == 1:
        return False

    for i in range(2,int(1+num**(1/2))):
        if(num%i==0):
            return False
    return True


def _gamma(num: float) -> float:
    if num <= 0:
        raise ValueError("math domain error")

    return quad(_integrand, 0, inf, args=(num))[0]


def _integrand(x: float, z: float) -> float:
    return math.pow(x, z - 1) * math.exp(-x)


def _hypot(*coordinates):
    return math.sqrt(sum(x**2 for x in coordinates))


def _norm(x):
    return math.sqrt(sum(x**2 for x in x ))



def _unitvector(x):
    xnorm = _norm(x)
    if xnorm == 0:
        raise ValueError("Can't normalise vector with length 0")
    return sum(x) / _norm(x)




def _relu(vector: list[float]):
    # compare two arrays and then return element-wise maxima.
    return np.maximum(0, vector)




def _sum_of_series(first_term, common_diff, num_of_terms):
    sums = (num_of_terms / 2) * (2 * first_term + (num_of_terms - 1) * common_diff)
    # formula for sum of series
    return sums


def _celsius(f):
    return (f-32)*(5/9)

def _fahrenheit(c):
    return (c*(9/5)+32)

"""
Reference: https://en.wikipedia.org/wiki/Gaussian_function
"""



def _gaussian(x, mu: float = 0.0, sigma: float = 1.0) -> int:
    return 1 / sqrt(2 * pi * sigma**2) * exp(-((x - mu) ** 2) / (2 * sigma**2))



def _sigmoid(u):
    return 1/(1+math.exp(-u))


def _polynomial(coeff,x):
    deg = len(coeff) -1 
    return sum([c*(x**(deg-i)) for i , c in enumerate(coeff)])




def floor(x) -> int:
    """
    Return the floor of x as an Integral.
    :param x: the number
    :return: the largest integer <= x.
    >>> import math
    >>> all(floor(n) == math.floor(n) for n
    ...     in (1, -1, 0, -0, 1.1, -1.1, 1.0, -1.0, 1_000_000_000))
    True
    """
    return int(x) if x - int(x) >= 0 else int(x) - 1
