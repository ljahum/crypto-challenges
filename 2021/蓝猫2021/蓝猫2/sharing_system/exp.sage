from itertools import product
from pwn import *
from icecream import *
from hashlib import sha256
# nc 118.190.62.234 52863
r = remote('0.0.0.0',20001)
r = remote('118.190.62.234',52863)
from time import *

def gopow():
    # print(r.recv(1024))
    r.recvuntil('sha256(XXXX+')
    s1 = r.recvuntil(') == ')[:-5]
    hashstr = r.recvline()[:-1]
    print(r.recvuntil('Give me XXXX >'))
    print(s1,hashstr)
    tab = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in product(tab,repeat=4):
        tmp = ''.join(i)
        s0 =  bytes(tmp,encoding='utf-8')
        s = s0+s1
        hash_value = sha256(s).hexdigest()
        hash_value = bytes(hash_value,encoding='utf-8')
        if hash_value == hashstr:
            print(hash_value)
            ic("XXXX=",s0)
            ic(hash_value,hashstr)
            print(r.recv(2048))
            r.sendline(s0)
            break

gopow()


buf = r.recv(1024)
print(buf)
buf = r.recvuntil('Enter option > ')
print(buf)
r.sendline('1')

buf = r.recvline() # p
print(buf)
p = int(buf[3:-1])
print(p)

buf = r.recvuntil('key = (') # key1
x1 = r.recvuntil(', ')
y1 = r.recvuntil(')\n')
print(buf,x1,y1)

buf = r.recvuntil('Enter option > ')
print(buf)
r.sendline('2')

buf = r.recvline() # p
# print(buf)
p = int(buf[3:-1])
# print(p)

buf = r.recvuntil('key = (') # key1
x2 = r.recvuntil(', ')
y2 = r.recvuntil(')\n')
print(buf,x1,y1)

x1 = int(x1[:-2].decode())
y1 = int(y1[:-2].decode())
x2 = int(x2[:-2].decode())
y2 = int(y2[:-2].decode())
ic(x1)
ic(x2)
ic(y1)
ic(y2)
ic(p)
keys1 = [[x1,y1]]
keys2 = [[x2,y2]]
def getXY():
    for i in range(1,50):
        # print(r.recvuntil('Enter option > ').decode())
        r.sendline('3')
        r.recvuntil('umber (1-49) > ')
        r.sendline(str(i))
        r.recvuntil('key = (')
        x = int(r.recvuntil(', ')[:-2])
        y = int(r.recvuntil(')\n')[:-2])
        # print(x,y)
        keys1.append([x,y])


def getts(key):
    keys_1 = key
    XS=[]
    for i in range(49):
        xi = keys_1[i][0]
        xi_1 = keys_1[i+1][0]
        xs=[]
        for j in range(49):
            x1 = pow(xi,j+1,p)
            x2 = pow(xi_1,j+1,p)
            tmp = (x1-x2)%p
            xs.append(tmp)
        XS.append(xs)

    YS =[]
    for i in range(49):
        yi = keys_1[i][1]
        yi_1 = keys_1[i+1][1]
        YS.append([(yi-yi_1)%p])
    # print(YS)
    X = Matrix(Zmod(p),XS)
    Y = Matrix(Zmod(p),YS)
    invx = X.inverse()
    T = invx*Y
    # print(ts)

    TS = [i[0] for i in T]
    
    return TS


getXY()
print(keys1)
print(len(keys1))

# t = 58510083877094693891040277851267905853617844771064576929521712771940231668984770883328421254238895212042598002659174059244201616561130950785238401399837559644941651285130352373844849078590789578028528768860166902952495931639692465443534927973027133719331474369633030490640443060779278904144461746302422307614
# ts = [ t for _ in range(50 - 1)]
ts = getts(keys1)

tmp1=0
for i in range(0,49):
    XS = pow(x1,i+1,p)*ts[i]
    tmp1 = (tmp1 + XS)%p
k1 = (y1 - tmp1)%p

tmp2=0
for i in range(0,49):
    XS = pow(x2,i+1,p)*ts[i]
    tmp2 = (tmp2 + XS)%p
k2 = (y2 - tmp2)%p

ic(k1,k2)
# print(r.recv(1024))
print(r.recvuntil('Enter option > '))
r.sendline('5')


print(r.recvuntil('Please enter secret 1 > '))
r.sendline(str(k1))
print(r.recvuntil('Please enter secret 2 > '))
r.sendline(str(k2))
sleep(1)
print(r.recv(1024))
# nflag{0c10bc45-cb3b-4648-b11d-d8aa85f5e63b}