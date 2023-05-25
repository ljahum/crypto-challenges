from itertools import product, repeat
from tqdm import tqdm

from l2b import *
import string

def invshift_opt(c,k,mask):
    c = bin(c)[2:].rjust(64,'0')
    cip=[int(i) for i in c]
    
    mask = bin(mask)[2:].rjust(64,'0')
    mask=[int(i) for i in mask]
    
    ans={}
    idx = 63
    for i in range(k):
        ans[idx]=cip.pop()
        idx-=1

    for i in range(63-k,-1,-1):
    
        tmp = cip[i]^(ans[i+k]&mask[i])
        ans[i]=tmp
    
    flag =''
    for i in range(64):
        flag += str(ans[i]) 
    # ans=[str(ans[i]) for i in range(64)]
    # ans = "".join(ans)
    ans = int(flag,2)
    return ans
        

def invshift_ngt(c,k,mask):
    k=-k
    c = bin(c)[2:].rjust(64,'0')
    cip=[int(i) for i in c]
    
    mask = bin(mask)[2:].rjust(64,'0')
    mask=[int(i) for i in mask]
    
    ans={}
    for i in range(k):
        ans[i]=cip[i]
    
    
    for i in range(k,64):
        tmp = cip[i]^(ans[i-k]&mask[i])
        ans[i]=tmp
    flag =''
    for i in range(64):
        flag += str(ans[i]) 
    # ans=[str(ans[i]) for i in range(64)]
    # ans = "".join(ans)
    ans = int(flag,2)
    return ans
    
def invconvert(m, key):
    c_list = [0x37386180af9ae39e, 0xaf754e29895ee11a, 0x85e1a429a2b7030c, 0x964c5a89f6d3ae8c]
    for t in range(3,-1,-1):
        if(key[t]>0):
            m = invshift_opt(m, key[t], c_list[t])
        else:
            m = invshift_ngt(m, key[t], c_list[t])
    return m

def check(s):
    for i in s:
        if(i>32 and i<127):
            continue
        else:
            return False
    return True

ofb = "89b8aca257ee2748f030e7f6599cbe0cbb5db25db6d3990d"
c = [int(ofb[i:i+16],16) for i in range(0,48,16)]
c1 = c[0]
tmp = b'\x95\x9c\xc5z\xef\xc0\x0e\x8b'
tmp = bytes_to_long(tmp)
# tab = b'abcdefghijklmnopqrstuvwxyz'+b'0123456789'
tab = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
# for i in range(len(mxoriv)):
s1 = b'ByteCtf{'
keys = [-12, 26, -3, -31]
m1 =bytes_to_long( b'ByteCTF{')
M1 = tmp^invconvert(m1^c1,keys)
print(long_to_bytes(M1))
if(check(long_to_bytes(M1))==True):
    print(M1,m1)
    print(invconvert(m1^c1,keys))
IV = 16476971533267772345



iv = IV
groups = []
c = [int(ofb[i:i+16],16) for i in range(0,48,16)]
for i in range(3):
    tmp = convert(iv,keys)
    g = c[i]^tmp
    groups.append(g)
    iv = tmp
if(check(groups[1]) and check(groups[2])):
    print([long_to_bytes(i) for i in groups])
    print(keys)