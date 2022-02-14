from tools.lang import SELECT_THE_DIRECTORY
from tools.lang import DO_YOU_WANT_EXPLORE_SUBDIRECTORIES
from tools.lang import ENTER_A_NAME_FOR_YOUR_DB
from tools.lang import SELECT_THE_OLDER_BD
from tools.lang import SELECT_THE_NEWER_BD
from tools.lang import ENTER_A_NAME_FOR_YOUR_CDB
from tools.lang import CANNOT_HASH_FILE
from tools.lang import EXPLORING_DIR
from tools.lang import CANNOT_READ_DIRECTORY
from tools.lang import XLSX_DOESNT_MEET_COLUMNS

from tools.FileHash import FileHash
from tools.FileHash import STATS

from tools.util import file_browser
from tools.util import choose

from pathlib import Path

from hashlib import sha1
# from hashlib import md5
from sys import stdout
from os import get_terminal_size

from openpyxl import Workbook
from openpyxl import load_workbook

from zipfile import BadZipFile

# Utilities related to exploration of filesystem and creation of pseudo databases

BUFFER_SIZE = 65536


# User_input: Path, bool, str -> "/home", True, "db"
# Output:     list            -> [["/home"], PosixPath("/home/cdelaof/db.xlsx"), True]
#
def setup_pdb_creation() -> list:
    print(SELECT_THE_DIRECTORY)
    directory = file_browser(allow_files=False)

    print(DO_YOU_WANT_EXPLORE_SUBDIRECTORIES)
    explore_subdirectories = choose(["1", "2"], [True, False])

    pdb_name = input(ENTER_A_NAME_FOR_YOUR_DB) + ".xlsx"
    pdb_path = Path.cwd().joinpath(pdb_name)

    return [[directory], pdb_path, explore_subdirectories]


# User_input: Path, Path, str -> "C:\\db.xlsx", "C:\\db1.xlsx", "cdb"
# Output:     list            -> [WindowsPath("C:\\db.xlsx"), WindowsPath("C:\\db1.xlsx"), WindowsPath("C:\\cdb.xlsx")]
#
def setup_pdb_comparison() -> list:
    print(SELECT_THE_OLDER_BD)
    older_pdb = file_browser(allow_directories=False, allowed_extensions=[".xlsx"])

    print(SELECT_THE_NEWER_BD)
    newer_pdb = file_browser(allow_directories=False, allowed_extensions=[".xlsx"])

    comparison_pdb_name = input(ENTER_A_NAME_FOR_YOUR_CDB) + ".xlsx"
    comparison_pdb_path = Path.cwd().joinpath(comparison_pdb_name)

    return [older_pdb, newer_pdb, comparison_pdb_path]


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
        return str("{0}".format(func.hexdigest()))
    except (FileNotFoundError, PermissionError) as e:
        print(CANNOT_HASH_FILE % str(file_path))
        print(e)
        print()
        return ""


# Input: list, list, bool
#
# Notes: Uses reference
#
def explore_dir(directories, files, explore_subdirectories):
    columns = get_terminal_size()[0]
    directory_path = str(directories[0])
    directory_len = len(EXPLORING_DIR % directory_path)
    append_three_dots = directory_len > columns

    while directory_len + 4 > columns:  # +4 because "... " will be appended
        directory_path = directory_path[1:]
        directory_len -= 1

    if append_three_dots:
        msg = EXPLORING_DIR % ("... " + directory_path)
    else:
        msg = EXPLORING_DIR % directory_path

    extra_space = columns - len(msg)
    msg += (" " * extra_space)

    # I think it's a lot of processing just to display it nicely, maybe I will change it.
    stdout.write("\r")
    stdout.write(msg)
    stdout.flush()

    try:
        for item in directories[0].iterdir():
            if explore_subdirectories and item.is_dir():
                directories.append(item)
            elif item.is_file():
                file_hash = get_file_hash(item)
                files.append(FileHash(str(item), file_hash))
    except (PermissionError, FileNotFoundError) as e:
        print(CANNOT_READ_DIRECTORY % str(directories[0]))
        print(e)
        print()

    directories.pop(0)


# Input:  list     -> ["Ingredient", "Price"]
# Output: Workbook -> <openpyxl.workbook.workbook.Workbook object at [...]>
#
def create_workbook(columns) -> Workbook:
    workbook = Workbook()
    sheet = workbook.active

    for column, column_name in enumerate(columns):
        sheet.cell(row=1, column=(column + 1), value=column_name)

    return workbook


# Input:  list, Path -> ["Ingredient", "Price"], "/root/c.xlsx"
# Output: list       -> [<tools.FileHash.FileHash object at [...]>,
#                        <tools.FileHash.FileHash object at [...]>,
#                        ...]
#
def retrieve_workbook_objects(columns, file_path) -> list:
    try:
        workbook = load_workbook(file_path, True)
    except BadZipFile:
        print("ERROR; Cannot read file %a" % str(file_path))
        return list()

    sheet = workbook.active
    matched_columns = True

    files = list()

    for column, column_name in enumerate(columns):
        matched_columns = matched_columns and (sheet.cell(row=1, column=(column + 1)).value == column_name)

    if not matched_columns:
        print(XLSX_DOESNT_MEET_COLUMNS % (file_path, columns))
        workbook.close()
        return files

    # Starts in 2 because we don't want the column name as object
    # (The other +1 in 2 is because openpyxl cells start with 1 :v)
    for row in range(2, sheet.max_row + 1):
        file_hash = str(sheet.cell(row=row, column=1).value)
        file_path = Path(sheet.cell(row=row, column=2).value)
        file_stat = str(sheet.cell(row=row, column=3).value)

        files.append(FileHash(file_path, file_hash, file_stat))

    return files


# Input:  list, list
# Output: list
#
# Notes: example in README
#
def compare_data(older_db_data, newer_db_data) -> list:
    cdb_data = list()

    while older_db_data:
        old_data = older_db_data[0]
        remove_old_data_from_list = False

        for i_new_data, new_data in enumerate(newer_db_data):
            same_names = Path(old_data.get_file_path()).stem == Path(new_data.get_file_path()).stem

            # If hashes are the same
            if old_data.get_file_hash() == new_data.get_file_hash():

                if not same_names:
                    # If hashes are the same but the names are not, is considered as renamed
                    old_data.set_file_stat(STATS[2])
                    cdb_data.append(old_data)

                # If hashes and names are the same is considered as unmodified
                # so, not added to list of differences

                newer_db_data.pop(i_new_data)
                remove_old_data_from_list = True
                break
            elif same_names:
                # If hashes are not the same, but name is, then is considered as modified
                old_data.set_file_stat(STATS[3])

                cdb_data.append(old_data)
                newer_db_data.pop(i_new_data)
                remove_old_data_from_list = True
                break

        if not remove_old_data_from_list:
            # If a file was not found in newer data is considered as deleted
            old_data.set_file_stat(STATS[1])
            cdb_data.append(old_data)

        # Removes old files
        older_db_data.pop(0)

    # Any non-deleted file on newer data is considered as created
    while newer_db_data:
        newer_db_data[0].set_file_stat(STATS[0])
        cdb_data.append(newer_db_data[0])

        newer_db_data.pop(0)

    return cdb_data
