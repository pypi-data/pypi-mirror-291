
""" 

https://en.m.wikipedia.org/wiki/Physical_constant

https://en.m.wikipedia.org/wiki/List_of_physical_constants

https://physics.nist.gov/cuu/Constants/
# physics constnat 
# https://en.m.wikipedia.org/wiki/List_of_physical_constants


def power(number, macht=2):
    return number**macht

def root(number, macht=2):
    return number**(1/macht)

def exp(number):
    return 2.71828182845904523536028747135266249**number

def joule_to_ev(joule):
    return joule/(1.602e-19)

def ev_to_joule(ev):
    return ev*1.602e-19

"""

__all__ = ['minute','hour','day','week','year', 'Julian_year', 'm_e', 'm_p', 'm_n', 'G', 'g',
'p_0', 'N_A', 'R', 'k', 'sigma', 'h', 'c', 'epsilon', 'f', 'mu_0', 'elec', 'F', 'a_0', 'R_H'

]



# time in second
minute = 60.0
hour = 60 * minute
day = 24 * hour
week = 7 * day
year = 365 * day
Julian_year = 365.25 * day

#Massa's
m_e = 9.10938*10**-31
m_p = 1.67262*10**-27
m_n = 1.67493*10**-27



G = 6.67384*10**-11
g = 9.81
p_0 = 1.01325*10**5
N_A = 6.02214129*10**23
R = 8.3144621
k = 1.3806488*10**-23
sigma = 5.670373*10**-8
h = 6.62606957*10**-34
c = 2.99792458*10**8
epsilon = 8.854187817*10**-12
f = 8.987551787*10**9
mu_0 = 1.25664*10**-6
elec = 1.602176565*10**-19
F = 9.64853365*10**4
a_0 = 5.2917721092*10**-11
R_H = 1.096775834*10**7
