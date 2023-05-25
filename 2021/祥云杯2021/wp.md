# WriteUp for crypto in 翔云ber 2021



> 👴第二次打翔云ber，周六玩了一天，周天来做了几个水题

![](https://gitee.com/ljahum/images/raw/master/img/20210822143809.png)





## **Random_RSA**

把代码反过来写就完事了

但是要注意题目random.seed是在python2环境下算出的数据。。。。有点坑了

然后常规解泄露dp

```python
e = 65537
n = 248254007851526241177721526698901802985832766176221609612258877371620580060433101538328030305219918697643619814200930679612109885533801335348445023751670478437073055544724280684733298051599167660303645183146161497485358633681492129668802402065797789905550489547645118787266601929429724133167768465309665906113
dp = 905074498052346904643025132879518330691925174573054004621877253318682675055421970943552016695528560364834446303196939207056642927148093290374440210503657
c = 140423670976252696807533673586209400575664282100684119784203527124521188996403826597436883766041879067494280957410201958935737360380801845453829293997433414188838725751796261702622028587211560353362847191060306578510511380965162133472698713063592621028959167072781482562673683090590521214218071160287665180751

import gmpy2
from Crypto.Util.number import *


dp = 5372007426161196154405640504110736659190183194052966723076041266610893158678092845450232508793279585163304918807656946147575280063208168816457346755227057
e=0x10001
n=81196282992606113591233615204680597645208562279327854026981376917977843644855180528227037752692498558370026353244981467900057157997462760732019372185955846507977456657760125682125104309241802108853618468491463326268016450119817181368743376919334016359137566652069490881871670703767378496685419790016705210391
c=61505256223993349534474550877787675500827332878941621261477860880689799960938202020614342208518869582019307850789493701589309453566095881294166336673487909221860641809622524813959284722285069755310890972255545436989082654705098907006694780949725756312169019688455553997031840488852954588581160550377081811151

for i in range(1,65538):
    if (dp*e-1)%i == 0:
        if n%(((dp*e-1)//i)+1)==0:
            p=((dp*e-1)//i)+1
            q=n//(((dp*e-1)//i)+1)
            phi = (p-1)*(q-1)
            d = gmpy2.invert(e,phi)%phi
            print(long_to_bytes(pow(c,d,n)))

# flag{74281db3-c6f0-e59a-4da6-39b8c71250fe}
```

## guess

> 这个题妥妥的被找到非预期了。。。。

### Analysis and implement

这个地方是非预期的核心这里会随机选取一个key附加上明文上

KEY比较特别的是，其中每个元素要么在KEY[R]上，要么在KEY[R+1]上，这是该非预期的基础

```python
            self._send("Give me m0.")
            plaintext1 = int(self._recv().decode())
            self._send("Give me m1.")
            plaintext2 = int(self._recv().decode())

            if (
                plaintext1 <= 2
                or plaintext2 <= 2
                or len(bin(plaintext1)) != len(bin(plaintext2))
            ):
                return
            R = 2 * random.randint(0, 39)
            I = random.randint(0, 1)
            cipher1 = enc(n, g, plaintext1 * plaintext2 * KEY[R])
            cipher2 = enc(n, g, plaintext1 * plaintext2 * KEY[R + 1])
            self._send("This is a ciphertext.")
            self._send(str([cipher1, cipher2][I]))
```

然后我们可以输入一次密文来得到明文,但不能输入cipher1和cipher2

```python
cipher = int(self._recv().decode())
            plaintext = str(dec(n, g, LAM, cipher))
            if int(plaintext) == plaintext1 * plaintext2 * KEY[R] or int(plaintext) == plaintext1 * plaintext2 * KEY[R+1]:
                return
            self._send("This is the corresponding plaintext.")
            self._send(plaintext)
```

根据同态的原理可以构造payload绕过检测

$C_0={C_1}^{m_1}=g^{m_1*m_1*m_2*k}r^n\;mod\;n^2$

解密后可以得到：

$M/(m_1*m_1*m_2) = k$

此时如果输入0如果报错则当前k对应的下标是0，否则下标为1

又因为

```python
assert key[0] == 119 and key[1] ==  241 and key[2] ==  718 and key[3] == 647
```

由这个hint我们知道服务器上面的key是不变的

只要重复访问服务器就能把key表oracle出来然后解得得key到我们记录的表里面去找就好了

### solution

```python

import random
import hashlib
from math import gcd
from pwn import *  
from icecream import *
from MyRE import CatNum
from itertools import product
# from MyRE import *
# from rich import *
from rich.traceback import install
install()
# -----------------------------------

String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz" 
# nc 47.104.85.225 57811



def pow1():
    io.recvuntil('?+')
    s2 = io.recvuntil(') ')[:-2]
    HASH = io.recvuntil('\n')[3:-1]
    print(s2)
    print(HASH)
    for i in product(String,repeat=4):
        s1 = ''.join(i)
        # print(s1.encode())\
        s1 = s1.encode()
        s0 = s1+s2
        # print(s0)
        HASH1 = hashlib.sha256(s0).hexdigest().encode()
        # print(HASH1)
        # input()
        if(HASH==HASH1):
            print(s1)
            io.sendline(s1)
            return
        
def enc(n, g, m):
    while 1:
        r = random.randint(2, n - 1)
        if gcd(r, n) == 1:
            break
    c = (pow(g, m, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)
    return c
def init():
    # pow1()
    # io.interactive()
    buf = io.recvuntil('round')
    round = io.recvuntil('Step 1')
    ic(round)
    io.recvuntil('KeyGen. This is my public key.')

    buf = io.recvuntil('Step ')
    ans = CatNum(buf)
    n,g = int(ans[0]),int(ans[1])
    ic(n)
    ic(g)
    
    return n,g
# =====================================

key0={130, 899, 903, 521, 142, 783, 530, 148, 416, 288, 550, 939, 427, 299, 558, 942, 685, 307, 566, 313, 577, 585, 718, 983, 349, 355, 611, 995, 614, 746, 751, 114, 498, 885, 119, 637, 638, 639}
key1={128, 129, 646, 647, 521, 780, 396, 526, 653, 400, 783, 530, 148, 918, 281, 158, 286, 416, 548, 550, 936, 810, 939, 427, 299, 558, 942, 944, 430, 307, 309, 566, 313, 186, 577, 201, 585, 461, 718, 333, 977, 727, 216, 983, 860, 355, 613, 614, 232, 745, 746, 877, 237, 241, 113, 114, 244, 885, 119, 888, 121, 123, 637, 638, 639}
def get_index(k):
    if(k in key0):
        return '0'
    else:
        return '1'

def oracle(n,g):
    
    io.recvuntil('Please give me one decimal ciphertext.\n')
    c = enc(n,g,123321123321123321123321)
    io.sendline(str(c))
    io.recvuntil('Step 3')
    io.recvline()
# s3
    m1 =  787
    m2 =  929
    io.recvuntil('Give me m0.\n')
    io.sendline(str(m1))
    io.recvuntil('Give me m1.\n')
    io.sendline(str(m2))
    
    io.recvuntil('This is a ciphertext.\n')
    buf = io.recvline()
    ans = CatNum(buf)
    c1 = int(ans[0])
    # print(buf,c1)
    # init


    x1 = enc(n,g,787)
    c1x1 = pow(c1,m1,n**2)
    # ic(c1x1)
    io.sendline(str(c1x1))

    io.recvuntil('This is the corresponding plaintext.\n')
    buf = io.recvline()
    # print(ans)
    ans = CatNum(buf)
    tmp = int(ans[0])
    io.recvuntil('-> c0 , m1 -> c1)?\n')
    k = (tmp)//(m1*m2*m1)
    ic(k)
    _01 = get_index(k)
    io.sendline(_01)
    res = io.recvline()
    print(res)
    # io.interactive()
    return res,k
    
time=0
# nc 47.104.85.225 57811
io = remote('47.104.85.225',57811)     
pow1() 
for i in range(100):
    
    
    
    n,g = init()
    res,k = oracle(n,g)

    if(b'Sorry' in res):
        print(f'{k}:0')
        key0.add(k)
        time=0
        io.close()
        io = remote('47.104.85.225',57811)   
        pow1()      
    else:
        sleep(0.25)
        print(f'{k}:1')
        key1.add(k)
        time+=1
    if(time==32):
        print('get it')
        print(io.recv(2048))
        exit()
    
    
    print(f'key0={key0}')
    print(f'key1={key1}')
    print(time)
   
```

---


```shell
ic| round: b' 32
           Step 1'
ic| n: 140359393736491083554637764633966036595869523810831521796100389946301014713501052438423015898275061604402441271059379191254720192715521217765512578594812234847906891823150303725078568490730815789232226736630007558775806211165296878777428640046549542601742670073385256102038588867770586061404269183834130922097
ic| g: 140359393736491083554637764633966036595869523810831521796100389946301014713501052438423015898275061604402441271059379191254720192715521217765512578594812234847906891823150303725078568490730815789232226736630007558775806211165296878777428640046549542601742670073385256102038588867770586061404269183834130922098
ic| k: 130
b'Good! You are right\n'
130:1
get it
b'flag{e87fdfb6-8007-4e1c-861f-5bde3c8badb3}\n'
[*] Closed connection to 47.104.85.225 port 57811
```

## myRSA

> 小数学题，利用各种姿势消去z对解密得影响

核心点

```python
def encry(message,key,p,q,e):
    k1,k2 = key[random.randint(0,127)],key[random.randint(0,127)]
    x = p**2 * (p + 3*q - 1 ) + q**2 * (q + 3*p - 1) 
    y = 2*p*q + p + q
    z = k1 + k2 
    c = pow(b2l(message),e,p*q)
    return x * c + y * c + z # enc
```

首先

$设t=p+q$

$(enc-z)/c=(x+y)-4n=t^3-t^2+t$

但由于  $f(t)=t^3-t^2+t-9999$   的图像在x轴四位数后几乎是一条直线，我们推断，此时z对于解这个方程没有实质性的影响

![](https://gitee.com/ljahum/images/raw/master/img/20210822150727.png)

测试后发现确实可以消去第一次加密时z的影响

解密时也可以用x+y消去z对flag的影响

`ic(z//(x+y))`



```python
from Crypto.Util.number import *
from Crypto.Util.number import getPrime,bytes_to_long as b2l
import libnum
from gmpy2 import iroot
from icecream import *
import sympy as sp  # 导入sympy包、

def getpq(n,e,enc,c):
    tmp = 400000
    ic(tmp)
    ans = enc//c -tmp -4*n
    
    x = sp.Symbol('x')  # 定义符号变量
    f = x**3 - x**2 + x - ans  # 定义要求解的一元三次方程
    ans = sp.solve(f)
    # print(ans)
    
    t = int(ans[2].round())
    ic(t)
    tmp = iroot(t*t-4*n,2)
    ic(tmp)
    if(tmp[1] == True):
        delta = tmp[0]
        p = (t+delta)//2
        ans = t**3 - t**2 + t
        print(n%p)
        ic(p)
        return p
# 一次交互后得到的数据
n = 66027874281672625418586014781126070908243950646389324074550248999679090401150270793389452270314828298481437497840416396018574761898600856029902467560028361877554457938912404358968210921272837218306889478597234820590780596868027285957738861052042217870708996313230729115851397741357365848182263953315379303203
e = 65537
message = b'1231231312312312313123'
c = pow(b2l(message),e,n)
enc = 2786282534107784071949674754303734020650420550514064517704448066809278965224884310691670432441397979710035489386642473027744366146283566077172758576117265010888225901430814453103910642061532363684990980080593171873048076522753507082554621333455105446034271978972878134597921516292423901550995709181303022297139396128082022193615685724911328311390083321186035987746342068856533118816750276771278003232809361817465525887406183533073435476911136829775173155132394236172457900926847903014330722145729653282601258124899631596559793043199596264295846181613188399943356771658381560774428425036945242894731920547142207496951001372212394788053725065262462489938796299464287972476543278196732420981982981923866883740677815684307375214870832207719694203331026829445710224285190480
flagenc = 78903156043541822956852921255839504785260043170754244208159263853595508405000661899479307588531494172830632220991906679919999441798497272603229277113581316208572288228086544225197245626229321664099299589135332933949675253738548931053641537046898654150676091285693057337873250759686984233682913388477992334871253653295943818266597281224943136933411417199795127815822097900855479634034406709830823051590719193303685067733559940313006125179805670789881285419162909762014157603424444680011222474284489067733520824336575376527926069324059697680207015464280592590151869974781941122398578485426146276184697907560587701585522746826606269636562989809117072089021357481402267496699431701068851120069674664273560247308363437176623358041554600504472302094490793591097239195676611890
# =========================
p =getpq(n,e,enc,c)
q = n//p
print(n==p*q)
# k = k1+k2    
x = p**2 * (p + 3*q - 1 ) + q**2 * (q + 3*p - 1) 
y = 2*p*q + p + q
z = enc-(x+y)*c
print(z)
# print(z==k)

flagc = (flagenc)//(x+y)
ic(z//(x+y))

# q=n//p
# print(q)
# n=p*q
phi=(p-1)*(q-1)

d = libnum.invmod(e,phi)
print(long_to_bytes(pow(flagc,d,n)))
# bytes_to_long()
# long_to_bytes()
'''
return x * c + y * c + z
'''
# flag{ed649951-9ce9-46e0-a42b-d0ba588e43e1}
```

## Challenge-attachment



<img src="https://gitee.com/ljahum/images/raw/master/img/20210822143313.png" style="zoom:50%;" />