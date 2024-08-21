# https://stackoverflow.com/questions/27115917/gauss-legendre-quadrature-in-python

# https://github.com/sigma-py/quadpy

def degree(pairs, max_iteration=1e6):
    deg = 0 
    diffs = [pair[1] for pair in pairs]
    iteration = max_iteration
    while iteration >0:
        iteration -=1
        n = len(diffs) -1
        diffs = [diffs[i+1] - diffs[i] for i in range(n)]
        if (all([i ==0 for i in diffs])):
            break 
            
        deg +=1
    return deg



def simpson(fx, x0, xn, n):
    h = (xn - x0) / n

    return (h / 3) * (
    fx(x0) + fx(xn) +
    (4 * sum([fx(x0 + (i*h)) for i in range(1, n, 2)])) +
    (2 * sum([fx(x0 + (i*h)) for i in range(2, n-1, 2)]))
  )
    
    
def trapezoidal(fx, x0, xn, n):
    h = (xn - x0) / n

    return h * (
    ((fx(x0) + fx(xn)) / 2) + (
      sum([fx(x0 + (i*h)) for i in range(1, n)])
    )
    )
    
    
    

def trapezoidal(f,a,b,n):
    h = (b-a)/n
    f_sum=0
    for i in range(1,n,1):
        x = a+i*h
        f_sum= f_sum + f(x)
    return h*(0.5*f(a) + f_sum+ 0.5*f(b))

def trapezoidal(f,a,b,n):
    h = (b-a)/n
    result = 0.5*f(a)+0.5*f(b)
    for i in range(1,n):
        result  += f(a+i*h)
    result *=h
    return result 

from math import exp 
v = lambda t: 3*(t**2)*exp(t**3)
n = 4
trapezoidal(v,0,1,n)

def midpoint(f,a,b,n):
    h = (b-a)/n
    f_sum =0 
    for i in range(0,n,1):
        x = (a+h/2.0)+ i*h
        f_sum = f_sum +f(x)
    return  h*f_sum

import math
#the function to be integrated:
def f(x):
    return x ** 4 * (1 - x) ** 4 / (1 + x ** 2)
 
#define a function to do integration of f(x) btw. 0 and 1:
def trap(f, n):
    h = 1 / float(n)
    intgr = 0.5 * h * (f(0) + f(1))
    for i in range(1, int(n)):
        intgr = intgr + h * f(i * h)
    return intgr
 
print(trap(f, 100))

from math import *
n = 1
while abs(trap(f, n) - trap(f, n * 2)) > 1e-6:
    n += 1
print(n)

import math
#the function to be integrated:
def f(x):
    return math.exp(-x**2)
 
#define a function to do integration of f(x) btw. a and b:
def trap(f, n, a, b):
    h = (b - a) / float(n)
    intgr = 0.5 * h * (f(a) + f(b))
    for i in range(1, int(n)):
        intgr = intgr + h * f(a + i * h)
    return intgr
 
a = -10
b = 10
n = 100
 
while(abs(trap(f, n, a, b) - trap(f, n * 4, a * 2, b * 2)) > 1e-6):
    n *= 4
    a *= 2
    b *= 2
 


print(trap(f,n,a,b))



def integrate(N,a,b):
    
    def f(x):
        
        # type your function after return 
        return x**2
    value=0
    value2=0
    for n in range(1,N+1):
        value += f(a+(n-(1/2))* ((b-1)/N))
        value2 = ((b-1)/N) *value 
        return value2 



