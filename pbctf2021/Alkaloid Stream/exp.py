from Crypto.Util.number import *
from Crypto.Util.strxor import *
from data import *


keys = []
tmp = pub.copy()
for key in tmp:
    if key[0] == 0:
        keys.append(key[1])
        tmp.remove(key)
        print('last key:' + str(key[1]))
    elif key[1] == 0:
        keys.append(key[0])
        tmp.remove(key)
        print('last key:' + str(key[0]))

fake = keys[0]
for _ in range(len(pub) - 1):
    for key in tmp:
        if key[0] == fake:
            keys.insert(0, key[1])
            tmp.remove(key)
            fake = 0
        elif key[1] == fake:
            keys.insert(0, key[0])
            tmp.remove(key)
            fake = 0
    if len(keys) <= len(pub) // 3:
        for i in keys:
            fake ^= i
    else:
        for i in keys[:len(pub)//3]:
            fake ^= i


print(len(keys))
print(keys)


def recover_keystream(key, public):
    st = set(key)
    keystream = ''
    for v0, v1 in public:
        if v0 in st:
            keystream += '0'
        elif v1 in st:
            keystream += '1'
        else:
            assert False, "Failed to recover the keystream"
    return keystream


stream = recover_keystream(keys, pub)
print(strxor(long_to_bytes(int(stream, 2)), long_to_bytes(cipher)))
# b'pbctf{super_duper_easy_brute_forcing_actually_this_one_was_made_by_mistake}'


# pbctf{super_duper_easy_brute_forcing_actually_this_one_was_made_by_mistake}