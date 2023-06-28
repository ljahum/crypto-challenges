from random import Random
from hashlib import md5
rng = Random()
leak = []
for i in range(1250):
    leak.append(rng.getrandbits(16))
m = rng.getrandbits(64)
flag = "flag{"+str(m)+"}"
print(flag)
flag_md5 = md5(flag.encode()).hexdigest()
f = open("output.txt","w")
f.write(f"leak = {leak}\n")
f.write(f"flag_md5 = {flag_md5}\n")
f.close()