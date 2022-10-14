"""
# RSA

* influenced by https://github.com/sybrenstuvel/python-rsa
"""

import math
import modular
from time import time
from utils import RsaTransformations as Rsa
from secrets import SystemRandom, token_bytes
from typing import Callable
from base64 import b64encode, b64decode

# TODO
# PKCS1/PKCS8
# X509 encoded key spec for storing keys on disk

class Key:
    """RSA key key generator"""

    def retry_inverse(x: int, n: int) -> int:
        """Retry modular inverse until one is found"""

        if x >= n: raise ValueError(f'reduce {x} modulo {n}')
        try:
            return modular.inverse(x, n)
        except ValueError:
            Key.retry_inverse(x + 1, n)

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
            sk = Key.retry_inverse(pk, phi)
        if debug:
            print(f'key gen time: {time() - start}')
            print(f'modulus: {p * q}')
        return b64encode(Rsa.int2bytes(pk)), b64encode(Rsa.int2bytes(sk))

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

# ------------------
# --- unit tests ---
# ------------------

import sys

sys.setrecursionlimit(2000)

n, pk, sk, g, enc, dec = make(
    299047036163466364593578671668105626794065326168257844506186760677132120379225668124615386505435634772733711855433506678212683219321934400431853837348621859006132708571197703124787540096917574784669270398109378338035186349072231512072877113120037670314261590067246212799116837416098173423817299815147,
    196763460946331349352499186611298628881243819903022496947907288526248422121851804346103094757867302222609503531023139472071798569335158505187945748246438168058674072267295382468467831591298752055972131783828041051056215358125513302847552420440611465989162677681036110999725853317071074438332295580687,
    [0])

# 1000 random inverses
num_test = 100
a, b, c, d = 0, 0, 0, 0
start = time()
for _ in range(num_test):
    l = SystemRandom().randint(1, min(100, math.ceil(n.bit_length() / 8)))
    x = Rsa.trim(token_bytes(l))
    x = b'\x01' if x == b'' else x
    try:
        ee = enc(x)
        dd = dec(ee)
        if dd == x:
            c += 1
        else:
            d += 1
            print(f'Fail:\n\
- {l}\n\
- {x.hex()}\n\
- {ee.hex()}\n\
- {dd.hex()}')
    except UnicodeDecodeError: a += 1
    except ValueError:
        b += 1
        print(f'ValueError: {x}')

print(f'** Test run time: {time() - start}')
if c == num_test: print('** All encrypt/decrypt tests passed!')
else: print(f'\
# -------------------------------- #\n\
# --- 1000 Random test results --- #\n\
# -------------------------------- #\n\
  UnicodeDecodeError: {a}\n\
  ValueError:         {b}\n\
  Incorrect:          {d}\n\
  Correct:            {c}\n\
# -------------------------------- #\n\
  Total:              {a + b + c + d}')
