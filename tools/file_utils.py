from tools.lang import CANNOT_HASH_FILE
from tools.lang import CANNOT_READ_CONTENTS
from tools.lang import FILES_AT
from tools.lang import DIRECTORIES_AT
from tools.lang import FILES_AND_DIRECTORIES_AT
from tools.lang import GO_BACK
from tools.lang import SELECT_AN_OPTION
from tools.lang import DO_YOU_WANT_TO_MOVE_OR_SELECT_IT
from tools.lang import PATH_DOESNT_EXIST
from tools.lang import CANNOT_COPY_OR_MOVE_FILE

from tools.util import choose
from tools.util import create_selectable_list

from hashlib import sha1
from hashlib import sha224
from hashlib import sha256
from hashlib import sha384
from hashlib import sha512
from hashlib import md5

from pathlib import Path

from subprocess import call


# File utils

BUFFER_SIZE = 65536

current_directory = Path.cwd()


# Input:  Path ; Path("/home/cdelaof26/pgitHash/settings")
# Output: str  ; "config_data"
#
def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError, PermissionError):
        return ""


# Input:  Path, str ; Path("/Users/cdelaof26/pgitHash/settings"), "configData"
# Output: Bool      ; True
#
def write_file(file_path, data):
    try:
        with open(file_path, "w") as file:
            return file.write(data)
    except (IsADirectoryError, FileNotFoundError, PermissionError):
        return False


# Input:  str ; "/Users/cdelaof/Desktop/hello.txt"
# Output: str ; 5d41402abc4b2a76b9719d911017c592
#
def create_file_hash(file_path, hash_func):
    global BUFFER_SIZE

    if hash_func == "sha1":
        func = sha1()
    elif hash_func == "sha224":
        func = sha224()
    elif hash_func == "sha256":
        func = sha256()
    elif hash_func == "sha384":
        func = sha384()
    elif hash_func == "sha512":
        func = sha512()
    else:
        func = md5()

    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                func.update(data)
        return str("{0}".format(func.hexdigest()))
    except (FileNotFoundError, PermissionError) as e:
        print(CANNOT_HASH_FILE % str(file_path))
        print(e)
        print()
        return ""


# Input:  Path, bool, bool, bool, list -> Path("/home/cdelaof/"), False
# Output: list                         -> ['.bash', 'Desktop', 'Documents', 'Downloads']
#
def retrieve_files_and_directories(path,
                                   retrieve_full_path,
                                   allow_files=True,
                                   allow_directories=True,
                                   allowed_extensions=None) -> list:
    items_found = list()

    try:
        for item in path.iterdir():
            # If there is any only-allowed extension
            # verifies if a file is allowed
            if allowed_extensions is not None and \
                    item.suffix not in allowed_extensions and \
                    not item.is_dir():
                continue

            if retrieve_full_path:
                if allow_files and allow_directories:
                    items_found.append(item.resolve())
                elif allow_files and item.is_file():
                    items_found.append(item.resolve())
                elif item.is_dir():
                    items_found.append(item.resolve())
            else:
                if allow_files and allow_directories:
                    items_found.append(item.name)
                elif allow_files and item.is_file():
                    items_found.append(item.name)
                elif item.is_dir():
                    items_found.append(item.name)
    except (PermissionError, FileNotFoundError) as e:
        print(CANNOT_READ_CONTENTS % str(path))
        print(e)
        print()

    return items_found


# Input:      bool, bool -> True, False
# User_input: int        -> 0
# Output:     Path       -> "/path/to/selected/file1"
#
def file_browser(allow_files=True, allow_directories=True, allowed_extensions=None) -> Path:
    global current_directory

    if allow_files and allow_directories:
        title = FILES_AND_DIRECTORIES_AT
    elif allow_files:
        title = FILES_AT
    else:
        title = DIRECTORIES_AT

    while True:
        if current_directory.exists() and current_directory.is_file():
            current_directory = current_directory.parent
        elif not current_directory.exists():
            current_directory = Path.cwd()

        print("\n" + title % str(current_directory))
        items = retrieve_files_and_directories(current_directory,
                                               False,
                                               allow_files,
                                               True,
                                               allowed_extensions)
        items += [GO_BACK]

        printable_list, options = create_selectable_list(items)

        print(printable_list)
        print(SELECT_AN_OPTION)
        option = input("> ")
        usr_path = None

        verified = option in options

        if not verified:
            # Needed to remove Darwin '\' for spaced directories
            if Path.cwd().anchor == "/":
                option = option.replace("\\", "")

            # Removes any space at start or end
            option = option.strip()

            tmp_path = Path(option)
            item_exist = tmp_path.exists()

            verified = (item_exist and tmp_path.is_file() and allow_files) or \
                       (item_exist and tmp_path.is_dir() and allow_directories)

            if verified:
                usr_path = tmp_path

        if verified and option != options[-1]:
            if usr_path is None:
                option_value = items[int(option)]
                current_directory = current_directory.joinpath(option_value)
            else:
                current_directory = usr_path

            if current_directory.is_file():
                # Select automatically if it's a file
                return current_directory

            if current_directory.is_dir() and not allow_directories:
                # If directories can't be selected, moves into automatically
                continue

            # If directories are allowed, prompt will ask if move into or select it
            print(DO_YOU_WANT_TO_MOVE_OR_SELECT_IT)
            if choose(["1", "2"], [False, True]):
                # Select it
                if current_directory.exists():
                    return current_directory

                # If somehow it disappears, user is told about that
                print(PATH_DOESNT_EXIST % (allow_files, allow_directories))
        elif option == options[-1]:
            current_directory = current_directory.parent
        else:
            print(PATH_DOESNT_EXIST % (allow_files, allow_directories))


# Input: Path
#
def create_directory(dir_path) -> bool:
    # Using format by %a and % doesn't work for unicode characters
    # That's why is needed use {0} and .format()
    # return call("mkdir %a" % str(dir_path), shell=True) == 0

    # mkdir will break since \" is used
    # Without \" names with space would be taken as two parameters
    # Use ' instead could solve it, but it's more common than ", so above problem will happened as well
    dir_path = str(dir_path).replace("\"", "\\\"")

    return call("mkdir \"{0}\"".format(dir_path), shell=True) == 0


# Input: Path
#
def create_directories(final_path):
    last_path = final_path
    while not final_path.exists():
        if create_directory(last_path):
            last_path = final_path
        else:
            last_path = last_path.parent


# Input: Path, Path
#
def copy_file(file_path, destiny_dir, move_file=False):
    # Command for Darwin and Linux
    if Path.cwd().anchor == "/":
        if not move_file:
            result = call("cp \"{0}\" \"{1}\"".format(str(file_path), str(destiny_dir)), shell=True)
        else:
            result = call("mv \"{0}\" \"{1}\"".format(str(file_path), str(destiny_dir)), shell=True)
    else:
        if not move_file:
            result = call("copy \"{0}\" \"{1}\"".format(str(file_path), str(destiny_dir)), shell=True)
        else:
            result = call("move \"{0}\" \"{1}\"".format(str(file_path), str(destiny_dir)), shell=True)

    if result != 0:
        print(CANNOT_COPY_OR_MOVE_FILE % (str(file_path), str(destiny_dir)))
