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

class Hash:
    """sha256 + sha512 hash functions"""

    import hashlib

    def sha256(s: bytes, n: int = 10_000) -> bytes:
        """sha256 hash function

        returns 32 bytes
        """
        if n < 10_000: n = 10_000
        m = Hash.hashlib.sha256()
        m.update(s.encode('utf-8'))
        return m.digest()[32:]

    def sha512(s: str, n: int = 10_000) -> bytes:
        """sha512 hash function

        returns 64 bytes
        """
        if n < 10_000: n = 10_000
        m = Hash.hashlib.sha512()
        m.update(s.encode('utf-8'))
        return m.hexdigest()[128:]

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

class RsaTransformations:
    """RSA transformation functions"""

    def trim(x: bytes) -> bytes:
        """Drop the leading `\\x00` bytes"""
        while x and not x[0]:
            x = x[1:]
        return x

    def hex_int(c: str) -> int:
        """Corresponding hex number"""
        if n < 0 or n > 15: raise ValueError('Invalid hex digit')
        return int(c, 16)

    def int_hex(n: int) -> str:
        """Corresponding hex digit"""
        if n < 0 or n > 15: raise ValueError('Invalid hex number')
        if n // 10: return chr(n + 87)
        else: return chr(n + 48)

    def bytes2int(bs: bytes) -> int:
        """bytes to int"""
        return int(bs.hex(), 16)

    def int2bytes(num: int) -> bytes:
        """int to bytes"""
        res = ''
        while num:
            res += RsaTransformations.int_hex(num % 16)
            num = num // 16
        if len(res) % 2: res += '0'
        res = bytes.fromhex(res[::-1])
        return res

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

# RSA tests

Rsa = RsaTransformations

hex_digits = '0123456789abcdef'
assert(all([Rsa.hex_int(x) == i for i, x in enumerate(hex_digits)]))
assert(all([Rsa.int_hex(i) == x for i, x in enumerate(hex_digits)]))

# 1000 random inverses
for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = Rsa.trim(token_bytes(n))
    x = b'\x01' if x == b'' else x
    if Rsa.int2bytes(Rsa.bytes2int(x)) != x:
        print(f'0: {x}\n\
1: {Rsa.bytes2int(x)}\n\
2: {Rsa.int2bytes(Rsa.bytes2int(x))}')
