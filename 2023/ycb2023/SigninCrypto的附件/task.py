from random import *
from Crypto.Util.number import *
from Crypto.Cipher import DES3
from flag import flag
from key import key
from iv import iv
import os
import hashlib
import secrets

K1= key
hint1 = os.urandom(2) * 8
xor =bytes_to_long(hint1)^bytes_to_long(K1)
print(xor)

def Rand():
    rseed = secrets.randbits(1024)
    List1 = []
    List2 = []
    seed(rseed)
    for i in range(624):
        rand16 = getrandbits(16)
        List1.append(rand16)
    seed(rseed)
    for i in range(312):
        rand64 = getrandbits(64)
        List2.append(rand64)
    with open("task.txt", "w") as file:
        for rand16 in List1:
            file.write(hex(rand16)+ "\n")
        for rand64 in List2:
            file.write(hex((rand64 & 0xffff) | ((rand64 >> 32) & 0xffff) << 16) + "\n")
'''
0xffffffffffffffff
0x360f2dfad17011d8
0x????2dfa????11d8

0x9e30bf907e2f3a3c
    ????bf90????3a3c
  a<<48 + bf90  + b<<16 + 3a3c
  
'''
Rand()

K2 = long_to_bytes(getrandbits(64))
K3 = flag[:8]

KEY = K1 + K2 + K3

IV=iv

IV1=IV[:len(IV)//2]
IV2=IV[len(IV)//2:]

digest1 = hashlib.sha512(IV1).digest().hex()
digest2 = hashlib.sha512(IV2).digest().hex()

digest=digest1+digest2
hint2=(bytes_to_long(IV)<<32)^bytes_to_long(os.urandom(8))
print(hex(bytes_to_long((digest.encode()))))
print(hint2)


mode = DES3.MODE_CBC
des3 = DES3.new(KEY, mode, IV)

pad_len = 8 - len(flag) % 8
padding = bytes([pad_len]) * pad_len
flag += padding

cipher = des3.encrypt(flag)

ciphertext=cipher.hex()
print(ciphertext)

# 334648638865560142973669981316964458403
# 0x62343937373634656339396239663236643437363738396663393438316230353665353733303939613830616662663633326463626431643139323130616333363363326631363235313661656632636265396134336361623833636165373964343533666537663934646239396462323666316236396232303539336438336234393737363465633939623966323664343736373839666339343831623035366535373330393961383061666266363332646362643164313932313061633336336332663136323531366165663263626539613433636162383363616537396434353366653766393464623939646232366631623639623230353933643833
# 22078953819177294945130027344
# a6546bd93bced0a8533a5039545a54d1fee647007df106612ba643ffae850e201e711f6e193f15d2124ab23b250bd6e1

# DSACTF{