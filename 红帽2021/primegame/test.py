from math import e
from decimal import *
import math
import random
import struct
from pretty_errors import *
from icecream import *
from rich import *
# ----------------------------
getcontext().prec = 100
E = Decimal(e)
print(e)
p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]
msg = b'SYCLOVER'
keys = []
A =[]
for i in range(24):
    keys.append(Decimal(p[i]).ln())
    print(Decimal(p[i]).ln()*2**256)
    A.append(math.floor(Decimal(p[i]).ln()*2**256))

sum_ = Decimal(0.0)
for i, c in enumerate(msg):
    sum_ += c * Decimal(keys[i])

ct = math.floor(sum_ * 2 ** 256)
print(A)
print(ct)
