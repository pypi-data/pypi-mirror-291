# https://math.stackexchange.com/questions/4472449/summation-in-the-form-of-jacobi-theta-function

# https://mathworld.wolfram.com/JacobiThetaFunctions.html

# https://en.wikipedia.org/wiki/Theta_function

def p(t):
    """Basic rectangular pulse"""
    return 1 * (abs(t) < 0.5)

def pt(t):
    """ Basic triangular pulse"""
    return (1 - abs(t)) * (abs(t) < 1)

def sgn(t):
    """Sign function"""
    return 1 * (t >= 0) - 1 * (t < 0)

def u(t):
    """Unit step function"""
    return 1 * (t >= 0)
