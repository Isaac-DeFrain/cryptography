# RSA unit tests

from rsa import make
import sys
import math
from time import time
import unittest
from rsa.utils import RsaTransformations as Rsa
from secrets import SystemRandom, token_bytes

class TestRsa(unittest.TestCase):
    def test_rsa_make(self):
        sys.setrecursionlimit(2000)

        n, _, _, _, enc, dec = make(
            299047036163466364593578671668105626794065326168257844506186760677132120379225668124615386505435634772733711855433506678212683219321934400431853837348621859006132708571197703124787540096917574784669270398109378338035186349072231512072877113120037670314261590067246212799116837416098173423817299815147,
            196763460946331349352499186611298628881243819903022496947907288526248422121851804346103094757867302222609503531023139472071798569335158505187945748246438168058674072267295382468467831591298752055972131783828041051056215358125513302847552420440611465989162677681036110999725853317071074438332295580687,
            [0])

        num_test = 100
        a, b, c, d = 0, 0, 0, 0
        start = time()
        for _ in range(num_test):
            l = SystemRandom().randint(1, min(100, math.ceil(n.bit_length() / 8)))
            x = Rsa.trim(token_bytes(l))
            x = b'\x01' if x == b'' else x
            try:
                ee = enc(x)
                dd = dec(ee)
                if dd == x:
                    c += 1
                else:
                    d += 1
                    print(f'Fail:\n\
- {l}\n\
- {x.hex()}\n\
- {ee.hex()}\n\
- {dd.hex()}')
            except UnicodeDecodeError: a += 1
            except ValueError:
                b += 1
                print(f'ValueError: {x}')
        print(f'** Test run time: {time() - start}')
        print(f'\
# -------------------------------- #\n\
# --- 1000 Random test results --- #\n\
# -------------------------------- #\n\
UnicodeDecodeError: {a}\n\
ValueError:         {b}\n\
Incorrect:          {d}\n\
Correct:            {c}\n\
# -------------------------------- #\n\
Total:              {a + b + c + d}')

if __name__ == '__main__':
    unittest.main()
