from itertools import count, islice
import mpmath
import cmath
import mpmath as mp 
import math 



# Basic definition of zeta func
# zeta(s) = sum(1/n^s)
# (Re(s) > 1)
def zeta1(s, t=1000000):
    term = (1 / (n ** s) for n in count(1))
    return sum(islice(term, t))



def zeta(s):
    """
    Riemann zeta function
    """
    return mp.zeta(s)



def basel(n = 2):
    """ 
    Basel problem on ζ(2)
    """
    return  math.pi ** n / 6


def hurwitz_zeta(s, a):
    """
     Hurwitz zeta function
    
    """
    
    return mp.zeta(s, a)


def bernoulli(n):
    """
    Bernoulli number
    
    """
    return mp.bernoulli(n)

def is_giuga_number(n):
    """
    Agoh–Giuga conjecture
    """
    def sum_of_divisors(m):
        divisor_sum = 0
        for i in range(1, m):
            if m % i == 0:
                divisor_sum += i
        return divisor_sum
    
    if n <= 1:
        return False
    
    
def von_staudt_clausen_denominator(n):
    """
    Von Staudt–Clausen theorem
    """
    if n == 1:
        return 1  # The denominator of B1 is 1
    elif n % 2 == 1 or n == 0:
        return 0  # Bn = 0 for odd n or n = 0
    else:
        result = 0
        for k in range(1, n):
            result += von_staudt_clausen_denominator(k) * binomial_coefficient(n, k)
        return 1 - result / (n - 1)

def binomial_coefficient(n, k):
    if 0 <= k <= n:
        result = 1
        for i in range(1, min(k, n - k) + 1):
            result = result * (n - i + 1) // i
        return result
    else:
        return 0
    
    divisor_sum = sum_of_divisors(n)
    return divisor_sum % n == (n - 1)
def xi(s):
    """
    Describing the Reimann Xi Function 
    """
    return 1/2*s*(s-1)*cmath.pi**(-s/2)*mpmath.gamma(s/2)*mpmath.zeta(s)

def dirichlet(s):
    """
    Dirichlet series
    """
    return mp.dirichlet(s)


def eulerprod(s):
    """ 
    
    Euler product
    """
    return mp.zeta(s)


def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def print_primes(limit):
    if limit < 2:
        return
    print("Prime numbers up to", limit, ":")
    for num in range(2, limit + 1):
        if is_prime(num):
            print(num, end=" ")



def countPrimes(n):
    
    """
    prime counting theorm
    :type n: int
    :rtype: int
    """
    count = 0
    primes = [False for i in range(n+1)]
    for i in range(2,n):
        
        if primes[i] == False:
            count+=1
            j = 2
            while j*i<n:
                
                primes[j*i] = True
                j+=1
    return count



def li(x):
    """ 
    Offset logarithmic integral
    """
    return mp.li(x)
