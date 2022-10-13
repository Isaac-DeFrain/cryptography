#! /usr/bin python3

from typing import Callable

# modular arithmetic

# check if x is a unit in Z/nZ
def is_unit(x: int, n: int) -> bool:
    res = False
    for y in range(1, n):
        if (x * y) % n == 1:
            res = True
            break
    return res

# list of all units of Z/nZ
def all_units(n: int):
    return list(filter(lambda x: is_unit(x, n), range(1, n)))

# inverse of x modulo n
def inverse(x: int, n: int) -> int:
    res = None
    for y in range(1, n):
        if (x * y) % n == 1:
            res = y
            break
    return res

# order of an element in Z/nZ
def order(x: int, n: int) -> int:
    res = 0
    for p in range(1, n):
        if pow(x, p, n) == 1:
            res = p
            break
    return res

# order of the group generated by x, <x>
def generated_group(x: int, n: int) -> "list[int]":
    group = [x]
    for p in range(2, n):
        y = pow(x, p, n)
        if not group.__contains__(y):
            group.append(y)
    return group

# order of <x> = oder of x in Z/nZ
def check(x: int, n: int) -> bool:
    if not is_unit(x, n):
        raise ValueError(f'{x} is not a unit of Z/{n}Z')
    return order(x, n) == len(generated_group(x, n))

# returns all functions for fixed n
def make(n: int) -> "tuple[Callable[[int], bool], Callable[[], list[int]], Callable[[int], int], Callable[[int], int], Callable[[int], list[int]], Callable[[int], bool]]":
    _is_unit = lambda x: is_unit(x, n)
    _all_units = lambda: all_units(n)
    _inverse = lambda x: inverse(x, n)
    _order = lambda x: order(x, n)
    _gen_group = lambda x: generated_group(x, n)
    _check = lambda x: check(x, n)
    return _is_unit, _all_units, _inverse, _order, _gen_group, _check
