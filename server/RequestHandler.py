import json
from data import db_session
from Constants import *
from lib.Packets import *
from data.models.user import *
from data.models.message import *


def get_user_by_token(token):
    session = db_session.create_session()

    user = session.query(User).filter(User.token == token).first()
    if not user:
        return

    if not user.check_token(token):
        return

    return user


class RequestParser:
    def __init__(self, server):
        db_session.global_init(DATABASE_URI)
        self.server = server
        self.request_handler = RequestHandler()

    def handle_request(self, request: dict, socket) -> Packet:
        try:
            header = request["header"]
            body = request["body"]

            if header == Headers.REGISTER:
                return self.request_handler.register(body, socket)

            if header == Headers.LOGIN:
                return self.request_handler.login(body, socket)

            if header == Headers.USER:
                return self.request_handler.user(body, socket)

            if header == Headers.ONLINE:
                return self.request_handler.online(body, socket)

            if header == Headers.SEND_MESSAGE:
                return self.request_handler.send_message(body, socket)

            if header == Headers.GET_MESSAGES:
                return self.request_handler.get_messages(body, socket)

            return BadRequestErrorPacket('invalid header')

        except Exception as e:
            return BadRequestErrorPacket(e)


class RequestHandler:
    def __init__(self, server):
        self.server = server

    def register(self, body, socket):
        session = db_session.create_session()

        name = body['name']
        login = body['login']
        password = body['password']

        user = session.query(User).get(login)
        if user:
            return BadRegisterErrorPacket("Bad register: login exists")

        user = User()
        user.name = name
        user.login = login
        user.set_password(password)

        session.add(user)
        session.commit()

        result = user.auth()
        socket.user = user
        session.commit()

        return result

    def login(self, body, socket):
        session = db_session.create_session()

        login = body['login']
        password = body['password']

        user = session.query(User).get(login)
        if not user:
            return BadLoginErrorPacket("Bad login: invalid login")

        result = user.check_auth(password)
        session.commit()

        if result.__class__ == AuthPacket:
            socket.user = user

        return result

    def send_message(self, body, socket):
        session = db_session.create_session()

        token = body['token']

        user = get_user_by_token(token)
        if not user:
            return BadTokenErrorPacket()

        socket.user = user

        data = body["data"]
        recipient_login = body["recipient_login"]

        recipient = session.query(User).filter(User.login == recipient_login).first()
        if not recipient:
            return BadRequestErrorPacket("recipient does not exist")

        if not data:
            return BadRequestErrorPacket("message is empty")

        message = Message()
        message.sender = user
        message.recipient = recipient
        message.data = data

        session.add(message)

        for socket in self.server.get_connections_by_user(recipient):
            socket.send(MessagePacket(message).to_bytes())

        session.commit()

        return OKPacket()

    def get_messages(self, body, socket):
        session = db_session.create_session()

        token = body['token']

        user = get_user_by_token(token)
        if not user:
            return BadTokenErrorPacket()

        socket.user = user

        login = body['login']
        recipient = session.query(User).get(login)

        if not recipient:
            return BadRequestErrorPacket("user does not exist")

        messages = session.query(Message).filter(((Message.sender == user) & (Message.recipient == recipient)) |
                                                 ((Message.sender == recipient) & (Message.recipient == user))) \
            .order_by(Message.sending_date).all()

        formatted_messages = []
        for message in messages:
            formatted_messages.append({'sender_login': message.sender.login,
                                       'recipient_login': message.recipient.login,
                                       'data': message.data,
                                       'sending_date': int(message.sending_date.timestamp())})

        return MessageBatchPacket(formatted_messages)

    def online(self, body, socket):
        session = db_session.create_session()

        token = body['token']

        user = get_user_by_token(token)
        if not user:
            return BadTokenErrorPacket()

        socket.user = user

        user.online()
        session.commit()

        return OKPacket()

    def user(self, body, socket):
        session = db_session.create_session()

        login = body['login']

        user = session.query(User).get(login)
        if not user:
            return BadLoginErrorPacket("Bad login: invalid login")

        return UserPacket(user)
