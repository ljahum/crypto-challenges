
from tqdm import tqdm
# -----------------------------------
from itertools import *

from expApi import *



# pypy3爆破秘钥

ofb = "89b8aca257ee2748f030e7f6599cbe0cbb5db25db6d3990d"
cbc = "3b752eda9689e30fa2b03ee748e0da3c989da2bba657b912"
tab = [-32,-31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31,32]
c = [int(cbc[i:i+16],16) for i in range(0,48,16)]
c2=c[1]
c3=c[2]
c1=c[0]
for k in tqdm(product(tab,repeat=4)):
    keys = list(k)
    # keys = [16 for _ in range(4)]    
    # IV = 10708643912928985573
    tmp = invconvert(c3,keys)
    g3 = long_to_bytes(tmp^c2)
    if(check(g3)==True):
        
        tmp = invconvert(c2,keys)
        g2 = long_to_bytes(tmp^c1)
        # print(g2)
        # print(g3)
        # print(keys)
        if(check(g2)==True):
            print(g2)
            print(g3)
            print(keys)
# keys = [-12, 26, -3, -31]

def getiv(keys,ofb):
    c = [int(ofb[i:i+16],16) for i in range(0,48,16)]
    m21 =bytes_to_long( b'ByteCTF{')
    IV = invconvert(m21^c[0],keys)
    return IV

keys = [-12, 26, -3, -31]
ofb = "89b8aca257ee2748f030e7f6599cbe0cbb5db25db6d3990d"
cbc = "3b752eda9689e30fa2b03ee748e0da3c989da2bba657b912"
IV = getiv(keys,ofb)
    
# CBC
iv = IV
groups = []
c = [int(cbc[i:i+16],16) for i in range(0,48,16)]

c3 = c[2]
c2 = c[1]
for i in range(3):
    tmp = invconvert(c[i],keys)
    groups.append(tmp^iv)
    iv = c[i]
flag2 = b''.join( [long_to_bytes(i) for i in groups])

# OFB
iv = IV
groups = []
c = [int(ofb[i:i+16],16) for i in range(0,48,16)]
for i in range(3):
    tmp = convert(iv,keys)
    g = c[i]^tmp
    groups.append(g)
    iv = tmp

flag1 = b''.join( [long_to_bytes(i) for i in groups])
print(flag1+flag2)

# ByteCTF{5831a241s-f30980q535af-2156547475u2t}$$$


