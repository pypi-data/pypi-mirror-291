#https://www.geeksforgeeks.org/orthogonal-distance-regression-using-scipy/
# https://en.wikipedia.org/wiki/Deming_regression
# https://gist.github.com/rehanguha/feedfa45043a3485a8b3a9dbccab1df5
def Cauchy(p,x) :
    # Cauchy / Lorentzian / Breit-Wigner peak with contant background:
    B           = p[0]    #   Constant Background
    x1_peak     = p[1]    #   Height above/below background
    x1          = p[2]    #   Central value
    width_x1    = p[3]    #   Half-Width at Half Maximum
    return ( B + x1_peak*(1/(1+((x-x1)/width_x1)**2)) )
def Gauss(p,x) :
    # A gaussian or Normal peak with constant background:
    B           = p[0]    #   Constant Background
    x1_peak     = p[1]    #   Height above/below background
    x1          = p[2]    #   Central value
    width_x1    = p[3]    #   Standard Deviation
    return ( B + x1_peak*numpy.exp(-(x-x1)**2/(2*width_x1**2)) )
def Semicircle(p,x) :
    # The upper half of a circle:
    R           = p[0]    #   Radius of circle
    x0          = p[1]    #   x coordinate of centre of circle
    y0          = p[2]    #   y coordinate of centre of circle
    from numpy import array, sqrt
    y=[]
    for i in range(len(x)) :
        y_squared = R**2-(x[i]-x0)**2
        if y_squared < 0 :
            y.append(y0)
        else :
            y.append(sqrt(y_squared)+y0)
    return array(y)

def Linear(p,x) :
    # A linear function with:
    #   Constant Background          : p[0]
    #   Slope                        : p[1]
    return p[0]+p[1]*x


def Cubic(p,x) :
    # A cubic function with:
    #   Constant Background          : p[0]
    #   Slope                        : p[1]
    #   Curvature                    : p[2]
    #   3rd Order coefficient        : p[3]
    return p[0]+p[1]*x+p[2]*x**2+p[3]*x**3