import json
from lib.Headers import *
from data.models.message import *
from data.models.user import *


class Packet:
    def __init__(self, data: dict):
        self.data = data

    def to_bytes(self):
        string_data = json.dumps(self.data, ensure_ascii=False)
        bytes_data = bytes(string_data, encoding="utf-8")

        return bytes_data


class ErrorPacket(Packet):
    def __init__(self, code, message):
        self.code = code
        self.message = message

        super().__init__({'header': Headers.ERROR, 'body': {'code': code, 'message': message}})


class SyntaxErrorPacket(ErrorPacket):
    def __init__(self):
        super().__init__(1, "Invalid syntax")


class BadRequestErrorPacket(ErrorPacket):
    def __init__(self, message):
        super().__init__(2, f"Bad request: {message}")


class BadRegisterErrorPacket(ErrorPacket):
    def __init__(self, message):
        super().__init__(3, message)


class BadLoginErrorPacket(ErrorPacket):
    def __init__(self, message):
        super().__init__(4, message)


class BadTokenErrorPacket(ErrorPacket):
    def __init__(self):
        super().__init__(5, "Invalid token.")


class OKPacket(Packet):
    def __init__(self):
        super().__init__({'header': Headers.OK})


class AuthPacket(Packet):
    def __init__(self, token: str):
        super().__init__({'header': Headers.AUTH, 'body': {'token': token}})


class MessagePacket(Packet):
    def __init__(self, message):
        super().__init__({'header': Headers.MESSAGE, 'body': {'sender_login': message.sender.login,
                                                              'recipient_login': message.recipient.login,
                                                              'data': message.data,
                                                              'sending_date': int(message.sending_date.timestamp())}})


class MessageBatchPacket(Packet):
    def __init__(self, messages: list):
        super().__init__({'header': Headers.MESSAGE_BATCH, 'body': {'messages': messages}})


class UserPacket(Packet):
    def __init__(self, user):
        super().__init__({'header': Headers.USER, 'body': {'login': user.login,
                                                           'name': user.name,
                                                           'registration_date': int(user.registration_date.timestamp()),
                                                           'last_online_data': int(user.last_online_date.timestamp())}})
