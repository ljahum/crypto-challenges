from pwn import *
from string import printable
from icecream import *
io = remote('127.0.0.1', 10001)
tab = (printable)
flag_len = 8
BLOCKSIZE = 16


def pad(data):
    data = bytes(data, encoding='utf-8')
    pad_len = BLOCKSIZE - (len(data) %
                           BLOCKSIZE) if len(data) % BLOCKSIZE != 0 else 0
    return (data + bytes([pad_len]) * pad_len).hex()


io.sendline(b'')
io.recvuntil(b'Amazing function: ')
buf = io.recvline()[:-1]
len_flag = len(buf)
for i in range(1, 16+1):
    io.sendline(b'aa'*i)
    io.recvuntil(b'Amazing function: ')
    buf = io.recvline()[:-1]
    if(len(buf) != len_flag):
        len_flag = (len_flag//2-i+1)
        break
    



flag_ = ''
for i in range(11, 49+1):

    io.sendline('aa'*i)

    io.recvuntil(b'Amazing function: ')
    buf = io.recvline()[:-1]
    # print('----------------------------')
    # for j in range(0, len(buf), 32):
    #     print(buf[j:j+32])
    # print('---------------------------')
    # print(buf)
    cipher = buf[96:128]

    for _ in tab:
        # print(_+flag_)
        payload = pad(_+flag_)

        io.sendline(payload)
        io.recvuntil(b'Amazing function: ')
        buf2 = io.recvline()
        # print(buf2)
        buf2 = (buf2[:32])
        # print(_)
        # print(buf2,cipher)
        if(buf2 == cipher):
            _ += flag_
            flag_ = _
            print(flag_)
            break
    # input()

print(flag_)
exit(0)

