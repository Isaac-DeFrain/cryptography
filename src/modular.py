# modular arithmetic

# inverse of x modulo n
def inverse(x, n):
    res = None
    finish = False
    for y in range(1, n):
        if finish: break
        if (x * y) % n == 1:
            finish = True
            res = y
    return res
