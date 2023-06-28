flag = b"flag{9293973663660867299}"
from hashlib import md5
m = 9293973663660867299


# m = rng.ge/trandbits(64)
flag = "flag{"+str(m)+"}"
print(flag)
flag_md5 = md5(flag.encode()).hexdigest()


print(flag_md5)