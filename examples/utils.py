"""
AES + Hash + Bits + RsaTransformations utils
"""

from Crypto.Cipher import AES
from secrets import token_bytes, token_hex, SystemRandom
from base64 import b64encode, b64decode
from typing import Callable

# AES
class Aes:
    """AES symmetric key cryptosystem

    - block cipher: CBC mode
    - key: 16, 24, 32 bytes
    - block: 16 bytes
    """

    def pad(s: str) -> str:
        """Pad to length multiple of 16"""
        return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    def unpad(s: str) -> str:
        """Drop the encoded number of chars"""
        return s[:-ord(s[len(s) - 1:])]

    def gen(n: int = 32) -> bytes:
        """Generate AES key"""
        return token_bytes(n)

    def encrypt(pt: str, key: bytes) -> bytes:
        """AES encryption function"""
        iv = token_bytes(16)
        aes = AES.new(key, AES.MODE_CBC, iv)
        return b64encode(iv + aes.encrypt(Aes.pad(pt)))

    def decrypt(_ct: bytes, key: bytes) -> str:
        """AES decryption function"""
        ct = b64decode(_ct)
        iv = ct[:16]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return bytes.decode(Aes.unpad(aes.decrypt(ct[16:])))

    def make(key: bytes = gen()) -> "tuple[bytes, Callable[[str], bytes], Callable[[bytes], str]]":
        """Make an encryption/decryption function pair from

        - generated key (default)
        - supplied key

        Returns (`key`, `encrypt`, `decrypt`)
        """
        encrypt = lambda pt: Aes.encrypt(pt, key)
        decrypt = lambda ct: Aes.decrypt(ct, key)
        return key, encrypt, decrypt

# ------------------
# --- unit tests ---
# ------------------

# AES tests

_, enc, dec = Aes.make()

for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = token_hex(n)
    assert(dec(enc(x)) == x)
