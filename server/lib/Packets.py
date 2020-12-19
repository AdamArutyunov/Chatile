import json

class Packet:
    def __init__(self, data: dict):
        self.data = data

    def to_bytes(self):
        string_data = json.dumps(self.data)
        bytes_data = bytes(string_data, encoding="utf-8")

        return bytes_data