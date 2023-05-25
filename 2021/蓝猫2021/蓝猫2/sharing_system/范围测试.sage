
# import string
# import random
# import socketserver
# import signal
# import codecs
import time
p1 = time.time()

from os import urandom
from hashlib import sha256
from random import randint
from Crypto.Util.number import inverse, getPrime, getRandomInteger
from icecream import *
n = 50
p = 127100161070729758324672563005919585088843557718198754483704240637539097558639707938939488773101162471030823228170890483077236346261016177325635908356835505581986535187340920340593665014827853496914359725363307847082205643499778919067969907971712520095774370034152191123554145608254118099051528821309936123263
# ts = [randint(1, p - 1) for _ in range(n - 1)]
t = 58510083877094693891040277851267905853617844771064576929521712771940231668984770883328421254238895212042598002659174059244201616561130950785238401399837559644941651285130352373844849078590789578028528768860166902952495931639692465443534927973027133719331474369633030490640443060779278904144461746302422307614
ts = [ t for _ in range(n - 1)]
secret_1 = getRandomInteger(256)
secret_1 = 32356368081981984303650022185405262362706441106255860481013566773788039706726

def init_keys(ts, data, p):
    n = len(ts) + 1
    keys = []
    for _ in range(n):
        x = getRandomInteger(1024)
        y = data
        for i in range(n - 1):
            y = (y + ts[i] * pow(x, i + 1, p)) % p
        keys.append([x, y])
    return keys
ic(len(ts))
keys_1 = init_keys(ts, secret_1, p)

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
    # print(TS)
    ic(TS == ts)


    p2 = time.time()
    # print(f'p2-p1 {s}')
    return TS
ts = getts(keys_1)
print(len(ts))


def gopow():
    s1 = b'JXXCe9pJLSpr'
    hashstr = b'510f0df96af2ec7a9ed321ef2158312095041920699402c73c8e3014d8e73c38'
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