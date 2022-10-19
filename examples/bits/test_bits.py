"""
Bits unit tests
"""

import unittest
from bits import *
from secrets import SystemRandom, token_hex

class TestBits(unittest.TestCase):
    def test_bits(self):
        """1000 random xor tests"""
        for _ in range(1000):
            n = SystemRandom().randint(1, 100)
            x, y = token_hex(n), token_hex(n)
            res = xor(x, y)
            assert(all(
                [res[i] == '0' if x[i] == y[i] else res[i] == '1' for i in range(n)]))

if __name__ == '__main__':
    unittest.main()
