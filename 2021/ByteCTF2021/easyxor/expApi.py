
import struct
import sys

def bytes_to_long(s):
    """Convert a byte string to a long integer (big endian).

    In Python 3.2+, use the native method instead::

        >>> int.from_bytes(s, 'big')

    For instance::

        >>> int.from_bytes(b'\x00P', 'big')
        80

    This is (essentially) the inverse of :func:`long_to_bytes`.
    """
    acc = 0

    unpack = struct.unpack

    # Up to Python 2.7.4, struct.unpack can't work with bytearrays nor
    # memoryviews
    if sys.version_info[0:3] < (2, 7, 4):
        if isinstance(s, bytearray):
            s = bytes(s)
        elif isinstance(s, memoryview):
            s = s.tobytes()

    length = len(s)
    if length % 4:
        extra = (4 - length % 4)
        s = b'\x00' * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
    return acc

def long_to_bytes(n, blocksize=0):
    """Convert an integer to a byte string.

    In Python 3.2+, use the native method instead::

        >>> n.to_bytes(blocksize, 'big')

    For instance::

        >>> n = 80
        >>> n.to_bytes(2, 'big')
        b'\x00P'

    If the optional :data:`blocksize` is provided and greater than zero,
    the byte string is padded with binary zeros (on the front) so that
    the total length of the output is a multiple of blocksize.

    If :data:`blocksize` is zero or not provided, the byte string will
    be of minimal length.
    """
    # after much testing, this algorithm was deemed to be the fastest
    s = b''
    n = int(n)
    pack = struct.pack
    while n > 0:
        s = pack('>I', n & 0xffffffff) + s
        n = n >> 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != b'\x00'[0]:
            break
    else:
        # only happens when n == 0
        s = b'\x00'
        i = 0
    s = s[i:]
    # add back some pad bytes.  this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * b'\x00' + s
    return s

def check(s):
    for i in s:
        if(i>32 and i<127):
            continue
        else:
            return False
    return True

def shift(m, k, c):
    if k < 0:
        return m ^ (m >> (-k)) & c
    return m ^ ((m << k) & c)

def convert(m, key):
    c_list = [0x37386180af9ae39e, 0xaf754e29895ee11a, 0x85e1a429a2b7030c, 0x964c5a89f6d3ae8c]
    for t in range(4):
        m = shift(m, key[t], c_list[t])
    return m

def invshift_opt(c,k,mask):
    c = bin(c)[2:].rjust(64,'0')
    cip=[int(i) for i in c]
    
    mask = bin(mask)[2:].rjust(64,'0')
    mask=[int(i) for i in mask]
    
    ans={}
    idx = 63
    for i in range(k):
        ans[idx]=cip.pop()
        idx-=1

    for i in range(63-k,-1,-1):
    
        tmp = cip[i]^(ans[i+k]&mask[i])
        ans[i]=tmp
    
    flag =''
    for i in range(64):
        flag += str(ans[i]) 
    ans = int(flag,2)
    return ans
        

def invshift_ngt(c,k,mask):
    k=-k
    c = bin(c)[2:].rjust(64,'0')
    cip=[int(i) for i in c]
    
    mask = bin(mask)[2:].rjust(64,'0')
    mask=[int(i) for i in mask]
    
    ans={}
    for i in range(k):
        ans[i]=cip[i]
    
    
    for i in range(k,64):
        tmp = cip[i]^(ans[i-k]&mask[i])
        ans[i]=tmp
    flag =''
    for i in range(64):
        flag += str(ans[i]) 
    ans = int(flag,2)
    return ans
    
def invconvert(m, key):
    c_list = [0x37386180af9ae39e, 0xaf754e29895ee11a, 0x85e1a429a2b7030c, 0x964c5a89f6d3ae8c]
    for t in range(3,-1,-1):
        if(key[t]>0):
            m = invshift_opt(m, key[t], c_list[t])
        else:
            m = invshift_ngt(m, key[t], c_list[t])
    return m