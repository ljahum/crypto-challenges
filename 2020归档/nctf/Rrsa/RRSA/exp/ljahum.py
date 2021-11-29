# -*- coding: utf-8 -*-

from socket import *
    

class remote():
    """Create a new easy-socket object
    __init__(self,host, port,timeout=5)
            host: str
            port: int
            timeout: int (default = 5)
    
    """
    def __init__(self,host, port,timeout=5):
        addr = (host, port)
        self.tcp = socket(AF_INET, SOCK_STREAM)
        self.tcp.settimeout(timeout)
        print(addr)
        self.tcp.connect(addr)

    def recvline(self):
        Recv_bytes = b'-'
        while Recv_bytes[len(Recv_bytes)-1] != 10:
            Recv_bytes += self.tcp.recv(1)
        return Recv_bytes[1:]
    def sendline(self,data):
        self.tcp.send(data+b'\n')

    def recv_all(self):
        data = b''
        try:
            while True:
                t = self.tcp.recv(1024)
                data += t
        finally:
            return data

    def recv_endswith(self, index):
        data = b''
        try:
            while True:
                t = self.tcp.recv(1)
                data += t
                
                if data.endswith(index):
                    return data
        finally:
            return data
        
    def recv_until(self, index):
        data = b''
        try:
            while True:
                t = self.tcp.recv(1)
                data += t
                if data.endswith(index):
                    return data[:len(index)]
        finally:
            return data

