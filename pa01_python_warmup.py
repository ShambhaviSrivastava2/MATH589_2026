def course_tag(name, section):
    """Return a cleaned course label.
    Convert both inputs to strings, strip surrounding whitespace, and return
    ``"Math 589<section>: <name>"``. Example:
    ``course_tag(" Grace Hopper ", " B ") == "Math 589B: Grace Hopper"``.
    """
    name = str(name).strip()
    section = str(section).strip()
    return f"Math 589{section}: {name}"


def vector_stats(xs):
    """Return basic statistics for the numbers in ``xs``.
    Accept any iterable. Return a dictionary with exactly these keys:
    ``"count"``, ``"total"``, ``"mean"``, ``"min"``, and ``"max"``.
    Raise ``ValueError`` if ``xs`` is empty.
    """
    xs = list(xs)
    if not xs:
        raise ValueError
    return {"count":len(xs), "total":sum(xs), "mean":sum(xs)/len(xs), "min":min(xs), 
            "max":max(xs)}
    


def centered(xs):
    """Return the data after subtracting its mean.
    Accept any iterable. Return a list of floats, one entry ``x - mean`` for
    each original entry ``x``. Raise ``ValueError`` if ``xs`` is empty.
    """
    xs = list(xs)
    if not xs:
        raise ValueError
    mean = sum(xs)/len(xs)
    return [x - mean for x in xs]



def dot_product(x, y):
    """Return the dot product of two equal-length iterables.
    For example, ``dot_product([1, 2, 3], [4, 5, 6])`` should return
    ``1*4 + 2*5 + 3*6 = 32``. Raise ``ValueError`` if the input lengths are
    different.
    """
    x = list(x)
    y = list(y)
    if len(x) != len(y):
        raise ValueError
    return sum(x[i]*y[i] for i in range(len(x)))



def first_sign_change(xs):
    """Return the first consecutive index pair with opposite signs.
    Return ``(i, i + 1)`` for the first adjacent pair ``xs[i]``,
    ``xs[i + 1]`` whose signs are opposite. Zero is neither positive nor
    negative. Return ``None`` if no such pair exists.
    """
    xs = list(xs)
    for i in range(len(xs)-1):
        if xs[i]*xs[i+1] < 0:
            return (i, i+1)
    return None



def evaluate_polynomial(coefficients, x):
    """Evaluate a polynomial using Horner's scheme.
    The coefficients are ordered from highest degree to constant term. For
    example, ``[2, -3, 1]`` represents ``2*x*x - 3*x + 1``. Return ``0`` for
    an empty coefficient list.
    """
    coefficients = list(coefficients)
    result = 0
    for i in range(len(coefficients)):
        result = result * x + coefficients[i]
    return result
    