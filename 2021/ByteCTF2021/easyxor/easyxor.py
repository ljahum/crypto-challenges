
from Crypto.Util.number import bytes_to_long, long_to_bytes
from random import randint, getrandbits




def shift(m, k, c):
    if k < 0:
        return m ^ (m >> (-k)) & c
    return m ^ ((m << k) & c)


def convert(m, key):
    c_list = [0x37386180af9ae39e, 0xaf754e29895ee11a, 0x85e1a429a2b7030c, 0x964c5a89f6d3ae8c]
    for t in range(4):
        m = shift(m, key[t], c_list[t])
    return m


def encrypt(m, k, iv, mode='CBC'):
    assert len(m) % 8 == 0
    num = len(m) // 8
    groups = []
    for i in range(num):
        groups.append(bytes_to_long(m[i * 8: (i + 1) * 8]))
    print(groups)
    last = iv
    cipher = []
    if mode == 'CBC':
        for eve in groups:
            cur = eve ^ last
            cur_c = convert(cur, k)
            cipher.append(cur_c)
            last = cur_c
    elif mode == 'OFB':
        for eve in groups:
            cur_c = convert(last, k)
            cipher.append(cur_c ^ eve)
            last = cur_c
    else:
        print( 'Not supported now!')
    # print(cipher)
    # for i in cipher:
    #     print(hex(i))
    return ''.join([hex(eve)[2:].strip('L').rjust(16, '0') for eve in cipher])


if __name__ == '__main__':
    # from secret import flag
    flag = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    if len(flag) % 8 != 0:
        flag += '$' * (8 - len(flag) % 8)
    print(flag)
    length = len(flag)
    num = length // 8
    # keys = [randint(-32, 32) for _ in range(4)]
    keys = [16 for _ in range(4)]
    IV = 10708643912928985573L
    front = flag[:length // 2]
    back = flag[length // 2:]
    cipher1 = encrypt(front, keys, IV, mode='OFB')
    cipher2 = encrypt(back, keys, IV)
    print("ofb = "+cipher1)
    print("cbc = "+cipher2)
    print( cipher1 + cipher2)
# 2ecbbd0feacd9295ae0ab5afdb65b2932f8b91077903fb1dae0a3707e2c3149f4baa52cf21d0bd782f8ab5266b95331f
