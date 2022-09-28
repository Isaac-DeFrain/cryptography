#! /usr/bin python3

import random

# check if g is a generator of Zn
def is_generator(g, n):
    pows = []
    finish = False
    g = g % n
    for p in range(0, n - 1):
        pows.append(g ** p % n)
    for m in range(1, n):
        if finish:
            break
        if not pows.__contains__(m):
            finish = True
    return not finish

# return list of generators of Zn
def generators(n):
    gens = []
    for g in range(2, n):
        if is_generator(g, n):
            gens.append(g)
    return gens

# return a randomly selected generator of Zn, if any exist
# otherwise, raise a ValueError
def random_gen(n):
    gens = generators(n)
    if not gens:
      raise ValueError("No generators of Zn")
    else:
      i = random.randint(0, len(gens) - 1)
      return gens[i]
