#! /usr/bin python3

def sgn(x): 1 if x > 0 else -1

# compute the GCD and Bezout coefficients
def eea(x, y):
    if x == 0 or y == 0: raise ValueError("EEA only works on nonzero integers")
    cx, cy = sgn(x), sgn(y)
    x, y = abs(x), abs(y)
    def aux(x, y):
        if x > y: aux(y, x)
        if x % y == 0: return y, 0, 1
        gcd, _a, _b = aux(y % x, x)
        a = _b - (y // x) * _a
        b = _a
        return gcd, a, b
    gcd, _a, _b = aux(x, y)
    a = cx * _a
    b = cy * _b
    return gcd, a, b

# check the GCD and Bezout coefficients for x, y
def check(a, x, b, y, gcd):
    return gcd == a * x + b * y
