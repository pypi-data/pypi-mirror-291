"""
a -> acceleration 
u -> initial veloctiy
v -> final velocity 
t -> time 

- we will find "acceleration " bu using formula "a = (v-u)*t"
- we will find "initial velocity" by using the formula "u = (v-a*t)"
- we will find "final velocity" by using the formula "v = u+a*t"
- we will find "Time" by using the formula "t = (v-u)/a" 

"""

def eq(a=None,u=None,v=None,t=None):
    
    if( u and v and  t !=None):
        a = (v-u)*t
        print("acceleration")
        return  a
    if(a and v and t  !=None):
        u = (v-a*t)
        return u
    if(a and u and t !=None):
        v = a+a*t
        return v 
    if(a and u and v !=None):
        t = (v-a)/a
        return t 
    
    else:
        print("Error")