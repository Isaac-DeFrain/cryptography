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
        if finish: break
        if not pows.__contains__(m):
            finish = True
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
    if not gens:
      raise ValueError(f'No multiplicative generators of 𝐙/{n}𝐙')
    else:
      i = random.randint(0, len(gens) - 1)
      return gens[i]

# compute the discrete log, if it exists
# otherwise, raise a ValueError
# x = base
# y = target
# n = modulus
def discrete_log(x, y, n):
    finish = False
    res = None
    x = x % n
    y = y % n
    for p in range(0, n - 2):
        if finish: break
        elif (x ** p) % n == y:
            finish = True
            res = p
    if finish:
        return res
    else:
        raise ValueError(f'{y} does not have a discrete log base {x} modulo {n}')

# check discrete logarithm
# x = base
# p = exponent
# y = target
# n = modulus
def check_discrete_log(x, p, y, n):
    return (x ** p) % n == y
