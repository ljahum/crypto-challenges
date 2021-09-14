#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import string
import random
import socketserver
import signal
import codecs
from os import urandom
from hashlib import sha256
from random import randint
from Crypto.Util.number import inverse, getPrime, getRandomInteger
# from flag import FLAG
FLAG = "SYC{123123123}"


BANNER = rb"""
  ___                 _     ___ _             _             ___         _             
 / __| ___ __ _ _ ___| |_  / __| |_  __ _ _ _(_)_ _  __ _  / __|_  _ __| |_ ___ _ __  
 \__ \/ -_) _| '_/ -_)  _| \__ \ ' \/ _` | '_| | ' \/ _` | \__ \ || (_-<  _/ -_) '  \ 
 |___/\___\__|_| \___|\__| |___/_||_\__,_|_| |_|_||_\__, | |___/\_, /__/\__\___|_|_|_|
                                                    |___/       |__/                  
"""

MENU = rb"""
[1] Get Your Key of Secret 1
[2] Get Your Key of Secret 2
[3] Get Others Keys of Secret 1
[4] Get Others Keys of Secret 2
[5] Submit Secret
[6] Exit
"""


def init_keys(ts, data, p):
    n = len(ts) + 1
    keys = []
    for _ in range(n):
        x = getRandomInteger(1024)
        y = data
        for i in range(n - 1):
            y = (y + ts[i] * pow(x, i + 1, p)) % p
        keys.append([x, y])
    return keys


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def proof_of_work(self):
        random.seed(urandom(128))
        alphabet = string.ascii_letters + string.digits
        proof = ''.join(random.choices(alphabet, k=16))
        hash_value = sha256(proof.encode('ascii')).hexdigest()
        self.send(('sha256(XXXX+%s) == %s' % (proof[4:], hash_value)).encode('ascii'))
        nonce = self.recv(prompt=b'Give me XXXX > ')
        if len(nonce) != 4 or sha256(nonce + proof[4:].encode('ascii')).hexdigest() != hash_value:
            return False
        return True

    def timeout_handler(self, signum, frame):
        self.send(b'\nTimeout!')
        raise TimeoutError

    def handle(self):
        signal.signal(signal.SIGALRM, self.timeout_handler)
        # signal.alarm(60)

        # if not self.proof_of_work():
        #     self.send(b'\nWrong!')
        #     self.request.close()
        #     return

        self.send(BANNER)

        secret_1 = getRandomInteger(256)

        secret_2 = getRandomInteger(256)
        print(secret_1,secret_2)
        
        n = 50
        p = getPrime(1024)
        # p = 127100161070729758324672563005919585088843557718198754483704240637539097558639707938939488773101162471030823228170890483077236346261016177325635908356835505581986535187340920340593665014827853496914359725363307847082205643499778919067969907971712520095774370034152191123554145608254118099051528821309936123263

        ts = [randint(1, p - 1) for _ in range(n - 1)]
        # t = 58510083877094693891040277851267905853617844771064576929521712771940231668984770883328421254238895212042598002659174059244201616561130950785238401399837559644941651285130352373844849078590789578028528768860166902952495931639692465443534927973027133719331474369633030490640443060779278904144461746302422307614
        # ts = [ t for _ in range(n - 1)]
        keys_1 = init_keys(ts, secret_1, p)
        keys_2 = init_keys(ts, secret_2, p)

        signal.alarm(240)

        while True:
            self.send(MENU, newline=False)
            try:
                choice = int(self.recv(prompt=b'Enter option > '))
            except:
                self.send(b'Error!')
                break

            # Get Your Key of Secret 1
            if choice == 1:
                self.send(('p = %s' % p).encode('ascii'))
                self.send(('key = (%s, %s)' % (keys_1[0][0], keys_1[0][1])).encode('ascii'))

            # Get Your Key of Secret 2
            elif choice == 2:
                self.send(('p = %s' % p).encode('ascii'))
                self.send(('key = (%s, %s)' % (keys_2[0][0], keys_2[0][1])).encode('ascii'))

            # Get Others Keys of Secret 1
            elif choice == 3:
                try:
                    user_no = int(self.recv(prompt=('Please enter user number (1-%d) > ' % (n - 1)).encode('ascii')))
                    
                except:
                    self.send(b'Error!')
                    break
                if 1 <= user_no <= n - 1:
                    self.send(('key = (%s, %s)' % (keys_1[user_no][0], keys_1[user_no][1])).encode('ascii'))
                    # print((keys_1[user_no][0], keys_1[user_no][1]))
                else:
                    self.send(b'Error!')
                    break

            # Get Others Keys of Secret 2
            elif choice == 4:
                self.send(b'Forbidden!')

            # Get Flag
            elif choice == 5:
                try:
                    s1 = int(self.recv(prompt=b'Please enter secret 1 > '))
                    s2 = int(self.recv(prompt=b'Please enter secret 2 > '))
                except:
                    self.send(b'Error!')
                    break
                if s1 == secret_1 and s2 == secret_2:
                    self.send(b'Wow! How smart you are! Here is your flag: ')
                    self.send(FLAG.encode('ascii'))
                    break
                else:
                    self.send(b'Sorry. Try again.')

            # Exit
            elif choice == 6:
                break

            else:
                self.send(b'Error!')
                break

        self.send(b'Bye!\n')
        self.request.close()


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 20001
    print(HOST, PORT)
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
