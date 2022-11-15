from getpass import getpass
from hashlib import pbkdf2_hmac
from secrets import token_bytes

# always salt your hash
salt = token_bytes(32)
hash = lambda x: pbkdf2_hmac('sha256', x, salt, 100_000)

# get a confirmed password within 5 attempts
attempts = 5
while attempts >= 0:
    p = hash(getpass('Password: ').encode('utf-8'))
    q = hash(getpass('Confirm: ').encode('utf-8'))
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
    return p == hash(getpass('Guess: ').encode('utf-8'))
