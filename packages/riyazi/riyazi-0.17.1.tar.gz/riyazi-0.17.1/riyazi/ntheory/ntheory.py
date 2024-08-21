""" 

Number - theoretical combinational and integer function

"""

__all__ = ['bernoulli', 'bernfrac', 'bernpoly', 'eulernum', 'eulerpoly', 
           'bell', 'bell_nth', 'bellTriangle',
           'stirling1', 'stirling2', 'stirling3', 'primepi', 'primepi2', 'riemannr', 'cyclotomic', 
           'mangoldt'] 
from fractions import Fraction
from math import factorial, comb
from .tests.utils import my_choose, my_factorial, my_power
from math import log
def prime_factors(n):
    factors = []
    # Start with 2, the first prime number
    divisor = 2
    while divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            n = n // divisor
        else:
            divisor += 1
    return factors




def bernoulli(m):
    if m ==0 :
        return 1
    else:
        t = 0
        for k in range(0, m): 
            t += comb(m,k )*bernoulli(k)/  (m-k +1)
        return 1-t
    

def bernfrac(n):
    lst=[1,1]+ [i**n for i in range(2, n+2)]
    for i in range(n):
        for j in range(n, i, -1): 
            lst[j+1] -= lst[j]
        lst[0] = Fraction(lst[i+2], i+2) - lst[0]
    return lst


def bernpoly():
    pass

def eulernum():
    pass

def eulerpoly():
    pass

import math
ITERATIONS = 1000
def bell(N):
    return float(round((1/math.e) * sum([(float(k)**N)/factorial(k) for k in range(ITERATIONS)])))

def bell_nth(num):
    lst_o = [0]*num # old list
    lst_n = [1]*num # new list
    j = 0
    k = 0
    for i in range(num):
        for j in range(i):
             if j>0:
                lst_n[j] = lst_n[j-1]+lst_o[j-1] # Creating the bell triangle
        lst_o = lst_n[:] # updating the old list with the new one
        k = lst_n[0] # Bell no
        lst_n[0] = lst_n[j] # making the last varible of old list the first varible of the new list
    return k

def bellTriangle(n):
    tri = [None] * n
    for i in range(n):
        tri[i] = [0] * i
    tri[1][0] = 1
    for i in range(2, n):
        tri[i][0] = tri[i - 1][i - 2]
        for j in range(1, i):
            tri[i][j] = tri[i][j - 1] + tri[i - 1][j - 1]
    return tri


import numpy as np
from scipy.special import factorial


class Stirling1():
    """Stirling numbers of the first kind
    """ 
    # based on
    # https://rosettacode.org/wiki/Stirling_numbers_of_the_first_kind#Python

    def __init__(self):
        self._cache = {}

    def __call__(self, n, k):
        key = str(n) + "," + str(k)

        if key in self._cache.keys():
            return self._cache[key]
        if n == k == 0:
            return 1
        if n > 0 and k == 0:
            return 0
        if k > n:
            return 0
        result = stirling1(n - 1, k - 1) + (n - 1) * stirling1(n - 1, k)
        self._cache[key] = result
        return result

    def clear_cache(self):
        """clear cache of Sterling numbers
        """
        self._cache = {}


stirling1 = Stirling1()


class Stirling2():
    """Stirling numbers of the second kind
    """
    # based on
    # https://rosettacode.org/wiki/Stirling_numbers_of_the_second_kind#Python

    def __init__(self):
        self._cache = {}

    def __call__(self, n, k):
        key = str(n) + "," + str(k)

        if key in self._cache.keys():
            return self._cache[key]
        if n == k == 0:
            return 1
        if (n > 0 and k == 0) or (n == 0 and k > 0):
            return 0
        if n == k:
            return 1
        if k > n:
            return 0
        result = k * stirling2(n - 1, k) + stirling2(n - 1, k - 1)
        self._cache[key] = result
        return result

    def clear_cache(self):
        """clear cache of Sterling numbers
        """
        self._cache = {}


stirling2 = Stirling2()


def stirling3(a, n, k, f):
    if n == k:
        f(a)
    else:
        for i in range(0, k):
            a[n] = i
            stirling3(a, n - 1, k, f)  # this call String
            a[n] = n - 1
        if k > 1:
            a[n] = k - 1
            stirling3(a, n - 1, k - 1, f)
            a[n] = n - 1
            




def primepi(n):
    # A simple implementation of the prime counting function
    count = 0
    for i in range(2, n + 1):
        if all(i % p != 0 for p in range(2, int(i**0.5) + 1)):
            count += 1
    return count

def primepi2(n):
    # A simple implementation of the prime counting function
    count = 0
    for i in range(2, n + 1):
        if all(i % p != 0 for p in range(2, int(i**0.5) + 1)):
            count += 1
    return count, count



def riemannr():
    pass 



def cyclotomic():
    pass

def mangoldt(n):
    """
    print(f"λ({n}) = {result}")
    """
    if n <= 1:
        return 0  # λ(1) = 0

    factors = prime_factors(n)  # Get the prime factors of n

    if len(factors) == 1 and n == factors[0]:
        return log(factors[0])
    else:
        return 0
