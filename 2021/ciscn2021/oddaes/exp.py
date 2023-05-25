from aes import AES
import os,hashlib,random 
from tqdm import tqdm

# -----------------------------------
f = open('keys-0.csv','r') 

plain = os.urandom(16) 
m1 = '973f5ae78bc933a8fc7f7ab98d53d16f' 
m2 = '628aab012199cdab83cc1aa72204ea98'
s = random.randint(0,255)

for i in tqdm(range(4266)): 
    key = f.readline().replace('\n','') 
    cipher,k = AES(bytes.fromhex(key)).encrypt_block_(plain,s) 
    piece1 = [k[0],k[1],k[4],k[7],k[10],k[11],k[13],k[14]] 
    m11 = hashlib.md5(bytes(piece1)).hexdigest() 
    piece2 = [k[2],k[3],k[5],k[6],k[8],k[9],k[12],k[15]] 
    m22 = hashlib.md5(bytes(piece2)).hexdigest() 
    if m11 == m1 and m22 == m2: 
        print(key) 
        print("CISCN{"+hashlib.md5(bytes.fromhex(key)).hexdigest()+"}")
        break