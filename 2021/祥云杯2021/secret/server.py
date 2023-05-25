#! /usr/bin/env python
import SocketServer
from libnum import n2s, s2n
from random import getrandbits
from hashlib import sha256

from secret import flag

p, g = 0xb5655f7c97e8007baaf31716c305cf5950a935d239891c81e671c39b7b5b2544b0198a39fd13fa83830f93afb558321680713d4f6e6d7201d27256567b8f70c3, \
       0x85fd9ae42b57e515b7849b232fcd9575c18131235104d451eeceb991436b646d374086ca751846fdfec1ff7d4e1b9d6812355093a8227742a30361401ccc5577


def h2(m):
    return int(sha256(m).hexdigest(), 16)


def key_gen(nbits):
    s = getrandbits(nbits) % p
    while s.bit_length() < nbits - 2:
        s = getrandbits(nbits) % p
    pk2 = pow(g, s, p)
    return pk2, s


def enc(m, pk2):
    m = s2n(m)
    e, v = getrandbits(256), getrandbits(256)
    E, V = pow(g, e, p), pow(g, v, p)
    s = v + e * h2(n2s(E) + n2s(V))
    c = m * pow(pk2, e + v, p) % p
    cap = (E, V, s)
    return c, cap


def rk_gen(sk2, pk1, group=9):
    x, r = getrandbits(512) % p, getrandbits(512) % p
    prefix = n2s(pow(g, x * sk2, p)).rjust(64, '\x00')
    encoder = [1, -pow(pk1, x * sk2, p) % p]
    for i in range(1, group + 1):
        pkj = getrandbits(512)
        new_encoder = [1]
        cur = pow(pkj, x * sk2, p)
        for j in range(1, i + 1):
            new_encoder.append((encoder[j] + (-1) * cur * encoder[j - 1]) % p)
        new_encoder.append(encoder[i] * cur * (-1) % p)
        encoder = new_encoder
    encoder[-1] += r
    dd = h2(prefix + n2s(r).rjust(64, '\x00')) | 1
    rk = sk2 * dd
    return rk, encoder[1:], prefix


def re_enc(rk, cipher):
    c, (E, V, s) = cipher
    E_ = pow(E, rk, p)
    V_ = pow(V, rk, p)
    s_ = s * rk % p
    return c, (E_, V_, s_)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class EncHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.sendall("Welcome to our netdisk system! Our system store only users' ciphertext\n")
        self.request.sendall("Now you can choose what you wanna do\n")
        self.request.sendall("1. generate your key\n2. start challenge\n2. get the ciphertext")
        pk1, sk1 = key_gen(512)
        cipher = enc(flag, pk1)
        pk2, sk2   = key_gen(512)
        while 1:
            mul = 1
            self.request.sendall('Input your choice\n')
            self.request.sendall("choice>")
            choice = self.request.recv(16).strip()
            if choice == '1':
                self.request.sendall('Please take good care of it!\n' + hex(pk2) + ',' + hex(sk2) + '\n')
            elif choice == '2':
                group_list = [32, 64, 128, 256]
                for group in group_list:
                    m = getrandbits(200)
                    plaintext = n2s(m)
                    cur_cipher = enc(plaintext, pk1)
                    rk, encoder, prefix = rk_gen(sk1, pk2, group=group)
                    mul *= rk
                    mul %=   p
                    new_cipher = re_enc(rk, cur_cipher)
                    self.request.sendall('The cipher shared to you\n' + str(new_cipher) + '\n')
                    self.request.sendall('prefix, encoder = ' + str((encoder, prefix.encode('hex'))) + '\n')
                    ans = self.request.recv(1024).strip()
                    if int(ans, 16) != m:
                        exit(1)
                self.request.sendall('You are a clever boy! Now I can share you some other information!\n' + hex(mul) + '\n')
            elif choice == '3':
                self.request.sendall(str(cipher) + '\n')
                exit(1)
            else:
                continue


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1213
    server = ThreadedTCPServer((HOST, PORT), EncHandler)
    server.serve_forever()

