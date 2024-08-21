""" 

`Tangential velocity`

`Initial Velocity`

`Relative Velocity`

`Orbital veloctiy`

`Wave velocity`

`Critical velocity`

`Terminal velocity`

`Circular velocity`



"""

pi = 3.14159
def angular_velocity(w=None,o=None, t=None):
    """
    w -> angular velocity 
    o -> thethe
    t -> time 
    
    formula
    -------------
    w = pi/30 second
    w = 2pi/t
    
    """
    w = pi/ (30*t)
    return w 

def linear_velocity(v=None, r=None, w=None):
    """
    v -> linear velocity 
    r -. radius
    w -> angular velocity 
    
    formula
    ----------
    v  = r*w 
    """
    v = r*(pi/30)
    return v 

        
        
def velocity(r,w):
    v = r*w
    return  v

pi = 3.14159
def angular_velocity(t):
    w = (2*pi) / t
    return w 

# speed

def speed(d,t):
    s = d/t
    return s 