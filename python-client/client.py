import socket
import bcrypt
import json
import datetime
import threading
from time import sleep

RUN_UPDATE = False


def update(token, login):
    messages = set()
    while RUN_UPDATE:
        all_messages = send_request(build_get_messages(token, login))['body']['messages']
        sleep(0.1)
        new_messages = all_messages[len(messages):]
        for message in new_messages:
            print(*format_message(message))

        messages = all_messages


def build_register(name, login, password):
    data = {
        "header": "register",
        "body": {
            "name": name,
            "login": login,
            "password": bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode('utf8')
        }
    }

    return data


def build_login(login, password):
    data = {
        "header": "login",
        "body": {
            "login": login,
            "password": password
        }
    }

    return data


def build_send_message(token, message_data, recipient_login):
    data = {
        'header': "send_message",
        "body": {
            "token": token,
            "data": message_data,
            "recipient_login": recipient_login
        }
     }

    return data


def build_get_messages(token, login):
    data = {
        'header': "get_messages",
        "body": {
            "token": token,
            "login": login
        }
    }

    return data


def send_request(data):
    string_data = json.dumps(data)
    bytes_data = string_data.encode('utf8')

    sock.send(bytes_data)
    response = sock.recv(10240)
    response_data = json.loads(response)
    return response_data


def format_message(message):
    return (datetime.datetime.fromtimestamp(message['sending_date']).strftime("[%d.%m.%Y %H:%M]"),
            message['sender_login'], '->', message['recipient_login'], "\t\t", message['data'])


sock = socket.socket()
sock.connect(('localhost', 1234))

while True:
    logged = False
    token = None

    print("Добро пожаловать в Chatile.")
    print("Доступные команды:")
    print("login: вход в систему")
    print("register: регистрация")

    command = input(">>> ").strip()
    while command not in ["login", "register"]:
        command = input(">>> ").strip()

    while not logged:
        if command == "login":
            login = input("Введите логин:\n>>> ")
            password = input("Введите пароль:\n>>> ")

            response = send_request(build_login(login, password))
            if response['header'] != 'error':
                token = response['body']['token']
                logged = True
            else:
                print(response['body']['message'])

        elif command == 'register':
            login = input("Введите логин:\n>>> ")
            password = input("Введите пароль:\n>>> ")
            name = input("Введите имя:\n>>> ")

            response = send_request(build_register(name, login, password))
            if response['header'] != 'error':
                token = response['body']['token']
                logged = True
            else:
                print(response['body']['message'])

    while True:
        print("Введите логин человека, с которым хотите пообщаться:")
        recipient_login = input()

        response = send_request(build_get_messages(token, recipient_login))

        RUN_UPDATE = True
        update_thread = threading.Thread(target=lambda: update(token, recipient_login))
        update_thread.start()

        if response['header'] == 'error':
            print(response['body']['message'])
        else:
            for message in response['body']['messages']:
                #print(*format_message(message))
                pass

        while True:
            message_text = input()
            if message_text == 'q':
                break

            send_request(build_send_message(token, message_text, recipient_login))

            #response = send_request(build_get_messages(token, recipient_login))
            #print(response)
            #print(*format_message(response['body']['messages'][-1]))

        RUN_UPDATE = False
        update_thread.join()

sock.close()
