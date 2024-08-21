# [wolfram](https://functions.wolfram.com/HypergeometricFunctions/)
"""
https://en.wikipedia.org/wiki/List_of_special_functions_and_eponyms


https://en.wikipedia.org/wiki/List_of_mathematical_functions

https://reference.wolfram.com/language/guide/SpecialFunctions.html
https://fungrim.org/topic/Gauss_hypergeometric_function.html

https://en.wikipedia.org/wiki/Hypergeometric_function

https://www.statisticshowto.com/beta-function/#:~:text=The%20incomplete%20beta%20function%20%28also%20called%20the%20Euler,%E2%89%A4%20x%20%E2%89%A4%201%2C%20a%2C%20b%20%3E%200.

https://mathworld.wolfram.com/HypergeometricFunction.html#:~:text=A%20generalized%20hypergeometric%20function%20is%20a%20function%20which,denominator%20is%20present%20for%20historical%20reasons%20of%20notation.%29

https://en.wikipedia.org/wiki/Generalized_hypergeometric_function
https://en.wikipedia.org/wiki/Hypergeometric_distribution
http://www.scientificlib.com/en/Mathematics/LX/GeneralizedHypergeometricFunction.html
def K(k):
    pi_div= 3.1415926535897/2
    return pi_div*(mpmath.hyp2f1(0.5,0.5,1,(k**2)))

def E(k):
    pi_div= 3.1415926535897/2
    return pi_div*(mpmath.hyp2f1(-0.5,0.5,1,(k**2)))

from math import gamma
def barnes(a,b,c,z):
    return ((gamma(a)*gamma(b))/ gamma(c)) *(mpmath.hyp2f1(a,b,c,z))

#https://en.wikipedia.org/wiki/Hypergeometric_function
from math import gamma
def gausum(a,b,c):
    return (gamma(c)*gamma(c-a-b))/ gamma(c-a)*gamma(c-b)
    
__all__ = ['hyp0f0', ' hyp0f1', 'hyp1f1', 'hyp1f2', 'hyp2f1', 'hyp2f2', 'hyp2f3', 'hyp2f0', 'hyp3f2',
           'hyper', 'hypercomb', 'meijerg', 'bihyper', 'hyper2d', 'appellf1', 'appellf2', 'appellf3',
           'appellf4']
"""



from mpmath import hyper 
from math import e
from math import factorial


def hyp0f0(z):
    return (pow(e,z))

def hyp0f0(z):
    x=0
    for k in range(1000):
        x += (pow(z,k)/factorial(k))
    return x 
def hyp0f1(b,z,**kwargs):
    return hyper([],[b],z,**kwargs)


def hyp1f1(a,b,z,**kwargs):
    return hyper([a],[b],z,**kwargs)


def hyp1f2(a1,b1,b2,z,**kwargs):
    return hyper([a1],[b1,b2],z,**kwargs)


def hyp2f1(a,b,c,z,**kwargs):
    return hyper([a,b],[c],z,**kwargs)


def hyp2f2(a1,a2,b1,b2,z,**kwargs):
    return hyper([a1,a2],[b1,b2],z,**kwargs)


def hyp2f3(a1,a2,b1,b2,b3,z,**kwargs):
    return hyper([a1,a2],[b1,b2,b3],z,**kwargs)


def hyp2f0(a,b,z,**kwargs):
    return hyper([a,b],[],z,**kwargs)


def hyp3f2(a1,a2,a3,b1,b2,z,**kwargs):
    return hyper([a1,a2,a3],[b1,b2],z,**kwargs)


