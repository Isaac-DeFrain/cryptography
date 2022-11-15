"""
Digital signatures
"""

from utils import *
from modular import Mod
from hashlib import sha256
from elliptic_curve import Weierstrass, Montgomery, Point
from secrets import SystemRandom, token_hex
from typing import Annotated, Union

# TODO
# Basic hash-based digital signature

# ECC public knowledge
# - the curve
# - public keys

curve = Annotated[
    tuple[int, int, int, tuple[int, int]],
    'Coefficients, modulus, and base point']

class BasedEC:
    """A elliptic curve and a base point

    - `curve`
    - `base`
    """

    # TODO
    # - Weierstrass
    #   - check discriminant
    def __init__(self, curve: Union[Montgomery, Weierstrass], base: Point):
        self.base = Point(-1, -1)
        if type(curve) == Weierstrass:
            if curve.check(base):
                self.base = base
            else:
                self.base = curve.points_n(1)[1]
            self.curve = curve
        if type(curve) == Montgomery:
            if curve.check(base):
                self.base = base
                self.curve = curve
            else:
                x = SystemRandom().randint(1, n)
                checked = []
                while x not in checked:
                    self.base = curve.points_n(1, x)[1]
                    checked.append(x)
                    x = (x + 1) % n
                if self.base == Point(-1, -1):
                    raise ValueError(f'Only point at infinity... something is wrong with {curve, type(curve)}')

class Key:
    """
    Elliptic curve key pair generation
    """

    def gen(self, bc: BasedEC):
        """
        Generate a key pair for the curve
        """
        gen = SystemRandom()
        a, b, n = bc.curve.form
        base = bc.base
        curve = Weierstrass(a, b, n)
        sk = gen.randint(2, n - 1)
        return sk, curve.scalar_mult(sk, base)

    def __init__(self, bc: BasedEC):
        sk, pk = Key.gen(self, bc)
        self.sk = sk
        self.pk = pk

class ECDSA:
    """
    Elliptic Curve Digital Signature Algorithm
    """

    def __init__(self, curve: BasedEC, key: Key, hash = sha256()):
        self.key = key
        self.hash = hash
        self.base = curve.base
        self.curve = curve.curve

    class Signature:
        """
        ECDSA signature
        """
        def __init__(self, x: int, s: int):
            self.x = x
            self.s = s

    # sign
    def sign(self, msg: str) -> Signature:
        a, b, n = self.curve.form
        if type(self.curve) == Weierstrass:
            curve = Weierstrass(a, b, n)
        else:
            curve = Montgomery(a, b, n)
        m = self.hash
        m.update(msg.encode('utf-8'))
        h = int(m.hexdigest(), 16) % n
        k = int(token_hex(32), 16) % n
        x = curve.scalar_mult(k, self.base).x
        s = (Mod(n).inverse(k) * (h + x * self.key.sk)) % n
        return ECDSA.Signature(x, s)

    def sign_msg(self, msg: str) -> tuple[str, Signature]:
        return msg, ECDSA.sign(self, msg)

    # verify
    def verify(self, msg: str, sig: Signature) -> bool:
        x, s = sig.x, sig.s
        curve = self.curve
        a, b, n = curve.form
        base = self.base
        m = self.hash
        m.update(msg.encode('utf-8'))
        h = int(m.hexdigest(), 16) % n
        c = Mod(n).inverse(s)
        add, smult = curve.add, curve.scalar_mult
        rx = add(smult((h * c) % n, base), smult((x * c) % n, self.key.pk)).x
        return x == rx

# EdDSA (Ed25519)
# Edward's twisted curve
# - Curve25519
# - SHA-512
# - a = 0, b = 0
# - p = 2**255 - 19
# - base = (9, ...)
# - base generates a cyclic subgroup of prime order 2**252 + 27742317777372353535851937790883648493

# Curve25519 is given in Montgomery form
# y**2 = x**3 + 4866612*x**2 + x (mod 2**255 - 19)
curve25519 = (0, 0, 0, 0)

# TODO

# Schnorr

# TODO
