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
rr = rc.predict_getrandbits(64)
print(hex(rr))

