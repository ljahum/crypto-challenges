from randcrack import RandCrack
from data import data1
from hashlib import md5
rc = RandCrack()
for i in range(len(data1)):
    if(i%3==0):
        r = bin(int(data1[i]))[2:].zfill(32)    
        rc.submit(int(r, 2))
    if(i%3==1):
        r = bin(int(data1[i]))[2:].zfill(64)    
        r1 = r[:32]
        r2 = r[32:]
        rc.submit(int(r2, 2))
        rc.submit(int(r1, 2))
    if(i%3==1):
        r = bin(int(data1[i]))[2:].zfill(96)    
        r1 = r[:32]
        r2 = r[32:64]
        r3 = r[64:]
        rc.submit(int(r3, 2))
        rc.submit(int(r2, 2))
        rc.submit(int(r1, 2))

tmp = rc.predict_getrandbits(32)
print(tmp)
flag = md5(str(tmp).encode()).hexdigest()
print(flag)
# 14c71fec812b754b2061a35a4f6d8421