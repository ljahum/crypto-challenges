from random import randint
from time import time

def seed_mt19937(seed):
    MT = [0] * 624
    MT[0] = seed
    for i in range(1, 624):
        MT[i] = (1812433253 * (MT[i-1] ^ (MT[i-1] >> 30)) + i) & 0xffffffff
    return MT

def extract_number(MT):
    if not isinstance(MT, list):
        raise TypeError("MT must be a list")
    N, M = 624, 397
    if len(MT) != N:
        raise ValueError(f"MT must have length {N}")
    # Twist update
    for i in range(N):
        x = (MT[i] & 0x80000000) + (MT[(i+1)%N] & 0x7fffffff)
        xA = x >> 1
        if x % 2 != 0:
            xA ^= 0x9908b0df
        MT[i] = MT[(i+M)%N] ^ xA
    # Temper
    y = MT[0]
    y ^= y >> 11
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= y >> 18
    return y & 0xffffffff

# Generate 32-bit random numbers using MT19937 algorithm
seed_value = 10
MT = seed_mt19937(seed_value)
for i in range(10):
    print(extract_number(MT))