#! /usr/bin python3

# compute the GCD and Bezout coefficients
def eea(r, n):
    c1 = 1 if r > 0 else -1
    c2 = 1 if n > 0 else -1
    r = abs(r)
    n = abs(n)
    def aux(r, n):
        if r > n: aux(n, r)
        if r % n == 0: return n, 0, 1
        gcd, a1, b1 = aux(n % r, r)
        a = b1 - (n // r) * a1
        b = a1
        return gcd, a, b
    gcd, a, b = aux(r, n)
    return gcd, c1 * a, c2 * b

# check the GCD and Bezout coefficients for x, y
def check(a, b, x, y, gcd):
    return gcd == a * x + b * y
