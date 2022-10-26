"""
SHA256 + SHA512 hash functions
"""

from bits import xor
import hashlib

def sha256(s: bytes, n: int = 10_000) -> bytes:
    """sha256 hash function

    returns 32 bytes
    """
    if n < 10_000: n = 10_000
    m = hashlib.sha256()
    curr = s
    while n:
        m.update(curr.hex().encode('utf-8'))
        curr = m.digest()
        n -= 1
    return m.digest()

def sha512(s: bytes, n: int = 10_000) -> bytes:
    """sha512 hash function

    returns 64 bytes
    """
    if n < 10_000: n = 10_000
    m = hashlib.sha512()
    curr = s
    while n:
        m.update(curr.hex().encode('utf-8'))
        curr = m.digest()
        n -= 1
    return m.digest()
