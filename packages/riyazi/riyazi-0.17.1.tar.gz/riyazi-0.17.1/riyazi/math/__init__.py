""" 
# Trigonomettic functions
   - sin
   - cos
   - tan
   - csc
   - sec
   - cot
# Trigonometry function with modified argument
 - cospi
 - sinpi
 # Inverse trigonometry function
 - asin
 - acos
 - atan
 - atan2
 - acsc
 - asec
 - acot
 
 # Sinc function
 - sinc
 - sincpi
 # Hyperbolic functions
 - sinh
 - cosh
 - tanh
 - sech
 - csch
 - coth
 # Inverse Hyperbolic function
 - acosh
 - asinh
 - atanh
 - asech
 - acoth
 - acsch
 
 
from ._numeric import* 
from ._sets import*
 from ._compression import* 

from . logic import (bitwise_and, bitwise_not, bitwise_or, bitwise_xor, 
                     logical_and, logical_not, logical_or, logical_xor)                  
"""

from . logarithms import*
from . trigonometry import*
from . logic import*
from . set_theory import*
from . numerics import *
from . series import*
from ..core.exponentiation import (expj, expjpi)