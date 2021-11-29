import aes
import os
import aegis
from aegis import _xor,_and
from pwn import *
import base64



def R(x):
    tmp = aes.bytes2matrix(x)
    aes.sub_bytes(tmp)
    aes.shift_rows(tmp)
    aes.mix_columns(tmp)
    return aes.matrix2bytes(tmp)


def invR(x3):
    tmp = aes.bytes2matrix(x3)
    aes.inv_mix_columns(tmp)
    aes.inv_shift_rows(tmp)
    aes.inv_sub_bytes(tmp)
    return aes.matrix2bytes(tmp)

def resolve(dk_1, ds_1, dk_2, ds_2):
    # here we check the 
    tmpk = aes.bytes2matrix(dk_1)
    aes.inv_mix_columns(tmpk)
    aes.inv_shift_rows(tmpk)
    d_k1 = aes.matrix2bytes(tmpk)

    tmpk = aes.bytes2matrix(dk_2)
    aes.inv_mix_columns(tmpk)
    aes.inv_shift_rows(tmpk)
    d_k2 = aes.matrix2bytes(tmpk)
    # result should be unique
    res = bytearray(16)
    # try to bruce it
    for i in range(16):
        x1 = set()
        for c in range(256):
            if aes.s_box[c] ^ aes.s_box[c^ds_1[i]] == d_k1[i] and aes.s_box[c] ^ aes.s_box[c^ds_2[i]] == d_k2[i]:
                x1.add(c)
        res[i] = x1.pop()
    assert(len(res) == 16)
    return bytes(res)

def encrypt(ph, aad, pt):
    ph.sendline(base64.standard_b64encode(pt))
    ph.sendline(base64.standard_b64encode(aad))
    ct = ph.recvline(keepends=False)
    ct = base64.standard_b64decode(ct.decode('utf-8'))
    tag = ph.recvline(keepends=False)
    tag = base64.standard_b64decode(tag.decode('utf-8'))
    return ct, tag


def decrypt(ph, aad, pt, index, ct):
    left_index = (index+1)*16
    right_index = (index+2)*16
    enc, tag = encrypt(ph, aad, pt[2*index-1])
    # print("enc[{}:{}]".format(left_index/32,right_index/32))
    # print("pt[{}:{}]".format(2*index-1, 2*index))
    ct1_2 = enc[left_index:right_index]
    # encrypt 3
    enc, tag = encrypt(ph, aad, pt[2*index])
    # print(pt[2*index])
    ct1_3 = enc[left_index:right_index]
    # decrypt s10
    # print(ct)
    # print(ct1_2)
    # print(ct)
    # print(ct1_2)
    dk1 = _xor(ct,ct1_2)
    dk2 = _xor(ct,ct1_3)
    # split S1/S5
    # pt split ,too
    s = resolve(dk1, pt[2*index-1][16*(index-1):16*(index)], 
                dk2, pt[2*index][16*(index-1):16*(index)])
    return s

def localTest():
    ph = remote("127.0.0.1",'10000')
    pt = []
    padding = b'\x00'*16
    p0 = b'\x00'*16
    p1 = b'\x00'*16
    p2 = b'\x00'*16
    pt.append(p0+p1+p2+padding*2)
    # for i in range(1,7):
    # pt.append(bytes([i%2+1]*16)+padding)
    # for s10
    pt.append(bytes([1]*16)+padding+padding)
    pt.append(bytes([2]*16)+padding+padding)
    # for s20
    pt.append(padding+bytes([1]*16)+padding+padding)
    pt.append(padding+bytes([2]*16)+padding+padding)
    # for s30
    pt.append(padding+padding+bytes([1]*16)+padding*2)
    pt.append(padding+padding+bytes([2]*16)+padding*2)
    iv = ph.recvline(keepends=False)
    aad = b''

    # encrypt 1
    enc, tag = encrypt(ph, aad, pt[0])
    print(enc)
    ct = []
    for i in range(5):
        ct.append(enc[i*16:(i+1)*16])

    s10 = decrypt(ph, aad, pt, 1, ct[2])
    # decrypt 2 
    s20 = decrypt(ph, aad, pt, 2, ct[3])
    # decrypt 3
    s30 = decrypt(ph, aad, pt, 3, ct[4])
    # s20 = s10 xor R(s14) ==> s14 = invR(s20 xor s10)
    s14 = invR(_xor(s20, s10))
    # s30 = s20 xor R(s24) ==> s24 = invR(s20 xor s30)
    # s24 = s14 xor R(s13) ==> s13 = invR(s14 xor s24)
    s24 = invR(_xor(s20, s30))
    s13 = invR(_xor(s24, s14))
    ph.recvuntil("Oops, something leak:")
    s12 = ph.recvline(keepends=False)
    print(s12)
    s12 = base64.standard_b64decode(s12.decode('utf-8'))
    # if pt = 00 then enc1 = (s12&s13) xor s14 xor s11
    # -> s11 = enc1 xor s14 xor (s12&s13)
    enc1 = enc[16:16*2]
    s11 = _xor(s14, _xor(enc1, _and(s12, s13)))
    # s15 = _xor(s12, _xor(enc12, _and(s16, s17)))
    s1 = s10+s11+s12+s13+s14
    ph.sendline(base64.standard_b64encode(s1))
    ph.interactive()

if __name__ == "__main__":
    localTest()