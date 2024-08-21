def is_composite(n):
    # composite number
    n = 0
    for i in range(1, n+1):
        if n % i == 0:
            n += 1
    if n > 2:
        print("The number is composite")
        
    else:
        print(" Sorry, your number is prime")
        
        
        
# A optimized school method based Python program to check
# if a number is composite.

def isComposite(n):

	# Corner cases
	if (n <= 1):
		return False
	if (n <= 3):
		return False

	# This is checked so that we can skip
	# middle five numbers in below loop
	if (n % 2 == 0 or n % 3 == 0):
		return True
	i = 5
	while(i * i <= n):
		
		if (n % i == 0 or n % (i + 2) == 0):
			return True
		i = i + 6
		
	return False

import math

def is_composite(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return True
    return False

def print_composite_numbers(start, end):
    for num in range(start, end + 1):
        if is_composite(num):
            print(num)
            
            
# Python3 program for the above approach

# Function to find the Nth Composite
# Numbers using Sieve of Eratosthenes
def NthComposite(N):

	# Sieve of prime numbers
	IsPrime = [True]*1000005

	# Iterate over the range [2, 1000005]
	for p in range(2, 1000005):
		if p * p > 1000005:
			break

		# If IsPrime[p] is true
		if (IsPrime[p] == True):
		
			# Iterate over the
			# range [p * p, 1000005]
			for i in range(p*p,1000005,p):
				IsPrime[i] = False

	# Stores the list of composite numbers
	Composites = []

	# Iterate over the range [4, 1000005]
	for p in range(4,1000005):

		# If i is not prime
		if (not IsPrime[p]):
			Composites.append(p)

	# Return Nth Composite Number
	return Composites[N - 1]



# Python3 implementation for checking
# Highly Composite Number
 
# Function to count the number
# of divisors of the N
def divCount(n):
     
    # Sieve method for prime calculation
    Hash = [True for i in range(n + 1)]
     
    p = 2
    while ((p * p) < n):
        if bool(Hash[p]):
            i = p * 2
             
            while i < n:
                Hash[i] = False
                i += p
                 
        p += 1
 
    # Traversing through
    # all prime numbers
    total = 1
     
    for P in range(2, n + 1):
        if (bool(Hash[P])):
 
            # Calculate number of divisor
            # with formula total div =
            # (p1+1) * (p2+1) *.....* (pn+1)
            # where n = (a1^p1)*(a2^p2)....
            # *(an^pn) ai being prime divisor
            # for n and pi are their respective
            # power in factorization
            count = 0
            if (n % P == 0):
                while (n % P == 0):
                    n = n // P
                    count += 1
         
                total = total * (count + 1)
                 
    return total
 
# Function to check if a number
# is a highly composite number
def isHighlyCompositeNumber(N):
     
    # Count number of factors of N
    NdivCount = divCount(N)
 
    # Loop to count number of factors of
    # every number less than N
    for i in range(N):
        idivCount = divCount(i)
 
        # If any number less than N has
        # more factors than N,
        # then return false
        if (idivCount >= NdivCount):
            return bool(False)
 
    return bool(True)



# Python3 code to get parity.

# Function to get parity of number n.
# It returns 1 if n has odd parity,
# and returns 0 if n has even parity
def getParity( n ):
	parity = 0
	while n:
		parity = ~parity
		n = n & (n - 1)
	return parity

# Driver program to test getParity()
n = 7
print ("Parity of no ", n," = ",
	( "odd" if getParity(n) else "even"))

# This code is contributed by "Sharad_Bhardwaj".


def getParity(n):
    return (bin(n).count("1"))%2



def parity(n):
    c=0
    n=bin(n)
    for i in n:
        if(i==1):
            c=c+1
        else:
            pass
    if(c%2!=0 and c==0):
        print('1')
    else:
        print('0')
        
        
# Find the number of divisors of a given integer is even or odd    
def divisor(n):
  x = len([i for i in range(1,n+1) if not n % i])
  return x



# Python implementation of Optimized approach
# to generate Aliquot Sequence

from math import sqrt

# Function to calculate sum of all proper divisors
def getSum(n):
	summ = 0 # 1 is a proper divisor

	# Note that this loop runs till square root
	# of n
	for i in range(1, int(sqrt(n)) + 1):
		if n % i == 0:

			# If divisors are equal, take only one
			# of them
			if n // i == i:
				summ += i

			# Otherwise take both
			else:
				summ += i
				summ += n // i

	# calculate sum of all proper divisors only
	return summ - n

# Function to print Aliquot Sequence for an input n.
def printAliquot(n):

	# Print the first term
	print(n, end=" ")
	s = set()
	s.add(n)

	nextt = 0
	while n > 0:

		# Calculate next term from previous term
		n = getSum(n)

		if n in s:
			print("Repeats with", n)
			break

		# Print next term
		print(n, end=" ")
		s.add(n)

# Python 3 program for aliquot sum

# Function to calculate sum of
# all proper divisors
def aliquotSum(n) :
	sm = 0
	for i in range(1,n) :
		if (n % i == 0) :
			sm = sm + i	
	
	return sm # return sum


def aliquotsum(val):
    # Write a Python program to calculate the aliquot sum of an given integer
    if not isinstance(val, int):
        print("Input must be an integer")
    if val <= 0:
        print("Input must be positive")
    res = sum(divisor for divisor in range(1, val // 2 + 1) if val % divisor == 0)
    print("Original Number : ",val)
    print("Aliquot Sum : ",res)
    
def is_coprime(a,b):
    
    hcf = 1

    for i in range(1, a+1):
        if a%i==0 and b%i==0:
            hcf = i

    return hcf == 1

def gcd(a, b):
      
    # Everything divides 0 
    if (a == 0 or b == 0):
        return False
def coprime(a, b) :
    return (gcd(a, b) == 1)

  
# Returns count of 
# co-prime pairs 
# present in array
def numOfPairs(arr, n) :
    count = 0
      
    for i in range(0, n-1) :
        for j in range(i+1, n) :
      
            if (coprime(arr[i], arr[j])) :
                count = count + 1
      
    return count



def HCF(p,q):
    while q != 0:
        p, q = q, p%q
    return p
def is_coprime(x, y):
    return HCF(x, y) == 1
