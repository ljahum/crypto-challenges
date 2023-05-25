from Crypto.Util.number import *


def get_my_prime(nibt, gamma):
    g = getPrime(int(nibt * gamma))
    while True:
        a = getPrime(int(nibt * (0.5 - gamma)))
        p = 2 * g * a + 1
        if isPrime(p):
            break

    while True:
        b = getPrime(int(nibt * (0.5 - gamma)))

        q = 2 * g * b + 1
        if isPrime(q):
            break
    print(g-a-b)
    
get_my_prime(1024, 0.3247)
# get_my_prime(1024, 0.2247)
