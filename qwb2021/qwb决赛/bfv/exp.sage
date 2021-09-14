from pwn import *
# from icecream import *
from tqdm import tqdm

from time import *
p1 = time()

# -----------------------------------
# get pk
# io = remote('0.0.0.0',10001)
io = remote('172.20.5.23',8001)

q = 2 ^ 54
t = 83
T = 3
d = 1024
delta = int(q / t)
sigma = 2
P.<x> = PolynomialRing(ZZ)
f = x ^ d + 1
R.<X> = P.quotient(f)

def Roundt(a):
	A = a.list()
	for i in range(len(A)):
		A[i] = A[i] % t
		if A[i] > (t / 2):
			A[i] = A[i] - t
	return R(A)


def Roundq(a):
	A = a.list()
	for i in range(len(A)):
		A[i] = A[i] % q
		if A[i] > (q / 2):
			A[i] = A[i] - q
	return R(A)
def mutual2(k, c, s):
	tmp = t * Roundq(c[0] + c[1] * s)
	TMP = tmp.list()
	for i in range(len(TMP)):
		TMP[i] = round(TMP[i] / q)
	tmp2 = Roundt(R(TMP))
	return tmp2



io.recvuntil('public key:[')
pk1 = io.recvuntil(']')[:-1]
io.recvuntil('[')
pk2 = io.recvuntil(']')[:-1]
# print(pk1)
# print(pk2[:100])
pk2 = [int(i) for i in pk2.split(b',')]
# print(pk2[:10])
pk1 = [int(i) for i in pk1.split(b',')]
pk=[R(pk1),R(pk2)]
for i in range(1024-5):
	print(io.recvuntil('>'))
	io.sendline('4')
	io.sendline(str(i))



M=delta//4+50
padding = [8,7, 6, 5, 4, 3, 2, 1,  0, -1, -2, -3, -4, -5,-4]
sks=      [-7,-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6,7]
rk=[100 for i in range(1024)]     

for x in range(len(sks)):
	
	print(io.recvuntil('>'))
	io.sendline('2')
	print(io.recvuntil('recv ct?(Y/N)'))
	io.sendline('Y')
	sleep(1)
	print(io.recvuntil('['))
	adminC1 = io.recvuntil(']')[:-1]
	print((io.recvuntil('[')))
	adminC2 = io.recvuntil(']')[:-1]
	adminC1 = [int(i) for i in adminC1.split(b',')]
	# print(pk2[:10])
	adminC2 = [int(i) for i in adminC2.split(b',')]

	print(io.recvuntil('continue?(Y/N)'))
	io.sendline('N')
	pad = padding[x]
	print(f'第{x}个了')
	for k in tqdm(range(1024)):
		t1=[0 for _ in range(d)]
		t1[k]=pad*M
		t2=M
		# ================================
		cc0=(pk[0]+R(t1)).list()
		payload_c1 = ''
		for i in cc0:
			payload_c1 += str(i)
			payload_c1+=' '
		payload_c2 = ''
		cc1=(pk[1]+R(t2)).list()
		for i in cc1:
			payload_c2 += str(i)
			payload_c2+=' '
		
		io.recvuntil('c1:')
		io.sendline(payload_c1)
		# sleep(1)
		io.recvuntil('c2:')
		io.sendline(payload_c2)
		# =====================================

		fb = io.recvline()
		if(b'True' in fb and rk[k]==100):
			rk[k] = sks[x]
	# input()
for i in range(len(rk)):
    if(rk[i]==100):
        rk[i]=7

sk = R(rk)
adminCT=[R(adminC1),R(adminC2)]
# cc0=R(ct[0].list())
# cc1=R(ct[1].list())

ans = mutual2(0,adminCT,sk)

x = ans.list()[:25]
admin_id =0
use=[]
ids=[]
for i in x:
	admin_id *= T
	admin_id += i
	use.append(i)
	ids.append(admin_id)

print(rk)
print(ids)
# io.interactive()
sleep(1)
for id in ids:
	print(io.recvuntil('>'))
	io.sendline('1')
	print(io.recvuntil('name:'))
	io.sendline('admin')
	print(io.recvuntil('id:'))
	io.sendline(str(id))
	print(io.recvline())
print(io.recvuntil('>'))
io.sendline('3')
io.sendlineafter('name:','admin')
io.sendlineafter('message:','give me the flag')
sleep(1)
print(io.recv(2048))
p2 = time()
print(p2-p1)