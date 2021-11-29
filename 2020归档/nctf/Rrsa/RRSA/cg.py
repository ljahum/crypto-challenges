import ljahum
from itertools import product
from hashlib import sha256
import string
import re
tcp = ljahum.remote('42.192.180.50', 30002)


def pow():
    table = string.ascii_letters + string.digits
    s = tcp.recv_until(b'+')
    s = tcp.recv_until(b')')
    hash2 = s[:-1].decode()
    hash2 = '2lVgpDHaofUTuyEw'
    s = tcp.recv_until(b'== ')
    shastr = tcp.recv_until(b'Give')[:-5]
    print('xxxx +',hash2,'=',shastr.decode())

    for _ in product(table, repeat=4):
        hash1 = ''.join(_)
        guess = hash1+hash2
        if (sha256(guess.encode()).hexdigest()) == 'c6dfd5c9a036123992c046dffceaf262bda2732a5baa5645d5194476a239bba1':
            print('yes')
            print('xxxx=',hash1)
            tcp.sendline(bytes(hash1, encoding='utf-8'))
            s = tcp.recv_all()
            print(s)
    

def main():
    pow()
    
    return

if __name__ == '__main__':
    main()


'''
4f8c9bf9a612ebb7bfcc0fc2e3ba9739c8e43097e6f4ac5d82afe3194d5f2394
9b3fb9358019b7de093fe4690cc1478981c255b490137cfa73d3ef35bc5873e5
XXXX+RkURKfd2TW7pJAGD
     5zZ9YA5sngQSjEjg
     ssvaPxwkqD7ishiF
     LsqXbbiqbJQT4BC9


'''
