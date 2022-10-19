class Gen:
    """
    Extensible prime number generator
    """

    def __init__(self, n: int, start: int = 0, current: int = 0):
        self.all = []
        if current != 0:
            self.__init__(current)
            for _ in self: pass
            self.all.append(start)
        self.curr = start
        self.length = current + n
        self.current = current

    def __iter__(self):
        return self

    def __is_next_prime(self, x: int):
        for p in self.all:
            if not x % p: return False
        return True

    def extend(self, n: int):
        if n > 0:
            self.length += n

    def __next__(self):
        p = self.curr + 2
        while not self.__is_next_prime(p):
            p += 1
        self.current += 1
        if self.current > self.length:
            raise StopIteration
        self.curr = p
        self.all.append(p)
        return p
