import os
import hashlib


def md5hash(file_path):
    file_path = os.path.normpath(file_path)
    file_name = os.path.basename(file_path)
    advanced = file_name.split('.')
    if advanced[1] == 'txt':
        with open(file_path, mode='r', encoding='utf-8') as file:
            for line in file:
                line_str = file.readline().strip()
                hash_line = hashlib.md5(line_str.encode('utf-8')).hexdigest()
                yield hash_line
    else:
        print('Это не текстовый файл')


if __name__ == '__main__':
    for i in md5hash('/Users/antongrutsin/Downloads/recipes.txt'):
        print(i)
