
__all__ =['kelvin','kelvin_zeros','ber','bei','berp','beip','ker','kei','kerp','keip',
'ber_zeros','bei_zeros','berp_zeros','beip_zeors','ker_zeros','kei_zeros','kerp_zeros','keip_zeros']

from math import e,pi
import mpmath as mp
# Kelvin functions as complex numbers
#https://en.wikipedia.org/wiki/Kelvin_functions
#https://dlmf.nist.gov/10#PT5

def kelvin(x):
    pass


def kelvin_zeros(nt):
    pass

def ber(n,x):
    return mp.besselj(n,x*pow(e,((3*pi*1j)/4)))

def bei(n,x):
    return mp.besselj(n,x*pow(e,((3*pi*1j)/4))).imag

def berp(x):
    pass

def beip(x):
    pass

def ker(n,x):
    return mp.bessely(n,x*pow(e,((3*pi*1j)/4)))

def kei(x):
    pass

def kerp(x):
    pass

def keip(x):
    pass


def ber_zeros(n):
    pass

def bei_zeros(nt):
    pass


def berp_zeros(nt):
    pass

def beip_zeors(nt):
    pass

def ker_zeros(nt):
    pass

def kei_zeros(nt):
    pass

def kerp_zeros(nt):
    pass

def keip_zeros(nt):
    pass





