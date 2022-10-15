#!/usr/bin python3

from utils import *
from elliptic_curve import *
from secrets import SystemRandom, token_bytes

# TODO
# Basic hash-based digital signature

# ECC public knowledge
# - the curve
# - public keys

# generate a key pair (sk, pk) for the curve
def gen_ecc_pair(curve):
    gen = SystemRandom()
    a, b, n, base = curve
    _, _, _, _, _, smult = make(a, b, n)
    sk = gen.randint(2, n - 1)
    return sk, smult(sk, base)

# ECDSA
# elliptic curve digital signature algorithm

# sign
def ecdsa_sign(msg, sk, curve):
    a, b, n, base = curve
    _, _, _, _, _, scalar_mult = make(a, b, n)
    _h = sha256(msg)
    h = int(str_to_bits(_h), base = 2) % n
    k = int(str_to_bits(token_bytes(n)[16:]), base = 2) % n
    r, _ = scalar_mult(k, base)
    s = (inverse(k, n) * (h + r * int(sk))) % n
    return r, s

# verify
def ecdsa_verify(msg, sig, _pk, curve):
    rcvd_r, s = sig
    a, b, n, base = curve
    _, _, _, _, add, smult = make(a, b, n)
    _h = sha256(msg)
    h = int(str_to_bits(_h), base = 2) % n
    c = inverse(s, n)
    rx, _ = add(smult((h * c) % n, base), smult((rcvd_r * c) % n, _pk))
    return rcvd_r == rx

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
