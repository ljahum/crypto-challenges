import string
import hashlib
a = "ebdb"

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

xrange=string.digits+string.ascii_letters
for i in xrange:
    for j in xrange:
        for x in xrange:
            for l in xrange:
                for y in xrange:
                    m=(str(i)+str(j)+str(x)+str(l)+str(y)+a)

                    if md5(m).startswith('f4ab1'):
                        print(md5(m))
                        print(str(i)+str(j)+str(x)+str(l)+str(y))