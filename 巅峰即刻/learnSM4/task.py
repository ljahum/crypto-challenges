import SocketServer
import signal,os,random,string
from hashlib import sha256
from sm4 import encrypt,decrypt,encrypt_


class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
        self.request.send('Give me XXXX:')
        x = self.request.recv(10)
        x = x.strip()
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest: 
            return False
        return True

    def dorecv(self,sz):
        try:
            return self.request.recv(sz).strip()
        except:
            return 0

    def dosend(self, msg):
        try:
            self.request.sendall(msg)
        except:
            pass


    def handle(self):
        flag =b'213123123213'
        signal.alarm(300)
        # if not self.proof_of_work():
        #     return
        key = os.urandom(16)
        print(key,len(key))
        key='0'*16
        key = int(key.encode('hex'),16)
        self.dosend("Welcome to the Crypto System.")
        from sm4 import _round_keys
        keys = _round_keys(key)
        print(keys[0])
        hint1 = sha256(str(keys[0])).hexdigest()
        self.dosend('hint is : '+hint1+'\n')
        hint = 'Next you have 16 shots.\n'
        self.dosend(hint)
        for i in range(8):
            self.dosend('r:')
            r = self.dorecv(0x10)
            r = int(r)
            if r <2:
                self.dosend('i:')
                i = self.dorecv(0x10)
                i = abs(int(i))
                if i <4:
                    self.dosend('msg(hex):\n')
                    msg = self.dorecv(40)
                    msg = int(msg[:32],16)
                    if msg == 0:
                        self.dosend('Dont cheat\n')
                        self.request.close()
                    else:
                        msg,leak = encrypt_(msg,key,r,i)
                        self.dosend(hex(msg)[2:10]+'\n')
                        self.dosend(str(leak)+'\n')

                else:
                    self.dosend('Dont cheat\n')
                    self.request.close()

            else:
                self.dosend('Dont cheat\n')
                self.request.close()
        self.dosend('Give me answer:')
        k1 = int(self.dorecv(20))
        if k1 == keys[0]:
            self.dosend(flag);
        self.request.close()


class ForkingServer(SocketServer.ForkingTCPServer, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10005
    server = ForkingServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
