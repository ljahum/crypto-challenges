from icecream import *
from Crypto.Util.number import *
from pwn import *
from MyRe import *
io= remote('1.14.95.121',9999)

# io=remote('0.0.0.0',10001)
# # print(io.recv(1024))
# 公钥手动拿一下吧

def unpadding(key):
    padding = key[-1]
    if(padding==0):
        return key,False
    for i in range(padding):
        if key[-i-1]!=padding:
            return key,False
    key = key[:-padding]
    return key,True


def IOfunc1(cip,iv):
    io.sendline(b"1")
    print(io.recv(1024))
    io.sendline(cip.hex().encode())
    print(io.recv(1024))
    io.sendline(iv.hex().encode())
    buf = io.recv(1024)
    print(buf)
    if(b'fake token' not in buf):
        print('yes')
        return True
    else:
        print("NO")
        return False

def stage1():
    fake_iv =b'0000000000000000'
    iv = origin_Iv
    mid= b''
    iv2= b''
    paddingLen=8
    for i in range(1,16+1):
        for fake_p in range(256):
            if(fake_p!=iv[-i] or i == paddingLen):
                tmp= bytes([fake_p])
                fake_iv=fake_iv[:-i]+tmp+iv2
                print(fake_iv,len(fake_iv))

                flag = IOfunc1(cipher,fake_iv)
                if(flag==False):
                    pass
                else:
                    mid_i= bytes([tmp[0]^(i)])
                    iv2 = tmp+iv2
                    iv2 = bytes([c^(i+1)^i for c in iv2])
                    print(iv2)
                    mid = mid_i+mid
                    break
    return mid

def getPUBKEY(origin_Iv,cipher):

    io.sendline(b'1')
    io.sendline(cipher.encode())

    io.sendline(origin_Iv.encode())
    print(io.recvuntil(b'0.0'))
    # b'\nN 0x9160397ebb06ccd89e9c759aa480bd4056560d622afa0a075c1751b18d9dd753f2892b5accbdcd194152ddd9014256c7421aa267769a61f2b1ed95c716f48c55\nE 0x10001\nc 1150782913519495523247129474108102034654763948774946193082900200029884260448771943553673742518413351682323397604890552672079416129502234917521602130879788\n\n1.check\n2.admin\n\n>'
    io.recvuntil(b'\nN')
    buf = io.recvline()
    # io.recvuntil(b'\nN')
    print(buf)
    N = int(CatHex(buf)[1],16)

    buf = io.recvline()
    print(buf)
    E = int(CatHex(buf)[2],16)
    buf = io.recvline()
    print(buf)
    c = int(CatNum(buf)[0],10)

    ic(    hex(N),E,c    )
    return N,E,c




io.recvuntil('token')
buf = io.recv(1024)
print(buf)
a = CatHex(buf)
print(a)
cipher = a[0]
origin_Iv= a[1]
N,E,c = getPUBKEY(origin_Iv,cipher)

cipher = bytes.fromhex(cipher)
print(cipher)
origin_Iv = bytes.fromhex(origin_Iv)
print(origin_Iv)

io.interactive()
# ============================================
# exit()
mid = stage1()


print("mid=",mid,len(mid))
sysKEY,_ = unpadding(long_to_bytes(bytes_to_long(mid)^ bytes_to_long(origin_Iv)))
print(sysKEY)
input()

N_str = hex(N)[2:]
c_str= hex(c)[2:]
ic(N_str)
input()
def bigger(pmid,c):
    tmp = (c*pow(pmid,E,N))%N
    tmp = long_to_bytes(tmp)
    c_str = tmp.hex().encode()
    #
    io.sendline(b'2')
    buf = io.recv(1024)
    # print(buf)
    io.sendline(N_str)
    io.sendline(c_str)
    io.recvuntil(b"[yes/no]")
    io.sendline(b'yes')
    buf = io.recvuntil(b"input admin password:")

    io.sendline(sysKEY.hex().encode())
    io.recvuntil(b'>')
    buf = io.recvline()

    print(io.recvuntil(b'1.check'))
    #
    leak_m = buf[:4]
    ic(leak_m)
    if(leak_m!=b'0000'):
        return True
    else:
        return False

# pad=240~260
pl = 2**240
ph = 2**260
pmid= (pl+ph)//2
input()
limit_n=2**496
for i in range(512):

    if(bigger(pmid,c)==True):

        ph=pmid-1
        pmid = (pmid+pl)//2
    else:
        pl=pmid+1
        pmid  =(pmid+ph)//2
    print(pmid)
gogogo = long_to_bytes(limit_n//pmid)[:16]
print(gogogo)
print(gogogo.hex())
io.interactive()

