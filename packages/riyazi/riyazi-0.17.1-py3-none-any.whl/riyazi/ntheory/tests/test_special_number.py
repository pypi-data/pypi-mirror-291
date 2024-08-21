# Armstrong number
"""
An Armstrong number is equal to the sum of its own digits each raised to the
power of the number of digits.

For example, 370 is an Armstrong number because 3*3*3 + 7*7*7 + 0*0*0 = 370.

Armstrong numbers are also called Narcissistic numbers and Pluperfect numbers.

On-Line Encyclopedia of Integer Sequences entry: https://oeis.org/A005188
"""
PASSING = (1, 153, 370, 371, 1634, 24678051, 115132219018763992565095597973971522401)
FAILING: tuple = (-153, -1, 0, 1.2, 200, "A", [], {}, None)


def armstrong_number(n: int) -> bool:
    """
    Return True if n is an Armstrong number or False if it is not.

    >>> all(armstrong_number(n) for n in PASSING)
    True
    >>> any(armstrong_number(n) for n in FAILING)
    False
    """
    if not isinstance(n, int) or n < 1:
        return False

    # Initialization of sum and number of digits.
    total = 0
    number_of_digits = 0
    temp = n
    # Calculation of digits of the number
    number_of_digits = len(str(n))
    # Dividing number into separate digits and find Armstrong number
    temp = n
    while temp > 0:
        rem = temp % 10
        total += rem**number_of_digits
        temp //= 10
    return n == total


def pluperfect_number(n: int) -> bool:
    """Return True if n is a pluperfect number or False if it is not

    >>> all(armstrong_number(n) for n in PASSING)
    True
    >>> any(armstrong_number(n) for n in FAILING)
    False
    """
    if not isinstance(n, int) or n < 1:
        return False

    # Init a "histogram" of the digits
    digit_histogram = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    digit_total = 0
    total = 0
    temp = n
    while temp > 0:
        temp, rem = divmod(temp, 10)
        digit_histogram[rem] += 1
        digit_total += 1

    for cnt, i in zip(digit_histogram, range(len(digit_histogram))):
        total += cnt * i**digit_total

    return n == total


def narcissistic_number(n: int) -> bool:
    """Return True if n is a narcissistic number or False if it is not.

    >>> all(armstrong_number(n) for n in PASSING)
    True
    >>> any(armstrong_number(n) for n in FAILING)
    False
    """
    if not isinstance(n, int) or n < 1:
        return False
    expo = len(str(n))  # the power that all digits will be raised to
    # check if sum of each digit multiplied expo times is equal to number
    return n == sum(int(i) ** expo for i in str(n))


def main():
    """
    Request that user input an integer and tell them if it is Armstrong number.
    """
    num = int(input("Enter an integer to see if it is an Armstrong number: ").strip())
    print(f"{num} is {'' if armstrong_number(num) else 'not '}an Armstrong number.")
    print(f"{num} is {'' if narcissistic_number(num) else 'not '}an Armstrong number.")
    print(f"{num} is {'' if pluperfect_number(num) else 'not '}an Armstrong number.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()


# automorphic number

"""
== Automorphic Numbers ==
A number n is said to be a Automorphic number if
the square of n "ends" in the same digits as n itself.

Examples of Automorphic Numbers: 0, 1, 5, 6, 25, 76, 376, 625, 9376, 90625, ...
https://en.wikipedia.org/wiki/Automorphic_number
"""

# Author : Akshay Dubey (https://github.com/itsAkshayDubey)
# Time Complexity : O(log10n)


def is_automorphic_number(number: int) -> bool:
    """
    # doctest: +NORMALIZE_WHITESPACE
    This functions takes an integer number as input.
    returns True if the number is automorphic.
    >>> is_automorphic_number(-1)
    False
    >>> is_automorphic_number(0)
    True
    >>> is_automorphic_number(5)
    True
    >>> is_automorphic_number(6)
    True
    >>> is_automorphic_number(7)
    False
    >>> is_automorphic_number(25)
    True
    >>> is_automorphic_number(259918212890625)
    True
    >>> is_automorphic_number(259918212890636)
    False
    >>> is_automorphic_number(740081787109376)
    True
    >>> is_automorphic_number(5.0)
    Traceback (most recent call last):
        ...
    TypeError: Input value of [number=5.0] must be an integer
    """
    if not isinstance(number, int):
        msg = f"Input value of [number={number}] must be an integer"
        raise TypeError(msg)
    if number < 0:
        return False
    number_square = number * number
    while number > 0:
        if number % 10 != number_square % 10:
            return False
        number //= 10
        number_square //= 10
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()



# bell number 

"""
Bell numbers represent the number of ways to partition a set into non-empty
subsets. This module provides functions to calculate Bell numbers for sets of
integers. In other words, the first (n + 1) Bell numbers.

For more information about Bell numbers, refer to:
https://en.wikipedia.org/wiki/Bell_number
"""


def bell_numbers(max_set_length: int) -> list[int]:
    """
    Calculate Bell numbers for the sets of lengths from 0 to max_set_length.
    In other words, calculate first (max_set_length + 1) Bell numbers.

    Args:
        max_set_length (int): The maximum length of the sets for which
        Bell numbers are calculated.

    Returns:
        list: A list of Bell numbers for sets of lengths from 0 to max_set_length.

    Examples:
    >>> bell_numbers(0)
    [1]
    >>> bell_numbers(1)
    [1, 1]
    >>> bell_numbers(5)
    [1, 1, 2, 5, 15, 52]
    """
    if max_set_length < 0:
        raise ValueError("max_set_length must be non-negative")

    bell = [0] * (max_set_length + 1)
    bell[0] = 1

    for i in range(1, max_set_length + 1):
        for j in range(i):
            bell[i] += _binomial_coefficient(i - 1, j) * bell[j]

    return bell


def _binomial_coefficient(total_elements: int, elements_to_choose: int) -> int:
    """
    Calculate the binomial coefficient C(total_elements, elements_to_choose)

    Args:
        total_elements (int): The total number of elements.
        elements_to_choose (int): The number of elements to choose.

    Returns:
        int: The binomial coefficient C(total_elements, elements_to_choose).

    Examples:
    >>> _binomial_coefficient(5, 2)
    10
    >>> _binomial_coefficient(6, 3)
    20
    """
    if elements_to_choose in {0, total_elements}:
        return 1

    if elements_to_choose > total_elements - elements_to_choose:
        elements_to_choose = total_elements - elements_to_choose

    coefficient = 1
    for i in range(elements_to_choose):
        coefficient *= total_elements - i
        coefficient //= i + 1

    return coefficient


if __name__ == "__main__":
    import doctest

    doctest.testmod()


# carmichael number 

"""
== Carmichael Numbers ==
A number n is said to be a Carmichael number if it
satisfies the following modular arithmetic condition:

    power(b, n-1) MOD n = 1,
    for all b ranging from 1 to n such that b and
    n are relatively prime, i.e, gcd(b, n) = 1

Examples of Carmichael Numbers: 561, 1105, ...
https://en.wikipedia.org/wiki/Carmichael_number
"""

from maths.greatest_common_divisor import greatest_common_divisor


def power(x: int, y: int, mod: int) -> int:
    """
    Examples:
    >>> power(2, 15, 3)
    2
    >>> power(5, 1, 30)
    5
    """

    if y == 0:
        return 1
    temp = power(x, y // 2, mod) % mod
    temp = (temp * temp) % mod
    if y % 2 == 1:
        temp = (temp * x) % mod
    return temp


def is_carmichael_number(n: int) -> bool:
    """
    Examples:
    >>> is_carmichael_number(4)
    False
    >>> is_carmichael_number(561)
    True
    >>> is_carmichael_number(562)
    False
    >>> is_carmichael_number(900)
    False
    >>> is_carmichael_number(1105)
    True
    >>> is_carmichael_number(8911)
    True
    >>> is_carmichael_number(5.1)
    Traceback (most recent call last):
         ...
    ValueError: Number 5.1 must instead be a positive integer

    >>> is_carmichael_number(-7)
    Traceback (most recent call last):
         ...
    ValueError: Number -7 must instead be a positive integer

    >>> is_carmichael_number(0)
    Traceback (most recent call last):
         ...
    ValueError: Number 0 must instead be a positive integer
    """

    if n <= 0 or not isinstance(n, int):
        msg = f"Number {n} must instead be a positive integer"
        raise ValueError(msg)

    return all(
        power(b, n - 1, n) == 1
        for b in range(2, n)
        if greatest_common_divisor(b, n) == 1
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    number = int(input("Enter number: ").strip())
    if is_carmichael_number(number):
        print(f"{number} is a Carmichael Number.")
    else:
        print(f"{number} is not a Carmichael Number.")


# catalan number

"""

Calculate the nth Catalan number

Source:
    https://en.wikipedia.org/wiki/Catalan_number

"""


def catalan(number: int) -> int:
    """
    :param number: nth catalan number to calculate
    :return: the nth catalan number
    Note: A catalan number is only defined for positive integers

    >>> catalan(5)
    14
    >>> catalan(0)
    Traceback (most recent call last):
        ...
    ValueError: Input value of [number=0] must be > 0
    >>> catalan(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input value of [number=-1] must be > 0
    >>> catalan(5.0)
    Traceback (most recent call last):
        ...
    TypeError: Input value of [number=5.0] must be an integer
    """

    if not isinstance(number, int):
        msg = f"Input value of [number={number}] must be an integer"
        raise TypeError(msg)

    if number < 1:
        msg = f"Input value of [number={number}] must be > 0"
        raise ValueError(msg)

    current_number = 1

    for i in range(1, number):
        current_number *= 4 * i - 2
        current_number //= i + 1

    return current_number


if __name__ == "__main__":
    import doctest

    doctest.testmod()


# hamming number

"""
A Hamming number is a positive integer of the form 2^i*3^j*5^k, for some
non-negative integers i, j, and k. They are often referred to as regular numbers.
More info at: https://en.wikipedia.org/wiki/Regular_number.
"""


def hamming(n_element: int) -> list:
    """
    This function creates an ordered list of n length as requested, and afterwards
    returns the last value of the list. It must be given a positive integer.

    :param n_element: The number of elements on the list
    :return: The nth element of the list

    >>> hamming(5)
    [1, 2, 3, 4, 5]
    >>> hamming(10)
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12]
    >>> hamming(15)
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24]
    """
    n_element = int(n_element)
    if n_element < 1:
        my_error = ValueError("a should be a positive number")
        raise my_error

    hamming_list = [1]
    i, j, k = (0, 0, 0)
    index = 1
    while index < n_element:
        while hamming_list[i] * 2 <= hamming_list[-1]:
            i += 1
        while hamming_list[j] * 3 <= hamming_list[-1]:
            j += 1
        while hamming_list[k] * 5 <= hamming_list[-1]:
            k += 1
        hamming_list.append(
            min(hamming_list[i] * 2, hamming_list[j] * 3, hamming_list[k] * 5)
        )
        index += 1
    return hamming_list


if __name__ == "__main__":
    n = input("Enter the last number (nth term) of the Hamming Number Series: ")
    print("Formula of Hamming Number Series => 2^i * 3^j * 5^k")
    hamming_numbers = hamming(int(n))
    print("-----------------------------------------------------")
    print(f"The list with nth numbers is: {hamming_numbers}")
    print("-----------------------------------------------------")


# harshad number 
"""
A harshad number (or more specifically an n-harshad number) is a number that's
divisible by the sum of its digits in some given base n.
Reference: https://en.wikipedia.org/wiki/Harshad_number
"""


def int_to_base(number: int, base: int) -> str:
    """
    Convert a given positive decimal integer to base 'base'.
    Where 'base' ranges from 2 to 36.

    Examples:
    >>> int_to_base(23, 2)
    '10111'
    >>> int_to_base(58, 5)
    '213'
    >>> int_to_base(167, 16)
    'A7'
    >>> # bases below 2 and beyond 36 will error
    >>> int_to_base(98, 1)
    Traceback (most recent call last):
        ...
    ValueError: 'base' must be between 2 and 36 inclusive
    >>> int_to_base(98, 37)
    Traceback (most recent call last):
        ...
    ValueError: 'base' must be between 2 and 36 inclusive
    """

    if base < 2 or base > 36:
        raise ValueError("'base' must be between 2 and 36 inclusive")

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    if number < 0:
        raise ValueError("number must be a positive integer")

    while number > 0:
        number, remainder = divmod(number, base)
        result = digits[remainder] + result

    if result == "":
        result = "0"

    return result


def sum_of_digits(num: int, base: int) -> str:
    """
    Calculate the sum of digit values in a positive integer
    converted to the given 'base'.
    Where 'base' ranges from 2 to 36.

    Examples:
    >>> sum_of_digits(103, 12)
    '13'
    >>> sum_of_digits(1275, 4)
    '30'
    >>> sum_of_digits(6645, 2)
    '1001'
    >>> # bases below 2 and beyond 36 will error
    >>> sum_of_digits(543, 1)
    Traceback (most recent call last):
        ...
    ValueError: 'base' must be between 2 and 36 inclusive
    >>> sum_of_digits(543, 37)
    Traceback (most recent call last):
        ...
    ValueError: 'base' must be between 2 and 36 inclusive
    """

    if base < 2 or base > 36:
        raise ValueError("'base' must be between 2 and 36 inclusive")

    num_str = int_to_base(num, base)
    res = sum(int(char, base) for char in num_str)
    res_str = int_to_base(res, base)
    return res_str


def harshad_numbers_in_base(limit: int, base: int) -> list[str]:
    """
    Finds all Harshad numbers smaller than num in base 'base'.
    Where 'base' ranges from 2 to 36.

    Examples:
    >>> harshad_numbers_in_base(15, 2)
    ['1', '10', '100', '110', '1000', '1010', '1100']
    >>> harshad_numbers_in_base(12, 34)
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B']
    >>> harshad_numbers_in_base(12, 4)
    ['1', '2', '3', '10', '12', '20', '21']
    >>> # bases below 2 and beyond 36 will error
    >>> harshad_numbers_in_base(234, 37)
    Traceback (most recent call last):
        ...
    ValueError: 'base' must be between 2 and 36 inclusive
    >>> harshad_numbers_in_base(234, 1)
    Traceback (most recent call last):
        ...
    ValueError: 'base' must be between 2 and 36 inclusive
    """

    if base < 2 or base > 36:
        raise ValueError("'base' must be between 2 and 36 inclusive")

    if limit < 0:
        return []

    numbers = [
        int_to_base(i, base)
        for i in range(1, limit)
        if i % int(sum_of_digits(i, base), base) == 0
    ]

    return numbers


def is_harshad_number_in_base(num: int, base: int) -> bool:
    """
    Determines whether n in base 'base' is a harshad number.
    Where 'base' ranges from 2 to 36.

    Examples:
    >>> is_harshad_number_in_base(18, 10)
    True
    >>> is_harshad_number_in_base(21, 10)
    True
    >>> is_harshad_number_in_base(-21, 5)
    False
    >>> # bases below 2 and beyond 36 will error
    >>> is_harshad_number_in_base(45, 37)
    Traceback (most recent call last):
        ...
    ValueError: 'base' must be between 2 and 36 inclusive
    >>> is_harshad_number_in_base(45, 1)
    Traceback (most recent call last):
        ...
    ValueError: 'base' must be between 2 and 36 inclusive
    """

    if base < 2 or base > 36:
        raise ValueError("'base' must be between 2 and 36 inclusive")

    if num < 0:
        return False

    n = int_to_base(num, base)
    d = sum_of_digits(num, base)
    return int(n, base) % int(d, base) == 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()


# hexagonal number 

"""
== Hexagonal Number ==
The nth hexagonal number hn is the number of distinct dots
in a pattern of dots consisting of the outlines of regular
hexagons with sides up to n dots, when the hexagons are
overlaid so that they share one vertex.

https://en.wikipedia.org/wiki/Hexagonal_number
"""

# Author : Akshay Dubey (https://github.com/itsAkshayDubey)


def hexagonal(number: int) -> int:
    """
    :param number: nth hexagonal number to calculate
    :return: the nth hexagonal number
    Note: A hexagonal number is only defined for positive integers
    >>> hexagonal(4)
    28
    >>> hexagonal(11)
    231
    >>> hexagonal(22)
    946
    >>> hexagonal(0)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a positive integer
    >>> hexagonal(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a positive integer
    >>> hexagonal(11.0)
    Traceback (most recent call last):
        ...
    TypeError: Input value of [number=11.0] must be an integer
    """
    if not isinstance(number, int):
        msg = f"Input value of [number={number}] must be an integer"
        raise TypeError(msg)
    if number < 1:
        raise ValueError("Input must be a positive integer")
    return number * (2 * number - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

# krishnamurthy number 
"""
 == Krishnamurthy Number ==
It is also known as Peterson Number
A Krishnamurthy Number is a number whose sum of the
factorial of the digits equals to the original
number itself.

For example: 145 = 1! + 4! + 5!
    So, 145 is a Krishnamurthy Number
"""


def factorial(digit: int) -> int:
    """
    >>> factorial(3)
    6
    >>> factorial(0)
    1
    >>> factorial(5)
    120
    """

    return 1 if digit in (0, 1) else (digit * factorial(digit - 1))


def krishnamurthy(number: int) -> bool:
    """
    >>> krishnamurthy(145)
    True
    >>> krishnamurthy(240)
    False
    >>> krishnamurthy(1)
    True
    """

    fact_sum = 0
    duplicate = number
    while duplicate > 0:
        duplicate, digit = divmod(duplicate, 10)
        fact_sum += factorial(digit)
    return fact_sum == number


if __name__ == "__main__":
    print("Program to check whether a number is a Krisnamurthy Number or not.")
    number = int(input("Enter number: ").strip())
    print(
        f"{number} is {'' if krishnamurthy(number) else 'not '}a Krishnamurthy Number."
    )

# perfect number 
"""
== Perfect Number ==
In number theory, a perfect number is a positive integer that is equal to the sum of
its positive divisors, excluding the number itself.
For example: 6 ==> divisors[1, 2, 3, 6]
    Excluding 6, the sum(divisors) is 1 + 2 + 3 = 6
    So, 6 is a Perfect Number

Other examples of Perfect Numbers: 28, 486, ...

https://en.wikipedia.org/wiki/Perfect_number
"""


def perfect(number: int) -> bool:
    """
    Check if a number is a perfect number.

    A perfect number is a positive integer that is equal to the sum of its proper
    divisors (excluding itself).

    Args:
        number: The number to be checked.

    Returns:
        True if the number is a perfect number, False otherwise.

    Start from 1 because dividing by 0 will raise ZeroDivisionError.
    A number at most can be divisible by the half of the number except the number
    itself. For example, 6 is at most can be divisible by 3 except by 6 itself.

    Examples:
    >>> perfect(27)
    False
    >>> perfect(28)
    True
    >>> perfect(29)
    False
    >>> perfect(6)
    True
    >>> perfect(12)
    False
    >>> perfect(496)
    True
    >>> perfect(8128)
    True
    >>> perfect(0)
    False
    >>> perfect(-1)
    False
    >>> perfect(12.34)
    Traceback (most recent call last):
      ...
    ValueError: number must be an integer
    >>> perfect("Hello")
    Traceback (most recent call last):
      ...
    ValueError: number must be an integer
    """
    if not isinstance(number, int):
        raise ValueError("number must be an integer")
    if number <= 0:
        return False
    return sum(i for i in range(1, number // 2 + 1) if number % i == 0) == number


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    print("Program to check whether a number is a Perfect number or not...")
    try:
        number = int(input("Enter a positive integer: ").strip())
    except ValueError:
        msg = "number must be an integer"
        print(msg)
        raise ValueError(msg)

    print(f"{number} is {'' if perfect(number) else 'not '}a Perfect Number.")

# polygonal number 
def polygonal_num(num: int, sides: int) -> int:
    """
    Returns the `num`th `sides`-gonal number. It is assumed that `num` >= 0 and
    `sides` >= 3 (see for reference https://en.wikipedia.org/wiki/Polygonal_number).

    >>> polygonal_num(0, 3)
    0
    >>> polygonal_num(3, 3)
    6
    >>> polygonal_num(5, 4)
    25
    >>> polygonal_num(2, 5)
    5
    >>> polygonal_num(-1, 0)
    Traceback (most recent call last):
        ...
    ValueError: Invalid input: num must be >= 0 and sides must be >= 3.
    >>> polygonal_num(0, 2)
    Traceback (most recent call last):
        ...
    ValueError: Invalid input: num must be >= 0 and sides must be >= 3.
    """
    if num < 0 or sides < 3:
        raise ValueError("Invalid input: num must be >= 0 and sides must be >= 3.")

    return ((sides - 2) * num**2 - (sides - 4) * num) // 2


if __name__ == "__main__":
    import doctest

    doctest.testmod()


# pronic number 
"""
== Pronic Number ==
A number n is said to be a Proic number if
there exists an integer m such that n = m * (m + 1)

Examples of Proic Numbers: 0, 2, 6, 12, 20, 30, 42, 56, 72, 90, 110 ...
https://en.wikipedia.org/wiki/Pronic_number
"""

# Author : Akshay Dubey (https://github.com/itsAkshayDubey)


def is_pronic(number: int) -> bool:
    """
    # doctest: +NORMALIZE_WHITESPACE
    This functions takes an integer number as input.
    returns True if the number is pronic.
    >>> is_pronic(-1)
    False
    >>> is_pronic(0)
    True
    >>> is_pronic(2)
    True
    >>> is_pronic(5)
    False
    >>> is_pronic(6)
    True
    >>> is_pronic(8)
    False
    >>> is_pronic(30)
    True
    >>> is_pronic(32)
    False
    >>> is_pronic(2147441940)
    True
    >>> is_pronic(9223372033963249500)
    True
    >>> is_pronic(6.0)
    Traceback (most recent call last):
        ...
    TypeError: Input value of [number=6.0] must be an integer
    """
    if not isinstance(number, int):
        msg = f"Input value of [number={number}] must be an integer"
        raise TypeError(msg)
    if number < 0 or number % 2 == 1:
        return False
    number_sqrt = int(number**0.5)
    return number == number_sqrt * (number_sqrt + 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

# proth number 
"""
Calculate the nth Proth number
Source:
    https://handwiki.org/wiki/Proth_number
"""

import math


def proth(number: int) -> int:
    """
    :param number: nth number to calculate in the sequence
    :return: the nth number in Proth number
    Note: indexing starts at 1 i.e. proth(1) gives the first Proth number of 3
    >>> proth(6)
    25
    >>> proth(0)
    Traceback (most recent call last):
        ...
    ValueError: Input value of [number=0] must be > 0
    >>> proth(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input value of [number=-1] must be > 0
    >>> proth(6.0)
    Traceback (most recent call last):
        ...
    TypeError: Input value of [number=6.0] must be an integer
    """

    if not isinstance(number, int):
        msg = f"Input value of [number={number}] must be an integer"
        raise TypeError(msg)

    if number < 1:
        msg = f"Input value of [number={number}] must be > 0"
        raise ValueError(msg)
    elif number == 1:
        return 3
    elif number == 2:
        return 5
    else:
        """
        +1 for binary starting at 0 i.e. 2^0, 2^1, etc.
        +1 to start the sequence at the 3rd Proth number
        Hence, we have a +2 in the below statement
        """
        block_index = int(math.log(number // 3, 2)) + 2

        proth_list = [3, 5]
        proth_index = 2
        increment = 3
        for block in range(1, block_index):
            for _ in range(increment):
                proth_list.append(2 ** (block + 1) + proth_list[proth_index - 1])
                proth_index += 1
            increment *= 2

    return proth_list[number - 1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    for number in range(11):
        value = 0
        try:
            value = proth(number)
        except ValueError:
            print(f"ValueError: there is no {number}th Proth number")
            continue

        print(f"The {number}th Proth number: {value}")

# triangular number

"""
A triangular number or triangle number counts objects arranged in an
equilateral triangle. This module provides a function to generate n'th
triangular number.

For more information about triangular numbers, refer to:
https://en.wikipedia.org/wiki/Triangular_number
"""


def triangular_number(position: int) -> int:
    """
    Generate the triangular number at the specified position.

    Args:
        position (int): The position of the triangular number to generate.

    Returns:
        int: The triangular number at the specified position.

    Raises:
        ValueError: If `position` is negative.

    Examples:
    >>> triangular_number(1)
    1
    >>> triangular_number(3)
    6
    >>> triangular_number(-1)
    Traceback (most recent call last):
        ...
    ValueError: param `position` must be non-negative
    """
    if position < 0:
        raise ValueError("param `position` must be non-negative")

    return position * (position + 1) // 2


if __name__ == "__main__":
    import doctest

    doctest.testmod()

# ugly nubmer 
"""
Ugly numbers are numbers whose only prime factors are 2, 3 or 5. The sequence
1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, … shows the first 11 ugly numbers. By convention,
1 is included.
Given an integer n, we have to find the nth ugly number.

For more details, refer this article
https://www.geeksforgeeks.org/ugly-numbers/
"""


def ugly_numbers(n: int) -> int:
    """
    Returns the nth ugly number.
    >>> ugly_numbers(100)
    1536
    >>> ugly_numbers(0)
    1
    >>> ugly_numbers(20)
    36
    >>> ugly_numbers(-5)
    1
    >>> ugly_numbers(-5.5)
    Traceback (most recent call last):
        ...
    TypeError: 'float' object cannot be interpreted as an integer
    """
    ugly_nums = [1]

    i2, i3, i5 = 0, 0, 0
    next_2 = ugly_nums[i2] * 2
    next_3 = ugly_nums[i3] * 3
    next_5 = ugly_nums[i5] * 5

    for _ in range(1, n):
        next_num = min(next_2, next_3, next_5)
        ugly_nums.append(next_num)
        if next_num == next_2:
            i2 += 1
            next_2 = ugly_nums[i2] * 2
        if next_num == next_3:
            i3 += 1
            next_3 = ugly_nums[i3] * 3
        if next_num == next_5:
            i5 += 1
            next_5 = ugly_nums[i5] * 5
    return ugly_nums[-1]


if __name__ == "__main__":
    from doctest import testmod

    testmod(verbose=True)
    print(f"{ugly_numbers(200) = }")


# weird number 
"""
https://en.wikipedia.org/wiki/Weird_number

Fun fact: The set of weird numbers has positive asymptotic density.
"""
from math import sqrt


def factors(number: int) -> list[int]:
    """
    >>> factors(12)
    [1, 2, 3, 4, 6]
    >>> factors(1)
    [1]
    >>> factors(100)
    [1, 2, 4, 5, 10, 20, 25, 50]

    # >>> factors(-12)
    # [1, 2, 3, 4, 6]
    """

    values = [1]
    for i in range(2, int(sqrt(number)) + 1, 1):
        if number % i == 0:
            values.append(i)
            if int(number // i) != i:
                values.append(int(number // i))
    return sorted(values)


def abundant(n: int) -> bool:
    """
    >>> abundant(0)
    True
    >>> abundant(1)
    False
    >>> abundant(12)
    True
    >>> abundant(13)
    False
    >>> abundant(20)
    True

    # >>> abundant(-12)
    # True
    """
    return sum(factors(n)) > n


def semi_perfect(number: int) -> bool:
    """
    >>> semi_perfect(0)
    True
    >>> semi_perfect(1)
    True
    >>> semi_perfect(12)
    True
    >>> semi_perfect(13)
    False

    # >>> semi_perfect(-12)
    # True
    """
    values = factors(number)
    r = len(values)
    subset = [[0 for i in range(number + 1)] for j in range(r + 1)]
    for i in range(r + 1):
        subset[i][0] = True

    for i in range(1, number + 1):
        subset[0][i] = False

    for i in range(1, r + 1):
        for j in range(1, number + 1):
            if j < values[i - 1]:
                subset[i][j] = subset[i - 1][j]
            else:
                subset[i][j] = subset[i - 1][j] or subset[i - 1][j - values[i - 1]]

    return subset[r][number] != 0


def weird(number: int) -> bool:
    """
    >>> weird(0)
    False
    >>> weird(70)
    True
    >>> weird(77)
    False
    """
    return abundant(number) and not semi_perfect(number)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    for number in (69, 70, 71):
        print(f"{number} is {'' if weird(number) else 'not '}weird.")

