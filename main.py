from tools.lang import WELCOME
from tools.lang import MENU
from tools.lang import EXIT
from tools.lang import WHAT_DO_YOU_WANT_TO_DO
from tools.lang import CANNOT_CREATE_DIR
from tools.lang import DO_YOU_WANT_PROCEED
from tools.lang import SELECT_A_FILE
from tools.lang import OPERATION_CANCELED

from tools.util import choose
from tools.util import get_random_number
from tools.util import regex_replace
from tools.util import replace_all_coincidences_on_data

from tools.file_utils import file_browser
from tools.file_utils import create_file_hash
from tools.file_utils import create_directory
from tools.file_utils import create_directories
from tools.file_utils import copy_file

from tools.explorer_utils import setup_pdb_creation
from tools.explorer_utils import explore_dir
from tools.explorer_utils import write_xlsx

from tools.explorer_utils import setup_pdb_comparison
from tools.explorer_utils import retrieve_workbook_objects
from tools.explorer_utils import compare_data

from tools.explorer_utils import setup_ach_comparison
from tools.explorer_utils import retrieve_workbook_origin_path
from tools.explorer_utils import apply_changes

from tools.explorer_utils import setup_cp

from tools.config_manager import retrieve_config
from tools.config_manager import settings_menu

# from tools.config_manager import PREFERRED_LANGUAGE
from tools.config_manager import HASH_ALGORITHM

from pathlib import Path


print(WELCOME)

blacklist_str, config = retrieve_config()


while True:
    try:
        print(MENU)
        print(EXIT)
        print(WHAT_DO_YOU_WANT_TO_DO)
        operation = choose(["1", "2", "3", "4", "5", "S", "CP", "E"])

        if operation == "1":
            # Create p-database
            directories, pdb_path, explore_subdirectories, divide_by_directory = setup_pdb_creation()
            data_origin_path = directories[0]
            files = list()

            hash_func = config[HASH_ALGORITHM]

            if not divide_by_directory:
                # Every single file found goes to the same xlsx file
                while directories:
                    explore_dir(directories, files, explore_subdirectories, hash_func, blacklist_str)
                print()

                write_xlsx(["Hash", "File_path", "Origin_path: " + str(data_origin_path)], files, pdb_path)
            else:
                # Every subdirectory has its own xlsx file, as well is created a directory tree
                files_base_name = pdb_path.name.replace(".xlsx", "")
                sys_slash = Path.cwd().anchor
                pdb_path = Path(str(pdb_path).replace(".xlsx", ""))

                if create_directory(pdb_path):
                    while directories:
                        # Removes data_origin_path to get just after it
                        partial_dir_path = str(directories[0]).replace(str(data_origin_path), "")
                        if partial_dir_path and partial_dir_path[0] == sys_slash:
                            # Filename cannot start with \ or / if we want to join it
                            partial_dir_path = partial_dir_path[1:]

                        # We rejoin it with the pdb_path
                        new_directory = pdb_path.joinpath(partial_dir_path)

                        file_name = files_base_name + "_" + directories[0].name + ".xlsx"
                        new_file = new_directory.joinpath(file_name)

                        create_directory(new_directory)
                        explore_dir(directories, files, explore_subdirectories, hash_func, blacklist_str)
                        write_xlsx(["Hash", "File_path", "Origin_path: " + str(data_origin_path)], files, new_file)
                        files = list()
                    print()
                else:
                    print(CANNOT_CREATE_DIR % pdb_path)
                    print(OPERATION_CANCELED)

        elif operation == "2":
            # Compare p-databases
            older_db, newer_db, cdb_path = setup_pdb_comparison()

            older_db_data, older_db_origin_path = retrieve_workbook_objects(["Hash", "File_path"], older_db, True)
            newer_db_data, newer_db_origin_path = retrieve_workbook_objects(["Hash", "File_path"], newer_db, True)

            if older_db_data and newer_db_data:
                cdb_data = compare_data(older_db_data, newer_db_data, older_db_origin_path, newer_db_origin_path)
                write_xlsx(["Hash", "File_path", "Notes"], cdb_data, cdb_path)

        elif operation == "3":
            # Apply changes
            older_db, newer_db, cdb_path = setup_ach_comparison()

            older_db_origin_path = retrieve_workbook_origin_path(None, older_db)[0]  # This method returns a list
            newer_db_data, newer_db_origin_path = retrieve_workbook_objects(["Hash", "File_path"], newer_db, True)

            cdb_data = retrieve_workbook_objects(["Hash", "File_path", "Notes"], cdb_path, False)

            if cdb_data:
                print(DO_YOU_WANT_PROCEED)
                if choose(["1", "2"], [True, False]):
                    apply_changes(cdb_data, newer_db_data, newer_db_origin_path, older_db_origin_path)

        elif operation == "4":
            # Hash single file
            print(SELECT_A_FILE)
            file_path = file_browser(allow_directories=False)
            hash_func = config[HASH_ALGORITHM]
            print(hash_func, create_file_hash(file_path, hash_func))

        elif operation == "5":
            # Modify origin path on existent xlsx
            print(SELECT_A_FILE)
            file_path = file_browser(allow_directories=False, allowed_extensions=[".xlsx"])
            db_data, db_origin_path = retrieve_workbook_objects(["Hash", "File_path"], file_path, True)
            limit = len(db_data)
            random_data_elements = [db_data[get_random_number(limit)], db_data[get_random_number(limit)],
                                    db_data[get_random_number(limit)], db_data[get_random_number(limit)],
                                    db_data[get_random_number(limit)]]
            text_to_replace, replacement = regex_replace(random_data_elements, db_origin_path)

            if text_to_replace != "":
                db_data, db_origin_path = replace_all_coincidences_on_data(db_data, db_origin_path,
                                                                           text_to_replace, replacement)
                write_xlsx(["Hash", "File_path", "Origin_path: " + str(db_origin_path)], db_data, file_path)

        elif operation == "S":
            # Settings
            blacklist_str, config = settings_menu(config)

        elif operation == "CP":
            # Recursive copy, not listened
            origin, destiny = setup_cp()
            directories = [origin]
            files = list()

            while directories:
                explore_dir(directories, files, True, None, blacklist_str)
                for file in files:
                    destiny_dir = file.get_file_path()
                    destiny_dir = destiny_dir.replace(str(origin), str(destiny))
                    destiny_dir = Path(destiny_dir).parent

                    create_directories(destiny_dir)
                    copy_file(file.get_file_path(), destiny_dir)
                files = list()
            print()

        elif operation == "E":
            # Exit
            break
    except KeyboardInterrupt:
        print(OPERATION_CANCELED)

print("Bye")
