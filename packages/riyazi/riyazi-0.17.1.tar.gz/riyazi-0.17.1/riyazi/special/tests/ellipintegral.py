import scipy.special as special

def jacobi_elliptic(u, m):
    sn = special.jacobi(u, m)[0]
    cn = special.jacobi(u, m)[1]
    tn = special.jacobi(u, m)[2]
    asin = special.jacobi_am(u, m)
    acos = special.jacobi_am(u, 1 - m)
    atan = special.jacobi_atn(u, m)
    return sn, cn, tn, asin, acos, atan


https://en.wikipedia.org/wiki/Lemniscate_elliptic_functions
https://en.wikipedia.org/wiki/Elliptic_integral#:~:text=Modern%20mathematics%20defines%20an%20%22elliptic%20integral%22%20as%20any,cannot%20be%20expressed%20in%20terms%20of%20elementary%20functions.
https://en.wikipedia.org/wiki/Elliptic_integral
https://en.wikipedia.org/wiki/Jacobi_elliptic_functions
https://en.wikipedia.org/wiki/Elliptic_function
http://www.mhtlab.uwaterloo.ca/courses/me755/web_chap3.pdf