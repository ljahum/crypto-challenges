from Crypto.PublicKey import RSA


rsakey = RSA.importKey(open("key.pem", "r").read())
n = rsakey.n
e = rsakey.e
print(f'n = {hex(n)}\ne={hex(e)}')

