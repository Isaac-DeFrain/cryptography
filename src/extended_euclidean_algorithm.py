#! /usr/bin python3

class EEA:
    def sgn(x: int) -> int:
        return 1 if x > 0 else -1

    # compute the GCD and Bezout coefficients
    def eea(x: int, y: int) -> "tuple[int, int, int]":
        if x == 0 or y == 0: raise ValueError("EEA only works on nonzero integers")
        cx, cy = EEA.sgn(x), EEA.sgn(y)
        x, y = abs(x), abs(y)
        def aux(x: int, y: int) -> "tuple[int, int, int]":
            if x > y: aux(y, x)
            if x % y == 0: return y, 0, 1
            gcd1, _a1, _b1 = aux(y % x, x)
            a1 = _b1 - (y // x) * _a1
            b1 = _a1
            return gcd1, a1, b1
        gcd, _a, _b = aux(x, y)
        a = cx * _a
        b = cy * _b
        return gcd, a, b

    # check the GCD and Bezout coefficients for x, y
    def check(a: int, x: int, b: int, y: int, gcd: int) -> bool:
        return gcd == a * x + b * y
