import socket

sock = socket.socket()
sock.connect(('localhost', 9090))

a = bytes(input(), encoding='utf-8')
sock.send(a)

data = sock.recv(1024)
sock.close()

print(data)