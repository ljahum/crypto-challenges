from pwn import *
from hashlib import sha256
from tqdm import tqdm
from Crypto.Util.number import *


def GCRT(mi, ai):
    assert (isinstance(mi, list) and isinstance(ai, list))
    curm, cura = mi[0], ai[0]
    for (m, a) in zip(mi[1:], ai[1:]):
        d = int(GCD(curm, m))
        c = a - cura
        assert (c % d == 0)
        K = c // d * inverse(curm // d, m // d)
        cura += curm * K
        curm = curm * m // d
        cura %= curm
    return cura % curm, curm


def proof_of_work(sh):
    sh.recvuntil("SHA256(\"")
    nonce = sh.recv(8)
    sh.recvuntil('with \"00000\"')
    for a in tqdm(range(0x30, 0x7f)):
        for b in range(0x30, 0x7f):
            for c in range(0x30, 0x7f):
                for d in range(0x30, 0x7f):
                    rest = chr(a) + chr(b) + chr(c) + chr(d)
                    m = (nonce.decode('latin1') + rest).encode("Latin-1")
                    if sha256(m).digest().hex().startswith("00000"):
                        sh.sendline(rest)
                        sh.recvuntil('again...God bless you get it...')
                        return


def io(sh, num):
    sh.sendline('god')
    sh.sendline(str(num))
    tmp = sh.recvuntil('\n')
    if len(tmp) > 100:
        return int(tmp)
    else:
        return int(sh.recvuntil('\n'))


primes = [4294966427, 4294966441, 4294966447, 4294966477, 4294966553, 4294966583, 4294966591, 4294966619, 4294966639, 4294966651, 4294966657, 4294966661, 4294966667, 4294966769, 4294966813, 4294966829,
          4294966877, 4294966909, 4294966927, 4294966943, 4294966981, 4294966997, 4294967029, 4294967087, 4294967111, 4294967143, 4294967161, 4294967189, 4294967197, 4294967231, 4294967279, 4294967291]


for i in range(2**10):
    sh = remote("0.0.0.0", 10000)
    # proof_of_work(sh)
    

    c = []
    index = 0
    for i in range(63):
        tmp = io(sh, primes[index])

        if tmp % primes[index] != 0:  # 这个判断是剔除k等于0的情况
            c.append(-1 * tmp)
            index += 1
            if index >= 32:  # 如果超过32个数的k不等于0，我们就可以拿来用了，但也不确定是否这32个数都为1
                break
    if index < 32:
        continue
    secret = GCRT(primes, c)[0]
    sh.sendline('bless')
    sh.sendline(str(secret))
    tmp = sh.recvuntil('\n')
    if len(tmp) < 5:
        tmp = sh.recvuntil('\n')
    if b'WRONG' in tmp:
        sh.close()
        continue
    print(tmp)
    sh.interactive()
