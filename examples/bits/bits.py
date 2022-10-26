"""
Bit manipulations
"""

def bits2str(raw_bits: str) -> str:
    diff = 8 - (len(raw_bits) % 8)
    bits = '0' * diff + raw_bits
    res = ''
    while bits:
        byte_bits = bits[:8]
        bits = bits[8:]
        res += chr(int(byte_bits, 2))
    return res

def str2bits(s: str) -> str:
    """
    Convert string to bits
    """
    return ''.join([f'{byte:08b}' for byte in s.encode('utf-8')])

def xor(a: str, b: str) -> str:
    """
    Bitwise xor
    """
    a, b = str2bits(a), str2bits(b)
    bitxor = lambda x, y, i: str(int(x[i]) ^ int(y[i]))
    min_range = range(0, min(len(a), len(b)))
    return ''.join([bitxor(a, b, i) for i in min_range])
