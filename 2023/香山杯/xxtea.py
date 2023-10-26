from Crypto.Util.number import *
from ctypes import *


def MX(z, y, total, key, p, e):
    temp1 = (z.value>>5 ^ y.value<<2) + (y.value>>3 ^ z.value<<4)
    temp2 = (total.value ^ y.value) + (key[(p&3) ^ e.value] ^ z.value)
    
    return c_uint32(temp1 ^ temp2)


def encrypt(n, v, key):
    delta = 0x9e3779b9 
    rounds = 6 + 52//n

    total = c_uint32(0)
    z = c_uint32(v[n-1])
    e = c_uint32(0)
    
    while rounds > 0:
        total.value += delta  
        e.value = (total.value >> 2) & 3
        for p in range(n-1):
            y = c_uint32(v[p+1])
            v[p] = c_uint32(v[p] + MX(z,y,total,key,p,e).value).value
            z.value = v[p]
        y = c_uint32(v[0])
        v[n-1] = c_uint32(v[n-1] + MX(z,y,total,key,n-1,e).value).value
        z.value = v[n-1]
        rounds -= 1 

    return v


def decrypt(n, v, key):
    delta = 0x9e3779b9
    rounds = 6 + 52//n 
    
    total = c_uint32(rounds * delta)
    y = c_uint32(v[0])
    e = c_uint32(0)

    while rounds > 0:
        e.value = (total.value >> 2) & 3
        for p in range(n-1, 0, -1):
            z = c_uint32(v[p-1])
            v[p] = c_uint32((v[p] - MX(z,y,total,key,p,e).value)).value
            y.value = v[p]
        z = c_uint32(v[n-1])  
        v[0] = c_uint32(v[0] - MX(z,y,total,key,0,e).value).value
        y.value = v[0]  
        total.value -= delta
        rounds -= 1

    return v 


#  test  
if __name__ == "__main__":
	# 该算法中每次可加密不只64bit的数据，并且加密的轮数由加密数据长度决定
    # v = [0x12345678, 0x78563412]
    k = [0x1, 0x2, 0x3, 0x4]
    k = [12345678 ,12398712 ,91283904 ,12378192 ]
    n = 9

    # print("Data is : ", hex(v[0]), hex(v[1]))
    # res = encrypt(n, v, k)
    # print("Encrypted data is : ", hex(res[0]), hex(res[1]))
    res =[689085350 ,626885696 ,1894439255 ,1204672445 ,1869189675 ,475967424 ,1932042439 ,1280104741 ,2808893494 ]#line:85
    res = decrypt(n, res, k)
    # print("Decrypted data is : ", hex(res[0]), hex(res[1]))
    flag =b''
    
    print(res)
    for i in res:
        flag+= long_to_bytes(i)
    print(flag)
"""
Data is :  0x12345678 0x78563412
Encrypted data is :  0xef86c2bb 0x25f31b5e
Decrypted data is :  0x12345678 0x78563412
"""
