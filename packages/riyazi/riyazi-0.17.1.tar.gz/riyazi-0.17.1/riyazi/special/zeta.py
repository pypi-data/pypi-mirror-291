""" 
https://keisan.casio.com/exec/system/1180573439#!

https://researchcode.com/code/1269628936/riemann-zeta-function/

https://math.stackexchange.com/questions/2640941/how-to-locate-zeros-of-the-riemann-zeta-function

https://en.wikipedia.org/wiki/Riemann_zeta_function


https://mpmath.org/doc/current/functions/zeta.html

https://mpmath.org/doc/current/functions/


__all__ = ['zeta', 'altzeta', 'dirichlet', 'stieltjes', 'zetazero', 'nzeros', 'siegelz', 'siegeltheta', 
'grampoint', 'backlunds', 'lerchphi', 'polylog', 'clsin', 'clcos', 'polyexp', 'primezeta', 'secondzeta']

"""
from itertools import count, islice

def binom(n, k):
    v = 1
    for i in range(k):
        v *= (n - i) / (i + 1)
    return v

def zetas(s, t=100):
    if s == 1: return complex("inf")
    term = (1 / 2 ** (n + 1) * sum((-1) ** k * binom(n, k) * (k + 1) ** -s 
                                   for k in range(n + 1)) for n in count(0))
    return sum(islice(term, t)) / (1 - 2 ** (1 - s))



def altzeta(s, terms=1000):
    result = 0
    sign = 1
    
    for n in range(1, terms + 1):
        result += sign / (n ** s)
        sign = -sign
    
    return result


def zeta(s, terms=1000):
    result = 0
    for n in range(1, terms + 1):
        result += 1 / (n ** s)
    return result

import numpy as np

def mzeta(x,q,N=100):
  s=0
  for j in np.arange(1,N):
    s+= 1./(1.*j+1.*q)**x
  return s  



import numpy as np 
def mzeta(x,q, N=100):
    s=0
    for j in np.arange(1,N):
        s += (1.) / ((1.*j+1.*q)**x)
    return s 


