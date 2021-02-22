from math import sin, cos, pi

def iexp(n):
    return complex(cos(n), sin(n))

def dft(xs):
    "naive dft"
    n = len(xs)
    return [sum((xs[k] * iexp(-2 * pi * i * k / n) for k in range(n)))
            for i in range(n)]