"""
Elliptic curves

- Weierstrass form
- Montgomery form
"""

from modular import Mod
from typing import Annotated, Union

class Point:
    """
    Point on an elliptic curve
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Weierstrass:
    """
    Weierstrass form of an elliptic curve
    """

    # --------------------
    # --- type aliases ---
    # --------------------

    # modulus of the underlying field Z/nZ
    modulus = Annotated[int, 'Modulus of Z/nZ']

    # coefficients of the Weierstrass form of the curve
    a_coeff = Annotated[int, 'a coefficient of Weierstrass form']
    b_coeff = Annotated[int, 'b coefficient of Weierstrass form']

    # ---------------
    # --- methods ---
    # ---------------

    def __init__(self, a: a_coeff, b: b_coeff, n: modulus):
        """
        Initialize a Weierstrass curve
        """
        self.form = a, b, n

    def f(self, x: int):
        """
        Compute right side of Weierstrass equation
        """
        a, b, n = self.form
        return (x ** 3 + a * x + b) % n

    def check(self, p: Point) -> bool:
        """
        Check that `p` is a point on the curve
        """
        _, _, n = self.form
        return p.y ** 2 % n == self.f(p.x)

    def points(self, *debug) -> list[Point]:
        """
        Return the list of all points on the elliptic
        curve over Z/nZ with Weierstrass form:

            `y^2 = x^3 + a*x + b`

        Includes the point at infinity, represented by (-1, -1)

        Inefficient implementation: use only on small fields
        """
        a, b, n = self.form
        pts = [Point(-1, -1)]
        for x in range(0, n):
            for y in range(0, n):
                p = Point(x, y)
                if self.check(p):
                    pts.append(p)
        if debug:
            print('+--------------------------------------------')
            print(f'+ Points of y^2 = x^3 + {a}x + {b} (mod {n})')
            print('+--------------------------------------------')
            print(f'+ {pts.__len__()} points over Z/{n}Z')
        return pts

    def points_n(self, k: int, lower: int = 0, *upper) -> list[Point]:
        """
        Find k points on the curve given `lower` and/or `upper` bound(s)

        Includes the point at infinity, represented by (-1, -1)
        """
        _, _, n = self.form
        pts = [Point(-1, -1)]
        upper = upper[0] if upper else n
        lower = lower
        count = 0
        while count < k and lower < upper:
            for y in range(lower, upper):
                p = Point(lower, y)
                if self.check(p):
                    count += 1
                    pts.append(p)
            lower += 1
        return pts

    def add(self, p: Point, q: Point) -> Point:
        """
        Elliptic curve point addition (Weierstrass form)
        """
        a, _, n = self.form
        # coordinates
        x1, y1 = p.x, p.y
        x2, y2 = q.x, q.y
        # identity and inverse rules
        if x1 == x2 and y1 == -y2: return Point(-1, -1)
        if p == Point(-1, -1): return q
        if q == Point(-1, -1): return p
        # otherwise
        mod = Mod(n)
        lam = ((3 * x1 ** 2 + a) * mod.inverse(2 * y1)
            if p == q else (y2 - y1) * mod.inverse(x2 - x1))
        x3 = (lam ** 2 - x1 - x2) % n
        y3 = (lam * (x1 - x3) - y1) % n
        return Point(x3, y3)

    def safe_add(self, p: Point, q: Point) -> Union[Point, None]:
        """
        Check that the points are on the curve before adding
        """
        if self.check(p) and self.check(q):
            return self.add(p, q)

    def scalar_mult(self, k: int, p: Point) -> Point:
        """
        Scalar multiplication
        """
        if k == 0: return Point(-1, -1)
        if k == 1: return p
        if k > 1:
            return self.add(p, self.scalar_mult(k - 1, p))
        else:
            raise ValueError(f'Expect element of Z/nZ, got: {k}')

class Montgomery:
    """
    Montgomery form of an elliptic curve
    """

    # --------------------
    # --- type aliases ---
    # --------------------

    # modulus of the underlying field Z/nZ
    modulus = Annotated[int, 'Modulus of Z/nZ']

    # coefficients of the Montgomery form of the curve
    a_coeff = Annotated[int, 'a coefficient of Montgomery form']
    b_coeff = Annotated[int, 'b coefficient of Montgomery form']

    # ---------------
    # --- methods ---
    # ---------------

    def __init__(self, a: a_coeff, b: b_coeff, n: modulus):
        """
        Initialize a new Montgomery
        """
        self.form = a, b, n

    def f(self, x: int) -> int:
        """
        Compute right side of Montgomery equation
        """
        a, _, n = self.form
        return (x ** 3 + a * x ** 2 + x) % n

    def check(self, p: Point) -> bool:
        """
        Check that `p` is a point on the curve
        """
        _, b, n = self.form
        return b * p.y ** 2 % n == self.f(p.x)

    def points(self, *debug) -> list[Point]:
        """
        Return the list of all points on the elliptic
        curve over Z/nZ with Montgomery form:

            `b*y^2 = x^3 + a*x^2 + x`

        Includes the point at infinity, represented by (-1, -1)

        Inefficient implementation: use only on small fields
        """
        a, b, n = self.form
        pts = [Point(-1, -1)]
        for x in range(0, n):
            for y in range(0, n):
                p = Point(x, y)
                if self.check(p):
                    pts.append(p)
        if debug:
            print('+-----------------------------------------------')
            print(f'+ Points of {b}y^2 = x^3 + {a}x^2 + x (mod {n})')
            print('+-----------------------------------------------')
            print(f'+ {pts.__len__()} points over Z/{n}Z')
        return pts

    def points_n(self, k: int, lower: int = 0, *upper) -> list[Point]:
        """
        Find k points on the curve given `lower` and/or `upper` bound(s)

        Includes the point at infinity, represented by (-1, -1)
        """
        _, _, n = self.form
        pts = [Point(-1, -1)]
        upper = upper[0] if upper else n
        lower = lower
        count = 0
        while count < k and lower < upper:
            for y in range(lower, upper):
                p = Point(lower, y)
                if self.check(p):
                    count += 1
                    pts.append(p)
            lower += 1
        return pts

    def add(self, p: Point, q: Point) -> Point:
        """
        Elliptic curve point addition (Montgomery form)
        """
        a, b, n = self.form
        # coordinates
        x1, y1 = p.x, p.y
        x2, y2 = q.x, q.y
        # identity and inverse rules
        if x1 == x2 and y1 == -y2: return Point(-1, -1)
        if p == Point(-1, -1): return q
        if q == Point(-1, -1): return p
        # otherwise
        mod = Mod(n)
        m = (y2 - y1) * mod.inverse(x2 - x1) % n
        if p != q:
            x3 = (b * m ** 2 - a - x1 - x2) % n
            y3 = (m * (2 * x1 + x2 + a) - b * m ** 3 - y1) % n
        else:
            l = (3 * x1 ** 2 + 2 * a * x1 + 1) * mod.inverse(2 * b * y1) % n
            x3 = (b * l ** 2 - a - 2 * x1) % n
            y3 = ((3 * x1 + a) * l - b * l ** 3 - y1) % n
        return Point(x3, y3)

    def safe_add(self, p: Point, q: Point) -> Union[Point, None]:
        """
        Check that the points are on the curve before adding
        """
        if self.check(p) and self.check(q):
            return self.add(p, q)

    def scalar_mult(self, k: int, p: Point) -> Point:
        """
        Scalar multiplication
        """
        if k == 0: return Point(-1, -1)
        if k == 1: return p
        if k > 1:
            return self.add(p, self.scalar_mult(k - 1, p))
        else:
            raise ValueError(f'Expect element of Z/nZ, got: {k}')

# TODO conversion between forms
