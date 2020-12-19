import json
from data import db_session
from Constants import *

class RequestHandler:
    def __init__(self):
        db_session.global_init(DATABASE_URI)

    def handle_request(self, request_bytes: bytes):
        try:
            decoded_request = request_bytes.decode(encoding="utf-8")
            request = json.loads(decoded_request)
        except Exception as e:
            return json.dumps()



