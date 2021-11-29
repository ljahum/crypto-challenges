from block_cipher import encrypt_data, decrypt_data, decrypt

from collections import defaultdict
from tqdm import tqdm

print('[!] generating lookup table...')
ENCRYPTIONS_OF_ZERO = defaultdict(list)
for key in tqdm(range(2**24)):
    ct = encrypt_data(0, key)
    ENCRYPTIONS_OF_ZERO[ct].append(key)


def meet_in_the_middle(ct):
    print('[!] performing meet-in-the-middle attack for', ct)
    possible = defaultdict(list)
    for key in tqdm(range(2**24)):
        dec = decrypt_data(ct, key)
        if dec in ENCRYPTIONS_OF_ZERO:
            possible[key] = ENCRYPTIONS_OF_ZERO[dec]
    return possible


def recover_keys(Z, C):
    print('[!] recovering keys...')
    z1, z2, z3, z4 = Z
    c1, c2, c3, c4 = C
    for b0 in tqdm(z1):
        for a0 in z1[b0]:
            p1 = decrypt(c1, a0, b0)
            for c, z in zip([c2, c3, c4], [z2, z3, z4]):
                for a1 in z[b0]:
                    if p1 == decrypt(c, a1, b0):
                        b1 = recover_keys_part2(Z, C, a0, b0)
                        if b1:
                            print(f'a1 = {a1}, b1 = {b1}')
                            return True
    return False


g_tables = {5: [(5737111, 2983937),
                (15406556, 16284948),
                (14172222, 14132908),
                (4000971, 16383744)],
            6: [(8204186, 1546264),
                (229766, 3208405),
                (9550202, 13483954),
                (13257058, 5195482)],
            7: [(1658768, 11512735),
                (1023507, 9621913),
                (7805976, 1206540),
                (2769364, 9224729)]}

def recover_keys_part2(Z, C, a0, b0):
    z1, z2, z3, z4 = Z
    c1, c2, c3, c4 = C
    for c, z in zip([c2, c3, c4], [z2, z3, z4]):
        for b1 in z:
            if a0 in z[b1] and decrypt(c, a0, b1) == decrypt(c1, a0, b0):
                return b1
    return False


for i in [5, 6]:
    Z = [meet_in_the_middle(g_tables[i][j][1]) for j in range(4)]
    C = [g[0] for g in g_tables[i]]
    for i in range(4):
        if recover_keys([Z[i]] + Z[:i] + Z[i+1:], [C[i]] + C[:i] + C[i+1:]):
            break
