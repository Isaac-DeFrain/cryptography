"""
AES + Hash + Bits + RsaTransformations utils
"""

from Crypto.Cipher import AES
from secrets import token_bytes, token_hex, SystemRandom
from base64 import b64encode, b64decode

# AES
class Aes:
    """AES symmetric key cryptosystem

    - block cipher: CBC mode
    - key: 16, 24, 32 bytes
    - block: 16 bytes
    """

    def pad(self, s: str) -> str:
        """
        Pad to length multiple of 16
        """
        return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    def unpad(self, s: str) -> str:
        """
        Drop the encoded number of chars
        """
        return s[:-ord(s[len(s) - 1:])]

    def gen(self, n: int = 32) -> bytes:
        """
        Generate AES key
        """
        return token_bytes(n)

    def encrypt(self, pt: str) -> bytes:
        """
        AES encryption function
        """
        iv = token_bytes(16)
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + aes.encrypt(self.pad(pt)))

    def decrypt(self, _ct: bytes) -> str:
        """
        AES decryption function
        """
        ct = b64decode(_ct)
        iv = ct[:16]
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(aes.decrypt(ct[16:]))

    def __init__(self, key: bytes = b''):
        if not key:
            key = self.gen()
        self.key = key

# ------------------
# --- unit tests ---
# ------------------

# AES tests

aes = Aes()
for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = token_hex(n)
    assert(aes.decrypt(aes.encrypt(x)) == x)
