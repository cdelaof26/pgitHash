from tools.lang import CANNOT_HASH_FILE
from tools.lang import EXPLORING_DIR


from tools.FileHash import FileHash

from hashlib import sha1
from hashlib import md5
from sys import stdout
from os import get_terminal_size

# Utilities related to exploration of filesystem and creation of pseudo databases

BUFFER_SIZE = 65536


# Input:  str ; "/Users/cdelaof/Desktop/hello.txt"
# Output: str ; 5d41402abc4b2a76b9719d911017c592
#
def get_file_hash(file_path):
    global BUFFER_SIZE

    # if hash_func == "md5":
    #    func = md5()
    # else:
    func = sha1()

    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                func.update(data)
        return "{0}".format(func.hexdigest())
    except (FileNotFoundError, PermissionError) as e:
        print(CANNOT_HASH_FILE % file_path)
        print(str(e) + "\n")
        return ""


# Input: list, list, bool
#
# Notes: Uses reference
#
def explore_dir(directories, files, explore_subdirectories):
    columns = get_terminal_size()[0]
    msg = EXPLORING_DIR % directories[0].name
    extra_space = columns - len(msg)
    if extra_space > 0:
        msg += (" " * extra_space)

    stdout.write("\r")
    stdout.write(msg)
    stdout.flush()

    for item in directories[0].iterdir():
        if explore_subdirectories and item.is_dir():
            directories.append(item)
        elif item.is_file():
            file_hash = get_file_hash(item)
            files.append(FileHash(str(item), file_hash))

    directories.pop(0)
