from Crypto.Cipher import AES
from secrets import token_bytes, token_hex
from base64 import b64encode, b64decode

# AES
# key: 16, 24, 32 bytes
# block: 16 bytes

# padding
pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# generate key (default 32 bytes)
def gen(*n: int):
    if len(n) == 0: return token_bytes(32)
    return token_bytes(n[0])

# encryption
def encrypt(pt: str, key: bytes):
    iv = token_bytes(16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return key, b64encode(iv + aes.encrypt(pad(pt)))

# decryption
def decrypt(_ct, key):
    ct = b64decode(_ct)
    iv = ct[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return bytes.decode(unpad(aes.decrypt(ct[16:])))

# make an encryption/decryption pair
# - from a generated key
# - from a supplied key
def make(*k):
    if len(k) == 0: key = gen()
    else: key = k[0]
    enc = lambda pt: encrypt(pt, key)
    dec = lambda ct: decrypt(ct, key)
    return key, enc, dec

# SHA256
# returns first min(n, 32) chars of hash as hex string if n != 0 else 32
def sha256(s: str, *_n: int) -> str:
    if len(_n) == 0 or _n[0] < 10_000: n = 10_000
    else: n = _n[0]
    import hashlib
    m = hashlib.sha256()
    m.update(s.encode('utf-8'))
    if n == 0: return m.hexdigest()[32:]
    else: sha256(m.hexdigest(), n - 1)

# SHA512
# returns first min(n, 64) chars of hash as hex string if n != 0 else 64
def sha512(s: str, *_n: int) -> str:
    if len(_n) == 0 or _n[0] < 10_000: n = 10_000
    else: n = _n[0]
    import hashlib
    m = hashlib.sha512()
    m.update(s.encode('utf-8'))
    if n == 0: return m.hexdigest()[64:]
    else: sha512(m.hexdigest(), n - 1)

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

# xor
# convert -> str -> bits
# xor corresponding bits
def xor(a, b) -> str:
    _a, _b = str(a), str(b)
    _a, _b = str_to_bits(_a), str_to_bits(_b)
    bitxor = lambda x, y, i: str(int(x[i]) ^ int(y[i]))
    min_range = range(0, min(len(_a), len(_b)))
    return ''.join([bitxor(_a, _b, i) for i in min_range])

# ------------------
# --- unit tests ---
# ------------------

# 1000 random inverses
for _ in range(1000):
    x = token_hex(32)
    assert(bits_to_str(str_to_bits(x)) == x)
