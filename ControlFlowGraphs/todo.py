from __future__ import annotations

from ControlFlowGraphs.helpers import And, Ne
from lang import *
from inst2dot import dotgen


@dotgen(ofile_prefix="archive")
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


@dotgen(ofile_prefix="archive")
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


@dotgen(ofile_prefix="archive")
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


@dotgen(ofile_prefix="archive")
def test_div(m, n):
    """
    Stores in the variable 'answer' the integer division of 'm' and 'n'.

    Examples:
        >>> test_div(0, 3)
        0
        >>> test_div(32, 8)
        4
        >>> test_div(3, 2)
        1
        >>> test_div(2, 3)
        0
        >>> test_div(3, 3)
        1
        >>> test_div(128, 64)
        2

        Implement for negatives too. In python, 3 // 2 == -2
        >>> test_div(-128, 64)
        -2
        >>> test_div(-128, 64)
        -2
        >>> test_div(-128, -64)
        2
        >>> test_div(-65, 64)
        -2
        >>> test_div(-65, -64)
        1
        >>> test_div(-3, 2)
        -2
        >>> test_div(3, -2)
        -2
    """
    env = Env(
        {
            "answer": 0,
            "neg_one": -1,
            "zero": 0,
            "one": 1,
            "aux_m": abs(m),
            "aux_n": abs(n),
            "neg_n": -abs(n),
            "ans_sign": (m < 0) != (n < 0),
        }
    )

    # This was made based on a manual implementation that mimics how Python 3
    # handles integer division (the // operator). This is the impl:
    #
    # def div(m, n):
    #
    #    negative_result = (m < 0) != (n < 0)
    #    m, n = abs(m), abs(n)
    #
    #    quotient = 0
    #    while m >= n:
    #        m -= n
    #        quotient += 1
    #
    #    # Adjust the quotient for negative results
    #    if negative_result and m != 0:
    #        quotient = -(quotient + 1)
    #    elif negative_result:
    #        quotient = -quotient
    #
    #    return quotient
    #

    # Note: the helpers used in this function (Ne, And) are just shorthands
    # that instantiates existing instruction nodes.
    # They take a "dst" to write the result, and both return a tuple:
    #   (first_node, exit node if true, exit node if false)
    # This allows the caller to set the next nodes for each case, sometimes
    # avoiding the need for an explicit Bt

    ans = Add("answer", "answer", "zero")

    # Some comments above instructions refer to lines in the reference
    # algorithm above

    # ------------------------- Inside while block -------------------------- #
    # m -= n
    dec_n_from_m = Add("aux_m", "aux_m", "neg_n")
    # quotient += 1
    inc_q = Add("answer", "answer", "one")
    # aux_m_ge_n <- m >= n
    aux_m_ge_n = Geq("aux_m_ge_n", "aux_m", "aux_n")
    # ----------------------------------------------------------------------- #

    # m_ne_zero <- m != 0
    m_ne_zero, ne_true, ne_false = Ne("m_ne_zero", "aux_m", "zero")
    # ans_sign_and_m_ne_zero <- ans_sign AND m_ne_zero
    ans_sign_and_m_ne_zero, and_true, and_false = And(
        "ans_sign_and_m_ne_zero", "ans_sign", "m_ne_zero"
    )

    # tmp = (quotient + 1)
    ans_plus_one = Add("ans_plus_one", "answer", "one")
    # quotient = -tmp
    update_ans = Mul("answer", "ans_plus_one", "neg_one")

    # quotient = -quotient
    neg_ans = Mul("answer", "answer", "neg_one")

    # elif negative_result ↑
    if_ans_sign = Bt("ans_sign", neg_ans, ans)

    while0 = Bt("aux_m_ge_n", dec_n_from_m, m_ne_zero)

    ans_plus_one.add_next(update_ans)
    update_ans.add_next(ans)
    neg_ans.add_next(ans)
    ne_true.add_next(ans_sign_and_m_ne_zero)
    ne_false.add_next(if_ans_sign)
    and_true.add_next(ans_plus_one)
    and_false.add_next(if_ans_sign)
    dec_n_from_m.add_next(inc_q)
    inc_q.add_next(aux_m_ge_n)
    aux_m_ge_n.add_next(while0)

    interp(aux_m_ge_n, env)
    return env.get("answer")


@dotgen(ofile_prefix="archive")
def test_fact(n):
    """
    Stores in the variable 'answer' the factorial of 'n'.

    Examples:
        >>> test_fact(3)
        6
        >>> test_fact(0)
        1
        >>> test_fact(1)
        1
        >>> test_fact(5)
        120
        >>> test_fact(6)
        720
        >>> test_fact(10)
        3628800
        >>> test_fact(15)
        1307674368000
    """
    env = Env(
        {"n": n, "n_plus_one": n + 1, "count": 1, "answer": 1, "one": 1, "zero": 0}
    )
    answer_init = Add("answer", "answer", "zero")
    loop_cond = Lth("loop_cond", "count", "n_plus_one")
    inc_count = Add("count", "count", "one")
    multiply = Mul("answer", "answer", "count")

    # Loop setup
    check_loop = Bt("loop_cond", multiply, answer_init)
    multiply.add_next(inc_count)
    inc_count.add_next(loop_cond)
    loop_cond.add_next(check_loop)

    # Execution
    interp(loop_cond, env)
    return env.get("answer")
