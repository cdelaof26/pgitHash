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
from tools.lang import PROCESSED
from tools.lang import M_FILES_OF_N_FILES

from tools.FileHash import FileHash
from tools.FileHash import STATS

from tools.util import file_browser
from tools.util import choose
from tools.util import print_status

from pathlib import Path

from hashlib import sha1
# from hashlib import md5

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
    # I think it's a lot of processing just to display it nicely, maybe I will change it.
    print_status(EXPLORING_DIR, directories[0])

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
def retrieve_workbook_objects(columns, file_path, retrieve_common_parent) -> list:
    try:
        workbook = load_workbook(file_path, True)
    except BadZipFile:
        print("ERROR; Cannot read file %a" % str(file_path))
        return list()

    sheet = workbook.active
    matched_columns = True

    files = list()
    common_parent = None

    for column, column_name in enumerate(columns):
        matched_columns = matched_columns and (sheet.cell(row=1, column=(column + 1)).value == column_name)

    # Common parent is only available for p-databases
    # cp-databases uses column 3 for file_stat
    if retrieve_common_parent:
        # Basically does this:
        #       "Common_parent: Path_name".split(": ")
        #       ['Common_parent', 'Path_name']
        # If path common_parent_split[1] is found, then is retrieved
        #
        common_parent_split = sheet.cell(row=1, column=3).value
        common_parent_split = common_parent_split.split(": ")
        if len(common_parent_split) == 2:
            common_parent = common_parent_split[1]
        else:
            # If is needed common_parent but not found, then file
            # Doesn't meet the columns
            matched_columns = False

    if not matched_columns:
        print(XLSX_DOESNT_MEET_COLUMNS % (file_path, columns, common_parent is not None))
        workbook.close()
        return files

    # Starts in 2 because we don't want the column name as object
    # (The other +1 in 2 is because openpyxl cells start with 1 :v)
    for row in range(2, sheet.max_row + 1):
        file_hash = str(sheet.cell(row=row, column=1).value)
        file_path = Path(sheet.cell(row=row, column=2).value)
        file_stat = str(sheet.cell(row=row, column=3).value)

        files.append(FileHash(file_path, file_hash, file_stat))

    if retrieve_common_parent:
        return [files, common_parent]

    return files


# Input:  list, list
# Output: list
#
# Notes: example in README
#
def compare_data(older_db_data, newer_db_data, older_db_parent, newer_db_parent) -> list:
    cdb_data = list()

    old_parent_p_tmp = str(older_db_data[0].get_file_path())
    old_parent_index = old_parent_p_tmp.index(older_db_parent)
    # Removes path after the common parent
    old_parent = old_parent_p_tmp.replace(old_parent_p_tmp[old_parent_index:], "")

    files_processed = 1
    total_files = len(older_db_data)

    while older_db_data:
        print_status(PROCESSED, M_FILES_OF_N_FILES % (files_processed, total_files))

        old_data = older_db_data[0]
        remove_old_data_from_list = False

        old_data_p_tmp = str(old_data.get_file_path())
        old_data_p_index = old_data_p_tmp.index(older_db_parent)
        # Removes path before the common parent
        old_data_parent = old_data_p_tmp.replace(old_data_p_tmp[:old_data_p_index], "")
        # Removes filename
        old_data_parent = old_data_parent.replace(Path(old_data.get_file_path()).stem, "")

        for i_new_data, new_data in enumerate(newer_db_data):
            same_names = Path(old_data.get_file_path()).stem == Path(new_data.get_file_path()).stem

            new_data_p_tmp = str(new_data.get_file_path())
            new_data_p_index = new_data_p_tmp.index(newer_db_parent)
            # Removes path before the common parent
            new_data_parent = new_data_p_tmp.replace(new_data_p_tmp[:new_data_p_index], "")
            # Removes filename
            new_data_parent = new_data_parent.replace(Path(new_data.get_file_path()).stem, "")

            same_path = old_data_parent == new_data_parent

            # If hashes are the same
            if old_data.get_file_hash() == new_data.get_file_hash():

                if same_names and not same_path:
                    # If hashes and names are the same but parents not, is considered as moved
                    old_data.set_file_stat(STATS[4])
                    cdb_data.append(old_data)
                if not same_names and same_path:
                    # If hashes and parents are the same but the names are not, is considered as renamed
                    old_data.set_file_stat(STATS[2])
                    cdb_data.append(old_data)
                if not same_names and not same_path:
                    # If hashes are the same but names and parents are not, is considered as RenamedAndMoved
                    old_data.set_file_stat(STATS[5])
                    cdb_data.append(old_data)

                # If hashes, parents and names are the same is considered as unmodified
                # so, not added to list of differences

                newer_db_data.pop(i_new_data)
                remove_old_data_from_list = True
                break
            elif same_names:
                if same_path:
                    # If hashes are not the same, but parents and names are, then is considered as modified
                    old_data.set_file_stat(STATS[3])
                else:
                    # If hashes and parents are not the same, but names are, then is considered as ModifiedAndMoved
                    old_data.set_file_stat(STATS[6])

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
        files_processed += 1

    # Any non-deleted file on newer data is considered as created
    while newer_db_data:
        new_data = newer_db_data[0]

        # To push changes is needed change the path to the older one
        new_data_p_tmp = str(new_data.get_file_path())
        new_data_p_index = new_data_p_tmp.index(newer_db_parent)
        # Removes path before the common parent
        new_data_parent = new_data_p_tmp.replace(new_data_p_tmp[:new_data_p_index], "")
        # Changes appends old path after common parent
        new_data_parent = old_parent + new_data_parent

        new_data.set_file_stat(STATS[0])
        new_data.set_file_path(new_data_parent)

        cdb_data.append(newer_db_data[0])

        newer_db_data.pop(0)

    return cdb_data
