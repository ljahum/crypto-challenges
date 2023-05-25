# nc 118.190.62.234 61139
from pwn import *
from hashlib import sha256
from icecream import *
from itertools import product
from Crypto.Util.number import *

from tqdm import tqdm

r = remote('118.190.62.234',61139)
# r = remote('0.0.0.0',30001)


# print(buf)
def gopow():
	s1 = b'JXXCe9pJLSpr'
	hashstr = b'510f0df96af2ec7a9ed321ef2158312095041920699402c73c8e3014d8e73c38'
	print(s1,hashstr)
	tab = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	for i in product(tab,repeat=4):
		tmp = ''.join(i)
		s0 =  bytes(tmp,encoding='utf-8')
		s = s0+s1
		# proof = ''.join(random.choices(alphabet, k=16))
		hash_value = sha256(s).hexdigest()
		hash_value = bytes(hash_value,encoding='utf-8')
		# ic(hash_value,hashstr)
		# ic(s0,s)
		# input()
		if hash_value == hashstr:
			print(hash_value)
			ic("XXXX=",s0)
			ic(hash_value,hashstr)
			print(r.recv(2048))
			r.sendline(s0)
			break
		

	
gopow()
# buf = r.recvline(1024)
# r.interactive()

# print(r.recvline())
# print(r.recvline())
# 菜单
print(r.recv(2048).decode())
r.interactive()
'''
# =================
ans=[]
CC = 180931142957826775

lb = 2**2030
ub = 2**2050
for i in tqdm(range(1,2048)):

	r.recvuntil('Enter option >')
	r.sendline('1')
	r.recvuntil('Enter your plaintext in hex >')

	s=CC*(2**i)
	s = long_to_bytes(s).hex()
	r.sendline(s)
	r.recvuntil('Here is your ciphertext in hex: \n')
	buf = r.recvline()
	# print(buf)
	c = int(buf[:-1],16)
	# ic(c)
	# input()
	if(c&1==1):
		lb = (lb+ub)//2
	else:
		ub = (lb+ub)//2


	# ans.append(c)
ic(lb,ub//2)
# =======================
'''

'''
c = 180931142957826775
'''