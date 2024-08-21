from ..core.sets.set import (_union, _complement, _difference, _intersection, _power_set, _symmetric)

def union(lists):
    """
    Return lists of sets Union
    >>> from riyazi import* 
    >>> list1 = [3,2,1,8,5,3,1]
    >>> list2 = [9,5,6,3,4,2]
    >>> list3 = [1,0,9,2,8,5,4]
    >>> list4 = [5,3,6,8,2,2,0]
    >>> union([list1,list2,list3,list4])
    
    
    Refrence:
    ::
    # Wikipedia
    # ---------
    
    
    """
    return _union(lists)

def complement(u, a):
    """ 
    Complement sets
    """
    return _complement(u, a)


def difference(a, b):
    """ 
    >>> difference({1,2,3,4,5,6},{2,4,6,8})

    """
    return _difference(a, b)


def intersection(l1, l2):
    """ 
    intersection 
    """
    return _intersection(l1, l2)


def power_set(s):
    """ 
    Power sets
    """
    return _power_set(s)


def symmetric(A,B):
    """
    Return semmetric sets 
    
    >>> from riyazi import* 
    >>> 
    """
    
    return _symmetric(A,B) 