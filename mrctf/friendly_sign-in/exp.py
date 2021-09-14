# from outputdata import *
# from data import Ns
from itertools import product
from hashlib import sha512
# from Crypto.Util.number import *
from Crypto.Util.number import *
from libnum import lcm
from pwn import *
import string
tot_ans=[]
sh = remote('nairw.top',4800)
# sh = remote('0.0.0.0', 10000)
flag=[]

def sendans(ans):
    print(len(ans))
    for i in ans:
        sh.sendline(str(i))
    print('send done')
    buf = (sh.recv(1024))
    print(buf)
    flag.append(buf)
    
    # sh.interactive()

def pow1():
    buf = sh.recvuntil(' SHA512(\"')
    s1 = sh.recvuntil('" +')[:-3]
    print(s1)
    tab = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for i in product(tab, repeat=4):
        s2 = bytes(i)
        m = (s1+s2)
        if sha512(m).hexdigest().startswith("11111"):
            print(m)
            sh.sendline(s2)
            print(sha512(m).hexdigest())
            break
    

def check_ans(_N, _x) -> bool:
    check = 0
    for i in range(len(_N)):
        check += _N[i] * _x[i]
    return check == 0


def main(Ns):
    LCM = Ns[0]
    print(len(Ns))
    # input('ctn')
    for i in range(1, len(Ns)):
        LCM = lcm(Ns[i], LCM)

    ans=0
    t=0
    send= []
    print(sh.recv(1024))
    for i in range(0,len(Ns),2):
        # print('result:',LCM%Ns[i])
        send.append(-(Ns[i+1]))
        send.append((Ns[i]))
        # if(t&1==1):
        #     # ans += -(Ns[i]*(LCM//Ns[i]))
        #     send.append(-(LCM//Ns[i]))
            
        # else:
        #     # ans += (Ns[i]*(LCM//Ns[i]))
        #     send.append(LCM//Ns[i])
        # t+=1
    # print(ans)

    # ==================
    for i in range(1,224+1):
        for j in range(len(send)):
            send[j]=send[j]*i
        print(f'cheak:{check_ans(Ns, send)}',i)
        sendans(send)
        

if __name__ == '__main__':
    pow1()
    print(sh.recvuntil('N = ['))
    buf = (sh.recvuntil(']'))[:-1].decode()
    
    buf = (buf.split(','))
    Ns = []
    for i in buf:
        Ns.append(int(i))
    # print(Ns)
    main(Ns)
    print(flag)
    
