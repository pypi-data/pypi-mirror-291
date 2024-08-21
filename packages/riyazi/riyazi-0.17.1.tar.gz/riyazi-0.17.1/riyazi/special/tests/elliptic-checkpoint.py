

__all__ = ['ellipj','ellipk','ellipkm1','ellipkinc',
'ellipe','ellipeinc','elliprc','elliprd','elliprf',
'elliprg','elliprj']

from math import pi
import mpmath 
def ellipkm1(m):
    return (pi/2)* mpmath.hyp2f1(0.5,0.5,1,1-m)

from math import pi
import mpmath 
def ellipe(m):
    return (pi/2)* mpmath.hyp2f1(0.5,-0.5,1,m)


from math import pi
import mpmath 
def ellipk(m):
    return (pi/2)* mpmath.hyp2f1(0.5,0.5,1,m)



import math

def elliptic_nome(q=None, m=None, k=None, τ=None, q̄=None):
    if q is not None:
        return q
    elif m is not None:
        return math.sqrt(m)
    elif k is not None:
        return math.sin(math.pi * k**2)
    elif τ is not None:
        return math.exp(math.pi * math.sqrt(-1) * τ / 2)
    elif q̄ is not None:
        return math.sqrt(q̄)
    else:
        raise ValueError('One of the parameters q, m, k, τ, or q̄ must be provided')



import math
from cmath import sqrt,exp

def dedekind_eta(τ):
    q = exp(math.pi * sqrt(-1) * τ / 2)
    result = q**(1/24)
    n = 1
    while True:
        term = 1 - q**n
        if abs(term) < 1e-10:
            break
        result *= term
        n += 1
    return result




def kleinj(a, b):
    return 256 * (4 * a**3) / (4 * a**3 - 27 * b**2)

def kleinj(a, b):
    return 256 * (4 * a**3) / (4 * a**3 - 27 * b**2)


import math
def jacobi_elliptic(q, k, function):
    if function == 'sn':
        return math.sqrt(1 - k**2 * math.sin(math.pi * q)**2)
    elif function == 'cn':
        return math.sqrt(1 - k**2 * math.sin(math.pi * q)**2) / math.cos(math.pi * q)
    elif function == 'dn':
        return math.sqrt(1 - k**2 * math.sin(math.pi * q)**2) / math.cos(math.pi * q / 2)
    elif function == 'nc':
        return math.cos(math.pi * q) / math.sqrt(1 - k**2 * math.sin(math.pi * q)**2)
    else:
        raise ValueError('Invalid function')
    
    
    
