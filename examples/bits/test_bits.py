"""
Bits unit tests
"""

import unittest
from bits import xor
from secrets import SystemRandom, token_hex

class TestBits(unittest.TestCase):
    def test_bits(self):
        """1000 random xor tests"""
        for _ in range(1000):
            n = SystemRandom().randint(1, 100)
            x, y = token_hex(n), token_hex(n)
            res = xor(x, y)
            for i in range(n):
                # if ith chars are equal then the corresponding
                # chunk of 8 bits should all be 0's
                if x[i] == y[i]:
                    assert(all([res[8 * i + j] == '0' for j in range(8)]))

if __name__ == '__main__':
    unittest.main()
