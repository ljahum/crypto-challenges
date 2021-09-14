

from decimal import *
import math
import random
import struct
# from flag import flag

# assert (len(flag) == 48)
# msg1 = flag[:24]
# msg2 = flag[24:]
primes = [2]
for i in range(3, 90):
    f = True
    for j in primes:
        if i * i < j:
            print(i,j)
            break
        if i % j == 0:
            print(i,j)
            f = False
            break
    if f:
        primes.append(i)
print(primes)
print(len(primes))
keys = []
for i in range(24):
    keys.append(Decimal(primes[i]).ln())

print(keys)
for i in range(24):
    print(Decimal(keys[i]))