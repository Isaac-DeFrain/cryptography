from Crypto.Cipher import AES
from secrets import token_bytes, token_hex, SystemRandom
from base64 import b64encode, b64decode
from typing import Callable

# AES
class Aes:
    # key: 16, 24, 32 bytes
    # block: 16 bytes

    # padding
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    # generate key (default 32 bytes)
    def gen(*n: int):
        if len(n) == 0: return token_bytes(32)
        else: return token_bytes(n[0])

    # encryption
    def encrypt(pt: str, key: bytes) -> bytes:
        iv = token_bytes(16)
        aes = AES.new(key, AES.MODE_CBC, iv)
        return b64encode(iv + aes.encrypt(Aes.pad(pt)))

    # decryption
    def decrypt(_ct: bytes, key: bytes) -> str:
        ct = b64decode(_ct)
        iv = ct[:16]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return bytes.decode(Aes.unpad(aes.decrypt(ct[16:])))

    # make an encryption/decryption pair
    # - from a generated key
    # - from a supplied key
    def make(*k: bytes) -> "tuple[bytes, Callable[[str], bytes], Callable[[bytes], str]]":
        if len(k) == 0: key = Aes.gen()
        else: key = k[0]
        encrypt = lambda pt: Aes.encrypt(pt, key)
        decrypt = lambda ct: Aes.decrypt(ct, key)
        return key, encrypt, decrypt

class Hash:
    # SHA256
    # returns first min(n, 32) chars of hash as hex string if n != 0 else 32
    def sha256(s: str, *_n: int) -> str:
        if len(_n) == 0 or _n[0] < 10_000: n = 10_000
        else: n = _n[0]
        import hashlib
        m = hashlib.sha256()
        m.update(s.encode('utf-8'))
        if n == 0: return m.hexdigest()[32:]
        else: Hash.sha256(m.hexdigest(), n - 1)

    # SHA512
    # returns first min(n, 64) chars of hash as hex string if n != 0 else 64
    def sha512(s: str, *_n: int) -> str:
        if len(_n) == 0 or _n[0] < 10_000: n = 10_000
        else: n = _n[0]
        import hashlib
        m = hashlib.sha512()
        m.update(s.encode('utf-8'))
        if n == 0: return m.hexdigest()[64:]
        else: Hash.sha512(m.hexdigest(), n - 1)

class Bits:
    # convert string to bits
    def str_to_bits(s: str) -> str:
        return ''.join([f'{byte:08b}' for byte in s.encode('utf-8')])

    # undo the conversion
    def bits_to_str(b: str) -> str:
        group = False
        count = 0
        max_count = 1
        rem = b
        acc = []
        while rem:
            chk = rem[:8]
            rem = rem[8:]
            count += 1
            if chk[0] == '0': group = False
            if chk[:3] == '110':
                group = True
                max_count = 2
            elif chk[:4] == '1110':
                group = True
                max_count = 3
            elif chk[:5] == '11110':
                group = True
                max_count = 4
                print(max_count)
            while group:
                if count > max_count: raise ValueError('UTF8 only has byte groups up to length 4')
                elif chk[:2] == '10':
                    group = True
                    count += 1
                    chk += rem[:8]
                    rem = rem[8:]
                else:
                    group = False
                    count = 0
            acc.append(chk)
        return ''.join([chr(int(chk, 2)) for chk in acc])

    def xor(a, b) -> str:
        """bitwise xor"""
        _a, _b = str(a), str(b)
        _a, _b = Bits.str_to_bits(_a), Bits.str_to_bits(_b)
        bitxor = lambda x, y, i: str(int(x[i]) ^ int(y[i]))
        min_range = range(0, min(len(_a), len(_b)))
        return ''.join([bitxor(_a, _b, i) for i in min_range])

class RsaTransformations:
    """Rsa transformation functions"""

    def trim(x: bytes) -> bytes:
        while not x[0]:
            x = x[1:]
            if x == b'': break
        return x

    def hex_int(c: str) -> int:
        return int(c, 16)

    def int_hex(n: int) -> str:
        if n // 10: return chr(n + 87)
        else: return chr(n + 48)

    def bytes2int(bs: bytes) -> int:
        """raw bytes to int"""
        return int(bs.hex(), 16)

    def int2bytes(num: int) -> bytes:
        """int to raw bytes"""
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

# TODO

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

# 1000 random inverses
for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = token_hex(n)
    assert(Bits.bits_to_str(Bits.str_to_bits(x)) == x)

# 1000 random inverses
for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = token_hex(n)
    f = lambda x: x.encode('utf-8').hex()
    g = lambda x: bytes.fromhex(x).decode('utf-8')
    assert(g(f(x)) == x)
