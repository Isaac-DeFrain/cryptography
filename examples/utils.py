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

class Bits:
    """Bit and byte manipulations"""

    def str_to_bits(s: str) -> str:
        """convert string to bits"""
        return ''.join([f'{byte:08b}' for byte in s.encode('utf-8')])

    def xor(a, b) -> str:
        """bitwise xor"""
        _a, _b = str(a), str(b)
        _a, _b = Bits.str_to_bits(_a), Bits.str_to_bits(_b)
        bitxor = lambda x, y, i: str(int(x[i]) ^ int(y[i]))
        min_range = range(0, min(len(_a), len(_b)))
        return ''.join([bitxor(_a, _b, i) for i in min_range])

# ------------------
# --- unit tests ---
# ------------------

# AES tests

_, enc, dec = Aes.make()

for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = token_hex(n)
    assert(dec(enc(x)) == x)

# Bits tests

for x in range(2):
    for y in range(2):
        res = Bits.xor(x, y)
        n = len(res) - 1
        assert(Bits.xor(x, y)[n] == '0' if x == y else Bits.xor(x, y)[n] == '1')

# Hash tests

for _ in range(100):
    n = SystemRandom().randint(2, 100)
    s = token_hex(n)
    assert(Hash.sha256(s) == Hash.sha256(s))
    print(len(Hash.sha256(s)), Hash.sha256(s))
