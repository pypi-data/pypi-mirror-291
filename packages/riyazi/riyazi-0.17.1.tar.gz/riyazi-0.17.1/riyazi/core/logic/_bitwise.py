def _logical_and(x1,x2):
    return (x1&x2)

def _logical_not(x):
    return not x 

def _logical_or(x1,x2):
    return (x1|x2)

def _logical_xor(x1,x2):
    return (x1^x2)

def _bitwise_and(x1,x2):
    return (logical_and(x1,x2))

def _bitwise_not(x):
    return logical_not(x)

def _bitwise_or(x1,x2):
    return logical_or(x1,x2)


def _bitwise_xor(x1,x2):
    return logical_xor(x1,x2)