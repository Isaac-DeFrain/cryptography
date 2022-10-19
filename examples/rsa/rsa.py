"""
# RSA
"""

from time import time
from secrets import SystemRandom
from base64 import b64encode, b64decode
from utils import RsaTransformations as Rsa, Modular

# TODO
# PKCS1/PKCS8
# X509 encoded key spec for storing keys on disk

class Cipher:
    """
    RSA cryptosystem
    """

    def __init__(self, **primes):
        # TODO
        if primes['digits']:
            # generate random primes of size `primes['digits']` +- 5%
            ()
        else:
            p, q = primes['p'], primes['q']
            self.p = p
            self.q = q
            self.n = p * q

    def encrypt(self, pt: bytes, pk: bytes) -> bytes:
        """RSA encryption function

        - `pt`: arbitrary bytes
        - `pk`: base64 endocded
        """
        n = self.n
        m = Rsa.bytes2int(pt)
        e = Rsa.bytes2int(b64decode(pk))
        return Rsa.int2bytes(pow(m, e, n))

    def decrypt(self, ct: bytes, sk: bytes) -> bytes:
        """RSA decryption function

        - `ct`: arbitrary bytes
        - `sk`: base64 endocded
        """
        n = self.n
        c = Rsa.bytes2int(ct)
        d = Rsa.bytes2int(b64decode(sk))
        return Rsa.int2bytes(pow(c, d, n))

    class Key:
        """
        RSA key pair generator
        """

        def try_inverse(self, x: int, n: int) -> int:
            """
            Retry modular inverse until one is found or n is exceeded
            """
            if x > n: raise ValueError(f'reduce {x} modulo {n}')
            if x == n: raise ValueError(f'no inverse found')
            try:
                return Modular.inverse(x, n)
            except ValueError:
                self.try_inverse(x + 1, n)

        def gen(self, p: int, q: int, *debug):
            """
            Generate key pair for modulus n = p * q, where p, q are large primes

            Base64 encoded keys
            """
            phi = (p - 1) * (q - 1)
            sk = None
            start = time()
            while sk == None:
                pk = SystemRandom().randint((p // 2) * (q // 2), phi - 1)
                sk = self.try_inverse(pk, phi)
            if debug:
                print(f'key gen time: {time() - start}')
                print(f'modulus: {p * q}')
            self.pk = b64encode(Rsa.int2bytes(pk))
            self.sk = b64encode(Rsa.int2bytes(sk))

        def __init__(self, p: int, q: int, *debug):
            self.gen(p, q, *debug)

# TODO convenience method for generating primes
