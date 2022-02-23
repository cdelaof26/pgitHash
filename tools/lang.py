# Constants for text


# Universal

WHAT_DO_YOU_WANT_TO_DO = "What do you want to do?"
SELECT_AN_OPTION = "Select an option"
EXIT = "E. Exit"
SELECT_A_FILE = "Select a file"


# main

WELCOME = "\n       Welcome to pgitHash!"

MENU = "\nMain menu\n" \
       "1. Create database\n" \
       "2. Compare databases\n" \
       "3. Apply found changes\n" \
       "4. Hash single file\n\n" \
       "S. Settings"

DO_YOU_WANT_PROCEED = "THIS PROCESS WILL MODIFY SEVERAL DATA\n" \
                      "Do you want proceed?\n" \
                      "1. Yes\n" \
                      "2. No"

OPERATION_CANCELED = "\n\n      Operation canceled\n\n"


# config manager

SETTINGS_SAVED = "\nSettings saved"
CANNOT_SAVE_SETTINGS = "\nERROR; Cannot save Settings"

INVALID_SETTINGS = "Invalid settings, default loaded"

SETTINGS_MENU = "\nSettings\n" \
                "1. Select language       :  %a\n" \
                "2. Select hash algorithm :  %a"

SETUP_BLACKLIST = "3. Setup blacklist"
ENABLE_BLACKLIST = "3. Enable blacklist"
DEACTIVATE_BLACKLIST = "3. Deactivate blacklist"
DEACTIVATE_AND_DELETE_BLACKLIST = "4. Deactivate and delete blacklist"
MODIFY_BLACKLIST = "5. Modify blacklist"

ENTER_YOUR_STR = "Enter a list of blacklisted extensions or filenames\n" \
                 "Extensions must start with . (dot)\n\n" \
                 "      CASE MATTERS!"

BLACKLISTED_STRs = "\nBlacklisted names and extensions\n\n" \
                   "%a\n\n"

MODIFY_BLACKLIST_MENU = "1. Add items\n" \
                        "2. Delete items"

SELECT_ITEMS_TO_DELETE = "Select the items that you want remove"


# util

ITEM_NOT_FOUND = "Your option %a is not in list, try any of those: %a"

PRESS_CTRL_C_TO_EXIT = "Press ctrl + c to exit"
ENTERED_ITEMS = "Entered items %a"


# file utils

CANNOT_HASH_FILE = "\nERROR; Cannot hash %a"

CANNOT_READ_CONTENTS = "ERROR; Cannot read contents of %a"

FILES_AT = "Files at %a"
DIRECTORIES_AT = "Directories at %a"
FILES_AND_DIRECTORIES_AT = "Files and directories at %a"
GO_BACK = "Go back"
DO_YOU_WANT_TO_MOVE_OR_SELECT_IT = "Do you want move into or select it?\n" \
                                   "1. Move into\n" \
                                   "2. Select it"

PATH_DOESNT_EXIST = "Given path/file doesn't exist or it is not allowed to be used.\n" \
                    "Allowed selection\n" \
                    "   Select files:       %a\n" \
                    "   Select directories: %a"


# explorer utils

SELECT_THE_DIRECTORY = "Select the directory"
DO_YOU_WANT_EXPLORE_SUBDIRECTORIES = "Do you want to explore subdirectories?\n1. Yes\n2. No"

ENTER_A_NAME_FOR_YOUR_DB = "Enter a name for your database\n> "

SELECT_THE_OLDER_BD = "Select the older database file"
SELECT_THE_NEWER_BD = "Select the newer database file"
ENTER_A_NAME_FOR_YOUR_CDB = "Enter a name for your comparison result database\n> "
SELECT_THE_CDB = "Select the comparison database file"

EXPLORING_DIR = "Exploring %a"

SUCCEED = "\nSucceed"

XLSX_DOESNT_MEET_COLUMNS = "File %a doesn't meet the columns %a\n" \
                           "Common parent found: %a"

FILE_CREATED_AT = ", file created at %a\n"
NOT_FILES_FOUND = "\nNo files were found at given path, process ended\n"

CREATING = "Creating %a"
M_OBJECTS_OF_N_OBJECTS = "%a objects of %a"

PROCESSED = "Processed %a"
M_FILES_OF_N_FILES = "%a files of %a"

CANNOT_COPY_OR_MOVE_FILE = "ERROR; Cannot copy or move file %a to %a"
