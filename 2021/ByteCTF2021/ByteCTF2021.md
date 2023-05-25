---
title: "writeUP for easyXor in ByteCTF 2021"
subtitle: 
date: 2021-10-17 00:07:00+08:00
# weight: 1000
draft: true
author: "ljahum"
description: ""
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

> 笑死,xyb信号屏蔽拉满,蓝牙都不让用,只能来苟唯一一个不出网的题

> 总得来说水平还是比较绝绝子，延续了字节去年炼丹题的的优良传统，

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


### expApi

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

## document for JustDecrypt

> 还是比较有意思的炼丹题，有点CBC打oracle的感觉，总得来说还是比较有意思

task
```python
#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
import string
import random
import socketserver
import signal
import codecs
from os import urandom
from hashlib import sha256
from Crypto.Cipher import AES
from flag import FLAG

BANNER = rb"""

   ___           _    ______                           _   
  |_  |         | |   |  _  \                         | |  
    | |_   _ ___| |_  | | | |___  ___ _ __ _   _ _ __ | |_ 
    | | | | / __| __| | | | / _ \/ __| '__| | | | '_ \| __|
/\__/ / |_| \__ \ |_  | |/ /  __/ (__| |  | |_| | |_) | |_ 
\____/ \__,_|___/\__| |___/ \___|\___|_|   \__, | .__/ \__|
                                            __/ | |        
                                           |___/|_|        
"""

BLOCK_SIZE = 16


class AES_CFB(object):
    def __init__(self):
        self.key = urandom(BLOCK_SIZE)
        self.iv = urandom(16)
        self.aes_encrypt = AES.new(self.key, AES.MODE_CFB, self.iv)
        self.aes_decrypt = AES.new(self.key, AES.MODE_CFB, self.iv)

    def encrypt(self, plain):
        return self.aes_encrypt.encrypt(self.pad(plain))

    def decrypt(self, cipher):
        return self.unpad(self.aes_decrypt.decrypt(cipher))

    @staticmethod
    def pad(s):
        num = BLOCK_SIZE - (len(s) % BLOCK_SIZE)
        return s + bytes([num] * num)

    @staticmethod
    def unpad(s):
        return s[:-s[-1]]


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 1024
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def proof_of_work(self):
        random.seed(urandom(32))
        alphabet = string.ascii_letters + string.digits
        proof = ''.join(random.choices(alphabet, k=32))
        hash_value = sha256(proof.encode()).hexdigest()
        self.send(f'sha256(XXXX+{proof[4:]}) == {hash_value}'.encode())
        nonce = self.recv(prompt=b'Give me XXXX > ')
        if len(nonce) != 4 or sha256(nonce + proof[4:].encode()).hexdigest() != hash_value:
            return False
        return True

    def timeout_handler(self, signum, frame):
        raise TimeoutError

    def handle(self):
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(60)

            self.send(BANNER)

            # if not self.proof_of_work():
            #     self.send(b'\nWrong!')
            #     self.request.close()
            #     return

            self.send(b"It's just a decryption system. And I heard that only the Bytedancer can get secret.")

            aes = AES_CFB()

            # signal.alarm(300)

            for i in range(52):
                cipher_hex = self.recv(prompt=b'Please enter your cipher in hex > ')
                if len(cipher_hex) > 2048:
                    self.send(b"It's too long!")
                    continue
                try:
                    cipher = codecs.decode(cipher_hex, 'hex')
                except:
                    self.send(b'Not hex data!')
                    continue

                if len(cipher) == 0 or len(cipher) % BLOCK_SIZE != 0:
                    self.send(f'Cipher length must be a multiple of {BLOCK_SIZE}!'.encode())
                    continue

                plaintext = aes.decrypt(cipher)
                plaintext_hex = codecs.encode(plaintext, 'hex')
                self.send(b'Your plaintext in hex: \n%s\n' % plaintext_hex)

                if plaintext == b"Hello, I'm a Bytedancer. Please give me the flag!":
                    self.send(b'OK! Here is your flag: ')
                    self.send(FLAG.encode())
                    break

            self.send(b'Bye!\n')

        except TimeoutError:
            self.send(b'\nTimeout!')
        except Exception as err:
            self.send(b'Something Wrong!')
        finally:
            self.request.close()


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 30002
    print(HOST, PORT)
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

```

大抵是一下几个知识点：

- CFB模式机制
- 如何padding oracle

输入一个消息块来设置定长iv

输入\x00参数来获取流秘钥跑64次可以完全oracle

跑不满64次也可以对低位嗯猜

```python
from Crypto.Util.number import *
from pwn import *
from tqdm import tqdm
def main():
    r = remote('0.0.0.0', '30002')
    plaintext = b"Hello, I'm a Bytedancer. Please give me the flag!"+b"\x0f"*15

    def my_XOR(a, b):
        assert len(a) == len(b)
        return b''.join([long_to_bytes(a[i]^b[i]) for i in range(len(a))])

    def proof_of_work():
        rev = r.recvuntil(b"sha256(XXXX+")
        suffix = r.recv(28).decode()
        rev = r.recvuntil(b" == ")
        tar = r.recv(64).decode()

        def f(x):
            hashresult = hashlib.sha256(x.encode()+suffix.encode()).hexdigest()
            return hashresult == tar

        prefix = util.iters.mbruteforce(f, string.digits + string.ascii_letters, 4, 'upto')
        r.recvuntil(b'Give me XXXX > ')
        r.sendline(prefix.encode())

    def decrypt(msg):
        newmsg = msg + b'\x00'*(256+64-len(msg))
        r.recvuntil(b'Please enter your cipher in hex > ')
        r.sendline(newmsg.hex().encode())
        r.recvline()
        result = r.recvline().decode().strip()
        return bytes.fromhex(result)

    def decrypt_(msg):
        newmsg = msg + b'\x00'*(256-len(msg))
        r.recvuntil(b'Please enter your cipher in hex > ')
        r.sendline(newmsg.hex().encode())
        r.recvline()
        result = r.recvline().decode().strip()
        return bytes.fromhex(result)

    # proof_of_work()
    msg = b'\x00'*16
    decrypt(msg)
    c = b""
    for i in range(50):
        t = decrypt(c)[i]
        c += long_to_bytes(t^plaintext[i])

    decc = decrypt_(c)
    print(decc)
    res = r.recvline()+r.recvline()
    if b"Here is your flag" in res:
        print(r.recvline())
        print(r.recvline())
        r.close()
        return (True, len(decc))
    r.close()
    return (False, len(decc))

ll = []
while True:
    ss = main()
    ll.append(ss[1])
    if ss[0]: break
    print(len(ll), ll)

```