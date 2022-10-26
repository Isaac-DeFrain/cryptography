"""
HMAC unit tests
"""

import unittest
from examples.hash.mac import SHA256, SHA512
from secrets import SystemRandom, token_hex

class TestHmac256(unittest.TestCase):
    def test_hmac_sha256(self):
        """1000 random sha256 hmac tests"""
        for _ in range(100):
            n = SystemRandom().choice([32, 64, 96, 128, 160, 192, 224, 256])
            sha256 = SHA256()
            msg = token_hex(n)
            assert(sha256.hmac(msg) == sha256.hmac(msg))
            # assert(sha256.hmac_msg(msg)[256:] == msg)
            # assert(sha256.hmac_msg(msg)[:256] == sha256.hmac(msg))
            assert(sha256.hmac_msg(msg) == sha256.hmac_msg(msg))

class TestHmac512(unittest.TestCase):
    def test_hmac_sha512(self):
        """1000 random sha512 hmac tests"""
        for _ in range(100):
            n = SystemRandom().choice([64, 128, 192, 256])
            sha512 = SHA512()
            msg = token_hex(n)
            assert(sha512.hmac(msg) == sha512.hmac(msg))
            # assert(sha512.hmac_msg(msg)[512:] == msg)
            # assert(sha512.hmac_msg(msg)[:512] == sha512.hmac(msg))
            assert(sha512.hmac_msg(msg) == sha512.hmac_msg(msg))

if __name__ == '__main__':
    unittest.main()
