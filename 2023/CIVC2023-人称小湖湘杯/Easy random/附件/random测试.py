
import random
from hashlib import md5
random.seed(10)

bits = 32
for i in range(10):
    m = random.getrandbits(bits)
    print(m)

# m = random.getrandbits(bits)
# m = bin(m)[2:].rjust(bits,'0')
# print(len(m),m)

# m = random.getrandbits(bits)
# m = bin(m)[2:].rjust(bits,'0')
# print(len(m),m)

# 16 1001001001000111
# 16 0000100001010111

# 32 1001001001000111 0111000011010011 
# 32 0000100001010111 0111111010110001

# 64 0000100001010111 0111111010110001 1001001001000111 0111000011010011