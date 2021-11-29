from gmpy2 import *
from Crypto.Util.number import *
m = b'flag{happy_rsa_1}'
print(bytes_to_long(m))
    # 34852863801141329469000105527941672153469
q = 827089796345539312201480770649
print('c=', '0x7a7e031f14f6b6c3292d11a41161d2491ce8bcdc67ef1baa9eL'),
print('e=', '0x872a335')
c = 0x7a7e031f14f6b6c3292d11a41161d2491ce8bcdc67ef1baa9e
e = 0x872a335
d = invert(e,q-1)
print(long_to_bytes(pow(c,e,q)))
