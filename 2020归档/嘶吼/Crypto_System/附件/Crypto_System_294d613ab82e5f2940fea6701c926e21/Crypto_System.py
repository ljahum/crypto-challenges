# These three are constants
p = 12039102490128509125925019010000012423515617235219127649182470182570195018265927223
g = 10729072579307052184848302322451332192456229619044181105063011741516558110216720725

# random generation
m1 = "test1"
m2 = "test2"

# Initialization
r1, s1 = sign(m1)
# r1 will be provided to player

def int2str(data, mode="big"):
    if mode == "little":
        return sum([ord(data[_]) * 2 ** (8 * _) for _ in range(len(data))])
    elif mode == "big":
        return sum([ord(data[::-1][_]) * 2 ** (8 * _) for _ in range(len(data))])

def get_parameter(m):
    x = int2str(m, 'little')
    y = powmod(g, x, p)
    a = bytes_to_long(hashlib.sha256(long_to_bytes(y).rjust(128, "\0")).digest())
    b = powmod(a, a, p - 1)
    h = powmod(g, b, p)

    return y, h, b

def sign(m):
    y, h, b = get_parameter(m)
    r = getStrongPrime(512)
    s = (y * powmod(h, r, p)) % p 

    return str(r),str(s)

def verify(m, r, s):
    y, h, b = get_parameter(m)
    if s == ((y * powmod(h, r, p)) % p):
        return True
    else:
        return False

# Give me the (r2,s2)
if r2 != r1 and s2 == s1 and verify(m2, r2, s2):
    print("Congratulation!Here is your flag: %s" % flag)