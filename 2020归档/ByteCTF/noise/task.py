#!/usr/bin/env python3
from os import urandom
from random import choices
from hashlib import sha256
import signal
import string
import sys

# from flag import FLAG


def getrandbits(bit):
    return int.from_bytes(urandom(bit >> 3), "big")


def proof_of_work() -> bool:
    alphabet = string.ascii_letters + string.digits
    nonce = "".join(choices(alphabet, k=8))
    nonce = '00000000'    
    print(f'SHA256("{nonce}" + ?) starts with "00000"')
    suffix = input().strip()
    message = (nonce + suffix).encode("Latin-1")
    return sha256(message).digest().hex().startswith("00000")


def main():
    # signal.alarm(60)
    # if not proof_of_work():
    #     return
        
    secret = getrandbits(1024)
    print("Listen...The secret iz...M2@9c0f*#aF()I!($Ud3;J..."
          "Hello?...really noisy here again...God bless you get it...")
    for i in range(64):
        try:
            op = input().strip()
            num = input().strip()
        except EOFError:
            return
        if not str.isnumeric(num):
            print("INVALID NUMBER")
            continue
        num = int(num)
        if op == 'god':
            print(num * getrandbits(992) % secret)
        elif op == 'bless':
            if num == secret:

                try:
                    from datetime import datetime
                except Exception as e:
                    FLAG = "but something is error. Please contact the admin."

                print("SYC{123321}")
                return
            print("WRONG SECRET")
main()
