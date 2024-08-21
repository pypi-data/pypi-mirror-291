"""
Types of Bessel function 
-------------------------

1.) Modified Bessel functions
2.) Hankel functions
3.) Spherical Bessel function
4.) Spherical Hankel functions
5.) Bessel function
6.) Common Bessel
7.)  Drivative Bessel
8.) Integral Bessel
9.) Ricati Bessel 
10.) Zero Bessel 

https://www.cfm.brown.edu/people/dobrush/am34/Mathematica/ch7/bessel.html
https://en.wikipedia.org/wiki/Bessel_function

https://solitaryroad.com/c678.html

https://en.wikipedia.org/wiki/Bessel_function

https://functions.wolfram.com/Bessel-TypeFunctions/BesselK/introductions/Bessels/ShowAll.html

https://solitaryroad.com/c678.html

https://math.stackexchange.com/questions/2204475/derivative-of-bessel-function-of-second-kind-zero-order

https://en.wikipedia.org/wiki/Airy_function#:~:text=The%20Airy%20function%20is%20the%20solution%20to%20time-independent,a%20particle%20in%20a%20one-dimensional%20constant%20force%20field.

https://en.wikipedia.org/wiki/Bessel_function#Modified_Bessel_functions
https://www.omnicalculator.com/math/error-function
http://www.ece.northwestern.edu/local-apps/matlabhelp/techdoc/ref/erf.html#999009
# https://www.thermopedia.com/content/737/
https://en.wikipedia.org/wiki/Bessel_function

"""






__all__ = ['besselk', 'jv','jve','yn','yv','yve','kn','kv','kve',
'iv','ive','hankel1','hankel1e','hankel2','hankel2e',

'wright_bessel', 'lmbda',
'j0','j1','y0','y1','i0','i0e','i1','i1e',

'k0','k0e','k1','k1e',
'jvp','yvp','kvp','ivp','h1vp','h2vp',

'itj0y0','it2j0y0','iti0k0','it2i0k0',
'besselpoly',

'riccati_jn','riccati_yn',

'sph_jn','sph_yn', 'sph_i1n', 'sph_i2n','sph_h1n', 'sph_h2n',
'sph_kn',

'jnjnp_zeros','jnyn_zeros','jn_zeros','jnp_zeros',

'yn_zeros','ynp_zeros','y0_zeros','y1_zeros','y1p_zeros',
'airy','airye','ai_zeros','bi_zeros','itairy'

]


from cmath import exp, sqrt
from math import factorial,gamma, pi, sqrt
from mpmath import besselj,bessely,besselk,besseli,hankel1,hankel2
import math
from scipy.special import spherical_jn,spherical_yn
import numpy as np
import scipy.special as sp
import mpmath as mp 







from cmath import exp,pi
from mpmath import hypercomb
from math import inf

def besselk( n, z, **kwargs):
    if not z:
        return inf
    M = z
    if M < 1:
        # Represent as limit definition
        def h(n):
            r = (z/2)**2
            T1 = [z, 2], [-n, n-1], [n], [], [], [1-n], r
            T2 = [z, 2], [n, -n-1], [-n], [], [], [1+n], r
            return T1, T2
    # We could use the limit definition always, but it leads
    # to very bad cancellation (of exponentially large terms)
    # for large real z
    # Instead represent in terms of 2F0
    else:
        
        def h(n):
            return [([pi/2, z, exp(-z)], [0.5,-0.5,1], [], [], \
                [n+0.5, 0.5-n], [], -1/(2*z))]
    return hypercomb(h, [n], **kwargs)




















"""

Bessel functions
"""
def jv(v,z):
    return besselj(v,z)

def jve(v,z):
    return jv(v, z) * exp(-abs(z.imag))

def yn(n,x):
    return bessely(n,x)


def yv(v,z):
    return bessely(v,z)

def yve(v,z):
    return yv(v, z) * exp(-abs(z.imag))


def kn(n,x):
    return besselk(n,x)


def kv(v,x):
    return besselk(v,x)

def kve(v,z):
    return kv(v, z) * exp(z)

def iv(v,z):
    return besseli(v,z)

def ive(v,z):
    return iv(v, z) * exp(-abs(z.real))


def hankel1(n,x,**kwargs):
    return besselj(n,x,**kwargs) + 1j*bessely(n,x,**kwargs)

def hankel1e(v,z):
    return hankel1(v, z) * exp(-1j * z)

def hankel2(n,x,**kwargs):
    return besselj(n,x,**kwargs) - 1j*bessely(n,x,**kwargs)

def hankel2e(v,z):
    return  hankel2(v, z) * exp(1j * z)

def wright_bessel(a,b,x):
    res =0.0
    for k in range(100):
        res += pow(x,k) / ( factorial(k)*gamma((a*k)+b))
    return res

def lmbda(v,z):
    pass



"""
Common Bessel functions

"""


def j0(x):
    """Computes the Bessel function `J_0(x)`. See :func:`~riyazi.besselj`."""
    return besselj(0,x)

def j1(x):
    """Computes the Bessel function `J_1(x)`.  See :func:`~riyazi.besselj`."""
    return besselj(1,x)

def y0(x):
    return bessely(0,x)

def y1(x):
    return bessely(0,x)

def i0(x):
    return besseli(0,x)

def i0e(x):
    return exp(-abs(x))*i0(x)

def i1(x):
    return besseli(1,x)

def i1e(x):
    return exp(-abs(x))*i1(x)

def k0(x):
    return besselk(0,x)

def k0e(x):
    return exp(x)* k0(x)

def k1(x):
    return besselk(1,x)

def k1e(x):
    return exp(x) * k1(x)



"""
Drivative Bessel function 

"""

def jvp(n,x):
    return (0.5*(besselj(n-1,x)- besselj(n+1,x)))

def yvp(n,x):
    return (0.5*(bessely(n-1,x)- bessely(n+1,x)))


def kvp(n,x):
    return (-0.5*(besselk(n-1,x)+ besselk(n+1,x)))

def ivp(n,x):
    return (0.5*(besseli(n-1,x)+ besseli(n+1,x)))

def h1vp(v,z,n=1):
    return  (v*hankel1(v,z)/z)- (hankel1(v+1,z))


def h2vp(v,z,n=2):
    return  0.5*((hankel2(v-1,z))- (hankel2(v+1,z)))



"""
Integrals Bessel function

"""


def itj0y0(x):
    res = 0 
    for k in range(20):
        res += (pow((-x**2)/4,k)/ math.factorial(k)**2)
    return res


def it2j0y0():
    pass

def iti0k0():
    pass

def it2i0k0():
    pass


def besselpoly():
    pass






"""
Ricati Bessel function
"""


def riccati_jn(n,x):
    for rng in range(0,n+1):
        c = (x*spherical_jn(rng,x))
        print(c)

def riccati_yn(n,x):
    for rng in range(0,n+1):
        c = (x*spherical_yn(rng,x))
        print(c)



"""

Spherical Bessel function
"""


# jn()
def sph_jn(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.jv(n + 0.5, z)

# yn()
def sph_yn(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.yv(n + 0.5, z)

# iv1()
def sph_i1n(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.iv(n + 0.5, z)

# iv2()
def sph_i2n(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.iv(-n - 0.5, z)

# hankel1()
def sph_h1n(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.hankel1(n + 0.5, z)

# hankel2()
def sph_h2n(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.hankel2(n + 0.5, z)

# kn()
def sph_kn(n, z):
    return np.sqrt(0.5*np.pi/z)*sp.kv(n + 0.5, z)




"""

Zero Bessel function

"""

def jnjnp_zeros():
    pass


def jnyn_zeros():
    pass

def jn_zeros():
    pass

def jnp_zeros():
    pass


def yn_zeros():
    pass


def ynp_zeros():
    pass

def y0_zeros():
    pass

def y1_zeros():
    pass


def y1p_zeros():
    pass


""" 

Airy functions
"""




def ai(z):
    return ((1/pi) * sqrt(z/3))* mp.besselk(1/3,(2/3)*(z**(3/2)))

def aip(z):
    return ((-z/(pi*sqrt(3))) * mp.besselk(2/3,(2/3)*(z**(3/2))))

def bi(z):
    return (sqrt(z/3))*( mp.besseli(-1/3,(2/3)*(z**(3/2)))+mp.besseli(1/3,(2/3)*(z**(3/2))) )

def bip(z):
    return (z/sqrt(3))*( mp.besseli(-2/3,(2/3)*(z**(3/2)))+mp.besseli(2/3,(2/3)*(z**(3/2))))



def airy(z):
    return (ai(z),aip(z),bi(z),bip(z))




def airye(z):
    Ai,Aip,Bi,Bip = sp.airy(z)
    eAi  = Ai  * exp(2.0/3.0*z*sqrt(z)).real
    eAip = Aip * exp(2.0/3.0*z*sqrt(z)).real
    eBi  = Bi  * exp(-abs(2.0/3.0*(z*sqrt(z)).real)).real
    eBip = Bip * exp(-abs(2.0/3.0*(z*sqrt(z)).real)).real
    return eAi,eAip,eBi,eBip





def ai_zeros(nt):
    pass

def bi_zeros(nt):
    pass

def itairy(x):
    pass

