from hashlib import sha256
import string
from itertools import product
import re
from socket import *


host = '42.192.180.50'
port = 30002
buf = 1024
addr = (host, port)

tcp = socket(AF_INET, SOCK_STREAM)
tcp.connect(addr)
s = tcp.recv(buf)
print(s)
s = s.decode()
HASH1 = re.match(r'SHA256\(\"(.*)" \+', s).group(1)


# HASH1 = 'LaBgtOQt'

table = string.ascii_letters + string.digits

for i in product(table, repeat=4):
    HASH2 = ''.join(i)
    guess = HASH1 + HASH2
    # print(guess)
    if sha256(guess.encode()).hexdigest()[0:5] == '00000':
        # print(sha256(guess.encode()).hexdigest())
        print(guess)
        print(HASH2)
        send_bytes = bytes(HASH2+'\n',encoding="utf-8")
        
        tcp.send(send_bytes)
        # input()
        break

 # read line


tcp.send(b"bless\n")
tcp.send(b"1\n")
s = tcp.recv(buf)
print(s)
s = tcp.recv(buf)
print(s)
s = tcp.recv(buf)
print(s)

# s = tcp.recv(buf)
# print(s)
