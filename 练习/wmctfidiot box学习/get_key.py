import itertools
from binascii import hexlify, unhexlify
import Crypto.Random.random as random
from collections import Counter
from Crypto.Util.number import bytes_to_long, long_to_bytes, getRandomNBitInteger
from json import load
from tqdm import tqdm

cipher_flag, pairs = load(open("data", "r"))

sbox = [[11, 10, 1, 3, 8, 3, 14, 13, 0, 3, 9, 2, 4, 2, 11, 4, 6, 1, 6, 13, 6, 7, 7, 0, 10, 5, 4, 5, 9, 5, 10, 10, 6, 7, 15, 4, 7, 9, 15, 12, 1, 15, 14, 11, 14, 13, 1, 13, 8, 8, 9, 2, 12, 2, 0, 12, 8, 3, 0, 15, 11, 12, 5, 14], [0, 15, 2, 8, 3, 8, 12, 12, 9, 10, 14, 13, 4, 13, 14, 14, 2, 1, 15, 1, 1, 7, 3, 1, 10, 15, 6, 4, 6, 8, 5, 15, 4, 5, 7, 11, 7, 2, 5, 9, 11, 7, 11, 14, 6, 2, 11, 3, 12, 13, 9, 3, 9, 12, 4, 8, 10, 0, 5, 0, 0, 10, 6, 13], [5, 10, 3, 12, 3, 0, 6, 15, 13, 2, 0, 15, 8, 2, 3, 13, 9, 11, 0, 6, 14, 11, 2, 10, 1, 4, 12, 1, 7, 4, 7, 15, 5, 8, 7, 12, 5, 11, 0, 12, 14, 6, 9, 8, 14, 6, 9, 3, 4, 10, 1, 2, 10, 8, 7, 13, 15, 13, 4, 1, 5, 9, 14, 11], [4, 0, 7, 7, 7, 5, 4, 1, 10, 12, 11, 11, 11, 10, 15, 3, 12, 8, 3, 0, 2, 14, 14, 13, 2, 10, 6, 4, 6, 10, 2, 3, 14, 15, 8, 15, 9, 1, 11, 7, 5, 5, 6, 13, 6, 8, 0, 1, 3, 14, 0, 2, 9, 15, 8, 12, 1, 4, 9, 13, 9, 13, 5, 12], [
    9, 10, 3, 4, 2, 10, 12, 4, 5, 12, 5, 11, 5, 9, 13, 10, 7, 11, 7, 11, 1, 3, 2, 3, 3, 7, 1, 5, 15, 13, 9, 7, 12, 8, 8, 15, 0, 6, 0, 14, 15, 8, 8, 1, 0, 1, 0, 10, 14, 2, 14, 9, 13, 11, 6, 12, 15, 13, 14, 6, 4, 6, 4, 2], [0, 8, 12, 15, 0, 8, 3, 6, 7, 15, 9, 9, 2, 15, 9, 9, 1, 12, 13, 10, 5, 10, 12, 14, 5, 7, 14, 6, 4, 7, 5, 2, 1, 6, 4, 12, 0, 1, 14, 4, 3, 13, 11, 7, 3, 6, 11, 10, 1, 14, 2, 13, 13, 8, 15, 11, 11, 0, 5, 10, 2, 4, 8, 3], [9, 15, 3, 1, 15, 1, 7, 15, 10, 4, 0, 1, 0, 0, 3, 6, 9, 10, 12, 3, 3, 1, 12, 7, 8, 5, 2, 14, 2, 9, 2, 14, 6, 12, 13, 10, 11, 13, 9, 8, 6, 8, 5, 4, 11, 8, 14, 4, 12, 7, 13, 2, 10, 7, 13, 14, 6, 5, 5, 11, 4, 0, 15, 11], [13, 3, 1, 7, 1, 12, 10, 3, 14, 12, 14, 7, 10, 15, 5, 0, 2, 4, 13, 4, 13, 0, 8, 9, 11, 9, 10, 15, 3, 9, 12, 9, 11, 2, 8, 6, 10, 14, 11, 6, 2, 0, 6, 15, 12, 15, 6, 14, 7, 4, 13, 11, 0, 4, 7, 3, 2, 5, 1, 1, 5, 8, 8, 5]]
pbox = [19, 14, 15, 3, 10, 25, 26, 20, 23, 24, 7, 2, 18, 6, 30,
        29, 1, 4, 9, 8, 27, 5, 13, 0, 21, 16, 17, 22, 12, 31, 11, 28]
keys = []
pc_key = [2, 13, 16, 37, 34, 32, 21, 29, 15, 25, 44, 42, 18, 35, 5, 38, 39, 12, 30, 11, 7, 20,
          17, 22, 14, 10, 26, 1, 33, 46, 45, 6, 40, 41, 43, 24, 9, 47, 4, 0, 19, 28, 27, 3, 31, 36, 8, 23]


def gen_key():
    global keys
    keys = []
    key = getRandomNBitInteger(49) & ((1 << 48) - 1)
    key_bin = bin(key)[2:].rjust(48, '0')
    for i in range(6):
        key_bin = ''.join([key_bin[pc_key[j]] for j in range(48)])
        sub_key = int(key_bin, 2)
        keys.append(sub_key)


def inv_key(key):
    inv_key = [0]*48
    key_bin = bin(key)[2:].rjust(48, '0')
    for j in range(48):
        inv_key[pc_key[j]] = key_bin[j]
    return int(''.join(inv_key), 2)

def inv_keys(k6):
    keys = [0]*6
    keys[-1] = k6
    for i in range(4,-1,-1):
        keys[i] = inv_key(keys[i+1])
    return keys


def s(x, i):
    row = ((x & 0b100000) >> 4) + (x & 1)
    col = (x & 0b011110) >> 1
    return sbox[i][(row << 4) + col]


def p(x):
    x_bin = [int(_) for _ in bin(x)[2:].rjust(32, '0')]
    y_bin = [x_bin[pbox[i]] for i in range(32)]
    y = int(''.join([str(_) for _ in y_bin]), 2)
    return y


def e(x):
    x_bin = bin(x)[2:].rjust(32, '0')
    y_bin = ''
    idx = -1
    for i in range(8):
        for j in range(idx, idx + 6):
            y_bin += x_bin[j % 32]
        idx += 4
    return int(y_bin, 2)


def F(x, k):
    x_in = bin(e(x) ^ k)[2:].rjust(48, '0')
    y_out = ''
    for i in range(0, 48, 6):
        x_in_i = int(x_in[i:i+6], 2)
        y_out += bin(s(x_in_i, i // 6))[2:].rjust(4, '0')
    y_out = int(y_out, 2)
    y = p(y_out)
    return y

def enc_block(x):
    x_bin = bin(x)[2:].rjust(64, '0')
    l, r = int(x_bin[:32], 2), int(x_bin[32:], 2)
    for i in range(6):
        l, r = r, l ^ F(r, keys[i])
    y = (l + (r << 32)) & ((1 << 64) - 1)
    return y

def enc(pt):
    pad_len = (8 - len(pt) % 8) % 8
    pt += b'\x00' * pad_len
    ct = b''
    for i in range(0, len(pt), 8):
        ct_block = long_to_bytes(enc_block(bytes_to_long(pt[i:i+8]))).rjust(8, b'\x00')
        ct += ct_block
    return ct

#--------------------------
def inv_p(x):
    x_bin = [int(_) for _ in bin(x)[2:].rjust(32, '0')]
    y_bin = [0]*32
    for i in range(32):
        y_bin[pbox[i]] = x_bin[i]
    y = int(''.join([str(_) for _ in y_bin]), 2)
    return y


candidate_keys = [Counter() for _ in range(8)]

for _, cs in tqdm(pairs):
    c1, c2 = cs
    if c1 ^ c2 == 0x0000004000000000:
        continue

    l1, l2 = c1 >> 32, c2 >> 32
    r1, r2 = c1 & 0xffffffff, c2 & 0xffffffff
    # print(r1, r2)

    F_ = l1^l2^0x00000040
    F_ = inv_p(F_) # xor of the two outputs of sbox, 32bit

    Ep1 = e(r1) # 48bit
    Ep2 = e(r2) # 48bit

    for i in range(8):
        inp1 = (Ep1 >> (7-i)*6) & 0b111111   # 6bit
        inp2 = (Ep2 >> (7-i)*6) & 0b111111   # 6bit
        out_xor = (F_ >> (7-i)*4) & 0b1111   # 4bit
        for key in range(64):
            if s(inp1^key, i) ^ s(inp2^key, i) == out_xor:
                candidate_keys[i][key] += 1

print(candidate_keys)


# ----------------------
key6 = []
for c in candidate_keys:
    print(c.most_common(2))
    key6.append(c.most_common(1)[0][0])

print(key6)
# key6 = [53, 44, 38, 7, 7, 30, 29, 52]
k6 = sum(key6[i]<<(7-i)*6 for i in range(8))
# k6 = 236161043654516
keys = inv_keys(k6)
print(keys)

ps, cs = pairs[0]
p1, c1 = ps[0], cs[0]
assert enc_block(p1) == c1
# Ok! key is right!

# To decrypt, reverse the keys.
keys = keys[::-1]
print(enc(bytes.fromhex(cipher_flag)))
# b'WMCTF{D1ff3r3nti@1_w1th_1di0t_B0X3s}\x00\x00\x00\x00'