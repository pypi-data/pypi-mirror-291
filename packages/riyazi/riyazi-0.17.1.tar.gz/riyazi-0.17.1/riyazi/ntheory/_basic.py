""" 
Number Theory Algorithms
-----------------------------------------------------------



**Prime Factorization and Divisors**
-----------------------------------
- Prime factors
- Pollard’s Rho Algorithm for Prime Factorization
- Find all divisors of a natural number
- Sum of all proper divisors of a natural number
- Prime Factorization using Sieve O(log n) for multiple queries
- Find politeness of a number
- Print prime numbers in a given range using C++ STL
- k-th prime factor of a given number
- Smith Numbers


**Fibonacci Numbers:**
----------------------------------------
- Fibonacci Numbers
- Interesting facts about Fibonacci numbers
- How to check if a given number is Fibonacci number?
- Zeckendorf’s Theorem (Non-Neighbouring Fibonacci Representation)


**Catalan Numbers :**
----------------------------------
- Catalan numbers
- Applications of Catalan Numbers

**Modular Arithmetic :**
------------------------------
- Modular Exponentiation (Power in Modular Arithmetic)
- Modular multiplicative inverse
- Modular Division
- Multiplicative order
- Find Square Root under Modulo p | Set 1 (When p is in form of 4*i + 3)
- Find Square Root under Modulo p | Set 2 (Shanks Tonelli algorithm)
- Euler’s criterion (Check if square root under modulo p exists)
- Multiply large integers under large modulo
- Find sum of modulo K of first N natural number
- How to compute mod of a big number?
- BigInteger Class in Java
- Modulo 10^9+7 (1000000007)
- How to avoid overflow in modular multiplication?
- RSA Algorithm in Cryptography
- Find (a^b)%m where ‘a’ is very large
- Find power of power under mod of a prime


**Euler Totient Function:**
---------------------------------------

- Euler’s Totient Function
- Optimized Euler Totient Function for Multiple Evaluations
- Euler’s Totient function for all numbers smaller than or equal to n
- Primitive root of a prime number n modulo n

**nCr Computations :**
-----------------------------------

Binomial Coefficient
Compute nCr % p | Set 1 (Introduction and Dynamic Programming Solution)
Compute nCr % p | Set 2 (Lucas Theorem)
Compute nCr % p | Set 3 (Using Fermat Little Theorem)

**Chinese Remainder Theorem :**
-------------------------------------- 

Set 1 (Introduction)
Set 2 (Inverse Modulo based Implementation)
Cyclic Redundancy Check and Modulo-2 Division
Using Chinese Remainder Theorem to Combine Modular equations



**Factorial :**
----------------------------------------
# Factorial
# Legendre’s formula (Given p and n, find the largest x such that p^x divides n!)
# Sum of divisors of factorial of a number
# Count Divisors of Factorial
# Compute n! under modulo p
- Wilson’s Theorem
- Primality Test | Set 1 (Introduction and School Method)
- Primality Test | Set 2 (Fermat Method)
- Primality Test | Set 3 (Miller–Rabin)
- Primality Test | Set 4 (Solovay-Strassen)
- GFact 22 | (2^x + 1 and Prime)
- Euclid’s Lemma
- Sieve of Eratosthenes
- Segmented Sieve
- Sieve of Atkin
- Sieve of Sundaram to print all primes smaller than n
- Sieve of Eratosthenes in 0(n) time complexity
- Check if a large number is divisible by 3 or not
- Check if a large number is divisible by 11 or not
- To check divisibility of any large number by 999
- Carmichael Numbers
- Generators of finite cyclic group under addition
- Measure one litre using two vessels and infinite water supply
- Program to find last digit of n’th Fibonacci Number
- GCD of two numbers when one of them can be very large
- Find Last Digit Of a^b for Large Numbers
- Remainder with 7 for large numbers
- Count all sub-arrays having sum divisible by k
- Partition a number into two divisible parts
- Number of substrings divisible by 6 in a string of integers
- ‘Practice Problems’ on Modular Arithmetic
- ‘Practice Problems’ on Number Theory
- Ask a Question on Number theory
- Padovan, OESIS


"""
from functools import reduce
import math
from turtle import position

# Recursive function to return gcd of a and b
def gcd(a,b):
	if a == 0:
		return b
	return gcd(b % a, a)


# Function to return LCM of two numbers
def lcm(numbers):
	return reduce(lambda x, y: x * y // math.gcd(x, y), numbers, 1)



def fibonacci(n):
    """ 
    function that returns nth  fibonacci series
    The Fibonacci numbers are the numbers in the following integer sequence: 
     0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ……..
     
     >>> fibonacci(4)
         3
     >>> fibonacci(5)
         5
    >>> fibonacci(6)
        8
    
    """
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def fib(n):
    return fibonacci(n)
    
    
# Function to check Fibonacci number
def isFibonacci(N):
	if N == 0 or N == 1:
		return True
	a, b = 0, 1
	while True:
		c = a + b
		a = b
		b = c
		if c == N:
			return True
		elif c >= N:
			return False



def catalan(n):
    
    """ 
    # A recursive function to
    # find nth catalan number
    
    """
	# Base Case
    if n <= 1:
        return 1

	# Catalan(n) is the sum
	# of catalan(i)*catalan(n-i-1)
    res = 0
    for i in range(n):
        res += catalan(i) * catalan(n-i-1)  
    return res 

# Python program for nth Catalan Number
# Returns value of Binomial Coefficient C(n, k)


def binomialCoefficient(n, k):

	# since C(n, k) = C(n, n - k)
	if (k > n - k):
		k = n - k

	# initialize result
	res = 1

	# Calculate value of [n * (n-1) *---* (n-k + 1)]
	# / [k * (k-1) *----* 1]
	for i in range(k):
		res = res * (n - i)
		res = res / (i + 1)
	return res

# A Binomial coefficient based function to
# find nth catalan number in O(n) time


def catalan(n):
	c = binomialCoefficient(2*n, n)
	return c/(n + 1)


# Iterative Function to calculate (x^y)%p in O(log y)
def power(x, y, p):

	# Initialize result
	res = 1

	while (y > 0):

		# If y is odd, multiply x with result
		if ((y & 1) != 0):
			res = res * x

		# y must be even now
		y = y >> 1 # y = y/2
		x = x * x # Change x to x^2

	return res % p



def modInverse(A, M):
 
    for X in range(1, M):
        if (((A % M) * (X % M)) % M == 1):
            return X
    return -1




# Function to find modulo inverse of b. It returns
# -1 when inverse doesn't
# modInverse works for prime m
def modInverse(b,m):
    g = math.gcd(b, m)
    if (g != 1):
        # print("Inverse doesn't exist")
        return -1
    else:
        # If b and m are relatively prime,
        # then modulo inverse is b^(m-2) mode m
        return pow(b, m - 2, m)


# Function to compute a/b under modulo m
def modDivide(a,b,m):
    a = a % m
    inv = modInverse(b,m)
    if(inv == -1):
        print("Division not defined")
    else:
        print("Result of Division is ",(inv*a) % m)
        
        
        
# Function return smallest + ve
# integer that holds condition
# A ^ k(mod N ) = 1
def multiplicativeOrder(A, N) :
    if (gcd(A, N ) != 1) :
        return -1
 
    # result store power of A that raised
    # to the power N-1
    result = 1
 
    K = 1
    while (K < N) :
     
        # modular arithmetic
        result = (result * A) % N
 
        # return smallest + ve integer
        if (result == 1) :
            return K
 
        # increment power
        K = K + 1
     
    return -1

def squareRoot(n, p):
 
    n = n % p
     
    # One by one check all numbers from
    # 2 to p-1
    for x in range (2, p):
        if ((x * x) % p == n) :
            print( "Square root is ", x)
            return
 
    print( "Square root doesn't exist")
    
    
    
    
    
def squareRootExists(n, p):
    n = n % p
 
    # One by one check all numbers
    # from 2 to p-1
    for x in range(2, p, 1):
        if ((x * x) % p == n):
            return True
    return False


# Returns (a * b) % mod
def moduloMultiplication(a, b, mod):
  
    res = 0; # Initialize result
  
    # Update a if it is more than
    # or equal to mod
    a = a % mod
  
    while (b):
      
        # If b is odd, add a with result
        if (b & 1):
            res = (res + a) % mod
              
        # Here we assume that doing 2*a
        # doesn't cause overflow
        a = (2 * a) % mod
  
        b >>= 1; # b = b / 2
      
    return res



# of modulo K of first N
# natural numbers.
 
# Return sum of modulo K of
# first N natural numbers.
 
def findSum(N, K):
    ans = 0
 
    # Iterate from 1 to N &&
    # evaluating and adding i % K.
    for i in range(1, N + 1):
        ans += (i % K)
 
    return ans



def mod(num, a):
 
    # Initialize result
    res = 0
 
    # One by one process all digits
    # of 'num'
    for i in range(0, len(num)):
        res = (res * 10 + int(num[i])) % a
 
    return res




def factorial( n) :
    M = 1000000007
    f = 1

    for i in range(1, n + 1):
        f = f * i # WRONG APPROACH as
                # f may exceed (2^64 - 1)

    return f % M




# A python program to handle overflow
# when multiplying two numbers	

def multiply(a,b,mod):
	return ((a % mod) * (b % mod)) % mod

# Code contributed by Gautam goel (gautamgoel962)






  