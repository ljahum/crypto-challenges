import re
from json import dump

from tqdm import tqdm
from Crypto.Util.number import long_to_bytes, getRandomNBitInteger
from pwn import *

def gen_diff_input(diff):
    p1 = getRandomNBitInteger(64)
    p2 = p1 ^ diff
    return p1, p2


r = remote("81.68.174.63", 34129)
# context.log_level = "debug"

rec = r.recvuntil(b"required").decode()
cipher_flag = re.findall(r"\n([0-9a-f]{80})\n", rec)[0]
print(cipher_flag)
r.recvline()

pairs = []
for i in tqdm(range(10000)):
    p1, p2 = gen_diff_input(0x0000000000000040)
    r.sendline(long_to_bytes(p1).hex().encode())
    c1 = int(r.recvline(keepends=False), 16)
    r.sendline(long_to_bytes(p2).hex().encode())
    c2 = int(r.recvline(keepends=False), 16)
    pairs.append(((p1,p2), (c1,c2)))

r.close()


dump([cipher_flag, pairs], open("data", "w"))