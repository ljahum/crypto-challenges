---
title: "WriteUp for inCTF2021"
subtitle: 
date: 2021-08-16 00:07:00+08:00
# weight: 1000

author: "ljahum"
# description: "Personal Information"
tags: 
- crypto
# crypto 25math 6codes 5bin 4Nuil 
categories: 
- CTF

hiddenFromHomePage: false
math:
  enable: true
---
<!--more-->

# WriteUp for inCTF

## gold_digger

```python
def encrypt(msg, N,x):
    msg, ciphertexts = bin(bytes_to_long(msg))[2:], []
    for i in msg:
        while True:
            r = random.randint(1, N)
            if gcd(r, N) == 1:
                bin_r = bin(r)[2:]
                c = (pow(x, int(bin_r + i, 2), N) * r ** 2) % N
                ciphertexts.append(c)
                break
    return ciphertexts
```

The main problem

```python
c = (pow(x, int(bin_r + i, 2), N) * r ** 2) % N
```

if $flag_i$ is 1 ,the bin_r + i well be odd 

else the $r+i$ well be even

we can determine the flag by calculating  Jacobi symbol of c to N

### solution

```python
from Crypto.Util.number import *
import gmpy2
from data import ct
N = 76412591878589062218268295214588155113848214591159651706606899098148826991765244918845852654692521227796262805383954625826786269714537214851151966113019
x = 72734035256658283650328188108558881627733900313945552572062845397682235996608686482192322284661734065398540319882182671287066089407681557887237904496283

plaintext = ''

for line in ct:
    if gmpy2.jacobi(line,N) == -1:
        plaintext += '1'
    else:
        plaintext += '0'
print(long_to_bytes(int(plaintext,2)))
# inctf{n0w_I_4in7_73ll1ng_u_4_g0ldd1gg3r}
```

## Lost Baggag

In this challenge , we need to analyze a backpack encryption system

the challenge give us only pubkey and cipher

so，i tried Lattice reduction algorithm to solve it

sagemath lattice reduction code：

```python
import pickle
data = pickle.load(open('enc.pickle', 'rb'))
cip = data['cip']
pbkey = data['pbkey']
print(len(pbkey))


S = cip
M = pbkey

n = len(M)
L = matrix.zero(n + 1)

for row, x in enumerate(M):
    L[row, row] = 2
    L[row, -1] = x

L[-1, :] = 1
L[-1, -1] = S
f = open('LLLdata.txt','a+')
res = L.LLL()
for i in range(144):
    ans = list(res[i])
    
    f.write(str(ans)+'\n')
    print(ans)
```

The matrix is looks like:
$$
\begin{pmatrix} 2&0&0&\cdots&0&PK_1\\0&2&0&\cdots&0&PK_2 \\ 0&0&2&\cdots&0&PK_3 \\ \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\ 0&0&0&\cdots& 2 & PK _ n \\ 1&1&1&\cdots &1&ct\end{pmatrix}
$$



Lets check the LLLdata.txt

fortunately,I find a vector only have 1 and -1 

![](https://gitee.com/ljahum/images/raw/master/img/20210815214238.png)

try to docode it and get the flag

```python
from Crypto.Util.number import *
ans = [-1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1]


flag = ''
for i in ans:
    if(i == -1):
        flag+='1'
    else:
        flag+='0'
msg = int(flag[::-1],2)
print(long_to_bytes(msg))
flag = ''
for i in ans:
    if(i == -1):
        flag+='0'
    else:
        flag+='1'
msg = int(flag[::-1],2)
print(long_to_bytes(msg))
# inctf{wr5_m4_b4g?}
```





## Right Now Generator

> This challenge is easy after analysing
>
> It’s more like a reverse than a crypto....

### analysis and implement

Our major trouble is to find The Inverse function of functioncs below,

And how we think about finding seed-sequence from a-sequence given by the attachment

```python
	def wrap(self, pr=True):
		hsze = self.sze//2
		for i in range(self.sze):
			r1 = self.seed[i]
			r2 = self.seed[(i+hsze)%self.sze]
			self.seed[i] = ((r1^self.pad)*r2)%self.mod
		self.ctr = 0

	def next(self):
		a, b, c, d = (self.seed[self.ctr^i] for i in range(4))
		mod = self.mod
		k = 1 if self.ctr%2 else 2
		a, b, c, d = (k*a-b)%mod, (b-c)%mod, (c-d)%mod, (d-a)%mod
		self.ctr += 1
		if self.ctr==64:
			self.wrap(pr=False)
		return a

```
With a simple algebraic calculation

We can write out Inverse function easily

---

from a-sequence get seed-sequence:

```python
def from_aa_get_seed(aa):
	seed=[]
	for i in range(0,63,4):
		tmp = aa[i:i+4]
		a1,a2,a3,a4 = tmp
		s0 = (a1+a2)%mod
		s1 = (2*a2+a1)%mod
		s2 = (a3+a4)%mod
		s3 = (2*a4+a3)%mod
		seed = seed + [s0,s1,s2,s3]
	return seed
```

inv_wrap:

```python
def inv_wrap(seed):
	
	for i in range(32):
		
		r2 = seed[i]
		r1 = ((seed[i+32]*libnum.invmod(r2,mod))%mod)^pad
		seed[i+32]=r1
	for i in range(32):
		r2 = seed[i+32]
		r1 = ((seed[i]*libnum.invmod(r2,mod))%mod)^pad
		seed[i] = r1
	return seed
```

Combined them into decryption code

### Solution

```python

import random, hashlib, os, gmpy2, pickle
import libnum
from libnum.modular import invmod
from Crypto.Util.number import *

from Crypto.Cipher import AES

# -----------------------------------

pad = 0xDEADC0DE
sze = 64
mod = 18446744073709551629

def inv_wrap(seed):
	
	for i in range(32):
		
		r2 = seed[i]
		r1 = ((seed[i+32]*libnum.invmod(r2,mod))%mod)^pad
		seed[i+32]=r1
	for i in range(32):
		r2 = seed[i+32]
		r1 = ((seed[i]*libnum.invmod(r2,mod))%mod)^pad
		seed[i] = r1
	return seed

def from_aa_get_seed(aa):
	seed=[]
	for i in range(0,63,4):
		tmp = aa[i:i+4]
		
		a1,a2,a3,a4 = tmp
		s0 = (a1+a2)%mod
		s1 = (2*a2+a1)%mod
		s2 = (a3+a4)%mod
		s3 = (2*a4+a3)%mod
		seed = seed + [s0,s1,s2,s3]
	return seed
def from_leak_get_aa(leak):
	aa =[]
	for i in range(0,1024,16):
		
		tmp  =leak[i:i+16]
		s = bytes.fromhex(tmp)
		tmp = bytes_to_long(s)
		
		aa.append(tmp)
	return aa
def next(seed1,i):
	ctr = i
	a, b, c, d = (seed1[ctr^i] for i in range(4))
	mod = 18446744073709551629
	k = 1 if ctr%2 else 2 # 1 和 2 交替出现,可控
	a, b, c, d = (k*a-b)%mod, (b-c)%mod, (c-d)%mod, (d-a)%mod
	
	return a
enc = {'cip': '71d39d37d3c03e08b82d81ae3b4be658e2dbdaee6a73d73a3e88271f423db30f0422d4fb9475ceef281a746afa86eaee', 'iv': 'cbf411655acfd7f670968ccf44d74e05', 'leak': '3aeba43302ab9ad0df898103fc0223be23f5ec10f62ad48744c2ec06bc4ac9b2290aff5f5d17fc2ff2a1115e657ddced0f12238ca12b076bf85fed0ce621202d159c014907e39ba7373ada78a4dea3a76bfb9ff09a8f10705cd95a47edd743fde25f32ab545bf98bba1344bed511b0c095ddede11b4a35bc02acb34d3aef46c56bfc9b668c82c0d3da76307dd87016e1a7df478cdefb98d4fe991088f478f24390fac3d4f0d0673d2801f37df421ab17cb72af64a8b21ebf9d73c3ef35a8bd5fe98c62a910ef8b859b86a58bf670fe544266bc37a36d3828e7397bac0b817f41522e76a68661b3e9952ed3d2eb7846b2f9cd2c1cc44eda2ac536eb826ce922afaa4c7d61ff3db9023cf2fff8fb34791954fbb1541f043fe26e92fb79f119fbe175bd1b551dd1225275a457580bef4301505f474060f39caad6d3172f17a9a21f68e66b59a13e817b0201dbdbcc1e6c1d80ab2e8d38f7f0a62d0bb3577da845643273b1743f5aac064422bdbd85358f6da726f9114c5553432d4f4e2f43f997975add7ea3b6a56b689ff84f7635815879e28d8c7421b979449f5bccb29cce745862610af8c99379c60e1205d5e1eda9d2f5243d4da4325ac142bd196d1777bd2d4f61eb355b7fca3e16295d05e8a21e75f010272ce159afb49fa3d4b97bd242304e34599f7bc8edf5b4430bb42b12437b7c27583d303043311afd56fae70a7d6b'}

leak  = enc['leak']
aa = from_leak_get_aa(leak)
seed = from_aa_get_seed(aa)
seed_prev = inv_wrap(seed)
out1 = ''.join([format(next(seed_prev,i), '016x') for i in range(64)])
key = bytes.fromhex(out1)
key = hashlib.sha256(key).digest()[:16]
cip = enc['cip']
iv = enc['iv']
cip = bytes.fromhex(cip)
iv = bytes.fromhex(iv)
aes = AES.new(key, AES.MODE_CBC, iv)
flag = aes.decrypt(cip)
print(flag)
# b'inctf{S1mpl3_RN65_r_7h3_b35t!_b35e496b4d570c16}\x01'
```

## Eazy Xchange

there we can exchange gen_key into a simple form

```python
def gen_key(G, pvkey):
	G = sum([i*G for i in pvkey])
	return G
def gen_key(G, pvkey):
	tmp = sum([i for i in pvkey])
	return G*tmp
```

and the tmp is small $(tmp <1024)$

and there tell us $B=tmp*G$

```python
def gen_bob_key(EC, G):
	bkey = os.urandom(4)
	B = gen_key(G, bkey)
	return B, bkey

```

so 

$SS=tmp_1*tmp_2*G$

and $SS=tmp_1*tmp_2<1024*1024$

We can try out $tmp_1*tmp_2$ easily

```python
import os, hashlib, pickle
from tqdm import tqdm
# -----------------------------------
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = p - 3
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
EC = EllipticCurve(GF(p), [a, b])
G = EC.gens()[0] # 固定的点

def decrypt(cip, key,iv):
    key = hashlib.sha256(str(key).encode()).digest()[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(cip)

data = {'cip': '9dcc2c462c7cd13d7e37898620c6cdf12c4d7b2f36673f55c0642e1e2128793676d985970f0b5024721afaaf02f2f045', 'iv': 'cbd6c57eac650a687a7c938d90e382aa', 'G': '(38764697308493389993546589472262590866107682806682771450105924429005322578970 : 112597290425349970187225006888153254041358622497584092630146848080355182942680 : 1)'}
FLAG = data['cip']
iv = data['iv']
FLAG = bytes.fromhex(FLAG)
iv = bytes.fromhex(iv)
x = 38764697308493389993546589472262590866107682806682771450105924429005322578970
y = 112597290425349970187225006888153254041358622497584092630146848080355182942680
G = EC(x,y)
print(G)

SS = G
for i in tqdm(range(2,1024*1024)):
    
    SS = SS+G
    msg = decrypt(FLAG, SS.xy()[0],iv)
    if(b'inctf' in msg):
        print(msg)
        break
# inctf{w0w_DH_15_5o_c00l!_3c9cdad74c27d1fc}
```



## Encrypted Operations

这个有意思了（我提莫直接吓出母语）😫😫😫

审了一天

发现印度老哥这个vector的理解和我不一样，缝缝补补终于搞出来了

反正这个题应该很难有复现环境了

(其实能把homomorphic_system复写一遍应该还是可以的？放在docker里面还是比较好部署的)

就干脆简单说一下三个部分的思路好了🐫

prat1

```python
for (int x = 0; x < 20; x++)
    {
        for (int y = 0; y < 20; y++)
        {
            m[x][y] = ++val;
        }
    }

    int d = 20;
    int r = 3;
    int c = 3;
for (int i = 0; i < 18; i++)
    {
        for (int j = 0; j < 18; j++)
        {
            for (int p = 0; p < 3; p++)
            {
                for (int q = 0; q < 3; q++)
                {
                    mat.push_back(m[i + p][j + q]);
                }
            }
        }
    }

    for (int j = 0; j < int(mat.size()); j += 9)
    {
        v.push_back(slice(mat, j, j + 9));//切片矩阵化
    }

    idx = Genrand(0, v.size() - 1);
    vector<int64_t> temp1(begin(v[idx]), end(v[idx]));
    vector<int64_t> mvector = temp1;

    sum1 = accumulate(mvector.begin(), mvector.end(), 0);//随机先去一个切片求和

    FheEncrypt(mvector);

    EncryptedOperations();

    vector<int64_t> p = FheDecrypt();

    if (sum1 == 0)
    {
        cout << "\n\nCHALLENGE CORRUPTED!!!!";
        exit(0);
    }

    if (p[0] == sum1)
        cout << "\n\nYou got all the encrypted operations right! Great!!\n\nNow on to the next\n\n";
    else
        exit(0);
```

拿导外面跑一下发现其实就是对切片求和，由于temp1里面本质上是个等差数列，找一下规律就可以了

part2同理

payload1

```python
9 0 0 0
*
1
y

189 0 0 0
+
1
n

189 0 0 0
+
1
n
+

20 0 0 0
*
1
y

830 0 0 0
+
1
n

```

level2 对 p1 p2 取反使其抵消掉numVec里面除了m1[row[2]]以外的所有向量

在 userinp生成处，往后多选了一位，这个操作可以在EncryptedOperations中对m1[row[2]]右移一位抵消掉影响，最有一位并不会消失，而是会将vector的长度扩展一位

```c++
p = vector<int64_t>(p.begin(), p.begin() + 5 + 1);
```

exp

```python
from pwn import *
from pwnlib.util.iters import random_permutation
#  crypto.challenge.bi0s.in 1221

data = """9 0 0 0
*
1
y

189 0 0 0
+
1
n

189 0 0 0
+
1
n
+

20 0 0 0
*
1
y

830 0 0 0
+
1
n

0 0 0 0 0
>
1
n

-1 -1 -1 -1 -1
*
1
n

-1 -1 -1 -1 -1
*
1
n

"""
io = remote('crypto.challenge.bi0s.in',1221)
io.sendline(data)
io.recvuntil('flag')
io.recvuntil('flag')
buf = io.recv(2048)
if(b'inctf' in buf):
    print(buf)
    exit(0)
# inctfi{m4st3r_0f_Encrypt3d_0p3r4t1on5_B3c0m3_u_H4v3!!}
```

shell

```shell
❯❯ inctf  22:18 python3 -u "c:\Users\16953\Desktop\inctf\Encrypted Operations\src\exp.py"
[x] Opening connection to crypto.challenge.bi0s.in on port 1221
[x] Opening connection to crypto.challenge.bi0s.in on port 1221: Trying 34.106.211.122
[+] Opening connection to crypto.challenge.bi0s.in on port 1221: Done
b': inctfi{m4st3r_0f_Encrypt3d_0p3r4t1on5_B3c0m3_u_H4v3!!}\n\n\nThankyou for using the srvice! Sucessfully performed all operatoions!!\n\n\nExiting!!'
[*] Closed connection to crypto.challenge.bi0s.in port 1221
```











