#!/usr/bin/env python3
import hashlib, os, random, string
from secret import flag
from signal import alarm
from binascii import hexlify, unhexlify
# https://github.com/kravietz/pyOCB
from ocb.aes import AES
from ocb import OCB

aes = AES(128)
o = OCB(aes)
key = os.urandom(16)
o.setKey(key)

def proof_of_work():
    random.seed(os.urandom(8))
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
    digest = hashlib.sha256(proof.encode()).hexdigest()
    print("sha256(XXXX+%s) == %s" % (proof[4:],digest))
    print('Give me XXXX:')
    x = input()
    if len(x) != 4 or hashlib.sha256((x + proof[4:]).encode()).hexdigest() != digest: 
        return False
    return True

def encrypt(nonce,msg,associate_data):
    o.setNonce(nonce)
    tag, cipher = o.encrypt(bytearray(msg), bytearray(associate_data))
    return (bytes(cipher), bytes(tag))

def decrypt(nonce,cipher,tag,associate_data):
    o.setNonce(nonce)
    authenticated, message = o.decrypt(bytearray(associate_data), bytearray(cipher), bytearray(tag))
    if not authenticated:
        print("No no no!")
        return bytes(0)
    return bytes(message)

def main():
    alarm(60)
    if not proof_of_work():
        return
    for i in range(5):
        try:
            choice = int(input("Your choice:"))
            if choice == 1:
                nonce = unhexlify(input("Your nonce:"))
                msg = unhexlify(input("Your message:"))
                associate_data = b"From user"
                ciphertext, tag = encrypt(nonce, msg, associate_data)
                print("Your ciphertext:",hexlify(ciphertext).decode("utf-8"))
                print("Your tag:",hexlify(tag).decode("utf-8"))
            elif choice == 2:
                nonce = unhexlify(input("Your nonce:"))
                cipher = unhexlify(input("Your ciphertext:"))
                tag = unhexlify(input("Your tag:"))
                associate_data = b"From admin"
                msg = decrypt(nonce, cipher, tag, associate_data)
                if msg == b"I_am_admin_plz_give_me_the_flag":
                    print("Your flag:",flag)
                    break
            else:
                print("Wrong command!")
        except:
            print("Error!")

if __name__ == "__main__":
    main()