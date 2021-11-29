import aegis
import base64
import secrets
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
FLAG_PATH = path+"/flag.txt"
flag = open(FLAG_PATH).read().strip()
def encrypt():
    key = os.urandom(16)
    iv = os.urandom(16)
    cipher = aegis.Aegis128(key,16)
    # iv can be known
    print(base64.standard_b64encode(iv).decode('utf-8'))
    for _ in range(7):
        pt = base64.standard_b64decode(input().strip())
        aad = base64.standard_b64decode(input().strip())
        ct, tag = cipher.encrypt(iv, aad, pt)
        print(base64.standard_b64encode(ct).decode('utf-8'))
        print(base64.standard_b64encode(tag).decode('utf-8'))

    S2 = cipher.initialize(iv)
    S2 = cipher.state_update(S2, bytes(16))
    print("Oops, something leak:",end='')
    print(base64.standard_b64encode(S2[2]).decode('utf-8'))
    S1 = base64.standard_b64decode(input().strip())
    if S1 == b''.join(S2):
        print("You pass this challenge!!")
        print(flag)
    else:
        print("Failed!!")

    return 

if __name__ == "__main__":
    encrypt()
