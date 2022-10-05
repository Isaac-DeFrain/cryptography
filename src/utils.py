import hashlib
from os import urandom
from Crypto.Cipher import AES
# from Crypto import Random
from base64 import b64encode, b64decode

# AES
# key: 16, 24, 32 bytes
# block: 16 bytes

# padding
pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# encryption
def encrypt(pt):
    key = urandom(32)
    iv = urandom(16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return key, b64encode(iv + aes.encrypt(pad(pt)))

# decryption
def decrypt(_ct, key):
    ct = b64decode(_ct)
    iv = ct[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return bytes.decode(unpad(aes.decrypt(ct[16:])))

# SHA256
# returns first 32 chars of hash as hex string
def sha256(s, *_n: int):
    n = _n[0]
    if n < 0: raise ValueError('sha256 can only be applied a positive number of times')
    m = hashlib.sha256()
    m.update(bytes(str(s), 'utf-8'))
    if n == 0: return m.hexdigest()[32:]
    else: sha256(m.hexdigest(), n - 1)

# convert string to bits
def str_to_bits(s):
    res = [bin(byte)[2:] for byte in bytes(str(s), 'utf-8')]
    return ''.join(res)

# xor
# convert -> str -> bits
# xor each bit
def xor(a, b):
    _a, _b = str(a), str(b)
    _a, _b = str_to_bits(_a), str_to_bits(_b)
    res = [str(int(_a[i]) ^ int(_b[i])) for i in range(0, min(len(_a), len(_b)))]
    return ''.join(res)

