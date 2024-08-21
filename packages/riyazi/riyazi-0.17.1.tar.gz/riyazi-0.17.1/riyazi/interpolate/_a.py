import numpy as np


def lagrange(x, y, x_int):
    """Interpolates a value using the 'Lagrange polynomial'.
    Args:
        x: an array containing x values.
        y: an array containing y values.
        x_int: value to interpolate.
    Returns:
        y_int: interpolated value.
    """
    n = x.size
    y_int = 0

    for i in range(0, n):
        p = y[i]
        for j in range(0, n):
            if i != j:
                p = p * (x_int - x[j]) / (x[i] - x[j])
        y_int = y_int + p

    return [y_int]


def neville(x, y, x_int):
    """Interpolates a value using the 'Neville polynomial'.
    Args:
        x: an array containing x values.
        y: an array containing y values.
        x_int: value to interpolate.
    Returns:
        y_int: interpolated value.
        q: coefficients matrix.
    """
    n = x.size
    q = np.zeros((n, n - 1))

    # Insert 'y' in the first column of the matrix 'q'
    q = np.concatenate((y[:, None], q), axis=1)

    for i in range(1, n):
        for j in range(1, i + 1):
            q[i, j] = ((x_int - x[i - j]) * q[i, j - 1] -
                       (x_int - x[i]) * q[i - 1, j - 1]) / (x[i] - x[i - j])

    y_int = q[n - 1, n - 1]
    return [y_int, q]




"""Methods for numerical integration."""


def composite_simpson(f, b, a, n):
    """Calculate the integral from 1/3 Simpson's Rule.
    Args:
        f: function f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.
    Returns:
        xi: integral value.
    """
    h = (b - a) / n

    sum_odd = 0
    sum_even = 0

    for i in range(0, n - 1):
        x = a + (i + 1) * h
        if (i + 1) % 2 == 0:
            sum_even += f(x)
        else:
            sum_odd += f(x)

    xi = h / 3 * (f(a) + 2 * sum_even + 4 * sum_odd + f(b))
    return [xi]


def composite_trapezoidal(f, b, a, n):
    """Calculate the integral from the Trapezoidal Rule.
    Args:
        f: function f(x).
        a: the initial point.
        b: the final point.
        n: number of intervals.
    Returns:
        xi: integral value.
    """
    h = (b - a) / n

    sum_x = 0

    for i in range(0, n - 1):
        x = a + (i + 1) * h
        sum_x += f(x)

    xi = h / 2 * (f(a) + 2 * sum_x + f(b))
    return [xi]


def composite2_simpson(x, y):
    """Calculate the integral from 1/3 Simpson's Rule.
    Args:
        x: an array containing x values.
        y: an array containing y values.
    Returns:
        xi: integral value.
    """
    if y.size != y.size:
        raise Exception("'x' and 'y' must have same size.")

    h = x[1] - x[0]
    n = x.size

    sum_odd = 0
    sum_even = 0

    for i in range(1, n - 1):
        if (i + 1) % 2 == 0:
            sum_even += y[i]
        else:
            sum_odd += y[i]

    xi = h / 3 * (y[0] + 2 * sum_even + 4 * sum_odd + y[n - 1])
    return [xi]


def composite2_trapezoidal(x, y):
    """Calculate the integral from the Trapezoidal Rule.
    Args:
        x: an array containing x values.
        y: an array containing y values.
    Returns:
        xi: integral value.
    """
    if y.size != y.size:
        raise Exception("'x' and 'y' must have same size.")

    h = x[1] - x[0]
    n = x.size

    sum_x = 0

    for i in range(1, n - 1):
        sum_x += y[i]

    xi = h / 2 * (y[0] + 2 * sum_x + y[n - 1])
    return [xi]