""" 
# Elliptic arguments
- qfrom()
- qbarfrom()
- mfrom()
- kfrom()
- taufrom()

# Legendre elliptic integrals
- ellipk()
- ellipf()
- ellipe()
- ellippi()

# Carson symmetric elliptic integrals
- elliprf()
- elliprc()
- elliprj()
- elliprd()
- elliprg()

# Jacobi theta functions
- jtheta()

# jacobi elliptic functions
- ellipfun()

# Modular functions
- eta()
- kleinj()

__all__ = ['ellipj','ellipk','ellipkm1','ellipkinc',
'ellipe','ellipeinc','elliprc','elliprd','elliprf',
'elliprg','elliprj']
"""


from math import pi
import mpmath 
import mpmath as mp

import math

def qfrom(q=None, m=None, k=None, τ=None, q̄=None):
    """Elliptic nome"""
    if q is not None:
        return q
    elif m is not None:
        return math.sqrt(m)
    elif k is not None:
        return math.sin(math.pi * k**2)
    elif τ is not None:
        return math.exp(math.pi * math.sqrt(-1) * τ / 2)
    elif q̄ is not None:
        return math.sqrt(q̄)   # Wrong Output
    else:
        raise ValueError('One of the parameters q, m, k, τ, or q̄ must be provided')

def qbarfrom(q̄=None, q=None, m=None, k=None, τ=None ):
    """Elliptic nome"""
    if q is not None:
        return q
    elif m is not None:
        return math.sqrt(m)
    elif k is not None:
        return math.sin(math.pi * k**2)
    elif τ is not None:
        return math.exp(math.pi * math.sqrt(-1) * τ / 2)
    elif q̄ is not None:
        return float(pow(q̄,2))
    else:
        raise ValueError('One of the parameters q, m, k, τ, or q̄ must be provided')

def mfrom():
    pass


def kfrom():
    pass

def taufrom():
    pass



from math import pi
import mpmath 
def ellipk(m):
    return (pi/2)* mpmath.hyp2f1(0.5,0.5,1,m)

 
def ellipf():
    pass


from math import pi
import mpmath 
def ellipe(m):
    return (pi/2)* mpmath.hyp2f1(0.5,-0.5,1,m)
    

def ellippi():
    pass



def elliprf():
    pass


def elliprc():
    pass


def elliprj():
    pass

def elliprd():
    pass

def elliprg():
    pass

def jtheta():
    pass


def ellipfun():
    pass




def eta(tau):
    
    if rm.is_complex(tau) <= 0.0:
        raise ValueError("eta is only defined in the upper half-plane")
    q = mp.expjpi(tau/12)
    return q* mp.qp(q**24)


def kleinj(a, b):
    return 256 * (4 * a**3) / (4 * a**3 - 27 * b**2)



def ellipkm1(m):
    return (pi/2)* mpmath.hyp2f1(0.5,0.5,1,1-m)






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
    
    
    
