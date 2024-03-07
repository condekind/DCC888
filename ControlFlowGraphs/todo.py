from lang import *
import sys


def test_min(m, n):
    """
    Stores in the variable 'answer' the minimum of 'm' and 'n'

    Examples:
        >>> test_min(3, 4)
        3
        >>> test_min(4, 3)
        3
    """
    env = Env({"m": m, "n": n, "x": m, "zero": 0})
    m_min = Add("answer", "m", "zero")
    n_min = Add("answer", "n", "zero")
    p = Lth("p", "n", "m")
    b = Bt("p", n_min, m_min)
    p.add_next(b)
    interp(p, env)
    return env.get("answer")


def test_fib(n):
    """
    Stores in the variable 'answer' the n-th number of the Fibonacci sequence.

    Examples:
        >>> test_fib(2)
        2
        >>> test_fib(3)
        3
        >>> test_fib(6)
        13
    """
    env = Env({"c": 0, "N": n, "fib0": 0, "fib1": 1, "zero": 0, "one": 1})
    i0 = Lth("p", "c", "N")
    i2 = Add("aux", "fib1", "zero")
    i3 = Add("fib1", "aux", "fib0")
    i4 = Add("fib0", "aux", "zero")
    i5 = Add("c", "c", "one")
    i6 = Add("answer", "fib1", "zero")
    i1 = Bt("p", i2, i6)
    i0.add_next(i1)
    i2.add_next(i3)
    i3.add_next(i4)
    i4.add_next(i5)
    i5.add_next(i0)
    interp(i0, env)
    return env.get("answer")


def test_min3(x, y, z):
    """
    Stores in the variable 'answer' the minimum of 'x', 'y' and 'z'

    Examples:
        >>> test_min3(3, 4, 5)
        3
        >>> test_min3(5, 4, 3)
        3
    """
    env = Env({"x": x, "y": y, "z": z, "zero": 0})

    x_ans = Add("answer", "x", "zero")
    y_ans = Add("answer", "y", "zero")
    z_ans = Add("answer", "z", "zero")

    x_lt_y = Lth("x_lt_y", "x", "y")
    x_lt_z = Lth("x_lt_z", "x", "z")
    y_lt_z = Lth("y_lt_z", "y", "z")

    b0 = Bt("x_lt_z", x_ans, z_ans)
    b1 = Bt("y_lt_z", y_ans, z_ans)
    b2 = Bt("x_lt_y", x_lt_z, y_lt_z)

    x_lt_y.add_next(b2)
    x_lt_z.add_next(b0)
    y_lt_z.add_next(b1)

    interp(x_lt_y, env)
    return env.get("answer")


def equals(dst, v1, v2, next_if_true: Inst, next_if_false: Inst):
    """Requires both "zero": 0 and "one": 1 in your Env."""
    ans_true = Lth(dst, "zero", "one")
    ans_false = Lth(dst, "one", "zero")
    lt0 = Lth("__lt0_equals__", v1, v2)
    lt1 = Lth("__lt1_equals__", v2, v1)
    bt_second_false = Bt("__lt1_equals__", ans_false, ans_true)
    bt_first_false = Bt("__lt0_equals__", ans_false, bt_second_false)
    lt0.add_next(lt1)
    lt1.add_next(bt_first_false)
    return lt0


def test_equals(x, y):
    """
    >>> test_equals(3, 0)
    False
    >>> test_equals(0, 3)
    False
    >>> test_equals(32, 8)
    False
    >>> test_equals(3, 2)
    False
    >>> test_equals(2, 3)
    False
    >>> test_equals(3, 3)
    True
    >>> test_equals(0, 0)
    True
    >>> test_equals(1, 1)
    True
    >>> test_equals(True, True)
    True
    >>> test_equals(False, True)
    False
    >>> test_equals(True, False)
    False
    >>> test_equals(False, False)
    True
    """
    env = Env({"x": x, "y": y, "one": 1, "zero": 0})

    v1 = "x"
    v2 = "y"
    ans_true = Lth("answer", "zero", "one")
    ans_false = Lth("answer", "one", "zero")

    lt0 = equals("answer", v1, v2, ans_true, ans_false)
    interp(lt0, env)
    return env.get("answer")


def test_div(m, n):
    """
    Stores in the variable 'answer' the integer division of 'm' and 'n'.

    Examples:
        >>> test_div(30, 4)
        7
        >>> test_div(4, 3)
        1
        >>> test_div(1, 3)
        0
    """
    # TODO: Implement this method
    return env.get("answer")


def test_fact(n):
    """
    Stores in the variable 'answer' the factorial of 'n'.

    Examples:
        >>> test_fact(3)
        6
    """
    # TODO: Implement this method
    return env.get("answer")
