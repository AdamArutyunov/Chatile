import socket
import json
from RequestHandler import *

APP_PORT = 1234

sock = socket.socket()
sock.bind(('0.0.0.0', APP_PORT))
sock.listen(1000)

ChatileRequestHandler = RequestHandler()


while True:
    connection, address = sock.accept()
    data = connection.recv(10240)

    if not data:
        connection.close()

    try:
        decoded_request = data.decode(encoding="utf-8")
        request = json.loads(decoded_request)
    except Exception as e:
        connection.send()
        connection.close()
        continue

    response = ChatileRequestHandler.handle_request(request)

    connection.send(response)
    connection.close()
