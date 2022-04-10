from tools.lang import SETTINGS_SAVED
from tools.lang import CANNOT_SAVE_SETTINGS
from tools.lang import INVALID_SETTINGS
from tools.lang import SETTINGS_MENU
from tools.lang import SETUP_BLACKLIST
from tools.lang import ENABLE_BLACKLIST
from tools.lang import DEACTIVATE_BLACKLIST
from tools.lang import DEACTIVATE_AND_DELETE_BLACKLIST
from tools.lang import MODIFY_BLACKLIST
from tools.lang import SELECT_AN_OPTION
from tools.lang import EXIT
from tools.lang import ENTER_YOUR_STR
from tools.lang import DO_YOU_WANT_PROCEED
from tools.lang import BLACKLISTED_STRs
from tools.lang import MODIFY_BLACKLIST_MENU
from tools.lang import SELECT_ITEMS_TO_DELETE

from tools.file_utils import read_file
from tools.file_utils import write_file
from tools.file_utils import create_directory
from tools.file_utils import choose
from tools.file_utils import create_selectable_list

from tools.util import create_user_list
from tools.util import select_and_delete_items_from_list

from json import loads

from pathlib import Path

# Settings manager


SETTINGS_FOLDER = Path.cwd().joinpath("settings")
SETTINGS_FILE = SETTINGS_FOLDER.joinpath("settings")
BLACKLIST_FILE_STR = SETTINGS_FOLDER.joinpath("blacklist")

USE_BLACKLIST = False
CONFIGURED_BLACKLIST = BLACKLIST_FILE_STR.exists()

blacklist_str = list()

PREFERRED_LANGUAGE = "preferred_language"
HASH_ALGORITHM = "hash_algorithm"
USE_BLACKLIST_STR = "use_blacklist_extensions"

SETTINGS_KEYS = {PREFERRED_LANGUAGE, HASH_ALGORITHM, USE_BLACKLIST_STR}

DEFAULT_CONFIGURATION = {
    PREFERRED_LANGUAGE: "en",
    HASH_ALGORITHM: "sha1",
    USE_BLACKLIST_STR: "False"
}

AVAILABLE_LANGUAGES = ["en"]

AVAILABLE_HASH_ALGORITHMS = ["sha1", "sha224", "sha256", "sha384", "sha512", "md5"]


# Output: bool
#
def settings_exists() -> bool:
    return SETTINGS_FOLDER.exists() and SETTINGS_FILE.exists()


# Output: dict
#
def read_config() -> dict:
    global SETTINGS_FILE
    data = read_file(SETTINGS_FILE).replace("'", "\"")
    if not data:
        return dict()
    return loads(data)


def write_blacklist_file():
    global BLACKLIST_FILE_STR, blacklist_str
    write_file(BLACKLIST_FILE_STR, ",".join(blacklist_str))


# Input: dict
#
def write_config(data):
    global SETTINGS_FILE

    if write_file(SETTINGS_FILE, str(data)):
        print(SETTINGS_SAVED)
    else:
        print(CANNOT_SAVE_SETTINGS)


# Input: dict
#
def valid_settings(settings) -> bool:
    global SETTINGS_KEYS

    if not settings:
        return False

    for key in settings:
        if key not in SETTINGS_KEYS:
            return False

    return True


# Output: dict
#
def load_defaults() -> dict:
    if not SETTINGS_FOLDER.exists():
        create_directory(SETTINGS_FOLDER)

    write_config(str(DEFAULT_CONFIGURATION))

    return DEFAULT_CONFIGURATION


# Output: list
#
def retrieve_config() -> list:
    global SETTINGS_FOLDER, DEFAULT_CONFIGURATION, USE_BLACKLIST
    global BLACKLIST_FILE_STR, blacklist_str

    if settings_exists():
        settings = read_config()
        if valid_settings(settings):
            USE_BLACKLIST = settings[USE_BLACKLIST_STR] == "True" and BLACKLIST_FILE_STR.exists()

            if USE_BLACKLIST:
                blacklist_str = read_file(BLACKLIST_FILE_STR).split(",")

            return [blacklist_str, settings]

        print(INVALID_SETTINGS)

    return [blacklist_str, load_defaults()]


# Input: dict
#
def settings_menu(settings) -> list:
    global USE_BLACKLIST, CONFIGURED_BLACKLIST, BLACKLIST_FILE_STR
    global AVAILABLE_LANGUAGES, AVAILABLE_HASH_ALGORITHMS
    global PREFERRED_LANGUAGE, HASH_ALGORITHM, USE_BLACKLIST_STR
    global blacklist_str

    while True:
        print(SETTINGS_MENU % (settings[PREFERRED_LANGUAGE], settings[HASH_ALGORITHM]))
        options = ["1", "2", "3", "E"]

        if USE_BLACKLIST and CONFIGURED_BLACKLIST:
            print(DEACTIVATE_BLACKLIST)
            print(DEACTIVATE_AND_DELETE_BLACKLIST)
            print(MODIFY_BLACKLIST)
            options = ["1", "2", "3", "4", "5", "E"]
        elif not USE_BLACKLIST and CONFIGURED_BLACKLIST:
            print(ENABLE_BLACKLIST)
        elif not CONFIGURED_BLACKLIST:
            print(SETUP_BLACKLIST)

        print(EXIT)
        print(SELECT_AN_OPTION)
        option = choose(options)

        if option == "1":
            # Select language
            printable_list, lang_options = create_selectable_list(AVAILABLE_LANGUAGES)

            print(printable_list)
            print(SELECT_AN_OPTION)
            settings[PREFERRED_LANGUAGE] = choose(lang_options, AVAILABLE_LANGUAGES)

        elif option == "2":
            # Select hash algorithm
            printable_list, hash_options = create_selectable_list(AVAILABLE_HASH_ALGORITHMS)

            print(printable_list)
            print(SELECT_AN_OPTION)
            settings[HASH_ALGORITHM] = choose(hash_options, AVAILABLE_HASH_ALGORITHMS)

        elif option == "3":
            if USE_BLACKLIST and CONFIGURED_BLACKLIST:
                # DEACTIVATE_BLACKLIST
                settings[USE_BLACKLIST_STR] = "False"
                USE_BLACKLIST = False
            else:
                # ENABLE_BLACKLIST
                settings[USE_BLACKLIST_STR] = "True"
                USE_BLACKLIST = True

                if not CONFIGURED_BLACKLIST:
                    # SETUP_BLACKLIST
                    print(ENTER_YOUR_STR)
                    blacklist_str = create_user_list()
                    CONFIGURED_BLACKLIST = True
                    write_blacklist_file()

        elif option == "4":
            # DEACTIVATE_AND_DELETE_BLACKLIST
            print(DO_YOU_WANT_PROCEED)
            if choose(["1", "2"], [True, False]):
                settings[USE_BLACKLIST_STR] = "False"
                USE_BLACKLIST = False
                CONFIGURED_BLACKLIST = False

                BLACKLIST_FILE_STR.unlink()

        elif option == "5":
            # Modify blacklist
            while True:
                print(BLACKLISTED_STRs % blacklist_str)
                print(MODIFY_BLACKLIST_MENU)
                print(EXIT)
                modify_option = choose(["1", "2", "E"])

                if modify_option == "1":
                    # Add STRs
                    print(ENTER_YOUR_STR)
                    blacklist_str = blacklist_str + create_user_list()
                elif modify_option == "2":
                    # Delete STRs
                    print(SELECT_ITEMS_TO_DELETE)
                    select_and_delete_items_from_list(blacklist_str)
                else:
                    write_blacklist_file()
                    break

        elif option == "E":
            # Exit
            write_config(settings)
            return [blacklist_str, settings]
