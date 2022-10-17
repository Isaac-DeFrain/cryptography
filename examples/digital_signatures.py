"""
Digital signatures
"""

from utils import *
from modular import inverse
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

class BasedECC:
    """A elliptic curve and a base point

    - `curve`
    - `base`
    """

    # TODO
    # - Weierstrass
    #   - check discriminant
    def __init__(self, curve: Union[Montgomery, Weierstrass], base: Point):
        self.base = None
        if type(curve) == Weierstrass:
            if Weierstrass.check(curve, base):
                self.base = base
            else:
                try:
                    self.base = Weierstrass.points_n(1)[1]
                except ValueError: ()
            self.curve = curve
        if type(curve) == Montgomery:
            if Montgomery.check(curve, base):
                self.base = base
                self.curve = curve
            else:
                x = SystemRandom.randint(1, n)
                checked = []
                while x not in checked:
                    try:
                        self.base = Montgomery.points_n(1, x)[1]
                    except ValueError: ()

                    checked.append(x)
                    x = (x + 1) % n
                if self.base == None:
                    raise ValueError(f'Only point at infinity... something is wrong with {curve, type(curve)}')

class Key:
    """Elliptic curve key pair generation"""

    def gen(self, bc: BasedECC):
        """Generate a key pair for the curve"""

        gen = SystemRandom()
        a, b, n, base = bc.curve.weierstrass, bc.base
        curve = Weierstrass(a, b, n)
        sk = gen.randint(2, n - 1)
        return sk, curve.scalar_mult(sk, base)

    def __init__(self, bc: BasedECC):
        sk, pk = Key.gen(self, bc)
        self.sk = sk
        self.pk = pk

class ECDSA:
    """Elliptic Curve Digital Signature Algorithm"""

    def __init__(self, curve: BasedECC, key: Key, hash = sha256()):
        self.key = key
        self.hash = hash
        self.base = curve.base
        self.curve = curve.curve

    class Signature:
        """ECDSA signature"""

        def __init__(self, x: int, s: int):
            self.x = x
            self.s = s

    # sign
    def sign(self, msg: str) -> Signature:
        a, b, n = self.curve.weierstrass
        curve = Weierstrass(a, b, n)
        m = self.hash
        m.update(msg.encode('utf-8'))
        h = int(m.hexdigest(), 16) % n
        k = int(token_hex(32), 16) % n
        x, _ = curve.scalar_mult(k, self.base)
        s = (inverse(k, n) * (h + x * self.key.sk)) % n
        return ECDSA.Signature(x, s)

    def sign_msg(self, msg: str) -> tuple[str, Signature]:
        return msg, ECDSA.sign(self, msg)

    # verify
    def verify(self, msg: str, sig: Signature, curve) -> bool:
        x, s = sig.x, sig.x
        a, b, n, base = curve
        curve = Weierstrass(a, b, n)
        m = sha256()
        m.update(msg.encode('utf-8'))
        h = int(m.hexdigest(), 16) % n
        c = inverse(s, n)
        add = Weierstrass.add
        smult = Weierstrass.scalar_mult
        rx, _ = add(smult((h * c) % n, base), smult((x * c) % n, self.key.pk))
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
