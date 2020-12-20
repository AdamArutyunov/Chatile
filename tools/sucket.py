import socket
import bcrypt
import json

sock = socket.socket()
sock.connect(('localhost', 1234))
'''
print(bcrypt.hashpw('adam'.encode('utf8'), bcrypt.gensalt()))

data = {
    "body": {
        "name": "Adam Arutyunov",
        "login": "adam",
        "password": "$2b$12$pqoAR8vEXdkUQLsnOsFmrO01bfxG2SVxSiDBiA1RyPUXxpVU7zLtG"},
    "header": "register"
    }

a = json.dumps(data).encode('utf8')
sock.send(a)
data = sock.recv(1024)
response = json.loads(data)
print(response)
'''

data = {
    "body": {
        "name": "Adam Arutyunov",
        "login": "adam",
        "password": "adam"},
    "header": "login"
    }

a = json.dumps(data).encode('utf8')
sock.send(a)
data = sock.recv(1024)
response = json.loads(data)
print(response)


'''
token = response['body']['token']
print(token)

data = {'header': "send_message",
        "body": {
            "token": token,
            "data": "hello motherfucker",
            "recipient_login": "adam"
            }
        }

a = json.dumps(data).encode('utf8')

sock.send(a)
data = sock.recv(1024)
response = json.loads(data)
print(response)'''


token = response['body']['token']
print(token)

data = {'header': "get_messages",
        "body": {
            "token": token,
            "login": "adam"
            }
        }

a = json.dumps(data).encode('utf8')

sock.send(a)
data = sock.recv(1024)
response = json.loads(data)
print(response)


sock.close()
