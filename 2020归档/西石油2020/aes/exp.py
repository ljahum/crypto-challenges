import tcphum
tcp = tcphum.remote('das.wetolink.com', 42888, timeout=0.5)
s = tcp.recv_all()
print(s)
tcp.sendline(b'1')
s = tcp.recv_all()
print(s)
tcp.sendline(b'tcphum==========')

s = tcp.recv_until(b'Here is your token(in hex): ')
print(s)

s = tcp.recv_until(b'\n\n')[:-2]
print(s)
s = tcp.recv_all()
print(s)
tcp.sendline(b'2')
s = tcp.recv_all()
print(s)
token2 = bytes(input('token2='), encoding='utf-8')
print(token2)
tcp.sendline(token2)
s = tcp.recv_until(b'Hello, ')
print(s)
s = tcp.recv_until(b'\n\n')[:-2]
print(s) # m3
print(len(s))

s = tcp.recv_all()
print(s)
tcp.sendline(b'2')
s = tcp.recv_all()
print(s)
token3 = bytes(input('token3='), encoding='utf-8')
print(token3)
tcp.sendline(token3)
s = tcp.recv_all()
print(s)
