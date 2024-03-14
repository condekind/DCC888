from __future__ import annotations

from lang import *
from inst2dot import dotgen


def call_counter(func):
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        return func(*args, **kwargs)

    wrapper.num_calls = 0
    return wrapper


@call_counter
def Eq(dst, v1, v2, env: Env | None = None):
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

    lt0 = Lth(f"_lt0_eq_{Eq.num_calls}", v1, v2)
    lt1 = Lth(f"_lt1_eq_{Eq.num_calls}", v2, v1)
    bt_second_false = Bt(f"_lt1_eq_{Eq.num_calls}", ans_false, ans_true)
    bt_first_false = Bt(f"_lt0_eq_{Eq.num_calls}", ans_false, bt_second_false)
    lt0.add_next(lt1)
    lt1.add_next(bt_first_false)

    # We return both possible exit nodes, so the caller might assign a next
    # node to both, even though one of them is unreachable
    return (lt0, ans_true, ans_false)


@dotgen(ofile_prefix="archive")
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


@call_counter
def Ne(dst, v1, v2, env: Env | None = None):
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

    lt0 = Lth(f"_lt0_ne_{Eq.num_calls}", v1, v2)
    lt1 = Lth(f"_lt1_ne_{Eq.num_calls}", v2, v1)
    bt_second_false = Bt(f"_lt1_ne_{Eq.num_calls}", ans_true, ans_false)
    bt_first_false = Bt(f"_lt0_ne_{Eq.num_calls}", ans_true, bt_second_false)
    lt0.add_next(lt1)
    lt1.add_next(bt_first_false)

    # We return both possible exit nodes, so the caller might assign a next
    # node to both, even though one of them is unreachable
    return (lt0, ans_true, ans_false)


@dotgen(ofile_prefix="archive")
def test_not_equals(x, y):
    """
    >>> test_not_equals(3, 0)
    True
    >>> test_not_equals(0, 3)
    True
    >>> test_not_equals(32, 8)
    True
    >>> test_not_equals(3, 2)
    True
    >>> test_not_equals(2, 3)
    True
    >>> test_not_equals(3, 3)
    False
    >>> test_not_equals(0, 0)
    False
    >>> test_not_equals(1, 1)
    False
    >>> test_not_equals(True, True)
    False
    >>> test_not_equals(False, True)
    True
    >>> test_not_equals(True, False)
    True
    >>> test_not_equals(False, False)
    False
    """
    env = Env({"x": x, "y": y, "one": 1, "zero": 0})

    v1 = "x"
    v2 = "y"

    lt0, *_ = Ne("answer", v1, v2)

    interp(lt0, env)
    return env.get("answer")


@call_counter
def IfEq(v1, v2, dst_true, dst_false, env: Env | None = None):
    """
    IfEq differs from Eq in the sense that you don't pass a "dst" register to
    store the result of the comparison, but rather you pass the nodes that
    should come next for the cases in which (i) v1 == v2 is true,
    or (ii) v1 == v2 is false.

    Requires either an Env passed or both "zero": 0 and "one": 1 in your Env.
    If an Env is passed, "zero": 0 and "one": 1 are inserted into it.
    """

    if env is not None:
        env.set("zero", 0)
        env.set("one", 1)
        # Otherwise, we assume the user has these definitions

    lt0 = Lth(f"_lt0_ifeq_{Eq.num_calls}", v1, v2)
    lt1 = Lth(f"_lt1_ifeq_{Eq.num_calls}", v2, v1)
    bt_second_false = Bt(f"_lt1_ifeq_{Eq.num_calls}", dst_false, dst_true)
    bt_first_false = Bt(f"_lt0_ifeq_{Eq.num_calls}", dst_false, bt_second_false)
    lt0.add_next(lt1)
    lt1.add_next(bt_first_false)

    # We return both possible exit nodes, so the caller might assign a next
    # node to both, even though one of them is unreachable
    return lt0


@dotgen(ofile_prefix="archive")
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

    ans_true = Lth("answer", "zero", "one")
    ans_false = Lth("answer", "one", "zero")

    lt0 = IfEq("x", "y", ans_true, ans_false)

    interp(lt0, env)
    return env.get("answer")


@call_counter
def And(dst, v1, v2, env: Env | None = None):
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

    m0 = Mul(f"_m0_and_{And.num_calls}", v1, v2)
    ge0 = Geq(f"_ge_and_{And.num_calls}", f"_m0_and_{And.num_calls}", "one")
    b0 = Bt(f"_ge_and_{And.num_calls}", ans_true, ans_false)
    m0.add_next(ge0)
    ge0.add_next(b0)
    return (m0, ans_true, ans_false)


@dotgen(ofile_prefix="archive")
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

    and0, *_ = And("answer", "x", "y")

    interp(and0, env)
    return env.get("answer")
