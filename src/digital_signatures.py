#!/usr/bin python3

from utils import *
from elliptic_curve import *

# TODO
# Basic hash-based digital signature

# ECC public knowledge
# - the curve
# - public keys

# public key from private key + curve
def pk(sk, curve):
    a, b, n, base = curve
    _, _, _, _, _, smult = make(a, b, n)
    return smult(sk % n, base)

# ECDSA

def ecdsa_sign(msg, sk, curve):
    a, b, n, base = curve
    _, _, _, _, _, scalar_mult = make(a, b, n)
    _h = sha256(msg)
    h = int(str_to_bits(_h), base = 2) % n
    k = int(str_to_bits(urandom(n)[16:]), base = 2) % n
    r, _ = scalar_mult(k, base)
    s = (inverse(k, n) * (h + r * int(sk))) % n
    return r, s

def ecdsa_verify(msg, sig, _pk, curve):
    rcvd_r, s = sig
    a, b, n, base = curve
    _, _, _, _, add, smult = make(a, b, n)
    _h = sha256(msg)
    h = int(str_to_bits(_h), base = 2) % n
    c = inverse(s, n)
    rx, _ = add(smult((h * c) % n, base), smult((rcvd_r * c) % n, _pk))
    return rcvd_r == rx

# EdDSA

# TODO

# Schnorr

# TODO
