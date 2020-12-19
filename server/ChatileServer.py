import socket
import json
from RequestHandler import *
from lib.Packets import *
from random import randint


print("Creating socket...")
sock = socket.socket()
print("Socket created")

print("Configuring...")
sock.bind(('0.0.0.0', APP_PORT))
sock.listen(1000)

ChatileRequestHandler = RequestHandler()

print("Starting server...")
while True:
    connection, address = sock.accept()
    print(f"Accepted connection on {address[0]}")

    data = connection.recv(1024)
    print(f"New data: {data}")

    if not data:
        print("No data...")
        connection.close()
        continue

    print("Trying to decode request...")
    try:
        decoded_request = data.decode(encoding="utf-8")
        request = json.loads(decoded_request)
        print("Success.")
    except Exception as e:
        print("Error.")
        connection.send(SyntaxErrorPacket().to_bytes())
        connection.close()
        continue

    response = ChatileRequestHandler.handle_request(request)
    print(f"Response is {response.to_bytes().decode(encoding='utf-8')}")

    connection.send(response.to_bytes())
    connection.close()
