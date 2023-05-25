from Crypto.Util.number import *

from random import *
beta = 0.34
delta = 0.02
amplification = 2048
print(int(delta * amplification))
print((beta-delta) * amplification)
print((beta * amplification))
print(((1 - beta) * amplification))
dq = getrandbits(int(delta*amplification))
tmp = e*dq-1


