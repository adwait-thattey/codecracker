from math import sqrt, ceil
from collections import defaultdict


def sieve(N):
    """Dumb sieve of Eratosthemes, O(N*log(log(N)))"""
    b = [True] * (N + 1)
    b[0] = False
    b[1] = False

    lim = ceil(sqrt(N))
    i = 2
    while i <= lim:
        if b[i]:
            for n in range(i ** 2, N + 1, i):
                b[n] = False
        i += 1

    return {i for i, b in enumerate(b) if b}


def factor(n, P):
    """Given prime list, factorize n"""
    if n in P: return [n]
    f = []
    for p in P:
        while n % p == 0:
            n //= p
            f.append(p)
        if n in P:
            f.append(n)
            return f
    if n != 1:
        f.append(n)
    return f


P = sieve(10 ** 6 + 1)

n = int(input())
A = [int(x) for x in input().split()]

S = 0
for a in A:
    F = reversed(sorted(factor(a, P)))
    p = 1
    S += 1
    for f in F:
        p *= f
        S += p

print(S)



