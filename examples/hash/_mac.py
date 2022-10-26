"""
Hash-based Message Authentication Codes
"""

from bits import xor
from hashlib import sha256, sha512
from secrets import token_hex
from typing import Union

def inner_key(x: str) -> str:
    """
    Derive inner key
    """
    y = '5c' * len(x)
    return y[:len(x)]

def outer_key(x: str) -> str:
    """
    Derive outer key
    """
    y = '36' * len(x)
    return y[:len(x)]

class SHA256:
    """
    SHA256-based Message Authentication Code
    """

    def gen_key(self) -> str:
        """
        Generate a key for HMAC-SHA256, 128 hex digits
        """
        return token_hex(128)

    def __init__(self, key: Union[str, None] = None):
        if key:
            self.key = key
        else:
            self.key = self.gen_key()

    def hmac(self, msg: str) -> str:
        """
        SHA256-based message authentication code
        """
        shared_key = self.key
        m = sha256()
        inner = xor(inner_key(shared_key), shared_key)
        outer = xor(outer_key(shared_key), shared_key)
        m.update((inner + msg).encode('utf-8'))
        h = m.hexdigest()
        m.update((outer + h).encode('utf-8'))
        return m.hexdigest()

    def hmac_msg(self, msg: str) -> str:
        """
        `hmac + msg`
        """
        return self.hmac(msg) + msg

    def verify(self, msg: str, mac_msg: str) -> bool:
        """
        Verify hmac
        """
        mac, _msg = mac_msg[:256], mac_msg[256:]
        return mac == self.hmac(msg) and _msg == msg

class SHA512:
    """
    SHA512-based Message Authentication Code
    """

    def gen_key(self) -> str:
        """
        Generate a key for HMAC-SHA512, 256 hex digits
        """
        return token_hex(256)

    def __init__(self, key: Union[str, None] = None):
        if key:
            self.key = key
        else:
            self.key = self.gen_key()

    def hmac(self, msg: str) -> str:
        """
        SHA512-based message authentication code

        `msg + hmac(shared_key, msg)`
        """
        shared_key = self.key
        m = sha512()
        inner = xor(inner_key(shared_key), shared_key)
        outer = xor(outer_key(shared_key), shared_key)
        m.update((inner + msg).encode('utf-8'))
        h = m.hexdigest()
        m.update((outer + h).encode('utf-8'))
        return m.hexdigest()

    def hmac_msg(self, msg: str) -> str:
        """
        `hmac(shared_key, msg) + msg`
        """
        return self.hmac(msg) + msg

    def verify(self, msg: str, mac: str) -> bool:
        """
        Verify hmac
        """
        return mac == self.hmac(msg)
