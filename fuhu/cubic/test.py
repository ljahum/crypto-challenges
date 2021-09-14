from math import gcd
from functools import reduce
from fractions import Fraction as Frac
N=6
for x in range(1, 1000):
    print(x)
    for y in range(1, 1000):
        for z in range(1, 1000):
            anss = []
            mark = 0
            for i in range(1):
                if x * y * z == 0:  # positive integer
                    mark = 1
                    # print("This is not what i want!\n")
                    break
                if reduce(gcd, [x, y, z]) != 1:  # (kx, ky, kz)
                    mark = 1
                    # print("This is not what i want!\n")
                    break
                if Frac(x, y+z) + Frac(y, z+x) + Frac(z, x+y) != N:
                    mark = 1
                    # print("This is not what i want!\n")
                    break
            if(mark==0):
                print(x,y,x)
                input()
