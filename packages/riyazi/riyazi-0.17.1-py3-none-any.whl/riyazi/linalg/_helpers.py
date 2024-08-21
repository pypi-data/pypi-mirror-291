
__all__ = ['inv', 'solve', 'solve_banded', 'solveh_banded', 'solve_circulant', 'solve_triangular',
'solve_toeplitz', 'matmul_toeplitz', 'det', 'norm', 'lstsq1', 'pinv', 'pinvh', 'kron','khatri_rao',
'tril', 'triu', 'orthogonal_procrustes', 'matrix_balance', 'subspace_angles', 'bandwidth', 
'issymmetric', 'ishermitian']


import numpy as np 
from scipy import linalg
def inv(a):
    determinant = linalg.det(a)
    if len(a) == 2:
        return np.array([[a[1][1]/determinant, -1*a[0][1]/determinant],
                [-1*a[1][0]/determinant, a[0][0]/determinant]])

def solve(a,b):
    import numpy.linalg as ln 
    x = ln.inv(a).dot(b)
    return np.array(x)


#https://www.delftstack.com/howto/python/
def return_determinant(mat):
    if len(mat) == 2:
        return mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*return_determinant(return_matrix_minor(m,0,c))
    return determinant





def transpose(mat):
    return map(list,zip(*mat))

def minor(mat,i,j):
    return [row[:j] + row[j+1:] for row in (mat[:i]+mat[i+1:])]

def det(mat):
    if len(mat) == 2:
        return mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*det(minor(m,0,c))
    return determinant

def inverse(m):
    determinant = det(m)
    if len(m) == 2:
        return np.array([[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]])

    cfs = []
    for r in range(len(m)):
        cfRow = []
        for c in range(len(m)):
            minor = minor(m,r,c)
            cfRow.append(((-1)**(r+c)) * det(minor))
        cfs.append(cfRow)
    cfs =transpose(cfs)
    for r in range(len(cfs)):
        for c in range(len(cfs)):
            cfs[r][c] = cfs[r][c]/determinant
    return np.array([cfs])

m = [[4,3],[8,5]]
print(inverse(m))




import numpy as np 
from scipy import linalg
def inverse(a):
    determinant = linalg.det(a)
    if len(a) == 2:
        return np.array([[a[1][1]/determinant, -1*a[0][1]/determinant],
                [-1*a[1][0]/determinant, a[0][0]/determinant]])

    
    
    # https://www.delftstack.com/howto/python/
def inverse_matrix(m):
    determinant = return_determinant(m)
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    cfs = []
    for r in range(len(m)):
        cfRow = []
        for c in range(len(m)):
            minor = return_matrix_minor(m,r,c)
            cfRow.append(((-1)**(r+c)) * return_determinant(minor))
        cfs.append(cfRow)
    cfs = return_transpose(cfs)
    for r in range(len(cfs)):
        for c in range(len(cfs)):
            cfs[r][c] = cfs[r][c]/determinant
    return cfs



def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors



def multiply(A,B):
    rowsA = len(A)
    colsA = len(A[0])

    rowsB = len(B)
    colsB = len(B[0])

    if colsA != rowsB:
        print('Number of A columns must equal number of B rows.')
        sys.exit()

    C = zeros(rowsA, colsB)

    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total

    return C

def solve(a,b):
    import numpy.linalg as ln 
    x = ln.inv(a).dot(b)
    return np.array(x)

from numpy.linalg import *

def solve(a,b):
    from numpy.linalg import inv, dot
    x = inv(a).dot(b)
    return np.array(x)

#https://pythonnumericalmethods.berkeley.edu/notebooks/chapter14.05-Solve-Systems-of-Linear-Equations-in-Python.html

def solve_linear(equation,var='x'):
    expression = equation.replace("=","-(")+")"
    grouped = eval(expression.replace(var,'1j'))
    return -grouped.real/grouped.imag

solve_linear("x - 2*x + 5*x -46*(235-24) = x+2")



















# Decomputions


__all__ =[ 'lu','lu_factor','lu_solve','svd','svdvals',
'diagsvd','orth','null_space','ldl','cholesky',
'cholesky_banded','cho_factor','cho_solve',
'cho_solve_banded','polar','qr','qr_multiply',
'qr_update','qr_delete','qr_insert','rq','ordqz',
'schur','rsf2csf','hessenberg','cdf2rdf','cossin']

# Python3 program to decompose
# a matrix using Cholesky
# Decomposition
import math
MAX = 100;

def Cholesky_Decomposition(matrix, n):

	lower = [[0 for x in range(n + 1)]
				for y in range(n + 1)];

	# Decomposing a matrix
	# into Lower Triangular
	for i in range(n):
		for j in range(i + 1):
			sum1 = 0;

			# summation for diagonals
			if (j == i):
				for k in range(j):
					sum1 += pow(lower[j][k], 2);
				lower[j][j] = int(math.sqrt(matrix[j][j] - sum1));
			else:
				
				# Evaluating L(i, j)
				# using L(j, j)
				for k in range(j):
					sum1 += (lower[i][k] *lower[j][k]);
				if(lower[j][j] > 0):
					lower[i][j] = int((matrix[i][j] - sum1) /
											lower[j][j]);

	# Displaying Lower Triangular
	# and its Transpose
	print("Lower Triangular\t\tTranspose");
	for i in range(n):
		
		# Lower Triangular
		for j in range(n):
			print(lower[i][j], end = "\t");
		print("", end = "\t");
		
		# Transpose of
		# Lower Triangular
		for j in range(n):
			print(lower[j][i], end = "\t");
		print("");

# Driver Code
n = 3;
matrix = [[4, 12, -16],
		[12, 37, -43],
		[-16, -43, 98]];
Cholesky_Decomposition(matrix, n);

# This code is contributed by mits


def lu(A):

    import numpy as np

    # Return an error if matrix is not square
    if not A.shape[0]==A.shape[1]:
        raise ValueError("Input matrix must be square")

    n = A.shape[0] 

    L = np.zeros((n,n),dtype='float64') 
    U = np.zeros((n,n),dtype='float64') 
    U[:] = A 
    np.fill_diagonal(L,1) # fill the diagonal of L with 1

    for i in range(n-1):
        for j in range(i+1,n):
            L[j,i] = U[j,i]/U[i,i]
            U[j,i:] = U[j,i:]-L[j,i]*U[i,i:]
            U[j,i] = 0
    return (L,U)



def naive_lu_factor(A):
    """
        No pivoting.

        Overwrite A with:
            U (upper triangular) and (unit Lower triangular) L 
        Returns LU (Even though A is also overwritten)
    """
    n = A.shape[0]
    for k in range(n-1):                
        for i in range(k+1,n):          
            A[i,k] = A[i,k]/A[k,k]      # " L[i,k] = A[i,k]/A[k,k] "
            for j in range(k+1,n):      
                A[i,j] -= A[i,k]*A[k,j] # " U[i,j] -= L[i,k]*A[k,j] "

    return A # (if you want)



def lu_factor(A):
    """
        LU factorization with partial pivorting

        Overwrite A with: 
            U (upper triangular) and (unit Lower triangular) L 
        Return [LU,piv] 
            Where piv is 1d numpy array with row swap indices 
    """
    n = A.shape[0]
    piv = np.arange(0,n)
    for k in range(n-1):

        # piv
        max_row_index = np.argmax(abs(A[k:n,k])) + k
        piv[[k,max_row_index]] = piv[[max_row_index,k]]
        A[[k,max_row_index]] = A[[max_row_index,k]]

        # LU 
        for i in range(k+1,n):          
            A[i,k] = A[i,k]/A[k,k]      
            for j in range(k+1,n):      
                A[i,j] -= A[i,k]*A[k,j] 

    return [A,piv]

def ufsub(L,b):
    """ Unit row oriented forward substitution """
    for i in range(L.shape[0]): 
        for j in range(i):
            b[i] -= L[i,j]*b[j]
    return b


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


def bsub(U,y):
    """ Row oriented backward substitution """
    for i in range(U.shape[0]-1,-1,-1): 
        for j in range(i+1, U.shape[1]):
            y[i] -= U[i,j]*y[j]
        y[i] = y[i]/U[i,i]
    return y


# https://stackoverflow.com/questions/28441509/how-to-implement-lu-decomposition-with-partial-pivoting-in-python
# https://gist.github.com/angellicacardozo/4b35e15aa21af890b4a8fedef9891401
def make_hilbert(n):
    """Creates a Hilbert matrix of a given dimension.
    For more information `check here <https://en.wikipedia.org/wiki/Hilbert_matrix>`_
    Parameters
    ----------
    n : int
        The dimension (order) of the Hilbert matrix to be created.
      
    Returns
    -------
    hilbert: list of lists
        The Hilbert matrix of order `n`.
    """
    # Initializing an nXn matrix of zeros
    hilbert = [[0 for i in range(n)]for j in range(n)] 
    
    for i in range(0,n):
        for j in range(0,n):
            hilbert[i][j] = 1 / (i+j+1)
    
    return hilbert



def cholesky_decomposition(matrix):
    """Performs matrix decomposition using the Cholesky method.
    For more information, `check here <https://en.wikipedia.org/wiki/Cholesky_decomposition>`_
    Parameters
    ----------
    matrix : list of lists
        A matrix filled with numbers (no matter int or float) to perform Cholesky decomposition on.
  
    Returns
    -------
    L : list of lists
        The lower triangular matrix coming from the decomposition.
    """

    d = len(matrix)
    # Initializing an nxn matrix of zeros
    L = [[0 for i in range(d)] for j in range(d)]

    # Initializing the first element in the matrix
    L[0][0] = (matrix[0][0])**0.5

    # Initializing the first column of the matrix
    for i in range(1, d):
        L[i][0] = (matrix[0][i]) / (L[0][0])
    
    # Filling-in elsewhere
    for i in range(1, d):
        for j in range(1, i+1):
            # Filling the main diagonal
            if i == j:
                L[i][j] = (matrix[i][j] - sum((L[i][k]**2) for k in range(0, i)))**0.5
            
            # Filling below the main diagonal
            else:
                L[i][j] = (1 / L[j][j]) * (matrix[i][j] - sum(L[i][k]*L[j][k] for k in range(0, min(i,j))))
    
    return L

def show_matrix(matrix):
    """Prints a matrix of floats with 6 digits precision (each element in string format).
        
        Parameters
        ----------
        matrix: list of lists
            A matrix filled with floats.
      
        Returns
        -------
        None
            Just prints the matrix, and does not return anything.
    """
  
    for row in matrix:
        print([format(elem, "f") for elem in row])
        
        
        
        


__all__ = ['eig','eigvals','eigh','eigvalsh','eig_banded',
'eigvals_banded','eigh_tridiagonal','eigvalsh_tridiagonal',
]


#https://gist.github.com/bradley101/4cbdd43b329fe2ae09fbe23c3842dedd
def mat_mul(a, b):
    c = []
    for i in range(len(a)):
        c.append([0]*len(b[0]))
        for j in range(len(b[0])):
            for k in range(len(a[0])):
                c[i][j] += (a[i][k]*b[k][j])
    return c

def mat_pow(a, n):
    if n<=0:
        return None
    if n==1:
        return a
    if n==2:
        return mat_mul(a, a)
    t1 = mat_pow(a, n/2)
    if n%2 == 0:
        return mat_mul(t1, t1)
    return mat_mul(t1, mat_mul(a, t1))



__all__ = ['expm','logm','cosm','sinm','tanm','coshm',
'sinhm','tanhm','signm','sqrtm','funm','expm_frechet',
'expm_cond','fractional_matrix_power']


__all__ = ['solve_sylvester','solve_continuous_are',
'solve_discrete_are','solve_continuous_lyapunov',
'solve_discrete_lyapunov']


#_specialmat.py

__all__ = ['block_diag','circulant','companion',
'convolution_matrix','dft','fiedler','fiedler_companion',
'hadamard','hankel','helmert','hilbert','invhilbert',
'leslie','pascal','invpascal','toeplitz','tri']


import numpy as np

def construct_cirlulant(row):

    N =  np.size(row) #row.size
    
    C = np.empty((N, N))

    for i in range(N):

        C[i, i:] = row[:N-i]
        C[i, :i] = row[N-i:]

    return C

def construct_P(N):

    P = np.zeros((N, N))

    for i in range(N-1):
        P[i, i+1] = 1
    P[-1, 0] = 1

    return P
import numpy as np

def find_eigenvalues(n):

  matrix = [[1 if (i+j)%2 == 0 else 0  for j in range(n)] for i in range(n)] 
  A = np.array(matrix)

  eigs = list(map(lambda x: int(x),list(filter(lambda x: x > 10**(-13),list(set(np.linalg.eigvals(A)))))))
  return eigs



from math import factorial
def binomial(n, k):
    """binomial(n, k): return the binomial coefficient (n k)."""

    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return factorial(n) // (factorial(k) * factorial(n-k))

import numpy as np
def invhilb(n):
    """
    invhilb   Generate the exact inverse of the n-by-n Hilbert matrix.
    Limitations:
    Comparing invhilb(n) with inv(hilb(n)) involves the effects of two or
    three sets of roundoff errors:
        - The errors caused by representing hilb(n)
        - The errors in the matrix inversion process
        - The errors, if any, in representing invhilb(n)
    It turns out that the first of these, which involves representing
    fractions like 1/3 and 1/5 in floating-point, is the most significant.
    """
    H = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            H[i, j] = ((-1)**(i + j)) * (i + j + 1) * binomial(n + i, n - j - 1) * \
             binomial(n + j, n - i - 1) * binomial(i + j, i) ** 2
    return H


def hilb(n, m=0):
    """
    hilb   Hilbert matrix.
       hilb(n,m) is the n-by-m matrix with elements 1/(i+j-1).
       it is a famous example of a badly conditioned matrix.
       cond(hilb(n)) grows like exp(3.5*n).
       hilb(n) is symmetric positive definite, totally positive, and a
       Hankel matrix.
       References:
       M.-D. Choi, Tricks or treats with the Hilbert matrix, Amer. Math.
           Monthly, 90 (1983), pp. 301-312.
       N.J. Higham, Accuracy and Stability of Numerical Algorithms,
           Society for Industrial and Applied Mathematics, Philadelphia, PA,
           USA, 2002; sec. 28.1.
       M. Newman and J. Todd, The evaluation of matrix inversion
           programs, J. Soc. Indust. Appl. Math., 6 (1958), pp. 466-476.
       D.E. Knuth, The Art of Computer Programming,
           Volume 1, Fundamental Algorithms, second edition, Addison-Wesley,
           Reading, Massachusetts, 1973, p. 37.
       NOTE added in porting.  We do not use the function cauchy here to
       generate the Hilbert matrix.  That is done so we can unit test the
       the functions against each other.  Also, the function has been
       generalized to take by row and column sizes.  If only a row size
       is given, we assume a square matrix is desired.
    """
    if n < 1 or m < 0:
        raise ValueError("Matrix size must be one or greater")
    elif n == 1 and (m == 0 or m == 1):
        return np.array([[1]])
    elif m == 0:
        m = n

    v = np.arange(1, n + 1) + np.arange(0, m)[:, np.newaxis]
    return 1. / v


# Python3 Program to print
# symmetric pascal matrix.

# Print Pascal Matrix
def printpascalmatrix(n):
	C = [[0 for x in range(2 * n + 1)]
			for y in range(2 * n + 1)]
			
	# Calculate value of
	# Binomial Coefficient
	# in bottom up manner
	for i in range(2 * n + 1):
		for j in range(min(i, 2 * n) + 1):
			
			# Base Cases
			if (j == 0 or j == i):
				C[i][j] = 1;
				
			# Calculate value
			# using previously
			# stored values
			else:
				C[i][j] = (C[i - 1][j - 1] +
						C[i - 1][j]);
	
	# Printing the
	# pascal matrix
	for i in range(n):
		for j in range(n):
			print(C[i + j][i],
				end = " ");
		print();
	
# Driver Code
n = 5;
printpascalmatrix(n);

# This code is contributed by mits



__all__ = ['solve', 'solve_triangular', 'solveh_banded', 'solve_banded',
           'solve_toeplitz', 'solve_circulant', 'inv', 'det', 'lstsq',
           'pinv', 'pinvh', 'matrix_balance', 'matmul_toeplitz']


# https://integratedmlai.com/matrixinverse/
def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(rows):
            MC[i][j] = M[i][j]

    return MC



__all__ = ['solve', 'tensorsolve', 'tensorinv',
           'inv', 'cholesky',
           'eigvals',
           'eigvalsh', 'pinv',
           'det', 'svd',
           'eig', 'eigh','lstsq', 'norm',
           'qr',
           'LinAlgError'
           ]


# https://integratedmlai.com/matrixinverse/
def matrix_multiply(A,B):
    rowsA = len(A)
    colsA = len(A[0])

    rowsB = len(B)
    colsB = len(B[0])

    if colsA != rowsB:
        print('Number of A columns must equal number of B rows.')
        sys.exit()

    C = zeros_matrix(rowsA, colsB)

    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total

            # https://www.delftstack.com/howto/python/
def return_transpose(mat):
    return print(map(list,zip(*mat)))

#https://integratedmlai.com/matrixinverse/
def zeros_matrix(rows, cols):
    A = []
    for i in range(rows):
        A.append([])
        for j in range(cols):
            A[-1].append(0.0)
            
            
            
def invert_matrix(AM, IM):
    for fd in range(len(AM)):
        fdScaler = 1.0 / AM[fd][fd]
        for j in range(len(AM)):
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        for i in list(range(len(AM)))[0:fd] + list(range(len(AM)))[fd+1:]:
            crScaler = AM[i][fd]
            for j in range(len(AM)):
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
    return IM



def return_transpose(mat):
    return map(list,zip(*mat))

def return_matrix_minor(mat,i,j):
    return [row[:j] + row[j+1:] for row in (mat[:i]+mat[i+1:])]

def return_determinant(mat):
    if len(mat) == 2:
        return mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*return_determinant(return_matrix_minor(m,0,c))
    return determinant

def inverse_matrix(m):
    determinant = return_determinant(m)
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    cfs = []
    for r in range(len(m)):
        cfRow = []
        for c in range(len(m)):
            minor = return_matrix_minor(m,r,c)
            cfRow.append(((-1)**(r+c)) * return_determinant(minor))
        cfs.append(cfRow)
    cfs = return_transpose(cfs)
    for r in range(len(cfs)):
        for c in range(len(cfs)):
            cfs[r][c] = cfs[r][c]/determinant
    return cfs

m = [[4,3],[8,5]]
print(inverse_matrix(m))


def print_matrix(Title, M):
    print(Title)
    for row in M:
        print([round(x,3)+0 for x in row])
        
def print_matrices(Action, Title1, M1, Title2, M2):
    print(Action)
    print(Title1, '\t'*int(len(M1)/2)+"\t"*len(M1), Title2)
    for i in range(len(M1)):
        row1 = ['{0:+7.3f}'.format(x) for x in M1[i]]
        row2 = ['{0:+7.3f}'.format(x) for x in M2[i]]
        print(row1,'\t', row2)
        
def zeros_matrix(rows, cols):
    A = []
    for i in range(rows):
        A.append([])
        for j in range(cols):
            A[-1].append(0.0)

    return A

def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(rows):
            MC[i][j] = M[i][j]

    return MC

def matrix_multiply(A,B):
    rowsA = len(A)
    colsA = len(A[0])

    rowsB = len(B)
    colsB = len(B[0])

    if colsA != rowsB:
        print('Number of A columns must equal number of B rows.')
        sys.exit()

    C = zeros_matrix(rowsA, colsB)

    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total

    return C


def invert_matrix(A, tol=None):
    """
    Returns the inverse of the passed in matrix.
        :param A: The matrix to be inversed
 
        :return: The inverse of the matrix A
    """
    # Section 1: Make sure A can be inverted.
    check_squareness(A)
    check_non_singular(A)
 
    # Section 2: Make copies of A & I, AM & IM, to use for row ops
    n = len(A)
    AM = copy_matrix(A)
    I = identity_matrix(n)
    IM = copy_matrix(I)
 
    # Section 3: Perform row operations
    indices = list(range(n)) # to allow flexible row referencing ***
    for fd in range(n): # fd stands for focus diagonal
        fdScaler = 1.0 / AM[fd][fd]
        # FIRST: scale fd row with fd inverse. 
        for j in range(n): # Use j to indicate column looping.
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        # SECOND: operate on all rows except fd row as follows:
        for i in indices[0:fd] + indices[fd+1:]: 
            # *** skip row with fd in it.
            crScaler = AM[i][fd] # cr stands for "current row".
            for j in range(n): 
                # cr - crScaler * fdRow, but one element at a time.
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
 
    # Section 4: Make sure IM is an inverse of A with specified tolerance
    if check_matrix_equality(I,matrix_multiply(A,IM),tol):
        return IM
    else:
        raise ArithmeticError("Matrix inverse out of tolerance.")
        
        
        
        
# Python3 program to find adjoint and
# inverse of a matrix
N = 4

# Function to get cofactor of
# A[p][q] in temp[][]. n is current
# dimension of A[][]
def getCofactor(A, temp, p, q, n):

	i = 0
	j = 0

	# Looping for each element of the matrix
	for row in range(n):

		for col in range(n):

			# Copying into temporary matrix only those element
			# which are not in given row and column
			if (row != p and col != q):

				temp[i][j] = A[row][col]
				j += 1

				# Row is filled, so increase row index and
				# reset col index
				if (j == n - 1):
					j = 0
					i += 1


# Recursive function for finding determinant of matrix.
# n is current dimension of A[][].
def determinant(A, n):

	D = 0 # Initialize result

	# Base case : if matrix contains single element
	if (n == 1):
		return A[0][0]

	temp = [] # To store cofactors
	for i in range(N):
		temp.append([None for _ in range(N)])

	sign = 1 # To store sign multiplier

	# Iterate for each element of first row
	for f in range(n):

		# Getting Cofactor of A[0][f]
		getCofactor(A, temp, 0, f, n)
		D += sign * A[0][f] * determinant(temp, n - 1)

		# terms are to be added with alternate sign
		sign = -sign

	return D


# Function to get adjoint of A[N][N] in adj[N][N].
def adjoint(A, adj):

	if (N == 1):
		adj[0][0] = 1
		return

	# temp is used to store cofactors of A[][]
	sign = 1
	temp = [] # To store cofactors
	for i in range(N):
		temp.append([None for _ in range(N)])

	for i in range(N):
		for j in range(N):
			# Get cofactor of A[i][j]
			getCofactor(A, temp, i, j, N)

			# sign of adj[j][i] positive if sum of row
			# and column indexes is even.
			sign = [1, -1][(i + j) % 2]

			# Interchanging rows and columns to get the
			# transpose of the cofactor matrix
			adj[j][i] = (sign)*(determinant(temp, N-1))


# Function to calculate and store inverse, returns false if
# matrix is singular
def inverse(A, inverse):

	# Find determinant of A[][]
	det = determinant(A, N)
	if (det == 0):
		print("Singular matrix, can't find its inverse")
		return False

	# Find adjoint
	adj = []
	for i in range(N):
		adj.append([None for _ in range(N)])
	adjoint(A, adj)

	# Find Inverse using formula "inverse(A) = adj(A)/det(A)"
	for i in range(N):
		for j in range(N):
			inverse[i][j] = adj[i][j] / det

	return True


# Generic function to display the
# matrix. We use it to display
# both adjoin and inverse. adjoin
# is integer matrix and inverse
# is a float.
def display(A):
	for i in range(N):
		for j in range(N):
			print(A[i][j], end=" ")
		print()


def displays(A):
	for i in range(N):
		for j in range(N):
			print(round(A[i][j], 6), end=" ")
		print()


# Driver program

A = [[5, -2, 2, 7], [1, 0, 0, 3], [-3, 1, 5, 0], [3, -1, -9, 4]]
adj = [None for _ in range(N)]
inv = [None for _ in range(N)]

for i in range(N):
	adj[i] = [None for _ in range(N)]
	inv[i] = [None for _ in range(N)]


print("Input matrix is :")
display(A)

print("\nThe Adjoint is :")
adjoint(A, adj)
display(adj)

print("\nThe Inverse is :")
if (inverse(A, inv)):
	displays(inv)

# This code is contributed by phasing17

import numpy as np
# Python implementation of the Crout matrix decomposition
def crout(A):

    L = np.zeros((3, 3))
    U = np.zeros((3, 3))

    for k in range(0, 3):
        U[k, k] = 1 

        for j in range(i, 3):
            sum0 = sum([L[j, s] * U[s, k] for s in range(0, j)]) #range from index 0
            L[j, k] = A[j, k] - sum0 #reversed index

        for j in range(k+1, 3):
            sum1 = sum([L[k, s] * U[s, j] for s in range(0, i)]) #range from index 0
            U[k, j] = (A[k, j] - sum1) / L[k, k]