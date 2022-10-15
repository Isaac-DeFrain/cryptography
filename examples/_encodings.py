"""
Encodings
"""

from base64 import b64encode, b64decode
from secrets import SystemRandom, token_hex, token_bytes

# ASCII
# 128 chars represented by 7 bits
# range: \u0000 - \u007F

u0000 = '\u0000'.isascii()
u007F = '\u007F'.isascii()

assert(u0000 and u007F and not '\u0080'.isascii())

whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation + whitespace

def make_bit_chunk_list(s: str):
    return [f'{ord(i):08b}' for i in s]

def make_bit_seq(s: str) -> str:
    if not s.isascii():
        raise ValueError('ASCII only allowed')
    return ' '.join(f'{ord(i):08b}' for i in s)

def make_bit_chunk_list_var_len(s: str):
    return [f'{ord(i):b}' for i in s]

# printable ascii chars are represented by <= 7 bits
assert(all([x[0] == '0' for x in make_bit_chunk_list(printable)]))
assert(all([len(x) <= 7 for x in make_bit_chunk_list_var_len(printable)]))

# UTF-8
# all unicode chars represented by 1-4 bytes
# - \u0000 - \uFFFF
# - \u007FFF - \u07FFFF
# ascii is embedded in 1 byte representations

# equivalently
# all printable ASCII chars start with 0 in UTF-8
assert(
    list(filter(
        lambda x: not x[0] == '0',
        make_bit_chunk_list(printable))) == []
)

# ranges of unicode chars

assert(len([chr(x) for x in '\u0000'  .encode('utf-8')]) == 1)
assert(len([chr(x) for x in '\u007F'  .encode('utf-8')]) == 1)
assert(len([chr(x) for x in '\u0080'  .encode('utf-8')]) == 2)
assert(len([chr(x) for x in '\u07FF'  .encode('utf-8')]) == 2)
assert(len([chr(x) for x in '\u0800'  .encode('utf-8')]) == 3)
assert(len([chr(x) for x in '\u007FFF'.encode('utf-8')]) == 3)
assert(len([chr(x) for x in '\u008000'.encode('utf-8')]) == 4)
assert(len([chr(x) for x in '\u07FFFF'.encode('utf-8')]) == 4)
assert(len([chr(x) for x in '\u080000'.encode('utf-8')]) == 5)

# 1000 random inverses
for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = token_hex(n)
    f = lambda x: x.encode('utf-8')
    g = lambda x: x.decode('utf-8')
    assert(g(f(x)) == x)
    assert(len(f(x).hex()) == 2 * len(x))

# Base64

def b64_enc(s: str) -> str:
    return str(b64encode(s.encode('utf-8')), 'utf-8')

def b64_dec(s: str) -> str:
    return str(b64decode(s), 'utf-8')

# 1000 random inverses
for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = token_hex(n)
    assert(b64_dec(b64_enc(x)) == x)

for _ in range(1000):
    n = SystemRandom().randint(1, 100)
    x = token_bytes(n)
    assert(b64decode(b64encode(x)) == x)
