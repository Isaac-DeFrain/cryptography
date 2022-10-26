from math import ceil, floor, sqrt, log
from random import SystemRandom
from time import time
from secrets import token_bytes, choice

class RsaTransformations:
    """
    RSA transformation functions
    """

    def trim(self, x: bytes) -> bytes:
        """Drop the leading `\\x00` bytes"""
        while x and not x[0]:
            x = x[1:]
        return x

    def hex_int(self, c: str) -> int:
        """
        Corresponding hex number
        """
        try: n = int(c, 16)
        except ValueError: n = -1
        return n

    def int_hex(self, n: int) -> str:
        """
        Corresponding hex digit
        """
        if n < 0 or n > 15: raise ValueError('Invalid hex number')
        if n // 10: return chr(n + 87)
        else: return chr(n + 48)

    def bytes2int(self, bs: bytes) -> int:
        """
        `bytes` to `int`
        """
        return int(bs.hex(), 16)

    def int2bytes(self, num: int) -> bytes:
        """
        `int` to `bytes`
        """
        res = ''
        while num:
            res += self.int_hex(num % 16)
            num = num // 16
        if len(res) % 2: res += '0'
        res = bytes.fromhex(res[::-1])
        return res

class Modular:
    """
    Modular inverses via Extended Euclidean algorithm
    """

    def __sgn(self, x: int) -> int:
        """
        Returns sign `+`/`-`
        """
        return 1 if x > 0 else -1

    def eea(self, x: int, y: int) -> tuple[int, int, int]:
        """
        Compute the `gcd` and Bezout coefficients
        `a`, `b` s.t. `gcd = a*x + b*y`
        """
        if x == 0 or y == 0: raise ValueError('EEA only works on nonzero integers')
        cx, cy = self.__sgn(x), self.__sgn(y)
        x, y = abs(x), abs(y)
        def aux(x: int, y: int) -> tuple[int, int, int]:
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

    def inverse(self, x: int, n: int) -> int:
        """
        Inverse of `x` modulo `n` using extended Euclidean algorithm
        """
        gcd, a, _ = self.eea(x, n)
        if gcd != 1:
            print(f'{x} does not have an inverse mod {n}')
            return 0
        else:
            return a % n

class Prime:
    """
    Functionalities for generating primes via Miller-Rabin
    """

    def gen_bits(self, num_bits: int) -> str:
        """
        Generate a (mostly) random bit string of length `self.num_bits + 2`
        representing an odd int with at least `num_bits` significant bits
        """
        n = max(ceil(num_bits / 8), 1)
        # ensure: odd + sufficiently many bits
        bits = ''.join([f'{b:08b}' for b in token_bytes(n)])
        bits = f'1{bits}1'
        return bits

    def __rs(self) -> tuple[int, int]:
        """
        Generate Miller-Rabin values: `r`, `s`
        """
        m = self.p - 1
        r = m
        s = 0
        while m % 2 == 0:
            m = m // 2
            s *= 2
            r = m
        return r, s

    def miller_rabin_primality_test(self) -> bool:
        """
        Miller-Rabin primality test, detects (most) composite numbers quickly
        """
        p = self.p
        a = choice(range(1, p))
        r, s = self.__rs()
        if pow(a, r, p) == 1 or any([pow(a, 2**j * r, p) == p - 1 for j in range(0, s)]):
            return True
        else:
            return False

    def naive_primality_test(self) -> bool:
        """
        Naive primality test
        """
        p = self.p
        for k in filter(lambda x: x == 5 or x % 5, range(3, ceil(sqrt(p)), 2)):
            if not p % k: return False
        return True

    def __check(self, limit: float, debug: bool) -> int:
        """
        Attempt to generate a prime number `p`
        such that `p.bit_length() >= self.num_bits`
        """
        start = time()
        incrs = 0
        round = self.rounds
        while time() - start < limit :
            if not round:
                round = self.rounds
                incrs += 1
                self.p += 2
                if not self.p % 5:
                    incrs += 1
                    self.p += 2
            if self.miller_rabin_primality_test():
                if self.naive_primality_test():
                    if debug: print(f'Execution time: {time() - start} sec')
                    return self.p
            round -= 1
        return 0

    def __init__(self, num_bits: int, time_limit: int = 60, debug: bool = False):
        """
        Initialize a prime number with at least `num_bits` significant bits.
        Give up after `time_limit` sec.
        """
        self.num_bits = num_bits
        self.rounds = max(num_bits // 2, 1)
        self.bits = self.gen_bits(num_bits)
        self.p = int(self.bits, 2)
        if self.__check(time_limit, debug) == 0:
            raise ValueError(f'Exceeded time limit before finding >= {num_bits}-bit prime. Consider increasing the time limit.')

# ------------------
# --- Unit tests ---
# ------------------

# -----------
# --- Rsa ---
# -----------

Rsa = RsaTransformations()

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
    x = b'\x01' + x
    assert(Rsa.int2bytes(Rsa.bytes2int(x)) == x)

# ---------------
# --- Modular ---
# ---------------

# 1000 random inverse tests
for _ in range (1000):
    n = 0
    while not n % 2:
        n = SystemRandom().randint(100, 10000)
    # n is odd => n is not divisible by 2
    m = floor(log(n, 2))
    # x == 2**k < n
    x = pow(2, SystemRandom().randint(1, m))
    a = Modular().inverse(x, n)
    assert(x * a % n == 1)

# --------------
# --- Primes ---
# --------------

# double check that `Prime`s are actually prime even
# though that should be obvious from their generation
# only checking small primes 12-27 bits
for _ in range(1000):
    n = choice(range(10, 25))
    p = Prime(n, 10)
    for k in range(2, ceil(sqrt(p.p))):
        if not p.p % k: assert False
