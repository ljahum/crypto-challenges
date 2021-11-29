from pwn import *
io = remote('127.0.0.1', 10001)
buf = io.recv(1024)
print(buf)
io.sendline(b'aa')
buf = io.recvline()
print(buf)