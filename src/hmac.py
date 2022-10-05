# Hash-based Message Authentication Code

from utils import *

# derive inner key
def inner(x):
    y = '5c' * len(x)
    return y[:len(x)]

# derive outer key
def outer(x):
    y = '36' * len(x)
    return y[:len(x)]

# hmac
# authenticated: msg + hmac(shared_key, msg)
def hmac(shared_key, msg):
    inner_key = xor(inner(shared_key), shared_key)
    outer_key = xor(outer(shared_key), shared_key)
    h = sha256(inner_key + msg)
    return sha256(outer_key + h)

# verify
def verify(shared_key, msg, mac):
    return mac == hmac(shared_key, msg)
