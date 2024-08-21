""" 
1.) factor
2.) Law exp
3.) product
"""

def a2minusb2(a,b):
    a2minusb2= (a+b)*(a-b)

    return a2minusb2 


def a3minusb3(a,b):
    a3minusb3= (a-b)*(a**2+a*b+b*b)

    return a3minusb3

def a3plusb3(a,b):
    a3plusb3= (a+b)* (a**2-a*b+b*b)
    return a3plusb3

def a4miniusb4(a,b):
    a4miniusb4= (a**2-b**2)*(a**2+b**2)
    return a4miniusb4


def a5miniusb5(a,b):
    a5miniusb5 = (a-b)*(a**4 + a**3*b + a**2*b**2 + a*b**3 + b**4 )
    return a5miniusb5

def a5plusb5(a,b):
    a5miniusb5 = (a+b)*(a**4 - a**3*b + a**2*b**2 + a*b**3 + b**4 )
    
    
# Low of Exponents 

def product_of_power(a, m,n):
    product_of_power = pow(a,m)*pow(a,n)

    return product_of_power

def quotient_of_power(a, m , n):
    quotient_of_power = pow(a,m) / pow(a,n)
    
    return quotient_of_power
    
    



# product

def a_minus_b2(a,b):
    a_minus_b2 = a**2- 2*a*b +b**2
    return a_minus_b2

def a_plus_b2(a,b):
    a_plus_b2 = a**2 + 2*a*b +b**2
    return a_plus_b2

def a_plus_b3(a,b):
    a_plus_b3 = a**3 + 3*a**2*b + 3*a*b**2 + b**3
    return a_plus_b3


def a_minus_b3(a,b):
    a_minus_b3 = a**3 - 3*a**2*b + 3*a*b**2 - b**3
    return a_minus_b3

def a_plus_b4(a,b):
    a_plus_b4 = a**4 + 4*a**3*b + 6*a**2*b**2 + 4*a*b**3 +b**4
    return a_plus_b4



def a_minus_b4(a,b):
    a_minus_b4 = a**4 - 4*a**3*b + 6*a**2*b**2 - 4*a*b**3 +b**4
    return a_minus_b4

def a_plus_b_plus_c2(a,b,c):
    a_plus_b_plus_c2 = a**2 + b**2 + c**2 + 2*a*b + 2*a*c + 2*b*c 
    return a_plus_b_plus_c2
    