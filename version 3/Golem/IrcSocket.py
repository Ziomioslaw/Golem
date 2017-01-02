#!/usr/bin/python
#-*- coding: utf-8 -*-
__author__="Ziomioslaw"
__date__ ="$2009-03-15 17:34:01$"
import socket

##
# Zakończnie linii używane w protocole IRC.
#
endofline = '\r\n'
packageSize = 4096

class IrcSocket:
    """IrcSocket - Dekorator na klasę Socket ze standardowej biblioteki
    """
    def __init__(self):
        self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recTmp = []

    def connect(self, network, port):
        self.mainSocket.connect((network, port))

    def send(self, data):
        self.mainSocket.send(data + endofline)

    def received(self):
        if (self.recTmp != []):
            return self.recTmp.pop(0).strip()
        while True:
            data = self.mainSocket.recv(packageSize)
            if data.find('PING') != -1:
                self.mainSocket.send('PONG ' + data.split()[1] + endofline)
            else:
                self.recTmp = data.split(endofline)
                return self.recTmp.pop(0).strip()

    def close(self):
        self.mainSocket.send('QUIT' + endofline)
        self.mainSocket.close()

if __name__ == "__main__":
    pass
