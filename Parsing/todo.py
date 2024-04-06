"""
This file implements a parser: a function that reads a text file, and returns
a control-flow graph of instructions plus an environment mapping variables to
integer values. The text file has the following format:

    [First line] A dictionary describing the environment
    [n-th line] The n-th instruction in our program.

As an example, the program below sums up the numbers a, b and c:

    {"a": 1, "b": 3, "c": 5}
    x = add a b
    l2 = x = add x c
"""

import re

import lang
from lang import Env, Inst, Add, Mul, Lth, Geq, interp


def line2env(line: str) -> Env:
    """
    Maps a string (the line) to a dictionary in python. This function will be
    useful to read the first line of the text file. This line contains the
    initial environment of the program that will be created. If you don't like
    the function, feel free to drop it off.

    Example
        >>> line2env('{"zero": 0, "one": 1, "three": 3, "iter": 9}').get('one')
        1
    """
    import json

    env_dict = json.loads(line)
    env_lang = Env()
    for k, v in env_dict.items():
        env_lang.set(k, v)
    return env_lang


def iname2inst(dst, iname: str, op1: str, op2: str):
    inst: Inst
    if iname == "add":
        inst = Add(dst, op1, op2)
    elif iname == "mul":
        inst = Mul(dst, op1, op2)
    elif iname == "lth":
        inst = Lth(dst, op1, op2)
    elif iname == "geq":
        inst = Geq(dst, op1, op2)
    else:
        raise ValueError("unknown inst: {}".format(iname))

    return inst


def file2cfg_and_env(lines):
    """
    Builds a control-flow graph representation for the strings stored in
    `lines`. The first string represents the environment. The other strings
    represent instructions.

    Example:
        >>> l0 = '{"a": 0, "b": 3}'
        >>> l1 = 'bt a 1'
        >>> l2 = 'x = add a b'
        >>> env, prog = file2cfg_and_env([l0, l1, l2])
        >>> interp(prog[0], env).get("x")
        3

        >>> l0 = '{"a": 1, "b": 3, "x": 42, "z": 0}'
        >>> l1 = 'bt a 2'
        >>> l2 = 'x = add a b'
        >>> l3 = 'x = add x z'
        >>> env, prog = file2cfg_and_env([l0, l1, l2, l3])
        >>> interp(prog[0], env).get("x")
        42

        >>> l0 = '{"a": 1, "b": 3, "c": 5}'
        >>> l1 = 'x = add a b'
        >>> l2 = 'x = add x c'
        >>> env, prog = file2cfg_and_env([l0, l1, l2])
        >>> interp(prog[0], env).get("x")
        9
    """
    insts = []

    if 0 == len(lines):
        return (Env(), insts)

    env = line2env(lines[0])

    _id = r"[a-zA-Z_][a-zA-Z0-9_]*"
    _num = r"[0-9]+"
    _bin_op = r"(add|mul|lth|geq)"
    _assignment = rf"({_id})\s*=\s*{_bin_op}\s+({_id})\s+({_id})"
    _branch = rf"(bt)\s+({_id})\s+({_num})"

    pat = re.compile(rf"(?P<assignment>{_assignment})|(?P<bt_expr>{_branch})")

    # This dict maps indices of Bt line occurrence -> line of inst to jump to
    # if the condition is true. It seems this language assumes the false branch
    # is always the next instruction following the 'bt' line
    bt_if_true_children: dict[int, int] = {}

    for idx, ln in enumerate(lines[1:]):

        m = pat.search(ln.strip())

        if not m:
            continue
            # raise ValueError(f"No match for {ln = }")

        if m.group("assignment"):
            dst, iname, op1, op2 = [g for g in m.groups() if g is not None][1:]

            # Instantiate the instruction
            inst = iname2inst(dst, iname, op1, op2)

            # Link a previous existing instruction to the current one
            if len(insts) > 0 and type(insts[-1]) != lang.Bt:
                insts[-1].add_next(inst)

            elif len(insts) > 0 and type(insts[-1]) == lang.Bt:
                # Set false-branch of the last inst (Bt) to the current inst
                insts[-1].nexts[-1] = inst

            insts.append(inst)

        elif m.group("bt_expr"):
            iname, op1, op2 = [g for g in m.groups() if g is not None][1:]

            # We store the line that the branch will jump to if cond is true
            bt_if_true_children[idx] = int(op2)

            # The true-branch will be resolved after all instructions have been
            # instantiated and added to `insts`
            inst = lang.Bt(op1, None, None)

            if len(insts) > 0 and type(insts[-1]) != lang.Bt:
                insts[-1].add_next(inst)

            elif len(insts) > 0 and type(insts[-1]) == lang.Bt:
                # Set false-branch of the last inst (Bt) to the current inst
                insts[-1].nexts[-1] = inst

            insts.append(inst)

    # After all insts have been added to the list, we resolve the jump targets
    # of `bt` insts (only the true branches need this)
    for parent, child in bt_if_true_children.items():
        insts[parent].nexts[0] = insts[child]

    return (env, insts)
