def _complement(U,A):
    return U-A

def _difference(A,B):
    print(type(A))
    print(type(B))
    if(type(A) ==type({dict})  and type(B) == type({dict})):
        
        return type((A-B))
    else:
        print("Enter both set value  data type")

def _intersection(l1, l2):
    temp = []

    for item in l1:
        if item in l2 and item not in temp:
            temp.append(item)

    return temp

def _power_set(s):

    power_set = [set()]

    for element in s:
        one_element_set = {element}
        power_set += [subset | one_element_set for subset in power_set]

    return power_set

def _symmetric(A,B):
    """symmetric"""
    print(type(A))
    print(type(B))

    if(type(A) ==type(set)  and type(B) == type({set})):
        return A^B
    else:("enter both  set data type ")


def _union(lists):
    
    all_elements = []
    for x in lists:
        all_elements = all_elements + x
    return set(set(all_elements))