## secret_share

> 下午来推了一半就出去吃东西去了😘😘
>
> 看了wp发现只要几个步骤串起来其实不难的，可能是因为我只会炼丹吧。。。

基本加解密：

enc

$E = g^e\mod p,V=g^v\mod p\ s = v+e(h2(E||V))$

$c = m*pk^{e+v}\mod p$

r_enc:

$E_- = g^{e\times skI\times dd} , V_-=g^{v\times skI\times dd}$

$E = g^{e},V=g^{v}$

$c = m\times (EV)^{skI}\mod p =m\times (E_-V_-)^{inv(dd,p-1)}\mod p$

这里拿到dd就可以搞解密了，解dd的前提是吧encoder搞清楚

encoder当时没细看，其实变化写完了一看就很简单了

>  照着👴们的消元学习了

连续4次推得sk拿到随机出来的m可以得到

$mul={sk}^4*dd_1*dd_2*dd_3*dd_4\%p$

$dd_i$是已知的,有些solve是域下开根

有些是神仙炫技直接 韦达定理 或者 费玛大定理



![](https://gitee.com/ljahum/images/raw/master/img/20210830211519.png)



拿到单独的sk后就可以搞事情了

EV都是已知，c也已知 直接算就🆗了

solve-step1

```python
from Crypto.Util.number import *
from icecream import *
from hashlib import sha256
from gmpy2 import *
import libnum
from pwn import *
from libnum import *
def h2(m):
    return int(sha256(m).hexdigest(), 16)

io=remote('0.0.0.0',10001)


#1
io.recvuntil('choice>')
io.sendline('1')
io.recvuntil('Please take good care of it!\n')
pk_sk=io.recvuntil('\n')[:-1].decode()[2:-1].split('L,0x')
pk,sk=int(pk_sk[0],16),int(pk_sk[1],16)

#2
io.recvuntil('choice>')
io.sendline('2')
pp, g = 0xb5655f7c97e8007baaf31716c305cf5950a935d239891c81e671c39b7b5b2544b0198a39fd13fa83830f93afb558321680713d4f6e6d7201d27256567b8f70c3, 0x85fd9ae42b57e515b7849b232fcd9575c18131235104d451eeceb991436b646d374086ca751846fdfec1ff7d4e1b9d6812355093a8227742a30361401ccc5577
group_list = [32, 64, 128, 256]
DD=1
for group in group_list:
    io.recvuntil('The cipher shared to you\n')
    cc=int(io.recvuntil('L, ')[1:-3])
    new_cipher=[cc]
    new_cipher+=eval(io.recvuntil(')\n')[:-2].decode().replace('L',''))
    c,E_,V_,s_=new_cipher

    io.recvuntil('prefix, encoder = ')
    Enc2,prefix=pre_enc=eval(io.recvuntil('\n')[:-1].decode().replace('L',''))
    prefix=int(prefix,16)
    encoder=[1,(-pow(prefix,sk,pp)) %pp]
    prefix = long_to_bytes(prefix).rjust(64, b'\x00')

    ml=[1]
    for i in range(len(Enc2)):
        ml.append((ml[-1]*encoder[-1]+Enc2[i]*(-1)**(i+1))%pp)
    r=-ml[-1]%pp
    dd = h2(prefix + long_to_bytes(r).rjust(64, b'\x00')) | 1
    DD*=dd
    d=libnum.invmod(dd,pp-1)
    tmp=E_*V_%pp
    xx=pow(tmp,d,pp)
    m=c*libnum.invmod(xx,pp)%pp
    io.send(hex(m)[2:])
io.recvuntil('You are a clever boy! Now I can share you some other information!\n0x')
mul=int(io.recvuntil('\n')[:-2],16)


ic(DD)
ic(mul)

#3
io.recvuntil('choice>')
io.sendline('3')
cc=int(io.recvuntil('L, ')[1:-3])
cipher=[cc]
cipher+=eval(io.recvuntil(')\n')[:-2].decode().replace('L',''))
ic(cipher)
```

solve-step2

```python
from gmpy2 import *
io=0xb5655f7c97e8007baaf31716c305cf5950a935d239891c81e671c39b7b5b2544b0198a39fd13fa83830f93afb558321680713d4f6e6d7201d27256567b8f70c3
D=15987058835088036058838351739905403758810826722245822649290306549906899936826738229650730140126509371862930340608846190807298868677166971678478129606238898364288362139315516922003581996769819030117310508402522153899137933429897987557331966070437119010259514160059698255241259153692392463260794449949596746727
mul=7194716155235037744823597029059822446255314248196377746260315999958188811928743123657567494196521690514320209430663462342437059567384744437239548754416135
c=mul*libnum.invmod(D,io)%io
e=4
R.<x> = Zmod(io)[]
f = x ^ e- c
f = f.monic()
res1 = f.roots()
print(res1)

```



solve-step3
```python
from Crypto.Util.number import *
from gmpy2 import *
pp=0xb5655f7c97e8007baaf31716c305cf5950a935d239891c81e671c39b7b5b2544b0198a39fd13fa83830f93afb558321680713d4f6e6d7201d27256567b8f70c3
sk=3415391405045794570454819264678842883406589094879440924771251075986414212665514615692960890299627279215019657097231396800926908716766924569917256830117771
cipher=[1452085683981538837849557434841689674477096081702343000869186835544808468459192026693029532721465657214194362000756249662047209552808256166535501585736401, 9299317806552199012103361766715291248186887467752322286719294121971787657296205598139365760833959784768412272593061318430853065277862724140493914797711689, 9287316455075844376168558534606543590293095721271733423230961724912040658757071778242087450272981713664977773510705690081763692753388091475741636185572383, 229110517869350912236518454062717456777603700368163296438479618211042488031942897036793380693680124455343059560507824269299022538059530971380675264277197]
c,E,V,s=cipher
xx=E*V%pp
m=c*libnum.invmod(pow(xx,sk,pp),pp)%pp
print(long_to_bytes(m))
#flag{504d0411-6707-469b-be31-9868200aca95}
```

学到很多





