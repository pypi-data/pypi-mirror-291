# https://encyclopediaofmath.org/wiki/Zeta-function

# https://en.wikipedia.org/wiki/Riemann_zeta_function 

# https://en.wikipedia.org/wiki/Particular_values_of_the_Riemann_zeta_function

# https://www.lmfdb.org/zeros/zeta/

# https://en.wikipedia.org/wiki/Riemann_hypothesis

# https://en.wikipedia.org/wiki/Siegel_zero

# https://oeis.org/wiki/Riemann_%CE%B6_function

# https://en.wikipedia.org/wiki/Z-transform

# https://liquipedia.net/valorant/ZETA_DIVISION

def wpzeros(t):
    """Precision needed to compute higher zeros"""
    wp = 53
    if t > 3*10**8:
        wp = 63
    if t > 10**11:
        wp = 70
    if t > 10**14:
        wp = 83
    return wp