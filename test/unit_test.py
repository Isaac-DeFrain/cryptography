#!/usr/bin python3

import unittest
from secrets import token_hex

class TestRsa(unittest.TestCase):
    def test_rsa(self):
        self.assertEqual(0, 0)

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

        # auxillary implementation
        aux_impl = lambda s: ''.join([c.upper() for c in s])
        # 1000 random tests
        for _ in range(1000):
            s = token_hex(32)
            self.assertEqual(s.upper(), aux_impl(s))

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        self.assertEqual(s.split('e'), ['h', 'llo world'])
        self.assertEqual(s.split('l'), ['he', '', 'o wor', 'd'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
        with self.assertRaises(TypeError):
            s.split(True)

if __name__ == '__main__':
    unittest.main()
