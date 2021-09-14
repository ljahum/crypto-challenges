from Crypto.Util.number import *
import hashlib
import os
import random
import string

def dec():
	try:
		cipher = int(raw_input("Your cipher: "))
		m = long_to_bytes(pow(cipher,d,n),BITS/8)
		print m[:2].encode('hex')
	except:
		exit()

def check():
	S = raw_input("You know my secret? (in hex): ").decode('hex')
	if S == secret:
		with open("./flag.txt") as f:
			print f.read()
		exit()
	else:
		print("V^V")
		exit()

def proof_of_work():
    s = "".join(random.sample(string.ascii_letters + string.digits, 20))
    prefix = s[:4]
    print("sha256(xxxx + %s) == %s " % (s[4:],hashlib.sha256(s.encode()).hexdigest()))
    print("give me xxxx:")
    ans = raw_input().strip()
    if len(ans) == 4 and ans == prefix:
        return True
    else:
        return False
try:

    if not proof_of_work():
        exit()
except:
    exit()



MENU = '''
1 dec()
2 check
'''

BITS = 512
secret = os.urandom(32)
p = getPrime(BITS/2)
q = getPrime(BITS/2)
n = p*q
e = 65537
d = inverse(e,(p-1)*(q-1))

try:
	pad = raw_input("Do you want the secret to be padded as PKCS1_v1_6?(y/n)")
	if pad == 'n':
		m = bytes_to_long(secret)
	else:
		mLen = len(secret)
		ps=[]
		k = BITS/8
		while len(ps) != k - mLen - 3:
			tmp = os.urandom(1)
			if ord(tmp) != 0:
				ps.append(tmp)
		ps = b"".join(ps)
		assert(len(ps) == k - mLen - 3)
		m = '\x00\x04' + ps + '\x00' + secret
		m = bytes_to_long(m)

except:
	print("V^V")
	exit()


c = pow(m,e,n)

print("e = "+str(e))
print("n = "+str(n))
print("c = "+str(c))

print(MENU)
while True:
	try:
		choice = int(raw_input("Your choice: "))
		if choice == 1:
			dec()
		elif choice == 2:
			check()
		else:
			exit()
	except Exception as e:
		print("V^V")
		exit()
	
