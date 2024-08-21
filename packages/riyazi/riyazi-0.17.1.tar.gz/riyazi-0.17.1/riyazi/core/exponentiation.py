from math import e 
def expj(x, /):
    """
    Convenience function for computing `e^{ix}`::

    """
    return pow(e, 1j*x) 



from math import pi
def expjpi(x, /):
    """
    Convenience function for computing `e^{i \pi x}`.
    Evaluation is accurate near zeros (see also :func:`~riyazi.cospi`,
    :func:`~riyazi.sinpi`)::
    """
    return pow(e, 1j*pi*x)