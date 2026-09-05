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
        eps = eps/2
    return eps/2



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
    if a*b>0:
        roots = 2*a*c/(-b + math.sqrt(D)), 2*a*c/(-b - math.sqrt(D))
    elif a*b<0:
        roots = 2*a*c/(-b - math.sqrt(D)), 2*a*c/(-b + math.sqrt(D))
    return roots




def naive_sum(xs):
    """Return the sum of ``xs`` using ordinary left-to-right accumulation.
    Accept any iterable of numbers. Do not call Python's built-in ``sum`` for
    this function; the point is to expose the behavior of the naive loop.
    """
    xs = list(xs)
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
    xs = list(xs)
    sum = []
    while len(xs) != 1:
        while len(sum) != 1:
            sum.append(xs[i]+xs[i+1] for i in range(0,len(xs)-1,2))
        xs = sum
    return xs[0]




def kahan_sum(xs):
    """Return the sum of ``xs`` using Kahan compensated summation.
    7
    Accept any iterable of numbers. Maintain both a running total and a
    compensation term for low-order bits lost to rounding. Return ``0.0`` for
    an empty input.
    """
    xs = list(xs)
    if not xs:
        return 0.0
    c = 0   # compensation variable
    S = 0   # initilaization of sum
    for x in xs:
        y = x - c
        t = S + y
        c += (t - S) - y
        S += t
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
    raise NotImplementedError