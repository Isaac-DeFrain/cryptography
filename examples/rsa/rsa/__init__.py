"""RSA module

TODO description
"""

from rsa.rsa import Key, encrypt, decrypt, make

__author__ = "Isaac DeFrain"
__date__ = "2022-15-10"
__version__ = "0.1"

# Do doctest if we're run directly
if __name__ == "__main__":
    import doctest

    doctest.testmod()

__all__ = [
    "Key",
    "encrypt",
    "decrypt",
    "make"
]