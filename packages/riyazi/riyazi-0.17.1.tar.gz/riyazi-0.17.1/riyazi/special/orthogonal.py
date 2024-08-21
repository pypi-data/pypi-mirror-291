""" 
# Legendre function
- legendre()
- legenp()
- legenq()

# chebyshev polynomials
- chebyt()
- chebyu()

# Jacobi polynomials
- jacobi()

# Gegenbauer polynomials
- gegenbauer()

# Hermite polynomial
- hermite()

# Laguerre   polynomial
- laguerre()

# spherical harmonics
- sherharm()



"""
from math import sqrt,pi, factorial, cos ,gamma, sin 
import mpmath 
# Spherical harmonics¶
def spherharm(l,m,theta,phi):
    return (sqrt( ((2*l)+1*factorial(l-m))) / (4*pi)*(factorial(l+m)))* mpmath.legenp(l,m)*cos()   


def laguerre(n,a,z):
    return (gamma(n+a+1)/(gamma(a+1)*gamma(n+1))) * mpmath.hyp1f1(-n,a+1,z)

def hermite(n,z):
    return (pow(2*z,n))* mpmath.hyp2f0(-n/2, (1-n)/2, (-1/pow(z,2)))


def legendre(n,x):
    return mpmath.hyp2f1(-n, n+1, 1, (1-x)/2)


def legenp(n,m,z):
    return (1/(gamma(1-m))) * (pow(1+z,m/2)/ (pow(1-z,m/2))) * mpmath.hyp2f1(-n,n+1,1-m,(1-z)/2)

def chebyu(n,x):
    return (sin((n+1)*x)) /sin(x)