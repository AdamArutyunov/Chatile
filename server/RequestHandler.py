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


class RequestHandler:
    def __init__(self):
        db_session.global_init(DATABASE_URI)

    def handle_request(self, request: dict) -> Packet:
        session = db_session.create_session()

        try:
            header = request["header"]
            body = request["body"]

            if header == Headers.REGISTER:
                name = body['name']
                login = body['login']
                password = body['password']

                user = session.query(User).filter(User.login == login).first()
                if user:
                    return BadRegisterErrorPacket("Bad register: login exists")

                user = User()
                user.name = name
                user.login = login
                user.set_password(password)

                session.add(user)
                session.commit()

                result = user.auth()
                session.commit()

                return result

            if header == Headers.LOGIN:
                login = body['login']
                password = body['password']

                user = session.query(User).filter(User.login == login).first()
                if not user:
                    return BadLoginErrorPacket("Bad login: invalid login")

                result = user.check_auth(password)
                session.commit()

                return result

            if header == Headers.SEND_MESSAGE:
                token = body['token']

                user = get_user_by_token(token)
                if not user:
                    return BadTokenErrorPacket()

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
                session.commit()

                return OKPacket()

            if header == Headers.GET_MESSAGES:
                token = body['token']

                user = get_user_by_token(token)
                if not user:
                    return BadTokenErrorPacket()

                login = body['login']
                recipient = session.query(User).filter(User.login == login).first()

                if not recipient:
                    return BadRequestErrorPacket("user does not exist")

                messages = session.query(Message).filter(((Message.sender == user) & (Message.recipient == recipient)) |
                                                         ((Message.sender == recipient) & (Message.recipient == user)))\
                    .order_by(Message.sending_date).all()

                formatted_messages = []
                for message in messages:
                    formatted_messages.append({'sender_login': message.sender.login,
                                               'recipient_login': message.recipient.login,
                                               'data': message.data,
                                               'sending_date': int(message.sending_date.timestamp())})

                return MessageBatchPacket(user.login, recipient.login,
                                          formatted_messages)

            return BadRequestErrorPacket('invalid header')

        except Exception as e:
            raise e
            return BadRequestErrorPacket(e)