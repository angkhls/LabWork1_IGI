# Lab work #3: Standard data types, collections, functions, modules
# Task 1: Compute ln(1-x) using power series expansion
# Version: 1.0
# Developer: Khlus Anhelina
# Date: 19.03.26

import math


def calculate_ln(x: float, eps: float = 1e-6):
    """
    Calculates ln(1-x) using power series: -sum(x^n / n, n=1..inf).

    Args:
        x: argument, must satisfy |x| < 1
        eps: precision of calculation (default 1e-6)

    Returns:
        Tuple (result, n) where result is the computed value and n is number of terms used.

    Raises:
        ValueError: if |x| >= 1
    """
    if abs(x) >= 1:
        raise ValueError(f"x must satisfy |x| < 1, got x = {x}")

    result = 0.0
    term = -x
    n = 1

    while abs(term) >= eps and n <= 500:
        result += term
        n += 1
        term = term * x * (n - 1) / n

    return result, n - 1


def math_ln(x: float):
    """
    Calculates ln(1-x) using Python's math module.

    Args:
        x: argument value

    Returns:
        float: math.log(1 - x)
    """
    return math.log(1 - x)