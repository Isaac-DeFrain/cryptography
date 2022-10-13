# RSA

# influenced by https://github.com/sybrenstuvel/python-rsa

import modular
from utils import Rsa
from secrets import SystemRandom, token_bytes
from time import time
from typing import Callable

# TODO
# PKCS1/PKCS8
# X509 encoded key spec for storing keys on disk

class Key:
    def retry_inverse(x: int, n: int) -> int:
        """retry modular inverse until one is found"""
        try:
            return modular.inverse(x, n)
        except ValueError:
            Key.retry_inverse(x + 1, n)

    def gen(p: int, q: int, *debug) -> 'tuple[int, int]':
        """
        generate key pair for modulus n = p * q, p, q primes
        """
        phi = (p - 1) * (q - 1)
        sk = None
        start = time()
        while sk == None:
            pk = SystemRandom().randint((p // 2) * (q // 2), phi - 1)
            sk = Key.retry_inverse(pk, phi)
        if debug != []: print(f'key gen time: {time() - start}')
        return pk, sk

def str2bytes(s: str) -> bytes:
    return s.encode('utf-8')

def bytes2str(bs: bytes) -> str:
    return bs.decode('utf-8')

def encrypt(p: int, q: int, pt: bytes, pk: int) -> bytes:
    n = p * q
    # padded = pad(msg, keylength)
    # payload = bytes2int(padded)
    # e = encrypt(payload, )
    m = Rsa.bytes2int(pt)
    return Rsa.int2bytes(pow(m, pk, n))

def decrypt(p: int, q: int, ct: bytes, sk: int) -> bytes:
    n = p * q
    c = Rsa.bytes2int(ct)
    res = Rsa.int2bytes(pow(c, sk, n))
    return res

def make(p: int, q: int, *debug) -> 'tuple[int, int, int, Callable[[], tuple[int, int]], Callable[[bytes], bytes], Callable[[bytes], str]]':
    """
    returns
    - modulus
    - pub key
    - secret key
    - RSA key pair generator
    - encryption function
    - decryption function
    """
    n = p * q
    print(f'mod: {n}')
    print(f'bits: {n.bit_length()}')
    pk, sk = Key.gen(p, q)
    g = lambda: Key.gen(p, q, *debug)
    enc = lambda pt: encrypt(p, q, pt, pk)
    dec = lambda ct: decrypt(p, q, ct, sk)
    return n, pk, sk, g, enc, dec

# ------------------
# --- unit tests ---
# ------------------

n, pk, sk, g, enc, dec = make(8683317618811886495518194401279999999, 43143988327398957279342419750374600193, [0])

# 1000 random inverses
a, b, c, d = 0, 0, 0, 0
for i in range(1000):
    n = SystemRandom().randint(1, 30)
    x = Rsa.trim(token_bytes(n))
    x = b'\x01' if x == b'' else x
    try:
        ee = enc(x)
        dd = dec(ee)
        if dd == x:
            c += 1
        else:
            d += 1
            print(f'Fail: {x}, {ee}, {dd}')
    except UnicodeDecodeError: a += 1
    except ValueError:
        b += 1
        print(f'ValueError: {x}')

print(f'\
# -------------------------------- #\n\
# --- 1000 Random test results --- #\n\
# -------------------------------- #\n\
  UnicodeDecodeError: {a}\n\
  ValueError:         {b}\n\
  Incorrect:          {d}\n\
  Correct:            {c}\n\
# -------------------------------- #\n\
  Total:              {a + b + c + d}')

# print(enc('00'), dec(enc('00')))
