
""" 
# Exponential integrals and error functions
# Error functions and fresnel integrals
https://www.johndcook.com/blog/gamma_python/
https://en.wikipedia.org/wiki/List_of_integrals_of_exponential_functions
https://en.wikipedia.org/wiki/Exponential_integral

# erf function
 https://www.johndcook.com/blog/cpp_erf/

 https://www.southampton.ac.uk/~fangohr/teaching/python/book/html/16-scipy.html

 https://math.stackexchange.com/questions/97/how-to-accurately-calculate-the-error-function-operatornameerfx-with-a-co

 http://hplgit.github.io/prog4comp/doc/pub/p4c-sphinx-Python/._pylight004.html

 https://code.activestate.com/recipes/576391-error-function-and-complementary-error-function/

 https://scipy-lectures.org/intro/scipy.html

 https://www.codeproject.com/Articles/38402/Getting-started-with-the-SciPy-Scientific-Python-l

 https://www.dcode.fr/error-function
 https://en.wikipedia.org/wiki/Error_function
 
 # erfinv function
 https://www.gigacalculator.com/calculators/error-function-calculator.php#:~:text=Inverse%20error%20function%20The%20inverse%20error%20function%2C%20denoted,a%20unique%20real%20number%20solution%20to%20the%20equation%3A

https://keisan.casio.com/exec/system/1180573448

"""
__all__ = ['ei', 'e1', 'expint', 'li', 'ci', 'si', 'chi', 'shi', 'erf', 'erfc',  'erfcx', 'erfi', 'erfinv',
           'erfcinv', 'npdf', 'ncdf', 'fresnels', 'fresnelc',  'wofz', 'dawsn', 'fresnel', 'fresnel_zeros',
           'modfresnelp', 'modfresnelm', 'voigt_profile', 'erf_zeros', 'fresnelc_zeros', 'fresnels_zeros']

from ..math.numerics import (erf, erfc, erfi, exp )
from scipy import special


def ei():
    pass

def e1():
    pass

def expint():
    pass

def li():
    pass

def ci():
    pass

def si():
    pass

def chi():
    pass

def shi():
    pass 


def erf(x):
    return erf(x)

def erfc(x):
    return 1-erf(x)

def erfcx(x):
    return exp(x**2)*erfc(x)

def erfi(z):
    return (-1j*special.erf(1j*z)).real

def erfinv(x):
    pass

def erfcinv(x):
    pass 



def npdf():
    pass

def ncdf():
    pass

def fresnels():
    pass

def fresnelc():
    pass




def wofz(z):
    return exp(-z**2) * erfc(-1j*z)

def dawsn():
    pass


def fresnel():
    pass

def fresnel_zeros():
    pass

def modfresnelp():
    pass

def modfresnelm():
    pass

def voigt_profile():
    pass

def erf_zeros():
    pass

def fresnelc_zeros():
    pass

def fresnels_zeros():
    pass





