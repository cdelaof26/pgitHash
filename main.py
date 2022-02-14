from tools.lang import WELCOME
from tools.lang import MENU
from tools.lang import WHAT_DO_YOU_WANT_TO_DO
from tools.lang import SUCCEED
from tools.lang import FILE_CREATED_AT
from tools.lang import NOT_FILES_FOUND

from tools.util import choose

from tools.explorer_utils import setup_pdb_creation
from tools.explorer_utils import explore_dir
from tools.explorer_utils import create_workbook

from tools.explorer_utils import setup_pdb_comparison
from tools.explorer_utils import retrieve_workbook_objects
from tools.explorer_utils import compare_data


print(WELCOME)

while True:
    print(MENU)
    print(WHAT_DO_YOU_WANT_TO_DO)
    operation = choose(["1", "2", "3", "E"])

    if operation == "1":
        # Create p-database
        directories, pdb_path, explore_subdirectories = setup_pdb_creation()
        files = list()

        while directories:
            explore_dir(directories, files, explore_subdirectories)
        print()

        if not files:
            print(NOT_FILES_FOUND)
        else:
            workbook = create_workbook(["Hash", "File_path"])
            sheet = workbook.active

            for i, file in enumerate(files):
                # i + 2 since first row is for column labels
                sheet.cell(row=(i + 2), column=1, value=file.get_file_hash())
                sheet.cell(row=(i + 2), column=2, value=file.get_file_path())

            workbook.save(pdb_path)
            workbook.close()

            print(SUCCEED + FILE_CREATED_AT % str(pdb_path))
    elif operation == "2":
        # Compare p-databases
        older_db, newer_db, cdb_path = setup_pdb_comparison()

        older_db_data = retrieve_workbook_objects(["Hash", "File_path"], older_db)
        newer_db_data = retrieve_workbook_objects(["Hash", "File_path"], newer_db)

        cdb_data = compare_data(older_db_data, newer_db_data)

        if not cdb_data:
            print(NOT_FILES_FOUND)
        else:
            workbook = create_workbook(["Hash", "File_path", "Notes"])
            sheet = workbook.active

            for i, file in enumerate(cdb_data):
                # i + 2 since first row is for column labels
                sheet.cell(row=(i + 2), column=1, value=str(file.get_file_hash()))
                sheet.cell(row=(i + 2), column=2, value=str(file.get_file_path()))
                sheet.cell(row=(i + 2), column=3, value=str(file.get_file_stat()))

            workbook.save(cdb_path)
            workbook.close()

            print(SUCCEED + FILE_CREATED_AT % str(cdb_path))
    elif operation == "3":
        # Apply changes
        print("WIB")
    elif operation == "E":
        # Exit
        break

print("Bye")
