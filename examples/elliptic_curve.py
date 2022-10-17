"""
Elliptic curves

- Weierstrass form
- Montgomery form
"""

from modular import inverse
from typing import Annotated

class Point:
    """Point on an elliptic curve"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Weierstrass:
    """Weierstrass form of an elliptic curve"""

    # --------------------
    # --- type aliases ---
    # --------------------

    # modulus of the underlying field Z/nZ
    modulus = Annotated[int, 'Modulus of Z/nZ']

    # coefficients of the Weierstrass form of the curve
    a_coeff = Annotated[int, 'b coefficient of Weierstrass form']
    b_coeff = Annotated[int, 'a coefficient of Weierstrass form']

    # ---------------
    # --- methods ---
    # ---------------

    def __init__(self, a: a_coeff, b: b_coeff, n: modulus):
        """Initialize a Weierstrass curve"""
        self.weierstrass = a, b, n

    def f(self, x: int):
        """Compute right side of Weierstrass equation"""
        a, b, n = self.weierstrass
        return (x ** 3 + a * x + b) % n

    def check(self, p: Point) -> bool:
        """Check that `p` is a point on the curve"""

        _, _, n = self.weierstrass
        return p.y ** 2 % n == Weierstrass.f(self, p.x)

    def points(self, *debug) -> list[Point]:
        """
        Return the list of all points on the elliptic
        curve over Z/nZ with Weierstrass form:

            `y^2 = x^3 + a*x + b`

        Includes the point at infinity, represented by (-1, -1)

        Inefficient implementation: use only on small fields
        """
        a, b, n = self.weierstrass
        pts = [(-1, -1)]
        for x in range(0, n):
            for y in range(0, n):
                p = x, y
                if Weierstrass.check(self, p): pts.append(p)
        if debug:
            print('+-----------------------------------------------')
            print(f'+ Points of y^2 = x^3 + {a}x + {b} (mod {n})')
            print('+-----------------------------------------------')
            print(f'+ {pts.__len__()} points over Z/{n}Z')
        return sorted(pts)

    def points_n(self, k: int, lower: int = 0, *upper) -> list[Point]:
        """Find k points on the curve given `lower` and/or `upper` bound(s)

        Includes the point at infinity, represented by (-1, -1)
        """
        _, _, n = self.weierstrass
        pts = [(-1, -1)]
        upper = upper[0] if upper else n
        lower = lower
        count = 0
        while count < k and lower < upper:
            for y in range(lower, upper):
                p = lower, y
                if Weierstrass.check(self, p):
                    count += 1
                    pts.append(p)
            lower += 1
        return pts

    def add(self, p: Point, q: Point) -> Point:
        """Elliptic curve point addition"""

        a, _, n = self.weierstrass
        # coordinates
        x1, y1 = p
        x2, y2 = q
        # identity and inverse rules
        if x1 == x2 and y1 == -y2: return (-1, -1)
        if p == (-1, -1): return q
        if q == (-1, -1): return p
        # otherwise
        lam = ((3 * x1 ** 2 + a) * inverse(2 * y1, n)
            if p == q else (y2 - y1) * inverse(x2 - x1, n))
        x3 = (lam ** 2 - x1 - x2) % n
        y3 = (lam * (x1 - x3) - y1) % n
        return Point(x3, y3)

    def safe_add(self, p: Point, q: Point) -> Point:
        """
        Check that the points are on the curve before adding
        """
        add = Weierstrass.add
        check = Weierstrass.check
        if check(self, p) and check(self, q):
            return add(self, p, q)

    def scalar_mult(self, k: int, p: Point) -> Point:
        """Scalar multiplication"""

        if k == 0: return (-1, -1)
        if k == 1: return p
        if k > 1:
            add = Weierstrass.add
            mult = Weierstrass.scalar_mult
            return add(self, p, mult(self, k - 1, p))
        else:
            raise ValueError(f'Expect element of Z/nZ, got: {k}')

class Montgomery:
    """Montgomery form of an elliptic curve"""

    def __init__(self):
        """Initialize a new Montgomery"""
        self.montgomery = 0, 0, 0

    # TODO
    def f(self, x: int) -> int:
        """Compute right hand side of Montgomery equation"""
        return x

    def check(self, p: Point) -> bool:
        """Check that `p` is a point on the curve"""

        _, _, n = self.montgomery
        # TODO
        return p.y ** 2 % n == Weierstrass.f(self, p.x)

    def points_n(self, k: int, lower: int = 0, *upper) -> list[Point]:
        """Find k points on the curve given `lower` and/or `upper` bound(s)

        Includes the point at infinity, represented by (-1, -1)
        """
        _, _, n = self.weierstrass
        pts = [(-1, -1)]
        upper = upper[0] if upper else n
        lower = lower
        count = 0
        while count < k and lower < upper:
            for y in range(lower, upper):
                p = lower, y
                if Weierstrass.check(self, p):
                    count += 1
                    pts.append(p)
            lower += 1
        return pts
