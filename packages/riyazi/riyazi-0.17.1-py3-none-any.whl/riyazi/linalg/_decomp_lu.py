"""LU decomposition functions."""

import numpy as np 


__all__ = ['lu', 'lu_solve', 'lu_factor']


def lu(A):

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
