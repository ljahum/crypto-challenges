---
title: "writeUP for easyXor in ByteCTF 2021"
subtitle: 
date: 2021-10-17 00:07:00+08:00
# weight: 1000
draft: true
author: "ljahum"
description: "Personal Information"
tags: 
- crypto
# crypto 25math 6codes 5bin 4Nuil 
categories: 
- CTF
# - CTF posts notes 其他

# 内波标题图片
featuredImage: 

# 外部标图图片
featuredImagePreview: 

hiddenFromHomePage: false
math:
  enable: true
---
<!--more-->

# writeUP for easyXor in ByteCTF 2021

> 笑死,xyb信号屏蔽拉满,蓝牙都不让用,只能来苟唯一一个不出网的题

## EASYXOR

主要难度在逆convert和猜ByteCTF{前缀大小写上🤭

convert



```python
def shift(m, k, c):
    if k < 0:
        return m ^ (m >> (-k)) & c
    return m ^ ((m << k) & c)
```

大概是因为有个位移导致部分数据泄露，分清左右顺序和前后一点点慢慢把m恢复出来

大致流程如下：

![](https://gitee.com/ljahum/images/raw/master/img/Notes_211017_110102.jpg)

inv convert：

```python

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
```

然后打表爆破keys，把api全部拖出来用pypy几分钟就跑完了

```python
❯❯ easyxor  10:22 pypy3 .\solve.py
5228891it [02:22, 34737.70it/s]b'15654747'
b'5u2t}$$$'
[-12, 26, -3, -31]
```

然后本题最难的地方来了，👴思索了2个小时愣是没有考虑前缀的情况

拿着`flag{xxx`爆了半天

然后才想起来学弟们打的是字节CTF

然后祥云被场地没网，工作人员不知道把👴的手机放哪里了，热点都找不到，只能猜前缀了

好在仗着👴不太优秀的变量命名功底给前缀`ByteCTF{`猜出来了

### solve

#### main

```python

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

```


#### expApi

```python

import struct
import sys

def bytes_to_long(s):
    """Convert a byte string to a long integer (big endian).

    In Python 3.2+, use the native method instead::

        >>> int.from_bytes(s, 'big')

    For instance::

        >>> int.from_bytes(b'\x00P', 'big')
        80

    This is (essentially) the inverse of :func:`long_to_bytes`.
    """
    acc = 0

    unpack = struct.unpack

    # Up to Python 2.7.4, struct.unpack can't work with bytearrays nor
    # memoryviews
    if sys.version_info[0:3] < (2, 7, 4):
        if isinstance(s, bytearray):
            s = bytes(s)
        elif isinstance(s, memoryview):
            s = s.tobytes()

    length = len(s)
    if length % 4:
        extra = (4 - length % 4)
        s = b'\x00' * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
    return acc

def long_to_bytes(n, blocksize=0):
    """Convert an integer to a byte string.

    In Python 3.2+, use the native method instead::

        >>> n.to_bytes(blocksize, 'big')

    For instance::

        >>> n = 80
        >>> n.to_bytes(2, 'big')
        b'\x00P'

    If the optional :data:`blocksize` is provided and greater than zero,
    the byte string is padded with binary zeros (on the front) so that
    the total length of the output is a multiple of blocksize.

    If :data:`blocksize` is zero or not provided, the byte string will
    be of minimal length.
    """
    # after much testing, this algorithm was deemed to be the fastest
    s = b''
    n = int(n)
    pack = struct.pack
    while n > 0:
        s = pack('>I', n & 0xffffffff) + s
        n = n >> 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != b'\x00'[0]:
            break
    else:
        # only happens when n == 0
        s = b'\x00'
        i = 0
    s = s[i:]
    # add back some pad bytes.  this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * b'\x00' + s
    return s

def check(s):
    for i in s:
        if(i>32 and i<127):
            continue
        else:
            return False
    return True

def shift(m, k, c):
    if k < 0:
        return m ^ (m >> (-k)) & c
    return m ^ ((m << k) & c)

def convert(m, key):
    c_list = [0x37386180af9ae39e, 0xaf754e29895ee11a, 0x85e1a429a2b7030c, 0x964c5a89f6d3ae8c]
    for t in range(4):
        m = shift(m, key[t], c_list[t])
    return m

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
```