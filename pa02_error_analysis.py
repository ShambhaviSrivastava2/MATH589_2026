"""Starter file for Programming Assignment 02.
Replace each ``raise NotImplementedError`` line. Do not change function names or
argument lists; the autograder imports this module directly.
"""
import math


def machine_epsilon_halving():
    """Return the traditional machine epsilon for Python ``float``.
    Use the halving experiment starting from ``eps = 1.0``. The returned value
    should be the smallest positive floating-point number found by this
    experiment such that ``1.0 + eps != 1.0`` but ``1.0 + eps/2.0 == 1.0``.
    For IEEE double precision, this is ``2**-52``.
    """
    eps = 1.0
    while 1.0 + eps != 1.0:
        eps = eps/2.0
    return 2.0 * eps



def unit_roundoff():
    """Return the unit roundoff for round-to-nearest arithmetic.
    For IEEE double precision, unit roundoff is one half of the traditional
    machine epsilon, namely ``2**-53``. You may compute it from
    ``machine_epsilon_halving()``.
    """
    return machine_epsilon_halving()/2



def stable_quadratic_roots(a, b, c):
    """Return both real roots of ``a*x*x + b*x + c = 0`` stably.
    Use a formula that avoids subtracting nearly equal floating-point numbers
    when ``abs(b)`` is large. Return a two-entry tuple sorted in increasing
    order. Raise ``ValueError`` if ``a == 0`` or if the discriminant is
    negative. You may assume the nondegenerate real-root cases tested by the
    autograder do not have a zero value of the stable auxiliary quantity.
    """
    D = b**2 - 4*a*c
    if a == 0 or D < 0:
        raise ValueError
    if a > 0:
        if (-b + math.sqrt(D)) <= 10e-5:
            roots = ((-b-math.sqrt(D))/2*a, 2*c/(-b - math.sqrt(D)))
        elif (-b - math.sqrt(D)) <= 10e-5:
            roots = (2*c/(-b + math.sqrt(D)), (-b+math.sqrt(D))/2*a)
    elif a < 0:
        if (-b + math.sqrt(D)) <= 10e-5:
            roots = (2*c/(-b - math.sqrt(D)), (-b-math.sqrt(D))/2*a)
        elif (-b - math.sqrt(D)) <= 10e-5:
            roots = ((-b+math.sqrt(D))/2*a, 2*c/(-b + math.sqrt(D)))
    return roots





def naive_sum(xs):
    """Return the sum of ``xs`` using ordinary left-to-right accumulation.
    Accept any iterable of numbers. Do not call Python's built-in ``sum`` for
    this function; the point is to expose the behavior of the naive loop.
    """
    sum = 0 
    for x in xs:
        sum += x
    return sum



def pairwise_sum(xs):
    """Return the sum of ``xs`` using pairwise summation.
    Accept any iterable of numbers. Convert it to a sequence if useful, then
    recursively or iteratively add balanced halves so that long sums have a
    shallower rounding-error tree than left-to-right summation. Return ``0.0``
    for an empty input.
    """
    if not xs:
        return 0.0
    
    if len(xs) == 1:
        return xs[0]
    
    mid = len(xs) // 2
    return pairwise_sum(xs[0: mid]) + pairwise_sum(xs[mid:])




def kahan_sum(xs):
    """Return the sum of ``xs`` using Kahan compensated summation.
    7
    Accept any iterable of numbers. Maintain both a running total and a
    compensation term for low-order bits lost to rounding. Return ``0.0`` for
    an empty input.
    """
    if not xs:
        return 0.0
    c = 0   # compensation variable
    S = 0   # initilaization of sum
    for x in xs:
        y = x - c
        t = S + y
        c = (t - S) - y
        S = t
    return S
    


def decode_minifloat(bitstring):
    """Decode an 8-bit ``(1.4.3)`` minifloat.
    The format has one sign bit, four exponent bits, three fraction bits, and
    exponent bias ``7``. Handle zeros, subnormals, normal numbers, infinities,
    and NaNs using the same conventions as IEEE binary formats:
    - exponent field ``0000`` and fraction ``000`` is signed zero;
    - exponent field ``0000`` and nonzero fraction is subnormal;
    - exponent field between ``0001`` and ``1110`` is normal;
    - exponent field ``1111`` and fraction ``000`` is signed infinity;
    - exponent field ``1111`` and nonzero fraction is NaN.
    Return a dictionary with exactly the keys ``"sign"``, ``"kind"``, and
    ``"value"``. The sign is ``1`` or ``-1``. The kind is one of ``"zero"``,
    ``"subnormal"``, ``"normal"``, ``"inf"``, or ``"nan"``. The value is the
    decoded Python ``float``, ``math.inf``, ``-math.inf``, or ``math.nan``.
    """
    dict = {}
    sign = int(bitstring[0], 2)
    exponent = int(bitstring[1:5], 2)
    fraction = int(bitstring[5:8], 2)
    if sign == 0:
        dict["sign"]= 1
    if sign == 1:
        dict["sign"]= -1
    if exponent == 0 and fraction == 0:
        dict["kind"]= "zero"
        if sign == 0:
            dict["value"]= 0.0
        if sign == 1:
            dict["value"]= -0.0
    elif exponent == 0 and fraction != 0:
        dict["kind"]= "subnormal"
        if sign == 0:
            dict["value"]= fraction/8 * 2**-6
        if sign == 1:
            dict["value"]= -fraction/8 * 2**-6
    elif 1 <= exponent <= 14:
        dict["kind"]= "normal"
        if sign == 0:
            dict["value"]= (1 + fraction/8) * 2**(exponent-7)
        if sign == 1:
            dict["value"]= -(1 + fraction/8) * 2**(exponent-7)
    elif exponent == 15 and fraction == 0:
        dict["kind"]= "inf"
        if sign == 0:
            dict["value"]= math.inf
        elif sign == 1:
            dict["value"]= -math.inf
    elif exponent == 15 and fraction != 0:
        dict["kind"]= "nan"
        dict["value"]= math.nan
    return dict