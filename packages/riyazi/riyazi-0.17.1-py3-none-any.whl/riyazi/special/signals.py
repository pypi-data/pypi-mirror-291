
__all__ = ['squarew', 'sawtoothw', 'unit_triangle', 'sigmoid', 'trianglew']


def squarew(t, amplitude=1, period=1):
    """ 
    Computes the square wave function using the definition:

    .. math::
    x(t) = A(-1)^{\left\lfloor{2t / P}\right\rfloor}

    where `P` is the period of the wave and `A` is the amplitude.

    **Examples**

    Square wave with period = 2, amplitude = 1 ::
    
    """
    A = amplitude 
    P = period
    return float(round((A*(pow(-1,2*t/P))).real))

def sawtoothw(t, amplitude=1, period=1):
    """ 
    Computes the sawtooth wave function using the definition:

    .. math::
    x(t) = A\operatorname{frac}\left(\frac{t}{T}\right)

    where :math:`\operatorname{frac}\left(\frac{t}{T}\right) = \frac{t}{T}-\left\lfloor{\frac{t}{T}}\right\rfloor`,
    `P` is the period of the wave, and `A` is the amplitude.

    **Examples**

    Sawtooth wave with period = 2, amplitude = 1 ::
    
    """
    A = amplitude
    P = period
    return A*(t/P)

def unit_triangle(t, amplitude=1):
    """ 
    Computes the unit triangle using the definition:

    .. math::
    x(t) = A(-\left| t \right| + 1)

    where `A` is the amplitude.

    **Examples**

    Unit triangle with amplitude = 1 ::
    
    """
    A = amplitude
    return (A*(-t)+1) # wrong

from math import e
def sigmoid(t, amplitude=1):
    """ 
    Computes the sigmoid function using the definition:

    .. math::
    x(t) = \frac{A}{1 + e^{-t}}

    where `A` is the amplitude.

    **Examples**

    Sigmoid function with amplitude = 1 ::
    """
    A = amplitude
    return (A / (1+pow(e, -t)))


def trianglew():
    pass 

