import numpy as np

def dft(x):
    """Compute the 1-D discrete Fourier Transform of a signal or sequence.

    Parameters:
    x (ndarray): The input signal or sequence.

    Returns:
    ndarray: The complex-valued DFT of the input signal.
    """
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
    return X


import numpy as np
import random

exp = np.exp
pi = np.pi

def mydft(X):
    n = len(X)
    out = []
    for k in range(n):
        temp = 0
        for i in range(n):
            temp += X[i] * exp(-2j*pi*k*i/n)
        out.append(temp)
    return np.array(out)

def myidft(X):
    n = len(X)
    out = []
    for k in range(n):
        temp = 0
        for i in range(n):
            temp += X[i] * exp(2j*pi*k*i/n)
        out.append(temp)
    return (1/n) * np.array(out)

import numpy as np

def fft(x):
    """
    Compute the discrete fouries transform of the signal x 
    """
    x = np.asarray(x, dtype=float)
    N = x.shape
    n = np.arange(N)
    k = n.reshape((N,1))
    M = np.exp(-2j*np.pi*k*n/N)
    return np.dot(M,x)



def fft2(x, s=None, axes=(-2,-1), norm=None, overwrite_x=False, workers=None,
         *, plan=None):
    """
    2-D discrete Fourier transform.
    """
    if plan is not None:
        raise NotImplementedError('Passing a precomputed plan is not yet '
                                  'supported by scipy.fft functions')
    return fftn(x, s, axes, norm, overwrite_x, workers)


def transform(vector, inverse=False):
    n = len(vector)
    if n>0 and n &(n-1) ==0:
        return transform_radix
def convolve(x,y, realoutput=True):
    assert len(x)==len(y)
    n = len(x)
    x = transform(x)
    y = transform(y)
    for i in range(n):
        x[i] *=y[i]
    x  = transform(x, inverse=True)
    
    if realoutput:
        for i in range(n):
            x[i] = x[i].real/n
            
    else:
        for i in range(n):
            x[i] /=n
    return x 


import numpy as np 


def DFT(x):
    """
    Function to calculate the 
    discrete Fourier Transform 
    of a 1D real-valued signal x
    """

    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    
    X = np.dot(e, x)
    
    return X