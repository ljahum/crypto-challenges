from Crypto.Util.number import*
from Crypto.Cipher import AES
from secret import msg,password,flag
import socketserver
import signal
assert len(msg) == 32
assert len(password) == 8

def padding(msg):
    return msg + bytes([0 for i in range((16 - len(msg))%16)])

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

    def recv(self):
        return self._recvall()

    def login(self):
        right_num = 0
        while 1:
            self.send(b'[~]Please input your password:')
            str1 = self.recv().strip()[:8]
            print(str1)
            print(password)
            true_num = 0
            for i in range(len(password)):
                if str1[i] != password[i]:
                    login = False
                    self.send(b'False!')
                    break
                else:
                    true_num = i + 1 

                if right_num > true_num:
                    continue
                else:
                    right_num = true_num

                if true_num == len(password):
                    login = True
                check = b''
                for i in range(0x2000):
                    check = self.aes.encrypt(padding(check[:-1] + str1[:i+1]))

            if login == True:
                self.send(b"Login Success")
                return True,check[:16]
            
        return False

    def handle(self):
        signal.alarm(100)
        self.aes = AES.new(padding(password),AES.MODE_ECB)
        _,final_check = self.login()
        if _ == 1:
            # assert msg.decode() == final_check.hex()
            self.send(b'Good Morning Master!')
            self.send(flag)
            
class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    print("HOST:POST " + HOST+":" + str(PORT))
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()