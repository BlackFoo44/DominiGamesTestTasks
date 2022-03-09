import sys
import os


def cur_file_dir():
    # Получить текущий путь к файлу
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def rename(path):
    file_list = os.listdir(path)
    # print(file_list)
    for file in file_list:
        # print(file)
        old_dir = os.path.join(path, file)
        filename = os.path.splitext(file)[0]
        # print(filename)
        filetype = os.path.splitext(file)[1]
        # print(filetype)
        new_name = filename.replace(filename, filename.lower())
        new_dir = os.path.join(path, new_name + filetype)
        os.rename(old_dir, new_dir)
        if os.path.isdir(new_dir):
            rename(new_dir)


if __name__ == "__main__":
    path = cur_file_dir()
    rename(path)
