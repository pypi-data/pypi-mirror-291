from mpmath import hyp1f1,hyp2f1
import scipy.special as sp 

from math import gamma
import mpmath as mp 
import scipy.special as sp
from mpmath import hyp2f1
from scipy.special import poch
from math import gamma


"""


__all__ = ['assoc_laguerre','eval_legendre','eval_chebyt','eval_chebyu',
'eval_chebyc','eval_chebys','eval_jacobi','eval_laguerre','eval_genlaguerre',
'eval_hermite', 'eval_hermitenorm', 'eval_gegenbauer','eval_sh_legendre',
'eval_sh_chebyt','eval_sh_chebyu','eval_sh_jacobi', 
'roots_legendre','roots_chebyt','roots_chebyu','roots_chebyc','roots_chebys',
'roots_jacobi','roots_laguerre','roots_genlaguerre','roots_hermite',
'roots_hermitenorm', 'roots_gegenbauer','roots_sh_legendre','roots_sh_chebyt',
'roots_sh_chebyu','roots_sh_jacobi',
'legendre','chebyt','chebyu','chebyc','chebys','jacobi','laguerre','genlaguerre',
'hermite','hermitenorm','gegenbauer','sh_legendre','sh_chebyt','sh_chebyu','sh_jacobi'

]

"""


# __all__ = ['assoc_laguerre','eval_chebyc','eval_chebys']


def assoc_laguerre(x,n):
    return hyp1f1(-n,1,x)

def eval_chebyc(n,x):
    return 2*sp.eval_chebyt(n,x/2)

def eval_chebys(n,x):
    return sp.eval_chebyu(n,x/2)

def eval_chebyt(n,x):
    return hyp2f1(n, -n, 1/2, (1-x)/2)

def eval_chebyu(n,x):
    return (n+1)* hyp2f1(-n, n+2, 3/2, (1-x)/2)

def eval_gegenbauer(n,alpha,z):
    return (sp.poch(2*alpha,n)/gamma(n+1))*(mp.hyp2f1(-n,2*alpha+n, alpha+(1/2), (1-z)/2))


def eval_genlaguerre(n,alpha,x):
    return sp.binom(n+alpha,n)*mp.hyp1f1(-n,alpha+1,x)

def eval_jacobi(n,alpha,beta,x):
    return (poch(alpha+1,n)/gamma(n+1))* hyp2f1(-n, 1+alpha+beta+n, alpha+1, (1-x)/2) 

def eval_laguerre(n,x):
    return mp.hyp1f1(-n,1,x)

def eval_legendre(n,x):
    return hyp2f1(-n, n+1, 1, (1-x)/2)

def eval_sh_chebyt(n,x):
    return sp.eval_chebyt(n,2*x-1)


def eval_sh_chebyu(n,x):
    return sp.eval_chebyu(n,2*x-1)

def eval_sh_jacobi(n,p,q,x):
    return (sp.binom(2*n+p-1,n)**(-1)) * (sp.eval_jacobi(n,p-q,q-1,2*x-1))

def eval_sh_legendre(n,x):
    return sp.eval_legendre(n,2*x-1)




"""
https://planetmath.org/LaguerrePolynomial#:~:text=Laguerre%20polynomial%201%201%20Definition%20The%20Laguerre%20polynomials,The%20Laguerre%20polynomials%20satisfy%20the%20orthogonality%20relation%20
https://keisan.casio.com/exec/system/1180573413
https://en.wikipedia.org/wiki/Hermite_polynomials


import scipy.special as sp 
def _scale(self, p):
        if p == 1.0:
            return
        self._coeffs *= p

        evf = self._eval_func
        if evf:
            self._eval_func = lambda x: evf(x) * p
        self.normcoef *= p
        
def sh_chebyu(n, monic=False):
    base = sp.sh_jacobi(n, 2.0, 1.5, monic=monic)
    if monic:
        return base
    factor = 4**n
    base._scale(factor)
    return base
"""


