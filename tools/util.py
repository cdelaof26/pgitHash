from tools.lang import ITEM_NOT_FOUND
from tools.lang import CANNOT_READ_DIRECTORY
from tools.lang import FILES_AT
from tools.lang import DIRECTORIES_AT
from tools.lang import FILES_AND_DIRECTORIES_AT
from tools.lang import GO_BACK
from tools.lang import SELECT_AN_OPTION
from tools.lang import DO_YOU_WANT_TO_MOVE_OR_SELECT_IT
from tools.lang import PATH_DOESNT_EXIST

from pathlib import Path

# General utilities


current_directory = Path.cwd()


# Input:      list, list -> ["1", "2", "A"], [True, False, 10]
# User_input: str        -> "a"
# Output:     object     -> 10
#
# Notes: non number values for options must be always uppercase.
#
def choose(options, options_values=None):
    selected_item = None

    while not selected_item:
        selected_item = input("> ").upper()

        if selected_item not in options:
            print(ITEM_NOT_FOUND % (selected_item, options))
            selected_item = None
        else:
            break

    if options_values is not None:
        return options_values[options.index(selected_item)]

    return selected_item


# Input:  list -> ["Pizza", "Hamburger", "Lasagna"]
# Output: int  -> 9
#
def search_longer_item(items) -> int:
    larger = -1
    for item in items:
        item_len = len(str(item))
        if item_len > larger:
            larger = item_len

    return larger


# Input:  list -> ["Apple", "Pineapple", "Grape"]
# Output: list -> ["0. 'Apple'\n1. 'Pineapple'\n2. 'Grape'\n", ['0', '1', '2']]
#
def create_selectable_list(items) -> list:
    options = list()
    printable_list = ""

    # Needed to add spaces to get something like:
    # 1.   Option 1
    # 2.   Option 2
    # ...
    # 100. Option 100
    longer_number = search_longer_item(list(range(len(items)))) + 1  # +1 because extra space after dot
    # forgive god for the above line

    for option, value in enumerate(items):
        option = str(option)

        options.append(option)

        spaces = " " * (longer_number - len(option))
        printable_list += option + "." + spaces + ("%a\n" % str(value))

    return [printable_list, options]


# Input:  Path, bool, bool, bool, list -> Path("/home/cdelaof/"), False
# Output: list                         -> ['.zprofile', 'Desktop', 'Documents', 'Downloads']
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
        print(CANNOT_READ_DIRECTORY % str(path))
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
        if current_directory.is_file():
            current_directory = current_directory.parent

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
            # Needed to remove Darwin '\' as well any extra space
            option = option.replace("\\", "").strip()

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
                return current_directory
        elif option == options[-1]:
            current_directory = current_directory.parent
        else:
            print(PATH_DOESNT_EXIST % (allow_files, allow_directories))
