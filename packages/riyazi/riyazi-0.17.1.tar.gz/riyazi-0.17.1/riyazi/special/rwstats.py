from math import log,exp,inf
"""
__all__ = ['bdtr','bdtrc','bdtri','bdtrik','bdtrin',
'btdtr','btdtri','btdtria','btdtrib','fdtr','fdtrc',
'fdtri','fdtridfd','gdtr','gdtrc','gdtria','gdtrib',
'gdtrix','nbdtr','nbdtrc','nbdtri','nbdtrik','nbdtrin',
'ncfdtr','ncfdtridfd','ncfdtridfn','ncfdtri','ncfdtrinc',
'nctdtr','nctdtridf','nctdtrit','nctdtrinc','nrdtrimn',
'nrdtrisd','pdtr','pdtrc','pdtri','pdtrik','stdtr',
'stdtridf','stdtrit','chdtr','chdtrc','chdtri','chdtriv',
'ndtr','log_ndtr','ndtri','ndtri_exp','chndtr','chndtridf',
'chndtrinc','chndtrix','smirnov','smirnovi','kolmogorov',
'kolmogi','tklmbda','logit','expit','log_expit','boxcox',
'boxcox1p','inv_boxcox','inv_boxcox1p','owens_t']

"""
#https://math.stackexchange.com/questions/231743/how-do-i-find-the-cumulative-distribution-function-of-a-binomial-random-variable
#https://en.wikipedia.org/wiki/Statistics

__all__ = ['logit','expit','log_expit','boxcox','boxcox1p','inv_boxcox','inv_boxcox1p','owens_t']





from math import log
def boxcox(x,lamda):
    if lamda ==0:
        return log(x)
    elif(lamda !=0):
        return (x**lamda-1)/lamda 



from math import log
def boxcox1p(x,lamda):
    if lamda ==0:
        return log(1+x)
    elif(lamda !=0):
        return ((1+x)**lamda-1)/lamda 


from math import exp 
def expit(x):
    return 1/ (1+exp(-x))


from math import exp,log
def invboxcox(y,ld):
    if ld == 0:
        
        return(exp(y))
    else:
        return(exp(log(ld*y+1)/ld))


import scipy.special as sp 
from math import log
def log_expit(x):
    return log(sp.expit(x))


from math import inf,log 
def logit(x):
    if x==0:
        return -inf
    elif(x==1):
        return inf
    
    else:
        return log(x/(1-x))









def logit(x):
    if x==0:
        return -inf
    elif(x==1):
        return inf 
    else:
        return log(x/(1-x))


def expit(x):
    return 1/ (1+exp(-x))


def log_expit(x):
    return log(expit(x))




def boxcox(x,lamda):
    if lamda ==0:
        return log(x)
    elif(lamda !=0):
        return (x**lamda-1)/lamda 

def boxcox1p(x,lamda):
    if lamda ==0:
        return log(1+x)
    elif(lamda !=0):
        return ((1+x)**lamda-1)/lamda 


def inv_boxcox(y,ld):
    if ld == 0:
        return(exp(y))
    else:
        return(exp(log(ld*y+1)/ld))


def inv_boxcox1p():
    pass


def owens_t():
    pass




