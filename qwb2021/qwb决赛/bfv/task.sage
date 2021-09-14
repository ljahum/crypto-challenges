from sage.stats.distributions.discrete_gaussian_integer import DiscreteGaussianDistributionIntegerSampler
from random import randint, getrandbits
from secret import flag
import sys
import signal
q = 2 ^ 54
t = 83
T = 3
d = 1024
delta = int(q / t)
sigma = 2
P.<x> = PolynomialRing(ZZ)
f = x ^ d + 1
R.<X> = P.quotient(f)
D = DiscreteGaussianDistributionIntegerSampler(sigma=sigma)

def sample_22():
    return R([randint(0,1) for _ in range(d)])

def sample1():
    return R([D() for _ in range(d)])


def sample2():
    return R([randint(0, q - 1) for _ in range(d)])

def sample3(x):
    return [randint(0, T - 1) for _ in range(x)]


def Roundq(a):
    A = a.list()
    for i in range(len(A)):
        A[i] = A[i] % q
        if A[i] > (q / 2):
            A[i] = A[i] - q
    return R(A)


def Roundt(a):
    A = a.list()
    for i in range(len(A)):
        A[i] = A[i] % t
        if A[i] > (t / 2):
            A[i] = A[i] - t
    return R(A)


def keygen():
    s = sample1()
    skl = s.list()
    skl = [-7,-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6,7 ] + skl
    skl = skl[:len(s.list())]
    s = R(skl)
    a = Roundq(sample2())
    e = Roundq(sample1())
    pk = [Roundq(-(a * s + e)), a]
    return s, pk


def encrypt(m):
    u = sample1()
    e1 = sample1()
    e2 = sample1()
    return (Roundq(pk[0] * u + e1 + delta * m), Roundq(pk[1] * u + e2))


def baseT(n, b=T):
    v = []
    while True:
        x = n // b
        y = n % b
        v.append(y)
        if x == 0:
            break
        n = x
    v.reverse()
    return v

def mutual(k, c, s):
    tmp = t * Roundq(c[0] + c[1] * s)
    TMP = tmp.list()
    for i in range(len(TMP)):
        TMP[i] = round(TMP[i] / q)
    tmp2 = Roundt(R(TMP))
    if tmp2[min(k, d)] == 0:
        print(True)
    else:
        print(False)

signal.alarm(1024)
sk, pk = keygen()
print(f"public key:{pk[0].list()}, {pk[1].list()}")

namelist = ["admin", "Adam", "Bruce", "Chris", "David"]
users = dict()
for i in namelist:
    users[i] = getrandbits(32)

menu = '''
1.Add friends
2.find friends
3.Send Message
4.Regist'''

friends = set()
while 1:
    print(f"Current number of users: {len(users)}")
    print(menu)
    op = int(input(">").strip())
    print(op)
    if op == 5:

        print(sk.list()[:40])
        print(users['admin'])
        print(baseT(users['admin']))
    if op == 1:
        name = input("name:").strip()
        id_num = int(input("id:").strip())
        if name in users.keys():
            if id_num == users[name]:
                friends.add(name)
            else:
                print("failed")
        else:
            print("failed")
    elif op == 2:
        op2 = input("recv ct?(Y/N)").strip()
        if op2.upper() == "Y":
            for name in users.keys():
                id_num = users[name]
                x = baseT(id_num)
                y = x + sample3(d - len(x))
                ct = encrypt(R(y))
                print(ct[0].list(), ct[1].list())
                op3 = input("continue?(Y/N)")
                if op3.upper() == "N":
                    break
                elif op3.upper() != "Y":
                    sys.exit(1)
        elif op2.upper() != "N":
            sys.exit(1)

        for i in range(len(users)):
            c1 = input("c1:").strip().split(" ")
            c2 = input("c2:").strip().split(" ")
            cc1 = list(map(int, c1))
            cc2 = list(map(int, c2))
            
            mutual(i, [R(cc1), R(cc2)], sk)

    elif op == 3:
        name = input("name:").strip()
        message = input("message:").strip()
        if name not in friends:
            print("failed")
        else:
            if name == "admin":
                if message == "give me the flag":
                    print(flag)
            else:
                print(f"send '{message}' to {name}")
    elif op == 4:
        name = input("name:").strip()
        if name not in users.keys():
            users[name] = getrandbits(32)
            print("succeeded")
        else:
            print("failed")
    else:
        sys.exit(1)
