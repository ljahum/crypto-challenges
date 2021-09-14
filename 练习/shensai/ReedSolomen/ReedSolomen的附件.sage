from secret import flag
from Crypto.Util.number import bytes_to_long

assert flag[:7] == b"DASCTF{" and flag[-1] == b'}'
message = bin(bytes_to_long(flag[7:-1]))[2:]
l = len(message)
padding = ((l - 1) // 8 + 1) * 8 - l
message = message.rjust(l + padding, '0')

blocks = []
for i in range(0, l + padding, 8):
    v = [int(c) for c in message[i:i+8]]
    blocks.append(v)

K.<x> = GF(2 ^ 8, modulus = 'primitive')
alpha = K([1, 1, 1, 0, 1, 0, 0, 1])
# alpha is the generator element in multiplieative cyclic group K

betas = [K(each) for each in blocks]

PR.<x> = PolynomialRing(K)
f = PR(betas)

import random

index = list(range(256))
random.shuffle(index)
index = index[:len(betas)]

print("Block nums = %d" % len(betas))

for each in index:
    print("f(alpha ^ %d) = %s" % (each, str(f(alpha ^ each))))


'''
Block nums = 32
f(alpha ^ 42) = x^7 + x^6 + x^2
f(alpha ^ 9) = x^7 + x^6 + x^5 + x^3 + x
f(alpha ^ 217) = x^7 + x^6 + x^5 + x^2
f(alpha ^ 152) = x^7 + x^6 + x^2 + 1
f(alpha ^ 114) = x^7 + x^4 + x^2
f(alpha ^ 202) = x^7 + x^6 + x^5 + x^3 + x^2 + 1
f(alpha ^ 233) = x^7 + x^6 + x^4
f(alpha ^ 244) = x^6 + x^4 + x
f(alpha ^ 20) = x^6 + x^5 + x^2
f(alpha ^ 125) = x^6 + x^5 + x^3 + x + 1
f(alpha ^ 164) = x^7 + x
f(alpha ^ 54) = x^7 + x^5 + x^3 + x
f(alpha ^ 161) = x^7 + x^5 + x^4 + x^3
f(alpha ^ 212) = x^6 + x^5 + x^2 + 1
f(alpha ^ 254) = x^5 + x^4 + x^3 + x^2 + 1
f(alpha ^ 157) = x^4 + x^3 + x^2 + x
f(alpha ^ 86) = x^5 + x^4 + x^2 + x
f(alpha ^ 238) = x^7 + x^4 + x + 1
f(alpha ^ 158) = x^7 + x^6 + x^4 + x^3 + x^2 + x
f(alpha ^ 93) = x^7 + x^6 + x^4 + 1
f(alpha ^ 232) = x^7 + x^6 + x^4 + 1
f(alpha ^ 223) = x^2 + x + 1
f(alpha ^ 159) = x^5 + x^4 + x^2 + x + 1
f(alpha ^ 156) = x^7 + x^6 + x^5 + x^2 + 1
f(alpha ^ 236) = x^7 + x^6 + x^5 + x
f(alpha ^ 179) = x^6 + x^4 + x^3 + x^2 + x
f(alpha ^ 145) = x^6 + x^5 + x^3 + x
f(alpha ^ 141) = x^4 + x^3 + x + 1
f(alpha ^ 181) = x^7 + x^5 + x^2 + x
f(alpha ^ 89) = x^7 + x^6 + x^5 + x^4 + x^3 + x^2 + x
f(alpha ^ 16) = 1
f(alpha ^ 198) = x^5 + x^4 + x^3 + x^2
'''