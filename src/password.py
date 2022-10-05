#!/usr/bin python3

from getpass import getpass
from hashlib import pbkdf2_hmac
from os import urandom

# always salt your hash
salt = urandom(32)
hash = lambda x: pbkdf2_hmac('sha256', x, salt, 100_000)

# get a confirmed password within 5 attempts
attempts = 5
while attempts >= 0:
    p = hash(bytes(getpass('Password: '), 'utf-8'))
    q = hash(bytes(getpass('Confirm: '), 'utf-8'))
    if p != q:
        if attempts == 1:
            print('Password mismatch. Try again. You have %s remaining attempt.' % attempts)
        elif attempts > 0:
            print('Password mismatch. Try again. You have %s remaining attempts.' % attempts)
        else:
            print('Sorry for your luck. Bye.')
        attempts -= 1
    else:
        print('Your password is: ' + p.hex())
        break

def guess():
    return p == hash(bytes(getpass('Guess: '), 'utf-8'))
