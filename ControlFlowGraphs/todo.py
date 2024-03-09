from lang import *
import sys

def call_counter(func):
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        return func(*args, **kwargs)
    wrapper.num_calls = 0
    return wrapper

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


@call_counter
def Eq(dst, v1, v2, env: Optional[Env] = None):
    """
    Requires either an Env passed or both "zero": 0 and "one": 1 in your Env.
    If an Env is passed, "zero": 0 and "one": 1 are inserted into it.
    """

    if env is not None:
        env.set("zero", 0)
        env.set("one", 1)
        # Otherwise, we assume the user has these definitions

    ans_true = Lth(dst, "zero", "one")
    ans_false = Lth(dst, "one", "zero")

    lt0 = Lth(f"__lt0_equals_{Eq.num_calls}__", v1, v2)
    lt1 = Lth(f"__lt1_equals_{Eq.num_calls}__", v2, v1)
    bt_second_false = Bt(f"__lt1_equals_{Eq.num_calls}__", ans_false, ans_true)
    bt_first_false = Bt(f"__lt0_equals_{Eq.num_calls}__", ans_false, bt_second_false)
    lt0.add_next(lt1)
    lt1.add_next(bt_first_false)

    # We return both possible exit nodes, so the caller might assign a next
    # node to both, even though one of them is unreachable
    return (lt0, ans_true, ans_false)


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

    lt0, *_ = Eq("answer", v1, v2)

    interp(lt0, env)
    return env.get("answer")


def test_if_equals(x, y):
    """
    >>> test_if_equals(3, 0)
    False
    >>> test_if_equals(0, 3)
    False
    >>> test_if_equals(32, 8)
    False
    >>> test_if_equals(3, 2)
    False
    >>> test_if_equals(2, 3)
    False
    >>> test_if_equals(3, 3)
    True
    >>> test_if_equals(0, 0)
    True
    >>> test_if_equals(1, 1)
    True
    >>> test_if_equals(True, True)
    True
    >>> test_if_equals(False, True)
    False
    >>> test_if_equals(True, False)
    False
    >>> test_if_equals(False, False)
    True
    """
    env = Env({"x": x, "y": y, "one": 1, "zero": 0})

    v1 = "x"
    v2 = "y"
    ans_true = Lth("answer", "zero", "one")
    ans_false = Lth("answer", "one", "zero")

    lt0, if_true, if_false = Eq("is_eq", v1, v2)
    b0 = Bt("is_eq", ans_true, ans_false)
    if_true.add_next(b0)
    if_false.add_next(b0)

    interp(lt0, env)
    return env.get("answer")


@call_counter
def And(dst, v1, v2, env: Optional[Env] = None):
    """
    Requires either an Env passed or both "zero": 0 and "one": 1 in your Env.
    If an Env is passed, "zero": 0 and "one": 1 are inserted into it.
    """
    if env is not None:
        env.set("zero", 0)
        env.set("one", 1)
        # Otherwise, we assume the user has these definitions

    ans_true = Lth(dst, "zero", "one")
    ans_false = Lth(dst, "one", "zero")

    m0 = Mul( f"__m0_and_{And.num_calls}__", v1, v2)
    ge0 = Geq(f"__ge_and_{And.num_calls}__", f"__m0_and_{And.num_calls}__", "one")
    b0 = Bt(f"__ge_and_{And.num_calls}__", ans_true, ans_false)
    m0.add_next(ge0)
    ge0.add_next(b0)
    return m0


def test_and(x, y):
    """
    >>> test_and(True, True)
    True
    >>> test_and(False, True)
    False
    >>> test_and(True, False)
    False
    >>> test_and(False, False)
    False
    >>> test_and(3, 0)
    False
    >>> test_and(0, 3)
    False
    >>> test_and(32, 8)
    True
    >>> test_and(3, 2)
    True
    >>> test_and(2, 3)
    True
    >>> test_and(3, 3)
    True
    >>> test_and(0, 0)
    False
    >>> test_and(1, 1)
    True
    """
    env = Env({"x": x, "y": y, "one": 1, "zero": 0})

    and0 = And("answer", "x", "y")

    interp(and0, env)
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
