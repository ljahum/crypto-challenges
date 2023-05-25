## guess

分析key.sage和题目源码可以推断服务器上的key文件可能是不变的

```python
hint = Matrix(key * vector([getRandomNBitInteger(1024) for _ in range(4)]) for _ in range(12))
open('key','w').write(str(key))
open('hint','w').write(str(hint))
```



```python
assert key[0] == 119 and key[1] ==  241 and key[2] ==  718 and key[3] == 647
```

分析step4可以发现这个检测可以稍微绕一下将KEY[R]或者KEY[R+1]恢复出来

```python
# step 4. Phase 2

            self._send(
                "Step 4 - Phase 2. Now, you can give me some ciphertexts,I will return the corresponding plaintext.But you can not give me the ciphertext that I give you in step 3."
            )
            self._send("Please give me one decimal ciphertext ")
            cipher = int(self._recv().decode())
            plaintext = str(dec(n, g, LAM, cipher))
            if int(plaintext) == plaintext1 * plaintext2 * KEY[R] or int(plaintext) == plaintext1 * plaintext2 * KEY[R+1]:
                return
            self._send("This is the corresponding plaintext.")
            self._send(plaintext)
```

分析cipher的生成可以发现没一个 KEY 对应的 I是不变的，我们只需要一次次把每一个KEY[R]恢复出来并通过服务器判断它对应的是1还是0就可以了

```python
			R = 2 * random.randint(0, 39)
            I = random.randint(0, 1)
            cipher1 = enc(n, g, plaintext1 * plaintext2 * KEY[R])
            cipher2 = enc(n, g, plaintext1 * plaintext2 * KEY[R + 1])
            self._send("This is a ciphertext.")
            self._send(str([cipher1, cipher2][I]))
```

exp

```python
import hashlib
from math import gcd
from pwn import *  
from itertools import product
# KEYSIZE = 512

def getnumber(txt):
    if(type(txt)!=str):
        txt = txt.decode()
    matchObj = re.findall(r'[0-9]+', txt)
    return matchObj

def gopow():
    String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz" 
    print('start pow')
    sh.recvuntil('?+')
    s2 = sh.recvuntil(') ')[:-2]
    s3 = sh.recvuntil('\n')[3:-1]
    for i in product(String,repeat=4):
        s1 = ''.join(i)
        s1 = s1.encode()
        s0 = s1+s2

        if(s3==hashlib.sha256(s0).hexdigest().encode()):
            print(s1)
            print('pow done')
            sh.sendline(s1)
            return
        
def enc(n, g, m):
    while 1:
        r = random.randint(2, n - 1)
        if gcd(r, n) == 1:
            break
    c = (pow(g, m, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)
    return c

def attack(n,g):
    c = enc(n,g,123456789123456789123456789)
    m1 =  0x10001
    m2 =  0x10001
    
    sh.recvuntil(' one decimal ciphertext.\n')
    sh.sendline(str(c))
    sh.recvuntil('Step 3')
    sh.recvline()
    sh.recvuntil('Give me m0.\n')
    sh.sendline(str(m1))
    sh.recvuntil('Give me m1.\n')
    sh.sendline(str(m2))
    sh.recvuntil(' ciphertext.\n')
    c1 = int(getnumber(sh.recvline())[0])
    c3 = pow(c1,m1,n**2)
    sh.sendline(str(c3))
    sh.recvuntil('corresponding plaintext.\n')
    
    tmp = int(getnumber(sh.recvline())[0])
    sh.recvuntil('m1 -> c1)?\n')
    k = (tmp)//(m1*m2*m1)
    sleep(0.1)
    sh.sendline(str(check(k)))
    res = sh.recvline()
    return res,k
List1=set()
List2=set()

List1={130, 899, 903, 521, 142, 783, 271, 530, 148, 288, 416, 550, 299, 939, 427, 685, 558, 942, 307, 566, 184, 313, 577, 585, 718, 983, 349, 355, 995, 611, 614, 746, 751, 498, 114, 885, 119, 637, 638, 639}
List2={128, 641, 129, 647, 780, 148, 286, 158, 548, 810, 427, 939, 685, 430, 307, 201, 333, 983, 216, 355, 614, 232, 746, 241, 113, 885, 888, 123}

def check(k):
    if(k in List1):
        return 0
    else:
        return 1

# nc 47.104.85.225 57811
sh = remote('47.104.85.225',57811)     
gopow() 
wins = 0
for i in range(40):
    buf = sh.recvuntil('round')
    round = sh.recvline()[:-1]
    sh.recvuntil('Step 1')
    print(f'round {round.decode()}')
    sh.recvuntil('KeyGen. This is my public key.')
    buf = sh.recvuntil('Step 2')
    ans = getnumber(buf)
    n,g = int(ans[0]),int(ans[1])
    
    res,k = attack(n,g)
    print(res)
    sleep(0.1)
    if(b'Good' in res):
        wins +=1
        print(f'List2.add({k})')
        List2.add(k)      
    else:
        wins = 0
        print(f'List1.add({k})')
        List1.add(k)
        sh.close()
        sh = remote('47.104.85.225',57811)   
        gopow()
        
    print(f'wins {wins}')
    if(wins==32):
        print(f'List2={List2}')
        print(sh.recv(2048))
        exit()
    
print(f'List1={List1}')
print(f'List2={List2}')

```

