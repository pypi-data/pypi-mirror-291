import cmath
import numpy as np
from math import log, ceil
import numpy as np 

__all__ = ['fft','ifft','fft2','ifft2', 'fftn', 'ifftn', 'rfft', 'irfft', 'rfft2','irfft2',
'rfftn', 'irfftn', 'hfft', 'ihfft', 'hfft2', 'ihfft2', 'hfftn','ihfftn']



def fft(x):
    """
    Compute the 1-D discrete Fourier Transform.
     `
    A recursive implementation of 
    the 1D Cooley-Tukey FFT, the 
    input should have a length of 
    power of 2. 
    """
    N = len(x)
    
    if N == 1:
        return x
    else:
        X_even = fft(x[::2])
        X_odd = fft(x[1::2])
        factor = \
          np.exp(-2j*np.pi*np.arange(N)/ N)
        
        X = np.concatenate(\
            [X_even+factor[:int(N/2)]*X_odd,
             X_even+factor[int(N/2):]*X_odd])
        return X

def ifft(X):
    '''
    Compute the 1-D inverse discrete Fourier Transform.
    IFFT of 1-d signals
    usage x = ifft(X) 
    unpadding must be done implicitly'''

    x = fft([x.conjugate() for x in X])
    return [x.conjugate()/len(X) for x in x]


def pad2(x):
    m, n = np.shape(x)
    M, N = 2 ** int(ceil(log(m, 2))), 2 ** int(ceil(log(n, 2)))
    F = np.zeros((M,N), dtype = x.dtype)
    F[0:m, 0:n] = x
    return F, m, n

def fft2(f):
    '''
    Compute the 2-D discrete Fourier Transform
    FFT of 2-d signals/images with padding
    usage X, m, n = fft2(x), where m and n are dimensions of original signal'''

    f, m, n = pad2(f)
    return np.transpose(fft(np.transpose(fft(f))))



def ifft2(x, y, z):
    """
    Compute the 2-D inverse discrete Fourier Transform.
    """
    x, y, z = fft2(np.conj(x))
    x =  np.matrix(np.real(np.conj(x)))/(y*z)
    return x[0:y, 0:z]
    

def fftn():
    """
    Compute the N-D discrete Fourier Transform.
    """
    pass

def ifftn():
    """
    Compute the N-D inverse discrete Fourier Transform.
    """
    pass

def rfft():
    """
    Compute the 1-D discrete Fourier Transform for real input.
    """
    pass

def irfft():
    """
    Computes the inverse of rfft.
    """
    pass

def rfft2():
    """
    Compute the 2-D FFT of a real array.
    """
    pass

def irfft():
    """
    Computes the inverse of rfft2
    """
    pass


def irfft2():
    """
    omputes the inverse of rfft2
    """
    pass

def rfftn():
    """
    Compute the N-D discrete Fourier Transform for real input.
    """
    pass

def irfftn():
    """
    Computes the inverse of rfftn
    """
    pass

def hfft():
    """
    Compute the FFT of a signal that has Hermitian symmetry, i.e., a real spectrum.
    """
    pass

def ihfft():
    """
    Compute the inverse FFT of a signal that has Hermitian symmetry.
    """
    pass

def hfft2():
    """
    Compute the 2-D FFT of a Hermitian complex array.
    """
    pass

def ihfft2():
    """
    Compute the 2-D inverse FFT of a real spectrum.
    """
    pass

def hfftn():
    """
    Compute the N-D FFT of Hermitian symmetric complex input, i.e., a signal with a real spectrum.
    """
    pass

def ihfftn():
    """
    Compute the N-D inverse discrete Fourier Transform for a real spectrum.
    """
    pass

