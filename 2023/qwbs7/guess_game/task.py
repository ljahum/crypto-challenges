from Crypto.Util.number import bytes_to_long, long_to_bytes
from os import urandom
from binascii import unhexlify

class cipher:
    def __init__(self, key, rounds=4):
        self.key = key
        self.rounds = rounds
        self.sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
        self.pbox = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
        self.rk = self.genrk(self.key)
    
    def substitution(self, state):
        output = 0
        for i in range(16):
            output += self.sbox[state >> (i*4) & 0xF] << (i*4)
        return output
    
    def permutation(self, state):
        output = 0
        for i in range(64):
            output += ((state >> i) & 0x1) << self.pbox[i]
        return output
    
    def genrk(self, key):
        rk = []
        for i in range(1, self.rounds+1):
            rk.append(key >> 16)
            key = ((key & (2**19-1)) << 61) + (key >> 19)
            key = (self.sbox[key >> 76] << 76)+(key & (2**76-1))
            key ^= i << 15
        return rk
    
    def addrk(self, state, rk):
        return state ^ rk
    
    def encrypt(self, pt):
        ct = b""
        state = pt
        for i in range(self.rounds-1):
            state = self.addrk(state, self.rk[i])
            state = self.substitution(state)
            state = self.permutation(state)
        state = self.addrk(state, self.rk[-1])
        ct += long_to_bytes(state)
        return ct

    def hint(self, pt):
        return self.encrypt(pt)

with open("flag.txt", "r") as f:
    flag = f.read()

op = '''1.get hint\n2.start game\n'''
count = 0
success = 0
key = int.from_bytes(urandom(10), "big")
guess = list(map(int, list(bin(key)[2:].zfill(80))))
game = cipher(key)
while True:
    print(op)
    user_input = int(input(">").strip())
    if user_input == 1:
        if count < 80:
            pt = int(input("pt in hex:"), 16)
            hint = game.hint(pt)
            count += 1
            print(hint.hex())
        else:
            print("Sorry~")
    elif user_input == 2:
        for i in range(len(guess)):
            user_guess = int(input(f"Round {i + 1} > ").strip())
            if user_guess == guess[i]:
                print("Right!")
                success += 1
            else:
                print("Wrong!")
        if success > 0.7 * len(guess):
            print(flag)
        else:
            print("Failed!")
            exit(-1)
    else:
        exit(-1)
