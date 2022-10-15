"""
# RSA

influenced by https://github.com/sybrenstuvel/python-rsa
"""

import math
from time import time
from typing import Callable
from secrets import SystemRandom
from base64 import b64encode, b64decode
from rsa.utils import RsaTransformations as Rsa, Modular

# TODO
# PKCS1/PKCS8
# X509 encoded key spec for storing keys on disk

def encrypt(p: int, q: int, pt: bytes, pk: bytes) -> bytes:
    """RSA encryption function

    - `pt`: arbitrary bytes
    - `pk`: base64 endocded
    """
    n = p * q
    m = Rsa.bytes2int(pt)
    e = Rsa.bytes2int(b64decode(pk))
    return Rsa.int2bytes(pow(m, e, n))

def decrypt(p: int, q: int, ct: bytes, sk: bytes) -> bytes:
    """RSA decryption function

    - `ct`: arbitrary bytes
    - `sk`: base64 endocded
    """
    n = p * q
    c = Rsa.bytes2int(ct)
    d = Rsa.bytes2int(b64decode(sk))
    return Rsa.int2bytes(pow(c, d, n))

class Key:
    """RSA key pair generator"""

    def try_inverse(x: int, n: int) -> int:
        """Retry modular inverse until one is found or n is exceeded"""

        if x > n: raise ValueError(f'reduce {x} modulo {n}')
        if x == n: raise ValueError(f'no inverse found')
        try:
            return Modular.inverse(x, n)
        except ValueError:
            Key.try_inverse(x + 1, n)

    def gen(p: int, q: int, *debug) -> 'tuple[bytes, bytes]':
        """
        Generate key pair for modulus n = p * q, where p, q are large primes

        Base64 encoded keys
        """
        phi = (p - 1) * (q - 1)
        sk = None
        start = time()
        while sk == None:
            pk = SystemRandom().randint((p // 2) * (q // 2), phi - 1)
            sk = Key.try_inverse(pk, phi)
        if debug:
            print(f'key gen time: {time() - start}')
            print(f'modulus: {p * q}')
        return b64encode(Rsa.int2bytes(pk)), b64encode(Rsa.int2bytes(sk))

    __all__ = [
        "try_inverse",
        "gen"
    ]

def make(p: int, q: int, *debug) -> 'tuple[int, int, int, Callable[[], tuple[bytes, bytes]], Callable[[bytes], bytes], Callable[[bytes], bytes]]':
    """Make RSA encrypt/decrypt function pair

    returns (`n`, `pk`, `sk`, `gen`, `encrypt`, `decrypt`)
    """
    n = p * q
    if debug: print(f'modulus bytes: {math.ceil(n.bit_length() / 8)}')
    pk, sk = Key.gen(p, q)
    g = lambda: Key.gen(p, q, *debug)
    enc = lambda pt: encrypt(p, q, pt, pk)
    dec = lambda ct: decrypt(p, q, ct, sk)
    return n, pk, sk, g, enc, dec

# TODO convenience method for generating primes

__all__ = [
    "Key",
    "encrypt",
    "decrypt",
    "make",
]

# if __name__ == "__main__":
#     print("Running doctests 1000x or until failure")
#     import doctest

#     for count in range(1000):
#         (failures, tests) = doctest.testmod()
#         if failures:
#             break

#         if count % 100 == 0 and count:
#             print("%i times" % count)

#     print("Doctests done")
