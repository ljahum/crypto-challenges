import os, hashlib, pickle
from tqdm import tqdm
# -----------------------------------
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = p - 3
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
EC = EllipticCurve(GF(p), [a, b])
G = EC.gens()[0] # 固定的点

def decrypt(cip, key,iv):
    key = hashlib.sha256(str(key).encode()).digest()[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(cip)

data = {'cip': '9dcc2c462c7cd13d7e37898620c6cdf12c4d7b2f36673f55c0642e1e2128793676d985970f0b5024721afaaf02f2f045', 'iv': 'cbd6c57eac650a687a7c938d90e382aa', 'G': '(38764697308493389993546589472262590866107682806682771450105924429005322578970 : 112597290425349970187225006888153254041358622497584092630146848080355182942680 : 1)'}
FLAG = data['cip']
iv = data['iv']
FLAG = bytes.fromhex(FLAG)
iv = bytes.fromhex(iv)
x = 38764697308493389993546589472262590866107682806682771450105924429005322578970
y = 112597290425349970187225006888153254041358622497584092630146848080355182942680
G = EC(x,y)
print(G)

SS = G
for i in tqdm(range(2,1024*1024)):
    
    SS = SS+G
    msg = decrypt(FLAG, SS.xy()[0],iv)
    if(b'inctf' in msg):
        print(msg)
        break
# inctf{w0w_DH_15_5o_c00l!_3c9cdad74c27d1fc}