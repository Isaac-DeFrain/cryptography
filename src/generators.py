#! /usr/bin python3

import random

# check if g is a generator of 𝐙/n𝐙
def is_generator(g, n):
    pows = []
    finish = False
    g = g % n
    for p in range(0, n - 1):
        pows.append(g ** p % n)
    for m in range(1, n):
        if not pows.__contains__(m):
            finish = True
            break
    return not finish

# return list of generators of 𝐙/n𝐙
def generators(n):
    gens = []
    for g in range(2, n):
        if is_generator(g, n):
            gens.append(g)
    return gens

# return a randomly selected generator of 𝐙/n𝐙, if any exist
# otherwise, raise a ValueError
def random_gen(n):
    gens = generators(n)
    if not gens: return None
    else:
      i = random.randint(0, len(gens) - 1)
      return gens[i]

# compute the discrete log, if it exists
# otherwise, return None
# x = base
# y = target
# n = modulus
def discrete_log(x, y, n):
    finish = False # early exit
    res = None
    x = x % n
    y = y % n
    for p in range(0, n - 2):
        if finish: break
        elif (x ** p) % n == y:
            finish = True
            res = p
    return res

# check discrete logarithm
# x = base
# p = exponent
# y = target
# n = modulus
def check_discrete_log(p, x, y, n):
    return (x ** p) % n == y

# make functions for specific value of n
def make(n):
    is_gen = lambda g: is_generator(g, n)
    gens = lambda: generators(n)
    rand_gen = lambda: random_gen(n)
    dlog = lambda x, y: discrete_log(x, y, n)
    check_dlog = lambda p, x, y: check_discrete_log(p, x, y, n)
    return is_gen, gens, rand_gen, dlog, check_dlog
