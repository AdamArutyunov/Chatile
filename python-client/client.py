import socket
import bcrypt
import json
import datetime
import threading
import colorama
from colorama import *
from time import sleep

colorama.init()
RUN_UPDATE = False


def update(token, login):
    messages = set()
    while RUN_UPDATE:
        try:
            all_messages = send_request(build_get_messages(token, login))['body']['messages']
            sleep(0.1)
            new_messages = all_messages[len(messages):]
            print(Fore.GREEN + Back.BLACK + Style.BRIGHT, end='')
            for message in new_messages:
                print(*format_message(message))
            print(Fore.YELLOW + Back.BLACK + Style.BRIGHT, end='')

            messages = all_messages
        except Exception as e:
            continue


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


def build_get_user(login):
    data = {
        'header': "get_user",
        "body": {
            "login": login
        }
    }

    return data


def build_online(token):
    data = {
        'header': 'online',
        'body': {
            'token': token
        }
    }

    return data


def send_request(data):
    string_data = json.dumps(data, ensure_ascii=False)
    bytes_data = string_data.encode('utf8')

    sock.send(bytes_data)
    response = sock.recv(10240)
    response_data = json.loads(response)
    return response_data


def format_message(message):
    return (datetime.datetime.fromtimestamp(message['sending_date']).strftime("(%d.%m.%Y %H:%M)"),
            message['sender_login'], "\t\t", message['data'])


sock = socket.socket()
sock.connect(('localhost', 1234))


response = send_request(build_get_user('123'))
print(response)

while True:

    logged = False
    token = None

    print(Fore.CYAN + Back.BLACK + Style.BRIGHT)
    print("Добро пожаловать в Chatile.")
    print("Доступные команды:")
    print("login: вход в систему")
    print("register: регистрация")

    print(Back.MAGENTA + Fore.WHITE)
    command = input(">>> ").strip()
    while command not in ["login", "register"]:
        command = input(">>> ").strip()

    while not logged:
        if command == "login":
            print(Back.RED + Fore.WHITE)
            login = input("Введите логин:\n>>> ")
            password = input("Введите пароль:\n>>> ")

            print(Fore.CYAN + Back.BLACK + Style.BRIGHT)
            print("Подключаемся...")
            response = send_request(build_login(login, password))
            if response['header'] != 'error':
                token = response['body']['token']
                logged = True
                print(Back.GREEN + Fore.WHITE + "Успешная авторизация!")
            else:
                print(Back.RED + Fore.WHITE + "Неверный логин или пароль!")

        elif command == 'register':
            print(Back.RED + Fore.WHITE)
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
        print(Back.CYAN + Fore.WHITE)
        print("Введите логин человека, с которым хотите пообщаться:")
        print(Back.MAGENTA + Fore.WHITE)
        recipient_login = input(">>> ")

        print(Fore.CYAN + Back.BLACK + Style.BRIGHT)
        print("Устанавливаем соединение...")
        response = send_request(build_get_messages(token, recipient_login))

        if response['header'] == 'error':
            print(Back.RED + Fore.WHITE)
            print("Мы не нашли пользователя с таким логином.")
            continue

        RUN_UPDATE = True
        update_thread = threading.Thread(target=lambda: update(token, recipient_login))
        update_thread.start()

        print("Соединение установлено. Приятного общения!")

        print(Fore.GREEN + Back.BLACK + Style.BRIGHT)

        while True:
            print(Fore.YELLOW + Back.BLACK + Style.BRIGHT, end='')
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
