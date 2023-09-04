from Crypto.Cipher import DES3
from Crypto.Util.number import *
'''
from hashlib import md5
from randcrack import RandCrack
from data import list1,list2

print(len(list2))
t=[]
for i in range(len(list2)):
    tmp2 = list2[i]
    x4 = tmp2&0xffff
    x2 = (tmp2&0xffff0000)>>16
    x3 = list1[i*2]
    x1 = list1[i*2+1]
    s1 = (x3<<16) +x4 
    s2 = (x1<<16)+x2
    
    t.append(s1)
    t.append(s2)
rc = RandCrack()
for i in t:
    rc.submit(i)
K2 = rc.predict_getrandbits(64)
print(hex(K2))

'''
enc = 'a6546bd93bced0a8533a5039545a54d1fee647007df106612ba643ffae850e201e711f6e193f15d2124ab23b250bd6e1'
enc = bytes.fromhex(enc)
r = b'\xfb\xc2'
hint1 = r * 8
xor = b'\xfb\xc2\xfb\xc2\xfb\xc2\xfb\xc2\x9f\xa3\x88\xa1\x8f\xa4\x9f\xa3'
K1 =bytes_to_long(hint1)^bytes_to_long(xor)

K1 =long_to_bytes(K1)


K2 = 0x77ab242d64a60e8e
K2 = long_to_bytes(K2)
# K2 =b'\x00\x00\x00\x00"Y\xcf3'
# 是的 iv高4字节和低4字节一样的
IV = b'GWHTGWHT'

for i in range(256):
    
    K3 = b'DASCTF{'+bytes([i])
    # print(K3)
    KEY = K1+K2+K3
    
    mode = DES3.MODE_CBC
    
    des3 = DES3.new(KEY, mode, IV)
    flag = des3.decrypt(enc)
    # print(flag)
    if(b'DAS' in flag):
        print(flag)
        
# b'DASCTF{8e5ee461-f4e1-4af2-8632-c9d62f4dc073}\x04\x04\x04\x04'