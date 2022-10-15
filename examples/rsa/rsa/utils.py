class RsaTransformations:
    """RSA transformation functions"""

    def trim(x: bytes) -> bytes:
        """Drop the leading `\\x00` bytes"""
        while x and not x[0]:
            x = x[1:]
        return x

    def hex_int(c: str) -> int:
        """Corresponding hex number"""
        n = int(c, 16)
        if n < 0 or n > 15: raise ValueError('Invalid hex digit')
        return n

    def int_hex(n: int) -> str:
        """Corresponding hex digit"""
        if n < 0 or n > 15: raise ValueError('Invalid hex number')
        if n // 10: return chr(n + 87)
        else: return chr(n + 48)

    def bytes2int(bs: bytes) -> int:
        """bytes to int"""
        return int(bs.hex(), 16)

    def int2bytes(num: int) -> bytes:
        """int to bytes"""
        res = ''
        while num:
            res += RsaTransformations.int_hex(num % 16)
            num = num // 16
        if len(res) % 2: res += '0'
        res = bytes.fromhex(res[::-1])
        return res

# -------------------------------------
# --- RSA transformation unit tests ---
# -------------------------------------

Rsa = RsaTransformations

from math import ceil
from secrets import token_bytes

hex_digits = '0123456789abcdef'
assert(all([Rsa.hex_int(x) == i for i, x in enumerate(hex_digits)]))
assert(all([Rsa.int_hex(i) == x for i, x in enumerate(hex_digits)]))

# 1000 random inverses
for n in range(1000):
    if n > 100:
        x = Rsa.trim(token_bytes(ceil(n / 10)))
    else:
      x = Rsa.trim(token_bytes(n))
    x = b'\x01' if x == b'' else x
    if Rsa.int2bytes(Rsa.bytes2int(x)) != x:
        print(f'0: {x}\n\
1: {Rsa.bytes2int(x)}\n\
2: {Rsa.int2bytes(Rsa.bytes2int(x))}')


class Modular:
    """
    Modular inverse

    via Extended Euclidean algorithm
    """

    def sgn(x: int) -> int:
        """Returns sign `+`/`-`"""
        return 1 if x > 0 else -1

    def eea(x: int, y: int) -> "tuple[int, int, int]":
        """Compute the GCD and Bezout coefficients"""
        if x == 0 or y == 0: raise ValueError("EEA only works on nonzero integers")
        cx, cy = Modular.sgn(x), Modular.sgn(y)
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

    def inverse(x: int, n: int) -> int:
        """Inverse of x modulo n using extended Euclidean algorithm"""

        gcd, a, _ = Modular.eea(x, n)
        if gcd != 1:
            raise ValueError(f'{x} does not have an inverse mod {n}')
        else:
            return a % n

# ----------------------------------
# --- Modular inverse unit tests ---
# ----------------------------------

# TODO
