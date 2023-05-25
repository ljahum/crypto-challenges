import random
import string
import hashlib
import sys
from collections import deque
from secret import plist, banner
import sys
assert max(plist) < 160

class generator:
    def __init__(self, key: list, iv: list, hint: bool, k=0, m=0):
        self.NFSR = deque()
        self.LFSR = deque()

        for i in range(80):
            self.NFSR.append(key[i])

        for i in range(64):
            self.LFSR.append(iv[i])

        for i in range(64, 80):
            self.LFSR.append(1)

        self.clock()

        if hint:
            s = self.NFSR + self.LFSR
            for i in range(k, k + m):
                s[i] ^= 1
            self.NFSR = deque(list(s)[:80])
            self.LFSR = deque(list(s)[80:])

    def clock(self):
        for i in range(160):
            zi = self.PRGA()
            self.NFSR[79] ^= zi
            self.LFSR[79] ^= zi

    def PRGA(self):
        x0 = self.LFSR[3]
        x1 = self.LFSR[25]
        x2 = self.LFSR[46]
        x3 = self.LFSR[64]
        x4 = self.NFSR[63]

        hx = x1 ^ x4 ^ (x0 & x3) ^ (x2 & x3) ^ (x3 & x4) ^ (x0 & x1 & x2) ^ (x0 & x2 & x3) \
             ^ (x0 & x2 & x4) ^ (x1 & x2 & x4) ^ (x2 & x3 & x4)

        zi = (self.NFSR[1] ^ self.NFSR[2] ^ self.NFSR[4] ^ self.NFSR[10] ^ self.NFSR[31] ^ self.NFSR[43] ^ self.NFSR[
            56]) ^ hx

        fx = self.LFSR[62] ^ self.LFSR[51] ^ self.LFSR[38] ^ self.LFSR[23] ^ self.LFSR[13] ^ self.LFSR[0]

        gx = self.LFSR[0] ^ self.NFSR[62] ^ self.NFSR[60] ^ self.NFSR[52] ^ self.NFSR[45] ^ self.NFSR[37] \
             ^ self.NFSR[33] ^ self.NFSR[28] ^ self.NFSR[21] ^ self.NFSR[14] ^ self.NFSR[9] ^ self.NFSR[0] \
             ^ (self.NFSR[63] & self.NFSR[60]) ^ (self.NFSR[37] & self.NFSR[33]) ^ (self.NFSR[15] & self.NFSR[9]) \
             ^ (self.NFSR[60] & self.NFSR[52] & self.NFSR[45]) ^ (self.NFSR[33] & self.NFSR[28] & self.NFSR[21]) \
             ^ (self.NFSR[63] & self.NFSR[45] & self.NFSR[28] & self.NFSR[9]) ^ (
                     self.NFSR[60] & self.NFSR[52] & self.NFSR[37] & self.NFSR[33]) \
             ^ (self.NFSR[63] & self.NFSR[60] & self.NFSR[21] & self.NFSR[15]) ^ (
                     self.NFSR[63] & self.NFSR[60] & self.NFSR[52] & self.NFSR[45] & self.NFSR[37]) \
             ^ (self.NFSR[33] & self.NFSR[28] & self.NFSR[21] & self.NFSR[15] & self.NFSR[9]) ^ (
                     self.NFSR[52] & self.NFSR[45] & self.NFSR[37] & self.NFSR[33] & self.NFSR[28] & self.NFSR[21])

        self.LFSR.popleft()
        self.LFSR.append(fx)
        self.NFSR.popleft()
        self.NFSR.append(gx)

        return zi

def proof_of_work():
    s = "".join(random.choices(string.ascii_letters + string.digits, k=20))
    prefix = s[:4]
    print(f"sha256(xxxx + {s[4:]}) == {hashlib.sha256(s.encode()).hexdigest()}")
    print("give me xxxx:")
    ans = input().strip()
    if len(ans) == 4 and ans == prefix:
        return True
    else:
        return False

if not proof_of_work():
    sys.exit(0)

with open("/root/task/flag.txt", "r")as f:
    flag = f.read()

print(banner + "\n")
print("Welcome to my number guessing game. If you win the game, I'll give you the flag\n")

count = 0
glist = random.choices(plist, k=32)
for round in range(len(glist)):
    guess = glist[round]
    k = guess // 2
    m = guess % 10
    if m == 0:
        m = 10
    key = bin(random.getrandbits(80))[2:].zfill(80)
    key = list(map(int, key))
    iv = bin(random.getrandbits(64))[2:].zfill(64)
    iv = list(map(int, iv))
    a = generator(key, iv, False)
    k1 = []
    for i in range(160):
        k1.append(a.PRGA())
    k1 = int("".join(list(map(str, k1))), 2)
    b = generator(key, iv, True, k, m)
    k2 = []
    for i in range(160):
        k2.append(b.PRGA())
    k2 = int("".join(list(map(str, k2))), 2)
    print(f"round {round+1}")
    print("Here are some tips might help your:")
    print(k1)
    print(k2)
    num = int(input(">"))
    if num == guess:
        count += 1
        print("you are smart!\n")
    else:
        print("wrong!\n")

if count == 32:
    print(flag)
    sys.exit(0)
else:
    print("you lose the game, bye!")
    sys.exit(0)