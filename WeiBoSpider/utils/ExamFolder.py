import os


def examfolder(dir_path):
    # 检查目录是否存在
    if not os.path.exists(dir_path):
        # 如果目录不存在，则创建它
        os.makedirs(dir_path)
    return dir_path


def examfile(file_path):
    return os.path.exists(file_path)


def get_newest_file(dir_path):
    # 获取目录中的所有文件
    files = os.listdir(dir_path)
    # 获取所有文件的创建时间
    creation_times = [os.path.getctime(os.path.join(dir_path, file)) for file in files]
    # 找出创建时间最新的文件
    newest_file = files[creation_times.index(max(creation_times))]
    newest_file_path = os.path.join(dir_path, newest_file)
    return newest_file_path, newest_file


class ExamFolder:
    def __init__(self):
        pass

    # 检查文件是否存在，不存在则创建 并返回创建路径
