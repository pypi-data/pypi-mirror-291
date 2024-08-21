
# __all__ = ['qp', 'q_bracket', 'qfac', 'qbinom', 'qbinom1', 'qhyper', 'qgamma', 'qbesselj1', 'qbesselj2',
# 'qbesselj3']

# https://en.wikipedia.org/wiki/Basic_hypergeometric_series
# https://dlmf.nist.gov/17
# https://github.com/ectomancer/pure_python

from math import sqrt, erf
from scipy.special import erfinv
from typing import List, TypeVar

Numeric = TypeVar('Numeric', int, float, complex)

EMPTY_PRODUCT = 1
EMPTY_SUM = 0
MINUS_ONE = -1

def qp(a: Numeric, q: Numeric, n: int=None) -> Numeric:
    """Pure Python q-Pochhammer symbol (a;q)_n is the q-analog of Pochhammer symbol.
    Also called q-shifted factorial.
    (a;q)_n = q_poch(a, q, n)
    (a;q)_infinity = q_poch(a, q)
    """
    #Special case of q-binomial thereom.
    if n is None:
        sum = EMPTY_SUM
        for n in range(30):
            sum += MINUS_ONE**n*q**(n*(n - 1)/2)/qp(q, q, n)*a**n
        return sum
    if not n:
        return 1
    signum_n = 1
    if n < 0:
        n = abs(n)
        signum_n = -1
    product = EMPTY_PRODUCT
    if signum_n == 1:
        for k in range(n):
            product *= 1 - a*q**k
    else:
        for k in range(1, n + 1):
            product *= 1/(1 - a/q**k)
    return product


def q_bracket(n: int, q: Numeric) -> Numeric:
    """Pure Python q_bracket of n [n]_q is the q-analog of n.
    Also called q-number of n.
    """
    if q == 1:
        return n
    return (1 - q**n)/(1 - q)


def qfac(n: int, q: Numeric, type: int=1) -> Numeric:
    """Pure Python q_factorial [n]!_q is the q-analog of factorial.
    type=1 is algorithm (1).
    type=2 is algorithm (2).
    """
    product = EMPTY_PRODUCT
    if type == 1:
        for k in range(1, n + 1):
            product *= q_bracket(k, q)
        return product
    elif type == 2:
        return qp(q, q, n)/(1 - q)**n
    
    
def qbinom(n: int, k: int, q: Numeric) -> Numeric:
    """Pure Python q-binomial coefficients [n choose k]_q is the q-analog of (n choose k).
    Also called Gaussian binomial coefficients, Gaussian coefficients or Gaussian polynomials.
    """
    return qfac(n, q)/(qfac(n - k, q)*qfac(k, q))
    
    
def qbinom1(n: int, k: int) -> int:
    """Pure Python binomial coefficient (n choose k) using q_binom function."""
    return int(qbinom(n, k, 1))



def qhyper(a_s: List[Numeric], b_s: List[Numeric], q: Numeric, z: Numeric, type: int=1) -> Numeric:
    """Pure Python unilateral basic hypergeometric series φ is the q-analog
    of generalized hypergeometric function.
    Also called q-hypergeometric series or q-hypergeometric function.
    type=1 is unilateral basic hypergeometric series φ.
    type=2 is bilateral basic hypergeometric series ψ.
    """
    sum = EMPTY_SUM
    j = len(a_s)
    k = len(b_s)
    if type == 1:
        for n in range(30):
            a_product = EMPTY_PRODUCT
            b_product = EMPTY_PRODUCT
            for a_item in a_s:
                a_product *= qp(a_item, q, n)
            for b_item in b_s:
                b_product *= qp(b_item, q, n)
            b_product *= qp(q, q, n)
            sum += a_product/b_product*(MINUS_ONE**n*q**qbinom1(n, 2))**(1 + k - j)*z**n
    if type == 2:
        sum_1 = EMPTY_SUM
        sum_2 = EMPTY_SUM
        for n in range(30):
            a_product = EMPTY_PRODUCT
            b_product = EMPTY_PRODUCT
            aq_product = EMPTY_PRODUCT
            bq_product = EMPTY_PRODUCT
            for a_item in a_s:
                a_product *= qp(a_item, q, n)
                #skip n=0 for sum_2, i.e. sum_2 starts at n=1
                if n:
                    aq_product *= q/qp(a_item, q, n)
            for b_item in b_s:
                b_product *= qp(b_item, q, n)
                #skip n=0 for sum_2, i.e. sum_2 starts at n=1
                if n:
                    bq_product *= q/qp(b_item, q, n)
            sum_1 += a_product/b_product*(MINUS_ONE**n*q**qbinom1(n, 2))**(k - j)*z**n
            sum_2 += bq_product/aq_product*(b_item/(a_item*z))**n
        sum = sum_1 + sum_2
    return sum



def qgamma(z: Numeric, q: Numeric) -> Numeric:
    """q-gamma function Γ_q is the q-analog of gamma function.
    Using q inversion, supports q>1.
    """
    if q > 1:
        #q inversion
        return qp(q**-1, q**-1)/qp(q**-z, q**-1)*(1 - q)**(1 - z)*qbinom1(z, 2)
    return qp(q, q)*(1 - q)**(1 - z)/qp(q**z, q)


def qbesselj1(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """first Jackson q-Bessel function J^(1)_𝜈 is one of three q-analogs for Bessel function
    of the first kind.
    Also called first basic Bessel function.
    """
    z_signum = 1
    if z.real < 0:
        if not z.imag:
            z = -z
            z_signum = -1
    𝜈_signum = 1
    if 𝜈 == int(𝜈.real):
        if not 𝜈.imag:
            if 𝜈 < 0:
                𝜈 = -𝜈
                𝜈_signum = -1
    result = qp(q**(𝜈 + 1), q)/qp(q, q)*(z/2)**𝜈*qhyper([0, 0], [q**(𝜈 + 1)], q, -z**2/4)
    if 𝜈_signum == -1:
        return result*z_signum**𝜈*𝜈_signum**𝜈
    return result*z_signum**𝜈

def qbesselj2(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """second Jackson q-Bessel function J^(2)_𝜈 is one of three q-analogs for Bessel function
    of the first kind.
    Also called second basic Bessel function.
    """
    z_signum = 1
    if z.real < 0:
        if not z.imag:
            z = -z
            z_signum = -1
    𝜈_signum = 1
    if 𝜈 == int(𝜈.real):
        if not 𝜈.imag:
            if 𝜈 < 0:
                𝜈 = -𝜈
                𝜈_signum = -1
    result = qp(q**(𝜈 + 1), q)/qp(q, q)*(z/2)**𝜈*qhyper([], [q**(𝜈 + 1)], q, (-z**2*q**(𝜈 + 1))/4)
    if 𝜈_signum == -1:
        return result*z_signum**𝜈*𝜈_signum**𝜈
    return result*z_signum**𝜈

def qbesselj3(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """third Jackson q-Bessel function J^(3)_𝜈 is one of three q-analogs for Bessel function
    of the first kind.
    Also called Hahn–Exton q-Bessel function or third basic Bessel function.
    """
    z_signum = 1
    if z.real < 0:
        if not z.imag:
            z = -z
            z_signum = -1
    result = qp(q**(𝜈 + 1), q)/qp(q, q)*(z/2)**𝜈*qhyper([0], [q**(𝜈 + 1)], q, (q*z**2)/4)
    return result*z_signum**𝜈


def qbesseli1(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """first modified Jackson q-Bessel function I^(1)_𝜈 is one of three q-analogs for modified Bessel functionn
    of the first kind.
    Also called first modified basic Bessel function and unified as one equation and called
    generalized modified q-Bessel function.
    """
    return qp(q**(𝜈 + 1), q)/qp(q, q)*(z/2)**𝜈*qhyper([0, 0], [q**(𝜈 + 1)], q, z**2/4)


def qbesseli2(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """second modified Jackson q-Bessel function I^(2)_𝜈 is one of three q-analogs for modified Bessel functionn
    of the first kind.
    Also called second modified basic Bessel function and unified as one equation and called
    generalized modified q-Bessel function.
    """
    return qp(q**(𝜈 + 1), q)/qp(q, q)*(z/2)**𝜈*qhyper([], [q**(𝜈 + 1)], q, q**(2*(𝜈 + 1)/2)*z**2/4)


def qbesseli3(z: Numeric, q: Numeric, 𝜈: int) -> Numeric:
    """third modified Jackson q-Bessel function I^(3)_𝜈 is one of three q-analogs for modified Bessel functionn
    of the first kind.
    Also called third modified basic Bessel function and unified as one equation and called
    generalized modified q-Bessel function.
    """
    return qp(q**(𝜈 + 1), q)/qp(q, q)*(z/2)**𝜈*qhyper([0], [q**(𝜈 + 1)], q, q**((𝜈 + 1)/2)*z**2/4)


def qbesselj1p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """q-difference operator applied to first Jackson q-Bessel function J^(1)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besselj1p(type=1) Jackson q-difference operator D_q.
    q_besselj1p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (qbesselj1(z, q, 𝜈) - qbesselj1(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return qbesselj1(z*q**0.5, q, 𝜈) - qbesselj1(z/q**0.5, q, 𝜈)


def qbesselj2p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """q-difference operator applied to second Jackson q-Bessel function J^(2)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besselj2p(type=1) Jackson q-difference operator D_q.
    q_besselj2p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (qbesselj2(z, q, 𝜈) - qbesselj2(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return qbesselj2(z*q**0.5, q, 𝜈) - qbesselj2(z/q**0.5, q, 𝜈)


def qbesselj3p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """Jackson q-difference operator applied to third Jackson q-Bessel function J^(3)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besselj3p(type=1) Jackson q-difference operator D_q.
    q_besselj3p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (qbesselj3(z, q, 𝜈) - qbesselj3(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return qbesselj3(z*q**0.5, q, 𝜈) - qbesselj3(z/q**0.5, q, 𝜈)


def qbesseli1p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """Jackson q-difference operator applied to first Jackson q-Bessel function I^(1)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besseli1p(type=1) Jackson q-difference operator D_q.
    q_besseli1p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (qbesseli1(z, q, 𝜈) - qbesseli1(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return qbesseli1(z*q**0.5, q, 𝜈) - qbesseli1(z/q**0.5, q, 𝜈)


def qbesseli2p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """Jackson q-difference operator applied to second Jackson q-Bessel function I^(2)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besseli2p(type=1) Jackson q-difference operator D_q.
    q_besseli2p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (qbesseli2(z, q, 𝜈) - qbesseli2(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return qbesseli2(z*q**0.5, q, 𝜈) - qbesseli2(z/q**0.5, q, 𝜈)


def qbesseli3p(z: Numeric, q: Numeric, 𝜈: int, type: int=1) -> Numeric:
    """Jackson q-difference operator applied to third Jackson q-Bessel function I^(3)_𝜈 is one of three q-analogs for first derivative of Bessel function
    of the first kind.
    q_besseli3p(type=1) Jackson q-difference operator D_q.
    q_besseli3p(type=2) symmetric q-difference operator 𝛿_q.
    """
    if type == 1:
        return (qbesseli3(z, q, 𝜈) - qbesseli3(q*z, q, 𝜈))/((1 - q)*z)
    elif type == 2:
        return qbesseli3(z*q**0.5, q, 𝜈) - qbesseli3(z/q**0.5, q, 𝜈)



def qe(x: Numeric, q: Numeric) -> Numeric:
    """q-exponential function e_q is a q-analog of exponential function exp."""
    return 1/(qp(((1 - q)*x), q))


def qE(x: Numeric, q: Numeric) -> Numeric:
    """q-exponential function E_q is a q-analog of exponential function exp."""
    return 1/(qp((-(1 - q)*x), q))


def qsin(x: Numeric, q: Numeric) -> Numeric:
    """q-sin is a q-analog of sine function sin."""
    result = 1/2j*(qe(1j*x, q) - qe(-1j*x, q))
    if not result.imag:
        return result.real
    return result


def qSin(x: Numeric, q: Numeric) -> Numeric:
    """q-Sin is a q-analog of sine function sin."""
    result = 1/2j*(qE(1j*x, q) - qE(-1j*x, q))
    if not result.imag:
        return result.real
    return result


def qcos(x: Numeric, q: Numeric) -> Numeric:
    """q-cos is a q-analog of cosine function cos."""
    result = 0.5*(qe(1j*x, q) + qe(-1j*x, q))
    if not result.imag:
        return result.real
    return result


def qCos1(x: Numeric, q: Numeric) -> Numeric:
    """q-Cos is a q-analog of cosine function cos."""
    result = 0.5*(qE(1j*x, q) + qE(-1j*x, q))
    if not result.imag:
        return result.real
    return result

















def qfunc(x):
    return 0.5-0.5*erf(x/sqrt(2))

def invQfunc(x):
    return sqrt(2)*erfinv(1-2*x)
