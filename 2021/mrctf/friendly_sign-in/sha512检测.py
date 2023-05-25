from Crypto.Util.number import *
from hashlib import sha512
from random import choices
import string
head = "yE11k4FS"
xrange = string.digits+string.ascii_letters
for i in xrange:
    for j in xrange:
        for x in xrange:
            for l in xrange:
                m = (head+str(i)+str(j)+str(x)+str(l)).encode()
                if sha512(m).hexdigest().startswith("11111"):
                    print(str(i)+str(j)+str(x)+str(l))
                    break
                
