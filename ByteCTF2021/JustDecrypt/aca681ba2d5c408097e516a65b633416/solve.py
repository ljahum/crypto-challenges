from Crypto.Util.number import *
from pwn import *
from tqdm import tqdm
def main():
    r = remote('0.0.0.0', '30002')
    plaintext = b"Hello, I'm a Bytedancer. Please give me the flag!"+b"\x0f"*15

    def my_XOR(a, b):
        assert len(a) == len(b)
        return b''.join([long_to_bytes(a[i]^b[i]) for i in range(len(a))])

    def proof_of_work():
        rev = r.recvuntil(b"sha256(XXXX+")
        suffix = r.recv(28).decode()
        rev = r.recvuntil(b" == ")
        tar = r.recv(64).decode()

        def f(x):
            hashresult = hashlib.sha256(x.encode()+suffix.encode()).hexdigest()
            return hashresult == tar

        prefix = util.iters.mbruteforce(f, string.digits + string.ascii_letters, 4, 'upto')
        r.recvuntil(b'Give me XXXX > ')
        r.sendline(prefix.encode())

    def decrypt(msg):
        newmsg = msg + b'\x00'*(256+64-len(msg))
        r.recvuntil(b'Please enter your cipher in hex > ')
        r.sendline(newmsg.hex().encode())
        r.recvline()
        result = r.recvline().decode().strip()
        return bytes.fromhex(result)

    def decrypt_(msg):
        newmsg = msg + b'\x00'*(256-len(msg))
        r.recvuntil(b'Please enter your cipher in hex > ')
        r.sendline(newmsg.hex().encode())
        r.recvline()
        result = r.recvline().decode().strip()
        return bytes.fromhex(result)

    # proof_of_work()
    msg = b'\x00'*16
    decrypt(msg)
    c = b""
    for i in range(50):
        t = decrypt(c)[i]
        c += long_to_bytes(t^plaintext[i])

    decc = decrypt_(c)
    print(decc)
    res = r.recvline()+r.recvline()
    if b"Here is your flag" in res:
        print(r.recvline())
        print(r.recvline())
        r.close()
        return (True, len(decc))
    r.close()
    return (False, len(decc))

ll = []
while True:
    ss = main()
    ll.append(ss[1])
    if ss[0]: break
    print(len(ll), ll)
