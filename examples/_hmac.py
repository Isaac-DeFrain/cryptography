"""
Hash-based Message Authentication Code
"""

from hashlib import _Hash, sha256, sha512
from utils import Bits

def inner(x):
    """derive inner key"""
    y = '5c' * len(x)
    return y[:len(x)]

def outer(x):
    """derive outer key"""
    y = '36' * len(x)
    return y[:len(x)]

def hmac(shared_key: str, msg: str) -> _Hash:
    """hmac

    authenticated: msg + hmac(shared_key, msg)
    """
    m = sha256()
    inner_key = Bits.xor(inner(shared_key), shared_key)
    outer_key = Bits.xor(outer(shared_key), shared_key)
    h = m.update((inner_key + msg).encode('utf-8'))
    return m.update((outer_key + h).encode('utf-8')).hexdigest()

def verify(shared_key, msg, mac):
    """Verify hmac"""
    return mac == hmac(shared_key, msg)
