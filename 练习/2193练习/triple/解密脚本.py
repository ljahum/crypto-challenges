from Crypto import Random
from Crypto.Cipher import AES
import base64
from hashlib import md5
from base64 import *
BLOCK_SIZE = 16



# https://blog.csdn.net/weixin_39912163/article/details/111422488


def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]



def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(encrypted[16:])


s1 = b'U2FsdGVkX19QwGkcgD0fTjZxgijRzQOGbCWALh4sRDec2w6xsY/ux53Vuj/AMZBDJ87qyZL5kAf1fmAH4Oe13Iu435bfRBuZgHpnRjTBn5+xsDHONiR3t0+Oa8yG/tOKJMNUauedvMyN4v4QKiFunw=='

s1 = b'U2FsdGVkX19ogzm2z2PdJ3Mm1qpQThMERB9ZcvgY4qVr3aZ8fkXHU6aaaI/60I4h'
s2 = b'BH1Ol7bvmfE='
s2 = b64decode(s2)


test = "U2FsdGVkX19ogzm2z2PdJ3Mm1qpQThMERB9ZcvgY4qVr3aZ8fkXHU6aaaI/60I4h"
key=b'202193'
result = decrypt(s1, key)

# result = decrypt(test, passphrase)
print(result)
ans=[]
for i in range(len(result)):
    ans.append(result[i]^s2[i%len(s2)])
    
