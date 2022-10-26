"""
Hash unit tests
"""

import unittest
from _hash import sha256, sha512
from secrets import SystemRandom, token_bytes

class TestSha256(unittest.TestCase):
    def test_sha256(self):
        """1000 random sha256 tests"""
        for _ in range(100):
            n = SystemRandom().choice([32, 64, 96, 128, 160, 192, 224, 256])
            msg = token_bytes(n)
            assert(len(sha256(msg)) == 32)
            assert(sha256(msg) == sha256(msg))

class TestSha512(unittest.TestCase):
    def test_sha512(self):
        """1000 random sha512 hmac tests"""
        for _ in range(100):
            n = SystemRandom().choice([64, 128, 192, 256])
            msg = token_bytes(n)
            assert(len(sha512(msg)) == 64)
            assert(sha512(msg) == sha512(msg))

if __name__ == '__main__':
    unittest.main()
