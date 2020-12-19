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

            if header == Headers.REGISTER:
                name = request['name']
                login = request['login']
                password = request['password']

                user = User()
                user.name = name
                user.login = login
                user.set_password(password)

                session.add(user)
                session.commit()

                return user.auth(password)

            if header == Headers.LOGIN:
                login = request['login']
                password = request['password']

                user = session.query(User).filter(User.login == login).first()
                if not user:
                    return BadLoginErrorPacket("Bad login: invalid login")

                return user.auth(password)

            if header == Headers.SEND_MESSAGE:
                token = request['token']

                user = get_user_by_token(token)
                if not user:
                    return BadTokenErrorPacket()

                data = request["data"]
                recipient_login = request["recipient_login"]

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
                token = request['token']

                user = get_user_by_token(token)
                if not user:
                    return BadTokenErrorPacket()

                login = request['login']
                recipient = session.query(User).get(User.login == login)

                if not recipient:
                    return BadRequestErrorPacket("user does not exist")

                messages = session.query(Message).filter((Message.sender == user) &
                                                         (Message.recipient == recipient))\
                    .order_by(Message.sending_date).all()

                return MessageBatchPacket(user.login, recipient.login,
                                          [message.to_dict(only=("data", "sending_time")) for message in messages])

        except Exception as e:
            return BadRequestErrorPacket(e)
