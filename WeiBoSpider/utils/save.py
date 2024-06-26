import json


class Save:
    def __init__(self, save_path, ):
        self.save_path = save_path

    def savetojson(self, file_name, data):
        with open(f'{self.save_path}/{file_name}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
