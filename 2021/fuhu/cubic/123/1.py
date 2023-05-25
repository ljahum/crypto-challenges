from sympy import sqrt
from fractions import Fraction as Frac


def continued_fraction(n):
    a = sqrt(n)
    for i in range(10):
        print(int(a))
        a = 1 / (a - int(a))

continued_fraction(24234/13123)


def pell(n):
    if int(sqrt(n))**2 == n:
        return (1, 0)
    l = []
    for i in continued_fraction(n):
        
        a = Frac(i)
        for j in l[::-1]:
            a = j + 1 / a
        if a.numerator**2 - n * a.denominator**2 == 1:
            return (a.numerator, a.denominator)
        l.append(i)


