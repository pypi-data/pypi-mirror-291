from ..core.logic._bitwise import (_bitwise_and, _bitwise_not, _bitwise_or, _bitwise_xor,
                                   _logical_and, _logical_not, _logical_or, _logical_xor)

__all__ = ['bitwise_and', 'bitwise_not', 'bitwise_or', 'bitwise_xor',
           'logical_and', 'logical_not', 'logical_or', 'logical_xor']


def bitwise_and(x, y):
    """ 
    Bitwise and Operator 
    """
    return _bitwise_and(x, y)




def bitwise_not(x, y):
    """ 
    Bitwise not Operator 
    
    """
    return _bitwise_not(x)

def bitwise_or(x, y):
    """ 
    Bitwise OR Operator 
    """
    return _bitwise_or(x,y)


def bitwise_xor(x, y):
    """ 
    Bitwise xor Operator
    """
    return _bitwise_xor(x, y)



# Logical Operator 

def logical_and(x, y ):
    """ 
    Logical and Operator
    
    """
    return _logical_and(x, y)


def logical_not(x):
    """ 
    Logical Not Operator 
    """
    return _logical_not(x)

def logical_or(x, y):
    """ 
    Logical OR Operator
    """
    return _logical_or(x, y)



def logical_xor(x, y):
    """ 
    Logical xor Operator
    """
    return _logical_xor(x, y)

def bitwise_and(x, y):
    """ 
    Bitwise and Operator 
    
    """
    return _logical_and(x,y)
