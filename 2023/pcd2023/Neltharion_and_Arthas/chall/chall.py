import binascii
import hashlib
from flag import flag
from Crypto.Cipher import AES
from Crypto.Util import *
import os

key1 = os.urandom(32)
key2 = b'tn*-ix6L*tCa*}i*'
key_len = len(key2)
assert flag.startswith(b'flag{')
assert (flag[13] == 45 and flag[18] == 45 and flag[23] == 45 and flag[28] == 45)
flag1 = b"2023: "+flag[:13]+flag[14:18]+flag[19:23]
flag2 = 

h = binascii.unhexlify(hashlib.sha256(key2).hexdigest())[:11]
gift1 = b'***********************************************************************************************'
gift2 = b'I tell you this, for when my days have come to an end , you, shall be King.'+h


def encrypt1(message, key):
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
    ciphertext = cipher.encrypt(message)
    return ciphertext.hex()


def encrypt2(message, key, iv):
    padding = bytes((key_len - len(message) % key_len) * '&', encoding='utf-8')
    message += padding
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(message)
    return ciphertext.hex()


print("enc_gift1 = "+encrypt1(gift1, key1))
print("enc_flag = "+encrypt1(flag1, key1))
print("enc_gift2 = "+encrypt2(gift2, key2, flag2))