def motion(u=None, v=None , a=None, t=None , s=None):
    """
    only give the three arguments
    
    u -> initial velocity 
    v -> final velocit 
    a -> acceleration 
    t -> time
    s -> distance 
    g -> gravity 
    
    
    
    """

    if(u !=None and a !=None and t !=None):
        v = u+a*t
        s = u + (a/2) *(2*t-1)
        
        print("final velocity ", "distance")
        return v ,s 
    
    
    elif(v !=None and a !=None and t !=None ):
        u = v + a*t
        print ("Initial velocity ")
        return u 
    
    
    elif(u !=None and v !=None and t !=None):
        a = (v/t)- u
        print("acceleration")
        return a 
    
    
    elif(u !=None and v !=None and a !=None):
        t = (v/a) -u
        s = (v**2 + u**2) / (2*a)
        print("time" ,"distance")
        return t , s
    
    
    
    
    else:
        print("Error")