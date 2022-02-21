from tools.lang import WELCOME
from tools.lang import MENU
from tools.lang import WHAT_DO_YOU_WANT_TO_DO
from tools.lang import DO_YOU_WANT_PROCEED

from tools.util import choose

from tools.explorer_utils import setup_pdb_creation
from tools.explorer_utils import explore_dir
from tools.explorer_utils import write_xlsx

from tools.explorer_utils import setup_pdb_comparison
from tools.explorer_utils import retrieve_workbook_objects
from tools.explorer_utils import compare_data

from tools.explorer_utils import setup_ach_comparison
from tools.explorer_utils import retrieve_workbook_common_parent
from tools.explorer_utils import apply_changes


print(WELCOME)

while True:
    print(MENU)
    print(WHAT_DO_YOU_WANT_TO_DO)
    operation = choose(["1", "2", "3", "E"])

    if operation == "1":
        # Create p-database
        directories, pdb_path, explore_subdirectories = setup_pdb_creation()
        common_parent = directories[0].name
        files = list()

        while directories:
            explore_dir(directories, files, explore_subdirectories)
        print()

        write_xlsx(["Hash", "File_path", "Common_parent: " + common_parent], files, pdb_path)
    elif operation == "2":
        # Compare p-databases
        older_db, newer_db, cdb_path = setup_pdb_comparison()

        older_db_data, older_db_parent = retrieve_workbook_objects(["Hash", "File_path"], older_db, True)
        newer_db_data, newer_db_parent = retrieve_workbook_objects(["Hash", "File_path"], newer_db, True)

        if older_db_data and newer_db_data:
            cdb_data = compare_data(older_db_data, newer_db_data, older_db_parent, newer_db_parent)
            write_xlsx(["Hash", "File_path", "Notes"], cdb_data, cdb_path)
    elif operation == "3":
        # Apply changes
        older_db, newer_db, cdb_path = setup_ach_comparison()

        old_db_parent = retrieve_workbook_common_parent(None, older_db)[0]  # This method returns a list
        newer_db_data, newer_db_parent = retrieve_workbook_objects(["Hash", "File_path"], newer_db, True)

        cdb_data = retrieve_workbook_objects(["Hash", "File_path", "Notes"], cdb_path, False)

        if cdb_data:
            print(DO_YOU_WANT_PROCEED)
            if choose(["1", "2"], [True, False]):
                apply_changes(cdb_data, newer_db_data, newer_db_parent, old_db_parent)
    elif operation == "E":
        # Exit
        break

print("Bye")
