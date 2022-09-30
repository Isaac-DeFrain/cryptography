#!/usr/bin python3

# solve x^2 = a (mod n) for x
def _sqrt(a, n):
    res = []
    for x in range(0, n):
        if x ** 2 % n == a % n: res.append(x)
    return res

# working with the elliptic curve:
#   y^2 = x^3 + ax + b (mod n)
def make(a, b, n):
    check = lambda x, y: y ** 2 % n == (x ** 3 + a * x + b) % n
    rhs = lambda x: (x ** 3 + a * x + b) % n
    sqrt = lambda a: _sqrt(a, n)
    return check, rhs, sqrt

# return the list of all points on the elliptic curve over 𝐙/n𝐙
# (-1, -1) is used in place of the point at infinity
def points(a, b, n):
    check = lambda x, y: y ** 2 % n == (x ** 3 + a * x + b) % n
    pts = [(-1, -1)]
    for y in range(0, n):
        for x in range(0, n):
            if check(x, y): pts.append((x, y))
    return sorted(pts)
