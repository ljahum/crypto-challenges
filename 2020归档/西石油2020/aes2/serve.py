from Crypto.Cipher import AES
import os
from icecream import *
import codecs
decode_hex = codecs.getdecoder("hex_codec")

BLOCKSIZE = 16
flag = b'SYC{oversyclover123sycloversyclover12}'
 
 
def pad(data):
        pad_len = BLOCKSIZE - (len(data) %
                               BLOCKSIZE) if len(data) % BLOCKSIZE != 0 else 0
        return data + bytes([pad_len]) * pad_len
 
def unpad(data):
        num = ord(data[-1])
        return data[:-num]
 
 
def enc(data,key):
    cipher = AES.new(key,AES.MODE_ECB)
    encrypt = cipher.encrypt(pad(data))
    return encrypt
 
 
def dec(data,key):
    try:
        cipher = AES.new(key,AES.MODE_ECB)
        encrypt = cipher.decrypt(data)
        return unpad(encrypt)
    except:
        exit()
 
 
def task():
        try:
                key = os.urandom(16)
                key = b'0'*16
                while True:
                        plaintext = decode_hex(input("Amazing function: "))[0]
                        m = plaintext+flag
                        #print(m)
                        cipher_ = enc(m, key).hex()
                        '''
                        print('----------------------------')
                        for i in range(0,len(cipher_),32):
                                print(cipher_[i:i+32])
                        print('---------------------------')
                        '''
                        print(cipher_)
        except Exception as e:
                print(str(e))
                exit()
if __name__ == "__main__":
        task()
        exit()
'''
socat tcp-listen:10001,fork exec:'python3 serve.py'
'''


