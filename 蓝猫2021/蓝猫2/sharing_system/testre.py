from pwn import *

import re

def CatData(txt,s1,s2):
    if(type(txt)==bytes):
        txt=txt.decode()
    if(type(s1)==bytes):
        s1=s1.decode()
    if(type(s2)==bytes):
        s2=s2.decode()
    
    s = r'(?<='+s1+').*?(?='+s2+')'
    matchObj = re.findall(s, txt)
    return matchObj

# 选取长度大于n的数字字符
def CatNum(txt,length):
    if(type(txt)==bytes):
        txt=txt.decode()
    matchObj = re.findall(r'[0-9a-fA-F]{'+str(length)+r',}', txt)
    return matchObj

sh  = remote('0.0.0.0',20001)
sleep(1)
# print(sh.recv(1024))

print(sh.recvuntil("ion > "))
sh.sendline('1')
p = sh.recvline()
print(p)
p = CatNum(p)[0]
print(p)
# key = sh.recvline()
# key1 ,key2 = CatNum(key)
# print(p)
# print(key1,key2)




