"""
__all__ = ['convolve', 'correlate', 'fftconvolve', 'oaconvolve', 'convolve2d', 
 'correlate2d', 'sepfir2d', 'choose_conv_method', 'correlation_lags']
 
 __all__ = [  # noqa: F822
    'correlate', 'correlation_lags', 'correlate2d',
    'convolve', 'convolve2d', 'fftconvolve', 'oaconvolve',
    'order_filter', 'medfilt', 'medfilt2d', 'wiener', 'lfilter',
    'lfiltic', 'sosfilt', 'deconvolve', 'hilbert', 'hilbert2',
    'cmplx_sort', 'unique_roots', 'invres', 'invresz', 'residue',
    'residuez', 'resample', 'resample_poly', 'detrend',
    'lfilter_zi', 'sosfilt_zi', 'sosfiltfilt', 'choose_conv_method',
    'filtfilt', 'decimate', 'vectorstrength',
    'timeit', 'cKDTree', 'dlti', 'upfirdn', 'linalg',
    'sp_fft', 'lambertw', 'get_window', 'axis_slice', 'axis_reverse',
    'odd_ext', 'even_ext', 'const_ext', 'cheby1', 'firwin'
]
"""

__all__ = ['convolve','convolve2d', 'fftconvolve','oaconvolve', 'correlate', 'correlated2d', 'sepfir2d', 
           'hilbert', 'hilber2']


def correlate():
    pass
def correlated2d():
    pass


import numpy as np
from scipy.fft import fftn, ifftn

def convolve(array1, array2):
    """
    # Example usage
    array1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    array2 = np.array([[0, 1], [2, 3]])

    result = convolve_nd(array1, array2)
    print(result)
    """
    # Get the dimensions of the input arrays
    shape1 = array1.shape
    shape2 = array2.shape

    # Calculate the output shape
    output_shape = tuple(np.add(shape1, shape2) - 1)

    # Initialize the output array
    output = np.zeros(output_shape)

    # Iterate through all possible positions of the kernel
    for index in np.ndindex(output_shape):
        value = 0
        # Iterate through the dimensions of the arrays
        for offset in np.ndindex(shape2):
            # Calculate the corresponding position in array1
            input_position = tuple(np.subtract(index, offset))
            
            # Check if the position is valid
            if all(0 <= pos < dim for pos, dim in zip(input_position, shape1)):
                value += array1[input_position] * array2[offset]

        output[index] = value

    return output

def convolve2d(array1, array2):
    """
    Convolve two 2-dimensional arrays.
    """
    if not array1.ndim == array2.ndim == 2:
        raise ValueError('convolve2d inputs must both be 2-D arrays')
    # Get the dimensions of the input arrays
    shape1 = array1.shape
    shape2 = array2.shape

    # Calculate the output shape
    output_shape = tuple(np.add(shape1, shape2) - 1)

    # Initialize the output array
    output = np.zeros(output_shape)

    # Iterate through all possible positions of the kernel
    for index in np.ndindex(output_shape):
        value = 0
        # Iterate through the dimensions of the arrays
        for offset in np.ndindex(shape2):
            # Calculate the corresponding position in array1
            input_position = tuple(np.subtract(index, offset))
            
            # Check if the position is valid
            if all(0 <= pos < dim for pos, dim in zip(input_position, shape1)):
                value += array1[input_position] * array2[offset]

        output[index] = value

    return output


def fftconvolve(array1, array2):
    # Get the shapes of the input arrays
    shape1 = array1.shape
    shape2 = array2.shape
    
    # Calculate the output shape
    output_shape = tuple(np.add(shape1, shape2) - 1)
    
    # Perform FFT on the input arrays
    fft_array1 = fftn(array1, output_shape)
    fft_array2 = fftn(array2, output_shape)
    
    # Element-wise multiplication in the frequency domain
    fft_result = fft_array1 * fft_array2
    
    # Perform inverse FFT to get the convolution result
    conv_result = ifftn(fft_result)
    
    # Extract the real part of the result (due to potential small imaginary parts)
    conv_result = np.real(conv_result)
    
    return conv_result



def oaconvolve(array1, array2):
    # Get the shapes of the input arrays
    shape1 = array1.shape
    shape2 = array2.shape
    
    # Calculate the output shape
    output_shape = tuple(np.add(shape1, shape2) - 1)
    
    # Perform FFT on the input arrays
    fft_array1 = fftn(array1, output_shape)
    fft_array2 = fftn(array2, output_shape)
    
    # Element-wise multiplication in the frequency domain
    fft_result = fft_array1 * fft_array2
    
    # Perform inverse FFT to get the convolution result
    conv_result = ifftn(fft_result)
    
    # Extract the real part of the result (due to potential small imaginary parts)
    conv_result = np.real(conv_result)
    
    return conv_result

def sepfir2d(matrix, kernel_row, kernel_col):
    # Get dimensions of the input matrix and kernels
    rows, cols = len(matrix), len(matrix[0])
    kernel_row_size, kernel_col_size = len(kernel_row), len(kernel_col)

    # Initialize the result matrix with zeros
    result = np.zeros((rows - kernel_row_size + 1, cols - kernel_col_size + 1))

    # Perform row-wise convolution
    for i in range(len(result)):
        for j in range(len(result[0])):
            for k in range(kernel_row_size):
                result[i][j] += np.sum(matrix[i + k][j : j + kernel_col_size] * kernel_row[k])

    # Perform column-wise convolution
    final_result = np.zeros((rows - kernel_row_size + 1, cols - kernel_col_size + 1))
    for i in range(len(result)):
        for j in range(len(result[0])):
            for k in range(kernel_col_size):
                final_result[i][j] += result[i + k][j] * kernel_col[k]

    return final_result


def hilbert(x, N=None, axis=-1):
    x = np.asarray(x)
    if np.iscomplexobj(x):
        raise ValueError("x must be real.")
    if N is None:
        N = x.shape[axis]
    if N <= 0:
        raise ValueError("N must be positive.")

    Xf = np.fft.fft(x, N, axis=axis)
    h = np.zeros(N, dtype=Xf.dtype)
    if N % 2 == 0:
        h[0] = h[N // 2] = 1
        h[1:N // 2] = 2
    else:
        h[0] = 1
        h[1:(N + 1) // 2] = 2

    if x.ndim > 1:
        ind = [np.newaxis] * x.ndim
        ind[axis] = slice(None)
        h = h[tuple(ind)]
    x = np.fft.ifft(Xf * h, axis=axis)
    return x


def hilbert2(x, N=None):
    x = np.atleast_2d(x)
    if x.ndim > 2:
        raise ValueError("x must be 2-D.")
    if np.iscomplexobj(x):
        raise ValueError("x must be real.")
    if N is None:
        N = x.shape
    elif isinstance(N, int):
        if N <= 0:
            raise ValueError("N must be positive.")
        N = (N, N)
    elif len(N) != 2 or np.any(np.asarray(N) <= 0):
        raise ValueError("When given as a tuple, N must hold exactly "
                         "two positive integers")

    Xf = np.fft.fft2(x, N, axes=(0, 1))
    h1 = np.zeros(N[0], dtype=Xf.dtype)
    h2 = np.zeros(N[1], dtype=Xf.dtype)
    for p in range(2):
        h = eval("h%d" % (p + 1))
        N1 = N[p]
        if N1 % 2 == 0:
            h[0] = h[N1 // 2] = 1
            h[1:N1 // 2] = 2
        else:
            h[0] = 1
            h[1:(N1 + 1) // 2] = 2
        exec("h%d = h" % (p + 1), globals(), locals())

    h = h1[:, np.newaxis] * h2[np.newaxis, :]
    k = x.ndim
    while k > 2:
        h = h[:, np.newaxis]
        k -= 1
    x = np.fft.ifft2(Xf * h, axes=(0, 1))
    return x



