from pwn import *
from Crypto.Util.number import *
from hashlib import sha256
import string
from pwnlib.util.iters import mbruteforce
import base64
#context.log_level = 'debug'

xor = lambda s1 , s2 : bytes([x1^x2 for x1,x2 in zip(s1,s2)])
table = string.ascii_letters+string.digits

def times2(input_data,blocksize = 16):
    assert len(input_data) == blocksize
    output =  bytearray(blocksize)
    carry = input_data[0] >> 7
    for i in range(len(input_data) - 1):
        output[i] = ((input_data[i] << 1) | (input_data[i + 1] >> 7)) % 256
    output[-1] = ((input_data[-1] << 1) ^ (carry * 0x87)) % 256
    assert len(output) == blocksize
    return output

def times3(input_data):
    assert len(input_data) == 16
    output = times2(input_data)
    output = xor_block(output, input_data)
    assert len(output) == 16
    return output

def back_times2(output_data,blocksize = 16):
    assert len(output_data) == blocksize
    input_data =  bytearray(blocksize)
    carry = output_data[-1] & 1
    for i in range(len(output_data) - 1,0,-1):
        input_data[i] = (output_data[i] >> 1) | ((output_data[i-1] % 2) << 7)
    input_data[0] = (carry << 7) | (output_data[0] >> 1)
    # print(carry)
    if(carry):
        input_data[-1] = ((output_data[-1] ^ (carry * 0x87)) >> 1) | ((output_data[-2] % 2) << 7)
    assert len(input_data) == blocksize
    return input_data

def xor_block(input1, input2):
    assert len(input1) == len(input2)
    output = bytearray()
    for i in range(len(input1)):
        output.append(input1[i] ^ input2[i])
    return output

def hex_to_bytes(input):
    return bytearray(long_to_bytes(int(input,16)))

def pow():
    io.recvuntil(b"XXXX+")
    suffix = io.recv(16).decode("utf8")
    io.recvuntil(b"== ")
    cipher = io.recvline().strip().decode("utf8")
    proof = mbruteforce(lambda x: sha256((x + suffix).encode()).hexdigest() ==
                        cipher, table, length=4, method='fixed')
    io.sendline(proof.encode()) 

def get_FLAG_data():
    io.recv()
    io.sendline(b'3')
    io.recvuntil(b'ciphertext: ')
    ciphertext = base64.b64decode(io.recvline()[:-1])
    io.recvuntil(b'tag: ')
    tag = base64.b64decode(io.recvline()[:-1])
    nonce = b'\x00'*16
    associate_data = b'from admin'
    return ciphertext,tag,nonce,associate_data

def Server_Enc(msg,nonce):
    io.recv()
    io.sendline(b'1')
    io.recv()
    io.sendline(base64.b64encode(nonce))
    io.recv()
    io.sendline(base64.b64encode(msg))

    associate_data = b'from baby'
    io.recvuntil(b'ciphertext: ')
    ciphertext = base64.b64decode(io.recvline()[:-1])
    io.recvuntil(b'tag: ')
    tag = base64.b64decode(io.recvline()[:-1])

    return ciphertext,tag

def Server_Dec(nonce,cip,tag,associate_data):
    io.recv()
    io.sendline(b'2')
    io.recv()
    io.sendline(base64.b64encode(nonce))
    io.recv()
    io.sendline(base64.b64encode(cip))
    io.recv()
    io.sendline(base64.b64encode(tag))
    io.recv()
    io.sendline(base64.b64encode(associate_data))
    io.recvuntil(b'plaintext: ')
    plaintext = base64.b64decode(io.recvline()[:-1])
    return plaintext

def get_my_enc(msg):
    nonce = bytearray(os.urandom(16))
    fake_m = bytearray(b'\x00'*15+b'\x80'+b'\x00'*16)
    cip,tag = Server_Enc(fake_m,nonce)
    m0 = bytearray(b'\x00'*15+b'\x80')
    m1 = bytearray(b'\x00'*16)

    c0 = cip[:16]
    c1 = cip[16:]

    enc = xor_block(Server_Dec(nonce,xor_block(c0,m0),c1,b""),m0)
    A = back_times2(enc)
    B = enc
    C = xor_block(B,c0)

    msg = msg
    new_nonce = xor_block(B,m0)
    new_msg = xor_block(msg,times2(C)) + m1
    new_msg = (bytes(new_msg))
    ENC,TAG = Server_Enc(new_msg,new_nonce)
    
    #io.interactive()
    return xor_block(ENC[:16],times2(C))

def my_pmac(header, blocksize = 16):
    assert len(header)
    m = int(max(1, math.ceil(len(header) / float(blocksize))))
    offset = get_my_enc(bytearray([0] * blocksize))
    offset = times3(offset)
    offset = times3(offset)
    checksum = bytearray(blocksize)
    for i in range(m - 1):
        offset = times2(offset)
        H_i = header[(i * blocksize):(i * blocksize) + blocksize]
        assert len(H_i) == blocksize
        xoffset = xor_block(H_i, offset)
        encrypted = get_my_enc(xoffset)
        checksum = xor_block(checksum, encrypted)
    offset = times2(offset)
    H_m = header[((m - 1) * blocksize):]
    print(H_m)
    assert len(H_m) <= blocksize
    if len(H_m) == blocksize:
        offset = times3(offset)
        checksum = xor_block(checksum, H_m)
    else:
        H_m = H_m + b'\x80'
        while len(H_m) < blocksize:
            H_m += b'\x00'
        assert len(H_m) == blocksize
        checksum = xor_block(checksum, H_m)
        offset = times3(offset)
        offset = times3(offset)
    final_xor = xor_block(offset, checksum)
    auth = get_my_enc(final_xor)
    return auth

if __name__ == "__main__":
    # io = remote("47.104.243.99",10001)
    io = remote("0.0.0.0",10002)
    pow()
    F_ciphertext,F_tag,F_nonce,F_associate_data = get_FLAG_data()

    print(len(F_ciphertext))
    FROMADMIN = my_pmac(b'from admin')
    print(FROMADMIN)
    FROMBABY = my_pmac(b'from baby')
    print(FROMBABY)
    F_associate_data = b'from baby'
    F_tag = xor_block(xor_block(F_tag, FROMADMIN),FROMBABY)

    print(Server_Dec(F_nonce,F_ciphertext,F_tag,F_associate_data))
    io.interactive()