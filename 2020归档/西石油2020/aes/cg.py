
from Crypto.Util.number import *
from Crypto.Cipher import AES
key = b'0'*16
iv = b'1'*16
name = b'admin==========='
m1 = b'yusa'*4

m2 = b'ljahum=========='
m = m1+m2
aes = AES.new(key, AES.MODE_CBC, iv)
# c = aes.encrypt(m)
c = b'"\xc3B\x1d\xc0d:T[\x1a\xf8u#\xdf\xfb\x1aI@\x1b0\x94n\xeb\x07"\xba\xa5\xb9\x1bU\x0cZ'

# print(c)
# print(m)
# print(len(c))

# token = bytes.fromhex('d813a1d3ae6350bb9b22ab199c8e0f3d996d1702c766d50a710670a9511174b2d2be4d76d807c1a6ad1aec3093a63514')
# --------------------------------------------------------------------------
name = bytes_to_long(b'admin===========')
m1 = bytes_to_long(b'yusa'*4)

m2 = bytes_to_long(b'ljahum==========')
token = iv + c
token = bytes.fromhex(
    '70f40ce71c964f4f2197e4b19e79a0db7e9a77d9a2dbec3f7450966dc5e926e28b71d0ec09115df06157a8c53605415e')

print('token1 = ',token.hex())
iv = bytes_to_long(token[:16])
c1 = bytes_to_long(token[16:32])
c2 = bytes_to_long(token[32:])
# c = long_to_bytes(c1)+long_to_bytes(c2)
# -----------------------------------------
c3 = name^(c1^m2)

c = long_to_bytes(c1)+long_to_bytes(c3)
token2 = long_to_bytes(iv) + c
print('token2 = ', token2.hex()) #write
m = (aes.decrypt(c))
# m = bytes.fromhex('d813a1d3ae6350bb9b22ab199c8e0f3d996d1702c766d50a710670a9511174b2d2be4d76d807c1a6ad1aec3093a63514')
print('m = ',m.hex())
# ------------------------------------------------------
m3 = bytes_to_long(b'\x9b\x14\x9fA`\r\x8a\xe80\xf7\xc0Qpg+O')

iv3 =long_to_bytes(m1^(c1^m3))

c = long_to_bytes(c3)+long_to_bytes(c2)

token3 = iv3 + c
print('token3 = ', token3.hex())  # write

m = (aes.decrypt(c))
print(m)
