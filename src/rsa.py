# RSA

from utils import *
from math import log
from modular import inverse
from secrets import token_bytes, token_hex

# convert string to int
def str_to_int(s: str) -> int:
    n = 0
    for c in s.encode('utf-8'):
        n = 256 * n + c
    return n

# undo conversion
def int_to_str(x: int) -> str:
    cs = []
    while x:
        cs.append(chr(x % 256))
        x = x // 256
    return ''.join(cs)[::-1]

# p, q primes
# generate key pair for modulus n = p * q
def gen(p: int, q: int):
    n = p * q
    pk = token_hex(int(log(n, 2)))
    sk = inverse(str_to_int(pk), (p - 1) * (q - 1))
    return pk.encode('utf-8'), str(sk).encode('utf-8')

# encryption
# pk is assumed to be utf-8 encoded
def encrypt(p: int, q: int, pt: str, pk: bytes) -> bytes:
    n = p * q
    msg = str_to_int(pt)
    e = str_to_int(pk.decode('utf-8'))
    return bytes(str(pow(msg, e, n)), 'utf-8')

# decryption
# sk is assumed to be utf-8 encoded
def decrypt(p: int, q: int, ct: bytes, sk: bytes) -> str:
    n = p * q
    _ct = int(ct.decode('utf-8'))
    d = str_to_int(sk.decode('utf-8'))
    return int_to_str(pow(_ct, d, n))

# returns the modulus, pub key, secret key, key generator, encryption, and decryption functions
def make(p: int, q: int):
    n = p * q
    pk, sk = gen(p, q)
    g = lambda: gen(p, q)
    enc = lambda pt: encrypt(p, q, pt, pk)
    dec = lambda ct: decrypt(p, q, ct, sk)
    return n, pk, sk, g, enc, dec

# ------------------
# --- unit tests ---
# ------------------

# 1000 random inverses
for _ in range(1000):
    x = token_hex(32)
    assert(int_to_str(str_to_int(x)) == x)

n, pk, sk, g, enc, dec = make(19, 23)
print(enc('hello'))
print(dec(enc('hello')))
