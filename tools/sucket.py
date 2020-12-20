import socket

sock = socket.socket()
sock.connect(('localhost', 1234))

for i in range(2):
    a = bytes('{"body":{"name":"stepkaaa","login":"stepanfffffff7kek","password":"$2a$14$t542x1V2NLsoZDr/pUDSL.PuhEIal5BnYCzQeSPTWh/rB4CwWi/wS","Addr":""},"header":"register"}', encoding='utf-8')
    sock.send(a)
    data = sock.recv(1024)
    print(data)


sock.close()

print(data)
