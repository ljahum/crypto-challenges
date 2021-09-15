## 蓝帽ber final



### twobyte

> 二分法

传入$C\times padding^e$



利用高位的two bytes判断$M\times padding和2^{496}$的大小关系(512-16=496)

利用二分法查找padding的值

查找约1000+次可以恢复secret

#### solve

```python
from subprocess import run
from Crypto.Util.number import long_to_bytes
from icecream import *
from pwn import *
import re

from pwnlib.util.iters import pad
def b2s(s):
    if(type(s)==str):
        return s
    else:
        return s.decode()

def CatNum(txt):
    txt = b2s(txt)
    matchObj = re.findall(r'[0-9]+', txt)
    return matchObj



def dec(n):
    print(io.recvuntil('Your choice: '))
    io.sendline('1')
    print(io.recvuntil('Your cipher: '))
    io.sendline(str(n))
    return io.recvline()[:-1]
def bigger(mid,c):
    # tmp1 = pow(mid,e,n)
    # ic(tmp1)
    tmp = (c*pow(mid,e,n))%n
    print(tmp)
    # ic(padding)
    m = dec(tmp)
    ic(m)
    if(m!=b'0000'):
        return True
    else:
        return False


io=remote('0.0.0.0',10001)
# print(io.recv(1024))
io.recvuntil('PKCS1_v1_6?(y/n)')
io.sendline('n')
e = int(CatNum(io.recvline())[0])
n = int(CatNum(io.recvline())[0])
c = int(CatNum(io.recvline())[0])
ic(e,c,n)

'''估算padding范围
padding = 1
h = 0
for i in range(512):
    tmp1 = pow(padding,e,n)
    ic(tmp1)
    tmp = (c*tmp1)%n
    print(tmp)
    ic(padding)
    m = dec(tmp)
    ic(m,i)
    if(m!=b'0000'):
        h=i
        input()
        break
    padding *= 2

'''


# pad=240~260
pl = 2**200
ph = 2**496
mid= (pl+ph)//2
input()
for i in range(512):
    # tmp = m*mid
    # ic(tmp-n)
    if(bigger(mid,c)==True):
        ph=mid-1
        mid = (mid+pl)//2
    else:
        pl=mid+1
        mid  =(mid+ph)//2
    # print(mid)
    # input()
ic(mid)
n=2**496
s =n//mid
secret = long_to_bytes(s)
ic(secret)
ic(secret.hex())
print(io.recvuntil('Your choice: '))
io.sendline('2')
io.sendline(secret.hex())
sleep(0.5)
print(io.recv(1024))

```



````shell
b'Your choice: '
b"You know my secret? (in hex): b'flag{ba1f2511fc30423bdbb183fe33f3dd0f}'\n"
[*] Closed connection to 0.0.0.0 port 10001
  /mnt/c/U/16953/Desktop/twoBytes took  11s at  11:38:42 AM
❯
````