import json


class Read:
    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def readjson(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
