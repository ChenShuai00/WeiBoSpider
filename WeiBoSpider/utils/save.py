import json


class Save:
    def __init__(self, save_path, file_name, data):
        self.save_path = save_path
        self.file_name = file_name
        self.data = data

    def saveToJson(self):
        with open(f'{self.save_path}/{self.file_name}', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False)
