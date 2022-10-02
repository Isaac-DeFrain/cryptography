#!/usr/bin python3

import hashlib
from elliptic_curve import *
from os import urandom
from Crypto.Cipher import AES
# from Crypto import Random
from base64 import b64encode, b64decode


# AES
# key: 16, 24, 32 bytes
# block: 16 bytes

# padding
pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# encryption
def encrypt(pt):
    key = urandom(32)
    iv = urandom(16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return key, b64encode(iv + aes.encrypt(pad(pt)))

# decryption
def decrypt(_ct, key):
    ct = b64decode(_ct)
    iv = ct[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return bytes.decode(unpad(aes.decrypt(ct[16:])))

# SHA256
# returns first 32 chars of hash as hex string
def sha256(s):
    m = hashlib.sha256()
    m.update(bytes(str(s), encoding = 'utf-8'))
    return m.hexdigest()[32:]

# convert string to bits
def str_to_bits(s):
    res = ''
    for x in [bin(byte)[2:] for byte in bytes(str(s), "utf-8")]:
      res += x
    return res

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
