import socket
import json
from RequestHandler import *
from lib.Packets import *
from random import randint

import threading
import socket
import argparse
import os


class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1000)
        #print('Listening at', sock.getsockname())

        while True:
            sc, sockname = sock.accept()
            #print('Accepted a new connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))

            server_socket = ServerSocket(sc, sockname, self)
            server_socket.start()

            self.connections.append(server_socket)
            #print('Ready to receive messages from', sc.getpeername())

    def broadcast(self, message, source):
        for connection in self.connections:
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):
        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):
        while True:
            message = self.sc.recv(9999999)
            if message:
                #print('{} says {!r}'.format(self.sockname, message))

                try:
                    decoded_request = message.decode(encoding="utf-8")
                    request = json.loads(decoded_request)
                    #print("Success.")
                except Exception as e:
                    #print("Error.")
                    self.sendall(SyntaxErrorPacket().to_bytes())
                    continue

                response = ChatileRequestHandler.handle_request(request)
                #print(f"Response is {response.to_bytes().decode(encoding='utf-8')}")

                self.send(response.to_bytes())

            else:
                #print('{} has closed the connection'.format(self.sockname))
                self.sc.close()
                server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message)


ChatileRequestHandler = RequestHandler()

server = Server('0.0.0.0', APP_PORT)
server.start()

exit = threading.Thread(target=exit, args=(server,))
exit.start()