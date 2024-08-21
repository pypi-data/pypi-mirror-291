def secant(f, x1, x2, tol):
    error = 1e3
    n = 0
    x3 = 0
    while error > tol:
        x3 = x1 - ((x2 - x1) / (f(x2) - f(x1))) * f(x1)
        x1 = x2
        x2 = x3
        error = abs(f(x3))
        n += 1
    print("Approximate solution: {:.4f}".format(x3))
    print("Number of iterations: {:d}".format(n))


import numpy as np
import matplotlib.pyplot as plt


def runge_kutta_system(f, g, x0, y0, a, b, h):
    t = np.arange(a, b + h, h)
    n = len(t)
    x = np.zeros(n)
    y = np.zeros(n)
    x[0] = x0
    y[0] = y0
    for i in range(n - 1):
        k1 = h * f(x[i], y[i], t[i])
        l1 = h * g(x[i], y[i], t[i])
        k2 = h * f(x[i] + k1 / 2, y[i] + l1 / 2, t[i] + h / 2)
        l2 = h * g(x[i] + k1 / 2, y[i] + l1 / 2, t[i] + h / 2)
        k3 = h * f(x[i] + k2 / 2, y[i] + l2 / 2, t[i] + h / 2)
        l3 = h * g(x[i] + k2 / 2, y[i] + l2 / 2, t[i] + h / 2)
        k4 = h * f(x[i] + k3, y[i] + l3, t[i] + h)
        l4 = h * g(x[i] + k3, y[i] + l3, t[i] + h)
        x[i + 1] = x[i] + (1 / 6) * (k1 + 2 * k2 + 2 * k3 + 2 * k4)
        y[i + 1] = y[i] + (1 / 6) * (l1 + 2 * l2 + 2 * l3 + 2 * l4)
    plt.plot(t, x, t, y)
    plt.show()




import numpy as np


def newton_raphson_system(F, J, x0, tol):
    x = x0
    error = 1e3
    n = 0
    while error > tol:
        dx = -np.linalg.solve(J(*x), F(*x))
        error = np.linalg.norm(dx) / np.linalg.norm(x)
        x += dx
        n += 1
    print("Iterations: ", n)
    return x



from numpy import sign
from numpy.lib.scimath import sqrt


def muller(f, x0, x1, x2, tol):
    error = 1e3
    x3 = 0
    while error > tol:
        c = f(x2)
        b = ((x0 - x2)**2 * (f(x1) - f(x2)) - (x1 - x2)**2 *
             (f(x0) - f(x2))) / ((x0 - x2) * (x1 - x2) * (x0 - x1))
        a = ((x1 - x2) * (f(x0) - f(x2)) - (x0 - x2) *
             (f(x1) - f(x2))) / ((x0 - x2) * (x1 - x2) * (x0 - x1))
        x3 = x2 - (2 * c) / (b + sign(b) * sqrt(b**2 - 4 * a * c))
        error = abs(x3 - x2)
        x0 = x1
        x1 = x2
        x2 = x3
    return x3



import numpy as np


def G(x):
    return np.exp(-(x**2))


def monte_carlo(G, a, b, M):
    s = 0
    for i in range(M):
        s += G(a + (b - a) * np.random.uniform(0, 1, 1))
    return ((b - a) / M) * s[0]


import pandas as pd


def bisection(f, a, b, tol):
    if f(a) * f(b) > 0:
        print("Interval not valid")
        return
    error = 1e3
    X_anterior = 0
    n = 1
    N = []
    Xa = []
    Xb = []
    Xm = []
    Fa = []
    Fb = []
    Fm = []
    E = []
    while error > tol:
        m = (a + b) / 2
        X_actual = m
        error = abs(X_anterior - X_actual)
        N.append(n)
        Xa.append(a)
        Xb.append(b)
        Xm.append(m)
        Fa.append(f(a))
        Fb.append(f(b))
        Fm.append(f(m))
        E.append(error)
        if f(a) * f(m) < 0:
            b = m
        else:
            a = m
        X_anterior = X_actual
        n += 1
    d = {
        "N": N,
        "Xa": Xa,
        "Xb": Xb,
        "Xm": Xm,
        "Fa": Fa,
        "Fb": Fb,
        "Fm": Fm,
        "E": E
    }
    TT = pd.DataFrame(d)
    TT.set_index("N", inplace=True)
    print(TT.to_string())




import numpy as np
from scipy.optimize import fsolve

musun = 132712000000
T = 365.25 * 86400 * 2 / 3
e = 581.2392124070273


def f(x):
    return ((T * musun ** 2 / (2 * np.pi)) ** (1 / 3) * np.sqrt(1 - x ** 2)
        - np.sqrt(.5 * musun ** 2 / e * (1 - x ** 2)))


x = fsolve(f, 0.01)
f(x)

x
from math import cos
import scipy.optimize
def func(x):
    y = x + 2*cos(x)
    return y
y = scipy.optimize.fsolve(func,0.2)
print (y)

from math import cos
import scipy.optimize
def func(x):
        y = [x[1]*x[0] - x[1] - 6, x[0]*cos(x[1]) - 3]
        return y
x0 = scipy.optimize.fsolve(func,[0, 2])
print(x0)

from math import sin
import scipy.optimize
def func(y):
        x= 4*sin(y) - 4
        return x
x= scipy.optimize.fsolve(func,0.3)
print (x)

import math

def rootsearch(f,a,b,dx):
    x1 = a; f1 = f(a)
    x2 = a + dx; f2 = f(x2)
    while f1*f2 > 0.0:
        if x1 >= b:
            return None,None
        x1 = x2; f1 = f2
        x2 = x1 + dx; f2 = f(x2)
    return x1,x2

def bisect(f,x1,x2,switch=0,epsilon=1.0e-9):
    f1 = f(x1)
    if f1 == 0.0:
        return x1
    f2 = f(x2)
    if f2 == 0.0:
        return x2
    if f1*f2 > 0.0:
        print('Root is not bracketed')
        return None
    n = int(math.ceil(math.log(abs(x2 - x1)/epsilon)/math.log(2.0)))
    for i in range(n):
        x3 = 0.5*(x1 + x2); f3 = f(x3)
        if (switch == 1) and (abs(f3) >abs(f1)) and (abs(f3) > abs(f2)):
            return None
        if f3 == 0.0:
            return x3
        if f2*f3 < 0.0:
            x1 = x3
            f1 = f3
        else:
            x2 =x3
            f2 = f3
    return (x1 + x2)/2.0

def roots(f, a, b, eps=1e-6):
    print ('The roots on the interval [%f, %f] are:' % (a,b))
    while 1:
        x1,x2 = rootsearch(f,a,b,eps)
        if x1 != None:
            a = x2
            root = bisect(f,x1,x2,1)
            if root != None:
                pass
                print (round(root,-int(math.log(eps, 10))))
        else:
            print ('\nDone')
            break

f=lambda x:x*math.cos(x-4)
roots(f, -3, 3)