def factorial(n):
    if n < 1 :
        return 1
    else:
        return n* factorial(n-1)

def fact(n):
    r=1.0
    while n > 0:
        r = r * n
        n = n - 1
    return(r)
    
def combination(m, k):
    if k <=m :
        return factorial(m)/ (factorial(k)* factorial(m-k))
    else:
        return 0
    
def my_factorial(n):
    ans = 1
    for i in range(1,n+1):
        ans *= i
    return ans

def my_power(n, p):
    # n^p
    ans = 1
    for i in range(p):
        ans *= n
    return ans

def my_choose(n, k):
    if n == k: return 1
    if k < n-k:
        delta = n - k
        i_max = k
    else:
        delta = k
        i_max = n - k
  
    ans = delta + 1
    for i in range(2, i_max+1):
        ans = (ans * (delta + i)) // i
    return ans



# https://www.rosettacode.org/wiki/Bell_numbers#Python

def _stirling2(n, k):
    sum = 0
    for j in range(0, k+1):
        a = my_power(-1, k-j)
        b = my_choose(k, j)
        c = my_power(j, n)
        sum += a * b * c

    return sum // my_factorial(k)


# https://jamesmccaffrey.wordpress.com/2020/07/30/computing-a-stirling-number-of-the-second-kind-from-scratch-using-python/

computed = {}

def _stirling2(n, k):
	key = str(n) + "," + str(k)

	if key in computed.keys():
		return computed[key]
	if n == k == 0:
		return 1
	if (n > 0 and k == 0) or (n == 0 and k > 0):
		return 0
	if n == k:
		return 1
	if k > n:
		return 0
	result = k * _stirling2(n - 1, k) + _stirling2(n - 1, k - 1)
	computed[key] = result
	return result