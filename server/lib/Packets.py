import json
from lib.Headers import *


class Packet:
    def __init__(self, data: dict):
        self.data = data

    def to_bytes(self):
        string_data = json.dumps(self.data)
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


class MessageBatchPacket(Packet):
    def __init__(self, sender_login: str, recipient_login: str, messages: list):
        super().__init__({'header': Headers.MESSAGES, 'body': {'messages': messages}})
