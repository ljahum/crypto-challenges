import ljahum
from itertools import product
from hashlib import sha256
import string
import re
tcp = ljahum.remote('42.192.180.50', 30002)


def pow():
    table = string.ascii_letters + string.digits
    
    hash2 = 'z5G9VjL2lKyXbeNQ'

    for _ in product(table, repeat=4):
        hash1 = ''.join(_)
        guess = hash1+hash2
        if (sha256(guess.encode()).hexdigest()) == '1de0166ffd64afe624c4f33a691e1981e570e221a00a25ab43272c368c9f5c06':
            print('yes')
            print('xxxx=', hash1)


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
