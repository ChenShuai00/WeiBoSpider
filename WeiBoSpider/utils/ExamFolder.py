import os


class ExamFolder:
    def __init__(self):
        pass

    def examfolder(self, dir_path):
        # 检查目录是否存在
        if not os.path.exists(dir_path):
            # 如果目录不存在，则创建它
            os.makedirs(dir_path)

        return dir_path



