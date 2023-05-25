from Crypto.Util.number import *
from hashlib import sha512
from random import choices
# from flag import flag
import string
from data import NS

flag =b'123321'


Bits = 512
length = 224


# def proof_of_work() -> bool:
#     alphabet = string.ascii_letters + string.digits
#     head = "".join(choices(alphabet, k=8))
#     print(f'POW: SHA512("{head}" + ?) starts with "11111"')
#     tail = input().strip()
#     message = (head + tail).encode()
#     return sha512(message).hexdigest().startswith("11111")

    
def check_ans(_N, _x) -> bool:
    check = 0
    for i in range(len(_N)):
        check += _N[i] * _x[i]
    return check == 0


def main():
    # if not proof_of_work():
        # return
    print("Welcome to MRCTF2021, enjoy this friendly sign-in question~")
    # flag_bits = bin(bytes_to_long(flag.encode()))[2:]
    N = NS
    print('N =', N)
    X = []
    for i in range(length):
        x = [int(input().strip()) for _ in range(length)]
        if x in X:
            print('No cheat!')
            return
        if x.count(0) > 0:
            print('No trivial!')
            return
        if not check_ans(N, x):
            print('Follow the rule!')
            return
        X.append(x)
        print('your gift:',i)


main()
