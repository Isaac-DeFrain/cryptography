#!/usr/bin python3

from modular import inverse

# check that y^2 = x^3 + a * x + b (mod n)
def _check(x, y, a, b, n):
    return y ** 2 % n == (x ** 3 + a * x + b) % n

# y^2 = f(x) (mod n) where
#   f(x) = x^3 + a * x + b
def _compute_f(x, a, b, n):
    return (x ** 3 + a * x + b) % n

# solve x^2 = a (mod n) for x
# returns all solutions in a list
def _sqrt(a, n):
    res = []
    for x in range(0, n):
        if x ** 2 % n == a % n: res.append(x)
    return res

# return the list of all points on the elliptic curve over 𝐙/n𝐙
# print length
def _points(a, b, n):
    check = lambda x, y: _check(x, y, a, b, n)
    pts = [(-1, -1)]
    for y in range(0, n):
        for x in range(0, n):
            if check(x, y): pts.append((x, y))
    print('+-----------------------------------------------')
    print(f'+ Points of y^2 = x^3 + {a}x + {b} (mod {n})')
    print('+ Note: (-1, -1) represents point at infinity')
    print('+-----------------------------------------------')
    print(f'+ {pts.__len__()} points over 𝐙/{n}𝐙')
    return sorted(pts)

# ECC arithmetic
# note: b does not affect addition
def _add(p, q, a, n):
    # coordinates
    x1, y1 = p
    x2, y2 = q
    # identity and inverse rules
    if x1 == x2 and y1 == -y2: return (-1, -1)
    if p == (-1, -1): return q
    if q == (-1, -1): return p
    # otherwise
    lam = ((3 * x1 ** 2 + a) * inverse(2 * y1, n)
        if p == q else (y2 - y1) * inverse(x2 - x1, n))
    x3 = (lam ** 2 - x1 - x2) % n
    y3 = (lam * (x1 - x3) - y1) % n
    return x3, y3

def _scalar_mult(k, p, a, n):
    if k == 0: return (-1, -1)
    if k == 1: return p
    if k > 1: return _add(p, _scalar_mult(k - 1, p, a, n), a, n)
    else: raise Exception

# functions for working with the elliptic curve:
#   y^2 = x^3 + ax + b (mod n)
def make(a, b, n):
    check = lambda x, y: _check(x, y, a, b, n)
    compute_f = lambda x: _compute_f(x, a, b, n)
    sqrt = lambda a: _sqrt(a, n)
    points = lambda: _points(a, b, n)
    add = lambda p, q: _add(p, q, a, n)
    scalar_mult = lambda k, p: _scalar_mult(k, p, a, n)
    return check, compute_f, sqrt, points, add, scalar_mult
