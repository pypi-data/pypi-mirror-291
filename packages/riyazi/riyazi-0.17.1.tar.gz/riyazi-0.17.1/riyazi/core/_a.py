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


def G(x):
    return np.exp(-(x**2))


def monte_carlo(G, a, b, M):
    s = 0
    for i in range(M):
        s += G(a + (b - a) * np.random.uniform(0, 1, 1))
    return ((b - a) / M) * s[0]


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


def newton_raphson(f, df, xi, tol):
    x = xi
    error = 1e3
    n = 1
    while error > tol:
        x = x - f(x) / df(x)
        error = abs(f(x))
        n += 1
    print("Approximate solution: {:.4f}".format(x))
    print("Number of iterations: {:d}".format(n))

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


def trigonometric_interpolation(x, y):
    n = int((len(x) - 1) / 2)
    x = np.array(x)
    y = np.array(y)
    A = np.ones((2 * n + 1, 2 * n + 1))
    for i in range(2 * n + 1):
        k = 1
        for j in range(1, n + 1):
            A[i, j] = np.cos(k * x[i])
            k += 1
        k = 1
        for j in range(n + 1, 2 * n + 1):
            A[i, j] = np.sin(k * x[i])
            k += 1
    coef = np.linalg.solve(A, y)
    xd = np.linspace(x[0], x[-1])
    yd = []
    for i in range(len(xd)):
        s = coef[0]
        for k in range(1, n + 1):
            s += coef[k] * np.cos(k * xd[i])
            s += coef[k + n] * np.sin(k * xd[i])
        yd.append(s)
    yd = np.array(yd)
    plt.plot(x, y, "*", xd, yd)
    plt.show()


def trapezoidal(fx, x0, xn, n):
    h = (xn - x0) / n

    return h * (
    ((fx(x0) + fx(xn)) / 2) + (
      sum([fx(x0 + (i*h)) for i in range(1, n)])
    )
  )

def simpson(fx, x0, xn, n):
    h = (xn - x0) / n

    return (h / 3) * (
    fx(x0) + fx(xn) +
    (4 * sum([fx(x0 + (i*h)) for i in range(1, n, 2)])) +
    (2 * sum([fx(x0 + (i*h)) for i in range(2, n-1, 2)]))
  )

from math import prod

def lagrange(pairs, x, n=None):
    
    result = 0
    max_n = len(pairs) - 1

    if n == None or n > max_n:
        n = max_n

    for i in range(n+1):
        (xi, yi) = pairs[i]

        li = prod([
          (x - pairs[j][0]) / (xi - pairs[j][0])
          for j in range(n+1)
          if j != i
        ])
    

    result += li * yi

    return result




def solve_triangular(A, b):
    n = len(b)
    x = np.empty_like(b)
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(n-1, i, -1):
            x[i] -= A[i, j] * x[j]
        x[i] /= A[i, i]
    return x





def gausselmin(a,b):
    n= len(b)
    # Elimination phase
    for k in range(0,n-1):
        for i in range(k+1,n):
            if a[i,k] != 0.0:
                lam = a [i,k] / a[k,k]
                a[i,k+1:n] = a[i,k+1:n] - lam*a[k,k+1:n]
                b[i] = b[i]- lam*b[k]
    
    # Back substution
    for k in range(n-1, -1, -1):
        b[k] = (b[k] - np.dot(a[k,k+1:n], b[k+1:n])) /a[k,k]
        
    return b
                
                
                
import numpy as np
def solve_triangulars(A, b):
    n = len(b)
    x = np.empty_like(b)
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(n-1, i, -1):
            x[i] -= A[i, j] * x[j]
        x[i] /= A[i, i]
    return x





import numpy as np
def forward_sub(L, b):
    """x = forward_sub(L, b) is the solution to L x = b
       L must be a lower-triangular matrix
       b must be a vector of the same leading dimension as L
    """
    n = L.shape[0]
    x = np.zeros(n)
    for i in range(n):
        tmp = b[i]
        for j in range(i-1):
            tmp -= L[i,j] * x[j]
        x[i] = tmp / L[i,i]
    return x



import numpy as np
def back_sub(U, b):
    """x = back_sub(U, b) is the solution to U x = b
       U must be an upper-triangular matrix
       b must be a vector of the same leading dimension as U
    """
    n = U.shape[0]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        tmp = b[i]
        for j in range(i+1, n):
            tmp -= U[i,j] * x[j]
        x[i] = tmp / U[i,i]
    return x



import numpy as np
def lu_solve(L, U, b):
    """x = lu_solve(L, U, b) is the solution to L U x = b
       L must be a lower-triangular matrix
       U must be an upper-triangular matrix of the same size as L
       b must be a vector of the same leading dimension as L
    """
    y = forward_sub(L, b)
    x = back_sub(U, y)
    return x



import numpy as np
def lu_decomp(A):
    """(L, U) = lu_decomp(A) is the LU decomposition A = L U
       A is any matrix
       L will be a lower-triangular matrix with 1 on the diagonal, the same shape as A
       U will be an upper-triangular matrix, the same shape as A
    """
    n = A.shape[0]
    if n == 1:
        L = np.array([[1]])
        U = A.copy()
        return (L, U)

    A11 = A[0,0]
    A12 = A[0,1:]
    A21 = A[1:,0]
    A22 = A[1:,1:]

    L11 = 1
    U11 = A11

    L12 = np.zeros(n-1)
    U12 = A12.copy()

    L21 = A21.copy() / U11
    U21 = np.zeros(n-1)

    S22 = A22 - np.outer(L21, U12)
    (L22, U22) = lu_decomp(S22)

    L = np.block([[L11, L12], [L21, L22]])
    U = np.block([[U11, U12], [U21, U22]])
    return (L, U)


import numpy as np
def linear_solve_without_pivoting(A, b):
    """x = linear_solve_without_pivoting(A, b) is the solution to A x = b (computed without pivoting)
       A is any matrix
       b is a vector of the same leading dimension as A
       x will be a vector of the same leading dimension as A
    """
    (L, U) = lu_decomp(A)
    x = lu_solve(L, U, b)
    return x



import numpy as np
def lup_solve(L, U, P, b):
    """x = lup_solve(L, U, P, b) is the solution to L U x = P b
       L must be a lower-triangular matrix
       U must be an upper-triangular matrix of the same shape as L
       P must be a permutation matrix of the same shape as L
       b must be a vector of the same leading dimension as L
    """
    z = np.dot(P, b)
    x = lu_solve(L, U, z)
    return x

import numpy as np
def lup_decomp(A):
    """(L, U, P) = lup_decomp(A) is the LUP decomposition P A = L U
       A is any matrix
       L will be a lower-triangular matrix with 1 on the diagonal, the same shape as A
       U will be an upper-triangular matrix, the same shape as A
       U will be a permutation matrix, the same shape as A
    """
    n = A.shape[0]
    if n == 1:
        L = np.array([[1]])
        U = A.copy()
        P = np.array([[1]])
        return (L, U, P)

    i = np.argmax(A[:,0])
    A_bar = np.vstack([A[i,:], A[:i,:], A[(i+1):,:]])

    A_bar11 = A_bar[0,0]
    A_bar12 = A_bar[0,1:]
    A_bar21 = A_bar[1:,0]
    A_bar22 = A_bar[1:,1:]

    S22 = A_bar22 - np.dot(A_bar21, A_bar12) / A_bar11

    (L22, U22, P22) = lup_decomp(S22)

    L11 = 1
    U11 = A_bar11

    L12 = np.zeros(n-1)
    U12 = A_bar12.copy()

    L21 = np.dot(P22, A_bar21) / A_bar11
    U21 = np.zeros(n-1)

    L = np.block([[L11, L12], [L21, L22]])
    U = np.block([[U11, U12], [U21, U22]])
    P = np.block([
        [np.zeros((1, i-1)), 1,                  np.zeros((1, n-i))],
        [P22[:,:(i-1)],      np.zeros((n-1, 1)), P22[:,i:]]
    ])
    return (L, U, P)


import numpy as np
def linear_solve(A, b):
    """x = linear_solve(A, b) is the solution to A x = b (computed with partial pivoting)
       A is any matrix
       b is a vector of the same leading dimension as A
       x will be a vector of the same leading dimension as A
    """
    (L, U, P) = lup_decomp(A)
    x = lup_solve(L, U, P, b)
    return x

# https://courses.physics.illinois.edu/cs357/sp2020/notes/ref-9-linsys.html


def LU(A):
	
	n = len(A) # Give us total of lines

	# (1) Extract the b vector
	b = [0 for i in range(n)]
	for i in range(0,n):
		b[i]=A[i][n]

	# (2) Fill L matrix and its diagonal with 1
	L = [[0 for i in range(n)] for i in range(n)]
	for i in range(0,n):
		L[i][i] = 1

	# (3) Fill U matrix
	U = [[0 for i in range(0,n)] for i in range(n)]
	for i in range(0,n):
		for j in range(0,n):
			U[i][j] = A[i][j]

	n = len(U)

	# (4) Find both U and L matrices
	for i in range(0,n): # for i in [0,1,2,..,n]
		# (4.1) Find the maximun value in a column in order to change lines
		maxElem = abs(U[i][i])
		maxRow = i
		for k in range(i+1, n): # Interacting over the next line
			if(abs(U[k][i]) > maxElem):
				maxElem = abs(U[k][i]) # Next line on the diagonal
				maxRow = k

		# (4.2) Swap the rows pivoting the maxRow, i is the current row
		for k in range(i, n): # Interacting column by column
			tmp=U[maxRow][k]
			U[maxRow][k]=U[i][k]
			U[i][k]=tmp

		# (4.3) Subtract lines
		for k in range(i+1,n):
			c = -U[k][i]/float(U[i][i])
			L[k][i] = c # (4.4) Store the multiplier
			for j in range(i, n):
				U[k][j] += c*U[i][j] # Multiply with the pivot line and subtract

		# (4.5) Make the rows bellow this one zero in the current column
		for k in range(i+1, n):
			U[k][i]=0

	n = len(L)

	# (5) Perform substitutioan Ly=b
	y = [0 for i in range(n)]
	for i in range(0,n,1):
		y[i] = b[i]/float(L[i][i])
		for k in range(0,i,1):
			y[i] -= y[k]*L[i][k]

	n = len(U)

	# (6) Perform substitution Ux=y
	x = [0 in range(n)]
	for i in range(n-1,-1,-1):
		x[i] = y[i]/float(U[i][i])
		for k in range (i-1,-1,-1):
			U[i] -= x[i]*U[i][k]

	return x


# https://gist.github.com/angellicacardozo/4b35e15aa21af890b4a8fedef9891401\
    
    
    
def LUdecomp(a):
    n = len(a)
    for k in range(0,n-1):
        for i in range(k+1,n):
            if a[i,k] !=0.0:
                lam = a[i,k]/ a[k,k]
                a[i,k+1:n] = a[i,k+1:n] - lam*a[k,k+1:n]
                a[i,k] = lam 
    return a 



def LUsolve(a,b):
    n = len(a)
    for k in range(1,n):
        b[k] = b[k] - np.dot(a[k,0:k], b[0:k])
    b[n-1]  = b[n-1] /a[n-1,n-1]
    for k in range(n-2,-1,-1):
        b[k] = (b[k] - np.dot(a[k,k+1:n], b[k+1:n])) /a[k,k]
    return b 
    
    
    
import math 

def is_pos_def(x):
    return np.all(np.linalg.eigvals(x) > 0)


def chleski(a):
    n = len(a)
    for k in range(n):
        a[k,k] = math.sqrt(a[k,k] - np.dot(a[k,0:k], a[k,0:k]))
        if is_pos_def(a) is False:
            print("Matrix is not positive definite")
            break
        for i in range(k+1,n):
            a[i,k]= (a[i,k] - np.dot(a[i,0:k], a[k,0:k])) / a[k,k]
        for k in range(1,n): a[0:k,k] = 0.0
        return a 
    
    
    
from math import sqrt, log10, floor
import numpy as np


_DEFAULT_MAX_ITER = 500
_DEFAULT_TOLER = 1e-4

def briot_ruffini(poly, a):
    quot = []
    aux = 0
    for coef in poly:
        aux *= a
        aux += coef
        quot.append(aux)
    remainder = quot[-1]
    quot = quot[:-1]
    return np.poly1d(quot), remainder

def _sign(x):
    return abs(x) // x

def _print_row(items, padding):
    for i, x in enumerate(items):
        try:
            items[i] = round(x, padding)
        except TypeError:
            pass
    print(*(str(i).rjust(padding+3) for i in items), sep='\t')

_bissection_header = ['iter', 'a', 'b', 'x', 'Fa', 'Fb', 'Fx', 'err']
_linear_header = ['iter', 'a', 'b', 'x', 'Fx', 'delta_x']
_quad_header = _linear_header.copy()
_quad_header.insert(3, 'c')

def bissection(func, a, b, max_iter=_DEFAULT_MAX_ITER, toler=_DEFAULT_TOLER, debug=False):
    precision = -floor(log10(toler))
    Fa, Fb = func(a), func(b)
    if Fa * Fb > 0:
        raise ValueError('f(a)*f(b) must be less than 0.')
    err = abs(b - a)
    if Fa > 0: a, b, Fa, Fb = b, a, Fb, Fa
    if debug: _print_row(_bissection_header, precision)
    for i in range(max_iter):
        err /= 2
        x = (a + b) / 2
        Fx = func(x)
        if debug: _print_row([i, a, b, x, Fa, Fb, Fx, err], precision)
        if err < toler: break
        if Fx < 0:
            a, Fa = x, Fx
        else:
            b, Fb = x, Fx
    return x, err

def secant(func, a, b, max_iter=_DEFAULT_MAX_ITER, toler=_DEFAULT_TOLER, debug=False):
    precision = -floor(log10(toler))
    if debug: _print_row(_linear_header, precision)
    Fa, Fb = func(a), func(b)
    if abs(Fa) < abs(Fb): a, b, Fa, Fb = b, a, Fb, Fa
    x, Fx = b, Fb
    for i in range(max_iter):
        delta_x = -Fx / (Fb - Fa) * (b - a)
        x += delta_x; Fx = func(x)
        if debug: _print_row([i, a, b, x, Fx, delta_x], precision)
        if abs(delta_x) < toler and abs(Fx) < toler: break
        a, b, Fa, Fb = b, x, Fb, Fx
    return x, delta_x

def regula_falsi(func, a, b, max_iter=_DEFAULT_MAX_ITER, toler=_DEFAULT_TOLER, debug=False):
    precision = -floor(log10(toler))
    Fa, Fb = func(a), func(b)
    if Fa * Fb > 0:
        raise ValueError('f(a)*f(b) must be less than 0.')
    if Fa > 0: a, b, Fa, Fb = b, a, Fb, Fa
    if debug: _print_row(_linear_header, precision)
    x, Fx = b, Fb
    for i in range(max_iter):
        delta_x = -Fx / (Fb - Fa) * (b - a)
        x += delta_x; Fx = func(x)
        if debug: _print_row([i, a, b, x, Fx, delta_x], precision)
        if abs(delta_x) < toler and abs(func(x)) < toler: break
        if Fx < 0:
            a, Fa = x, Fx
        else:
            b, Fb = x, Fx
    return x, delta_x

def pegasus(func, a, b, max_iter=_DEFAULT_MAX_ITER, toler=_DEFAULT_TOLER, debug=False):
    precision = -floor(log10(toler))
    Fa, Fb = func(a), func(b)
    if debug: _print_row(_linear_header, precision)
    x, Fx = b, Fb
    for i in range(max_iter):
        delta_x = -Fx / (Fb - Fa) * (b - a)
        x += delta_x; Fx = func(x)
        if debug: _print_row([i, a, b, x, Fx, delta_x], precision)
        if abs(delta_x) < toler and abs(func(x)) < toler: break
        if Fx * Fb < 0:
            a, Fa = b, Fb
        else:
            Fa *= Fb / (Fb + Fx)
        b, Fb = x, Fx
    return x, delta_x

def muller(func, a, c, max_iter=_DEFAULT_MAX_ITER, toler=_DEFAULT_TOLER, debug=False):
    precision = -floor(log10(toler))
    Fa, Fc, b = func(a), func(c), (a + c) / 2
    Fb = func(b)
    x, Fx, delta_x = b, Fb, c - a
    if debug: _print_row(_quad_header, precision)
    for i in range(max_iter):
        if abs(Fx) < toler and abs(delta_x) < toler: break
        h1, h2 = c - b, b - a
        r, t = h1 / h2, x
        A = (Fc - (r + 1) * Fb + r * Fa) / (h1 * (h1 + h2))
        B = (Fc - Fb) / h1 - A * h1
        C = Fb
        z = (-B + _sign(B) * sqrt(B**2 - 4 * A * C)) / (2 * A)
        x, delta_x = b + z, x - t
        Fx = func(x)
        if debug: _print_row([i, a, b, c, x, Fx, delta_x], precision)
        if x > b:
            a, Fa = b, Fb
        else:
            c, Fc = b, Fb
        b, Fb = x, Fx
    return x, delta_x

def wijngaarden_dekker_brent(func, a, b, max_iter=_DEFAULT_MAX_ITER, toler=_DEFAULT_TOLER, debug=False):
    precision = -floor(log10(toler))
    Fa, Fb = func(a), func(b)
    if Fa * Fb > 0:
        raise ValueError('Fa*Fb must be less than zero.')
    if debug: _print_row(['iter', 'x', 'Fx', 'z'], precision)
    c, Fc = b, Fb
    for i in range(max_iter):
        if Fb * Fc > 0: 
            c, Fc, d = a, Fa, b - a
            e = d
        elif abs(Fc) < abs(Fb):
            # the source material says it's if instead of elif here, but it does not work with IF.
            a, b, c, Fa, Fb, Fc = b, c, a, Fb, Fc, Fa
        tol = 2 * toler * max(abs(b), 1)
        z = (c - b) / 2
        if debug: _print_row([i, b, Fb, z], precision)
        if abs(z) <= tol or Fb == 0: break
        # pick between interpolation and bissection
        if abs(e) >= tol and abs(Fa) > abs(Fb):
            s = Fb / Fa
            if a == c:
                # linear interp
                p = 2 * z * s
                q = 1 - s
            else:
                # quadratic inverse interp
                q, r = Fa / Fc, Fb / Fc
                p = s * (2 * z * q * (q - r) - (b - a) * (r - 1))
                q = (q - 1) * (r - 1) * (s - 1)
            if p > 0:
                q = -q
            else:
                p = -p
            if 2 * p < min(3 * z * q - abs(tol * q), abs(e * q)):
                # accept interpolation
                e, d = d, p / q
            else:
                # uses bissection since interp failed
                d, e = z, z
        else:
            # bissection
            d, e = z, z
        a, Fa = b, Fb
        if abs(d) > tol:
            b += d
        else:
            b += _sign(z) * tol
        Fb = func(b)
    return b, z

def newton(func, dfunc, x0, toler=_DEFAULT_TOLER, max_iter=_DEFAULT_MAX_ITER,
           debug=False):
    return schroder(func, dfunc, x0, 1, toler, max_iter, debug)

def schroder(func, dfunc, x0, m, toler=_DEFAULT_TOLER, max_iter=_DEFAULT_MAX_ITER,
             debug=False):
    precision = -floor(log10(toler))
    Fx, DFx, x = func(x0), dfunc(x0), x0
    if debug:
        _print_row(['iter', 'x', 'Fx', 'DeltaX'], precision)
    for i in range(max_iter):
        delta_x = m * -Fx / DFx
        x += delta_x
        Fx, DFx = func(x), dfunc(x)
        if debug: _print_row([i, x, Fx, delta_x], precision)
        if abs(delta_x) < toler and abs(Fx) < toler or abs(DFx) == 0: break
    return x, delta_x


"""
Implementing Secant method in Python
Author: dimgrichr
"""
from math import exp


def f(x: float) -> float:
    """
    >>> f(5)
    39.98652410600183
    """
    return 8 * x - 2 * exp(-x)


def secant_method(lower_bound: float, upper_bound: float, repeats: int) -> float:
    """
    >>> secant_method(1, 3, 2)
    0.2139409276214589
    """
    x0 = lower_bound
    x1 = upper_bound
    for i in range(0, repeats):
        x0, x1 = x1, x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0))
    return x1



def ucal(u: float, p: int) -> float:
    """
    >>> ucal(1, 2)
    0
    >>> ucal(1.1, 2)
    0.11000000000000011
    >>> ucal(1.2, 2)
    0.23999999999999994
    """
    temp = u
    for i in range(1, p):
        temp = temp * (u - i)
    return temp


import numpy as np 

def divided_diff(x, y):
    '''
    function to calculate the divided
    differences table
    '''
    n = len(y)
    coef = np.zeros([n, n])
    # the first column is y
    coef[:,0] = y
    
    for j in range(1,n):
        for i in range(n-j):
            coef[i][j] = \
           (coef[i+1][j-1] - coef[i][j-1]) / (x[i+j]-x[i])
            
    return coef

def newton_poly(coef, x_data, x):
    '''
    evaluate the newton polynomial 
    at x
    '''
    n = len(x_data) - 1 
    p = coef[n]
    for k in range(1,n+1):
        p = coef[n-k] + (x -x_data[n-k])*p
    return p



#https://en.wikipedia.org/wiki/Newton_polynomial#:~:text=In%20the%20mathematical%20field%20of%20numerical%20analysis%2C%20a,polynomial%20for%20a%20given%20set%20of%20data%20points.

#https://en.wikipedia.org/wiki/Newton_polynomial

# https://en.wikipedia.org/wiki/Newton%27s_identities




from numpy import diagonal
from numpy import zeros
from sympy import simplify
from sympy import symbols


def coefficients(x, y):
    assert len(x) == len(y), "arguments must have the same size"
    size = len(x)
    result = zeros((size, size))
    result[:, 0] = y
    for column in range(1, size):
        result[column:, column] = (
            (result[column:, column-1] - result[column-1:-1, column-1])
            / (x[column:] - x[:-column])
        )
    return diagonal(result)


def expression(a, x):
    assert len(a) == len(x), "arguments must have the same size"
    size = len(a)

    x_ = symbols('x')
    xs = [1 for i in range(size)]
    result = [a[0] for i in range(size)]
    for i, x_i in enumerate(x[:-1], start=1):
        xs[i] = xs[i-1] * (x_ - x_i)
        result[i] = a[i] * xs[i]

    return simplify(sum(result))


def polynomial(x, y):
    a = coefficients(x, y)
    return expression(a, x)



"""Methods for polynomials."""


import numpy as np


def briot_ruffini(a, root):
    """Divide a polynomial by another polynomial.

    The format is: P(x) = Q(x) * (x-root) + rest.

    Args:
        a: an array containing the coefficients of the input polynomial.
        root: one of the polynomial roots.

    Returns:
        b: an array containing the coefficients of the output polynomial.
        rest: polynomial division Rest.
    """
    n = a.size - 1
    b = np.zeros(n)

    b[0] = a[0]

    for i in range(1, n):
        b[i] = b[i - 1] * root + a[i]

    rest = b[n - 1] * root + a[n]

    return [b, rest]


def newton_divided_difference(x, y):
    """Find the coefficients of Newton's divided difference.

    Also, find Newton's polynomial.

    Args:
        x: an array containing x values.
        y: an array containing y values.

    Returns:
        f: an array containing Newton's divided difference coefficients.
    """
    n = x.size
    q = np.zeros((n, n - 1))

    # Insert 'y' in the first column of the matrix 'q'
    q = np.concatenate((y[:, None], q), axis=1)

    for i in range(1, n):
        for j in range(1, i + 1):
            q[i, j] = (q[i, j - 1] - q[i - 1, j - 1]) / (x[i] - x[i - j])

    # Copy the diagonal values of the matrix q to the vector f
    f = np.zeros(n)
    for i in range(0, n):
        f[i] = q[i, i]

    # Prints the polynomial
    print("The polynomial is:")
    print("p(x)={:+.4f}".format(f[0]), end="")
    for i in range(1, n):
        print("{:+.4f}".format(f[i]), end="")
        for j in range(1, i + 1):
            print("(x{:+.4f})".format(x[j] * -1), end="")
    print("")

    return [f]


briot_ruffini(np.array([4,5]),5)

"""Methods for solutions of equations."""

import math


def bisection(f, a, b, tol, iter_max):
    """Calculate the root of an equation by the Bisection method.

    Args:
        f: function f(x).
        a: lower limit.
        b: upper limit.
        tol: tolerance.
        iter_max: maximum number of iterations.

    Returns:
        root: root value.
        iter: used iterations.
        converged: found the root.
    """
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        raise Exception("The function does not change signal at \
              the ends of the given interval.")

    delta_x = math.fabs(b - a) / 2

    x = 0
    converged = False
    i = 0
    for i in range(0, iter_max + 1):
        x = (a + b) / 2
        fx = f(x)

        print("i: {:03d}\t x: {:+.4f}\t fx: {:+.4f}\t dx: {:+.4f}\n"
              .format(i, x, fx, delta_x), end="")

        if delta_x <= tol and math.fabs(fx) <= tol:
            converged = True
            break

        if fa * fx > 0:
            a = x
            fa = fx
        else:
            b = x

        delta_x = delta_x / 2
    else:
        print("Warning: The method did not converge.")

    root = x
    return [root, i, converged]


def newton(f, df, x0, tol, iter_max):
    """Calculate the root of an equation by the Newton method.

    Args:
        f: function f(x).
        df: derivative of function f(x).
        x0: initial guess.
        tol: tolerance.
        iter_max: maximum number of iterations.

    Returns:
        root: root value.
        iter: used iterations.
        converged: found the root.
    """
    x = x0
    fx = f(x)
    dfx = df(x)

    converged = False
    print("iter: 0 x: {:.4f}\t dfx: {:.4f}\t fx: {:.4f}\n"
          .format(x, dfx, fx), end="")

    i = 0
    for i in range(1, iter_max + 1):
        delta_x = -fx / dfx
        x += delta_x
        fx = f(x)
        dfx = df(x)

        print("i:{:03d}\t x: {:.4f}\t dfx: {:.4f}\t fx: {:.4f}\t dx: {:.4f}\n"
              .format(i, x, dfx, fx, delta_x), end="")

        if math.fabs(delta_x) <= tol and math.fabs(fx) <= tol or dfx == 0:
            converged = True
            break
    else:
        print("Warning: The method did not converge.")

    root = x
    return [root, i, converged]


def secant(f, a, b, tol, iter_max):
    """Calculate the root of an equation by the Secant method.

    Args:
        f: function f(x).
        a: lower limit.
        b: upper limit.
        tol: tolerance.
        iter_max: maximum number of iterations.

    Returns:
        root: root value.
        iter: used iterations.
        converged: found the root.
    """
    fa = f(a)
    fb = f(b)

    if fb - fa == 0:
        raise Exception("f(b)-f(a) must be nonzero.")

    if b - a == 0:
        raise Exception("b-a must be nonzero.")

    if math.fabs(fa) < math.fabs(fb):
        a, b = b, a
        fa, fb = fb, fa

    x = b
    fx = fb

    converged = False
    i = 0
    for i in range(0, iter_max + 1):
        delta_x = -fx / (fb - fa) * (b - a)
        x += delta_x
        fx = f(x)

        print("i: {:03d}\t x: {:+.4f}\t fx: {:+.4f}\t dx: {:+.4f}\n"
              .format(i, x, fx, delta_x), end="")

        if math.fabs(delta_x) <= tol and math.fabs(fx) <= tol:
            converged = True
            break

        a, b = b, x
        fa, fb = fb, fx
    else:
        print("Warning: The method did not converge.")

    root = x
    return [root, i, converged]


"""Methods for ordinary differential equations."""

import numpy as np


def euler(f, a, b, n, ya):
    """Calculate the solution of the initial-value problem (IVP).

    Solve the IVP from the Euler method.

    Args:
        f: function f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.
        ya: initial value.

    Returns:
        vx: an array containing x values.
        vy: an array containing y values (solution of IVP).
    """
    vx = np.zeros(n)
    vy = np.zeros(n)

    h = (b - a) / n
    x = a
    y = ya

    vx[0] = x
    vy[0] = y

    fxy = f(x, y)
    print("i: {:03d}\t x: {:.4f}\t y: {:.4f}\n".format(0, x, y), end="")

    for i in range(0, n):
        x = a + (i + 1) * h
        y += h * fxy

        fxy = f(x, y)
        print("i: {:03d}\t x: {:.4f}\t y: {:.4f}\n"
              .format(i + 1, x, y), end="")
        vx[i] = x
        vy[i] = y

    return [vx, vy]


def taylor2(f, df1, a, b, n, ya):
    """Calculate the solution of the initial-value problem (IVP).

    Solve the IVP from the Taylor (Order Two) method.

    Args:
        f: function f(x).
        df1: 1's derivative of function f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.
        ya: initial value.

    Returns:
        vx: an array containing x values.
        vy: an array containing y values (solution of IVP).
    """
    vx = np.zeros(n)
    vy = np.zeros(n)

    h = (b - a) / n
    x = a
    y = ya

    vx[0] = x
    vy[0] = y

    print("i: {:03d}\t x: {:.4f}\t y: {:.4f}\n".format(0, x, y), end="")

    for i in range(0, n):
        y += h * (f(x, y) + 0.5 * h * df1(x, y))
        x = a + (i + 1) * h

        print(
            "i: {:03d}\t x: {:.4f}\t y: {:.4f}\n".format(
                i + 1, x, y), end="")
        vx[i] = x
        vy[i] = y

    return [vx, vy]


def taylor4(f, df1, df2, df3, a, b, n, ya):
    """Calculate the solution of the initial-value problem (IVP).

    Solve the IVP from the Taylor (Order Four) method.

    Args:
        f: function f(x).
        df1: 1's derivative of function f(x).
        df2: 2's derivative of function f(x).
        df3: 3's derivative of function f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.
        ya: initial value.

    Returns:
        vx: an array containing x values.
        vy: an array containing y values (solution of IVP).
    """
    vx = np.zeros(n)
    vy = np.zeros(n)

    h = (b - a) / n
    x = a
    y = ya

    vx[0] = x
    vy[0] = y

    print("i: {:03d}\t x: {:.4f}\t y: {:.4f}\n".format(0, x, y), end="")

    for i in range(0, n):
        y += h * (f(x, y) + 0.5 * h * df1(x, y) + (h ** 2 / 6) * df2(x, y) +
                  (h ** 3 / 24) * df3(x, y))
        x = a + (i + 1) * h

        print(
            "i: {:03d}\t x: {:.4f}\t y: {:.4f}\n".format(
                i + 1, x, y), end="")
        vx[i] = x
        vy[i] = y

    return [vx, vy]


def rk4(f, a, b, n, ya):
    """Calculate the solution of the initial-value problem (IVP).

    Solve the IVP from the Runge-Kutta (Order Four) method.

    Args:
        f: function f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.
        ya: initial value.

    Returns:
        vx: an array containing x values.
        vy: an array containing y values (solution of IVP).
    """
    vx = np.zeros(n)
    vy = np.zeros(n)

    h = (b - a) / n
    x = a
    y = ya

    k = np.zeros(4)

    vx[0] = x
    vy[0] = y

    print("i: {:03d}\t x: {:.4f}\t y: {:.4f}\n".format(0, x, y), end="")

    for i in range(0, n):
        k[0] = h * f(x, y)
        k[1] = h * f(x + h / 2, y + k[0] / 2)
        k[2] = h * f(x + h / 2, y + k[1] / 2)
        k[3] = h * f(x + h, y + k[2])

        x = a + (i + 1) * h
        y += (k[0] + 2 * k[1] + 2 * k[2] + k[3]) / 6

        print(
            "i: {:03d}\t x: {:.4f}\t y: {:.4f}\n".format(
                i + 1, x, y), end="")
        vx[i] = x
        vy[i] = y

    return [vx, vy]


def rk4_system(f, a, b, n, ya):
    """Calculate the solution of systems of differential equations.

    Solve from Runge-Kutta (Order Four) method.

    Args:
        f: an array of functions f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.
        ya: an array of initial values.

    Returns:
        vx: an array containing x values.
        vy: an array containing y values (solution of IVP).
    """
    m = len(f)

    k = [np.zeros(m), np.zeros(m), np.zeros(m), np.zeros(m)]

    vx = np.zeros(n + 1)
    vy = np.zeros((m, n + 1))

    h = (b - a) / n

    x = a
    y = ya

    vx[0] = x
    vy[:, 0] = y

    for i in range(0, n):

        for j in range(0, m):
            k[0][j] = h * f[j](x, y)

        for j in range(0, m):
            k[1][j] = h * f[j](x + h / 2, y + k[0] / 2)

        for j in range(0, m):
            k[2][j] = h * f[j](x + h / 2, y + k[1] / 2)

        for j in range(0, m):
            k[3][j] = h * f[j](x + h, y + k[2])

        x = a + i * h
        y = y + (k[0] + 2 * k[1] + 2 * k[2] + k[3]) / 6

        vx[i + 1] = x
        vy[:, i + 1] = y

    return [vx, vy]


"""Methods for Linear Systems."""

import numpy as np


def jacobi(a, b, x0, tol, iter_max):
    """Jacobi method: solve Ax = b given an initial approximation x0.

    Args:
        a: matrix A from system Ax=b.
        b: an array containing b values.
        x0: initial approximation of the solution.
        tol: tolerance.
        iter_max: maximum number of iterations.

    Returns:
        x: solution of linear the system.
        iter: used iterations.
    """
    # D and M matrices
    d = np.diag(np.diag(a))
    m = a - d

    # Iterative process
    i = 1
    x = None
    for i in range(1, iter_max + 1):
        x = np.linalg.solve(d, (b - np.dot(m, x0)))

        if np.linalg.norm(x - x0, np.inf) / np.linalg.norm(x, np.inf) <= tol:
            break
        x0 = x.copy()

    return [x, i]


def gauss_seidel(a, b, x0, tol, iter_max):
    """Gauss-Seidel method: solve Ax = b given an initial approximation x0.

    Args:
        a: matrix A from system Ax=b.
        b: an array containing b values.
        x0: initial approximation of the solution.
        tol: tolerance.
        iter_max: maximum number of iterations.

    Returns:
        x: solution of linear the system.
        iter: used iterations.
    """
    # L and U matrices
    lower = np.tril(a)
    upper = a - lower

    # Iterative process
    i = 1
    x = None
    for i in range(1, iter_max + 1):
        x = np.linalg.solve(lower, (b - np.dot(upper, x0)))

        if np.linalg.norm(x - x0, np.inf) / np.linalg.norm(x, np.inf) <= tol:
            break
        x0 = x.copy()

    return [x, i]


"""Iterative Methods for Linear Systems."""

import math
import numpy as np


def backward_substitution(upper, d):
    """Solve the upper linear system ux=d.

    Args:
        upper: upper triangular matrix.
        d: an array containing d values.

    Returns:
        x: solution of linear the system.
    """
    [n, m] = upper.shape
    b = d.astype(float)

    if n != m:
        raise Exception("'upper' must be a square matrix.")

    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        if upper[i, i] == 0:
            raise Exception("Matrix 'upper' is singular.")

        x[i] = b[i] / upper[i, i]
        b[0:i] = b[0:i] - upper[0:i, i] * x[i]

    return [x]


def forward_substitution(lower, c):
    """Solve the lower linear system lx=c.

    Args:
        lower: lower triangular matrix.
        c: an array containing c values.

    Returns:
        x: solution of linear the system.
    """
    [n, m] = lower.shape
    b = c.astype(float)

    if n != m:
        raise Exception("'lower' must be a square matrix.")

    x = np.zeros(n)

    for i in range(0, n):
        if lower[i, i] == 0:
            raise Exception("Matrix 'lower' is singular.")

        x[i] = b[i] / lower[i, i]
        b[i + 1:n] = b[i + 1:n] - lower[i + 1:n, i] * x[i]

    return [x]


def gauss_elimination_pp(a, b):
    """Gaussian Elimination with Partial Pivoting.

    Calculate the upper triangular matrix from linear system Ax=b (make a row
    reduction).

    Args:
        a: matrix A from system Ax=b.
        b: an array containing b values.

    Returns:
        a: augmented upper triangular matrix.
    """
    [n, m] = a.shape

    if n != m:
        raise Exception("'a' must be a square matrix.")

    # Produces the augmented matrix
    a = np.concatenate((a, b[:, None]), axis=1).astype(float)

    # Elimination process starts
    for i in range(0, n - 1):
        p = i

        # Comparison to select the pivot
        for j in range(i + 1, n):
            if math.fabs(a[j, i]) > math.fabs(a[i, i]):
                # Swap rows
                a[[i, j]] = a[[j, i]]

        # Checking for nullity of the pivots
        while p < n and a[p, i] == 0:
            p += 1

        if p == n:
            print("Info: No unique solution.")
        else:
            if p != i:
                # Swap rows
                a[[i, p]] = a[[p, i]]

        for j in range(i + 1, n):
            a[j, :] = a[j, :] - a[i, :] * (a[j, i] / a[i, i])

    # Checking for nonzero of last entry
    if a[n - 1, n - 1] == 0:
        print("Info: No unique solution.")

    return [a]


"""Methods for Interpolation."""

import numpy as np


def lagrange(x, y, x_int):
    """Interpolates a value using the 'Lagrange polynomial'.

    Args:
        x: an array containing x values.
        y: an array containing y values.
        x_int: value to interpolate.

    Returns:
        y_int: interpolated value.
    """
    n = x.size
    y_int = 0

    for i in range(0, n):
        p = y[i]
        for j in range(0, n):
            if i != j:
                p = p * (x_int - x[j]) / (x[i] - x[j])
        y_int = y_int + p

    return [y_int]


def neville(x, y, x_int):
    """Interpolates a value using the 'Neville polynomial'.

    Args:
        x: an array containing x values.
        y: an array containing y values.
        x_int: value to interpolate.

    Returns:
        y_int: interpolated value.
        q: coefficients matrix.
    """
    n = x.size
    q = np.zeros((n, n - 1))

    # Insert 'y' in the first column of the matrix 'q'
    q = np.concatenate((y[:, None], q), axis=1)

    for i in range(1, n):
        for j in range(1, i + 1):
            q[i, j] = ((x_int - x[i - j]) * q[i, j - 1] -
                       (x_int - x[i]) * q[i - 1, j - 1]) / (x[i] - x[i - j])

    y_int = q[n - 1, n - 1]
    return [y_int, q]


"""Methods for numerical integration."""


def composite_simpson(f, b, a, n):
    """Calculate the integral from 1/3 Simpson's Rule.

    Args:
        f: function f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.

    Returns:
        xi: integral value.
    """
    h = (b - a) / n

    sum_odd = 0
    sum_even = 0

    for i in range(0, n - 1):
        x = a + (i + 1) * h
        if (i + 1) % 2 == 0:
            sum_even += f(x)
        else:
            sum_odd += f(x)

    xi = h / 3 * (f(a) + 2 * sum_even + 4 * sum_odd + f(b))
    return [xi]


def composite_trapezoidal(f, b, a, n):
    """Calculate the integral from the Trapezoidal Rule.

    Args:
        f: function f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.

    Returns:
        xi: integral value.
    """
    h = (b - a) / n

    sum_x = 0

    for i in range(0, n - 1):
        x = a + (i + 1) * h
        sum_x += f(x)

    xi = h / 2 * (f(a) + 2 * sum_x + f(b))
    return [xi]


def composite2_simpson(x, y):
    """Calculate the integral from 1/3 Simpson's Rule.

    Args:
        x: an array containing x values.
        y: an array containing y values.

    Returns:
        xi: integral value.
    """
    if y.size != y.size:
        raise Exception("'x' and 'y' must have same size.")

    h = x[1] - x[0]
    n = x.size

    sum_odd = 0
    sum_even = 0

    for i in range(1, n - 1):
        if (i + 1) % 2 == 0:
            sum_even += y[i]
        else:
            sum_odd += y[i]

    xi = h / 3 * (y[0] + 2 * sum_even + 4 * sum_odd + y[n - 1])
    return [xi]


def composite2_trapezoidal(x, y):
    """Calculate the integral from the Trapezoidal Rule.

    Args:
        x: an array containing x values.
        y: an array containing y values.

    Returns:
        xi: integral value.
    """
    if y.size != y.size:
        raise Exception("'x' and 'y' must have same size.")

    h = x[1] - x[0]
    n = x.size

    sum_x = 0

    for i in range(1, n - 1):
        sum_x += y[i]

    xi = h / 2 * (y[0] + 2 * sum_x + y[n - 1])
    return [xi]


"""Numerical differentiation."""

import numpy as np


def derivative_backward_difference(x, y):
    """Calculate the first derivative.

    All values in 'x' must be equally spaced.

    Args:
        x: an array containing x values.
        y: an array containing y values.

    Returns:
        dy: an array containing the first derivative values.
    """
    if x.size < 2 or y.size < 2:
        raise Exception("'x' and 'y' arrays must have 2 values or more.")

    if x.size != y.size:
        raise Exception("'x' and 'y' must have same size.")

    def dy_difference(h, y0, y1):
        return (y1 - y0) / h

    n = x.size
    dy = np.zeros(n)
    for i in range(0, n):
        if i == n - 1:
            hx = x[i] - x[i - 1]
            dy[i] = dy_difference(-hx, y[i], y[i - 1])
        else:
            hx = x[i + 1] - x[i]
            dy[i] = dy_difference(hx, y[i], y[i + 1])

    return [dy]


def derivative_three_point(x, y):
    """Calculate the first derivative.

    All values in 'x' must be equally spaced.

    Args:
        x: an array containing x values.
        y: an array containing y values.

    Returns:
        dy: an array containing the first derivative values.
    """
    if x.size < 3 or y.size < 3:
        raise Exception("'x' and 'y' arrays must have 3 values or more.")

    if x.size != y.size:
        raise Exception("'x' and 'y' must have same size.")

    def dy_mid(h, y0, y2):
        return (1 / (2 * h)) * (y2 - y0)

    def dy_end(h, y0, y1, y2):
        return (1 / (2 * h)) * (-3 * y0 + 4 * y1 - y2)

    hx = x[1] - x[0]
    n = x.size
    dy = np.zeros(n)
    for i in range(0, n):
        if i == 0:
            dy[i] = dy_end(hx, y[i], y[i + 1], y[i + 2])
        elif i == n - 1:
            dy[i] = dy_end(-hx, y[i], y[i - 1], y[i - 2])
        else:
            dy[i] = dy_mid(hx, y[i - 1], y[i + 1])

    return [dy]


def derivative_five_point(x, y):
    """Calculate the first derivative.

    All values in 'x' must be equally spaced.

    Args:
        x: an array containing x values.
        y: an array containing y values.

    Returns:
        dy: an array containing the first derivative values.
    """
    if x.size < 6 or y.size < 6:
        raise Exception("'x' and 'y' arrays must have 6 values or more.")

    if x.size != y.size:
        raise Exception("'x' and 'y' must have same size.")

    def dy_mid(h, y0, y1, y3, y4):
        return (1 / (12 * h)) * (y0 - 8 * y1 + 8 * y3 - y4)

    def dy_end(h, y0, y1, y2, y3, y4):
        return (1 / (12 * h)) * \
               (-25 * y0 + 48 * y1 - 36 * y2 + 16 * y3 - 3 * y4)

    hx = x[1] - x[0]
    n = x.size
    dy = np.zeros(n)
    for i in range(0, n):
        if i in (0, 1):
            dy[i] = dy_end(hx, y[i], y[i + 1], y[i + 2], y[i + 3], y[i + 4])
        elif i in (n - 1, n - 2):
            dy[i] = dy_end(-hx, y[i], y[i - 1], y[i - 2], y[i - 3], y[i - 4])
        else:
            dy[i] = dy_mid(hx, y[i - 2], y[i - 1], y[i + 1], y[i + 2])

    return [dy]


from math import cos ,pi,sin
def complexRoot(n):
    """For negative Nth roots"""
    return cos(pi/n) + complex(0,1) * sin(pi / n)
