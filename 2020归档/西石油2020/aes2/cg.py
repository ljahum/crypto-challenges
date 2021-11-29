from Crypto.Cipher import AES
from gmpy2 import *
from Crypto.Util.number import *
# das.wetolink.com 42887

BLOCKSIZE = 16
def pad(data):
        pad_len = BLOCKSIZE - (len(data) %
                               BLOCKSIZE) if len(data) % BLOCKSIZE != 0 else 0
        return data + bytes([pad_len]) * pad_len
key = b'1'*16
m = 'tcphum=========='
name = 'admin==========='
aes = AES.new(key,AES.MODE_ECB)
m = b'a'*32
print(m.hex())
    
c = '7133b8a7b39eead68b05078806e14adcc229b4cd36b1a8499a1ed0728f0c132fa7c1f7b35365aceda9d563f41f244ac0bd990aaeb76f3e467a13d4e7803920c3'
c = bytes.fromhex(c)
print(len(c))
print(c[:16])
print(c[16:32])
print(c[32:48])
print(c[48:64])
# print(c[64:80])
# print(c[80:96])
# b'\xbc\xa0\xeeD\x99I\xf5P\x0fL\xd1\x92\xb23\xfc\xd2'
print(pad(b'}').hex())
