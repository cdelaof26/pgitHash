from tools.lang import ITEM_NOT_FOUND
from tools.lang import SELECT_AN_OPTION
from tools.lang import PRESS_CTRL_C_TO_EXIT
from tools.lang import ENTERED_ITEMS
from tools.lang import ENTER_THE_TEXT_TO_REPLACE
from tools.lang import ENTER_THE_REPLACEMENT_TEXT
from tools.lang import ARE_THE_REPLACEMENTS_OKAY

from sys import stdout
from os import get_terminal_size

from random import random
from re import sub

# General utilities


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
        printable_list += option + "." + spaces + ("\"{0}\"\n".format(str(value)))

    return [printable_list, options]


# Input: str, str -> "Exploring %a", "/path/to/dir/"
# print: str      -> Exploring ... h/to/dir/
#
# Notes: msg_constant should include 1 %a for formatting
#
def print_status(msg_constant, org_text):
    columns = get_terminal_size()[0]
    principal_text = str(org_text)
    full_msg_len = len(msg_constant.format(principal_text))
    append_three_dots = full_msg_len > columns

    # three dots are only appended if message len is greater than terminal columns
    while full_msg_len + 4 > columns:  # +4 because "... " will be appended
        principal_text = principal_text[1:]
        full_msg_len -= 1

    if append_three_dots:
        msg = msg_constant.format("... " + principal_text)
    else:
        msg = msg_constant.format(principal_text)

    extra_space = columns - len(msg)
    msg += (" " * extra_space)

    stdout.write("\r")
    stdout.write(msg)
    stdout.flush()


# Input:      list -> ["a", "b", "c"],
# User_input: str  -> "1"
#
# Notes: Uses reference
#
def select_and_delete_items_from_list(items):
    print(PRESS_CTRL_C_TO_EXIT)

    try:
        while True:
            printable_list, options = create_selectable_list(items)
            print(printable_list)
            print(SELECT_AN_OPTION)
            item = choose(options, items)

            items.remove(item)
    except KeyboardInterrupt:
        pass


# User_input: str  -> "a", "b", "c"
# Output:     list -> ["a", "b", "c"]
#
def create_user_list() -> list:
    print(PRESS_CTRL_C_TO_EXIT)
    items = list()
    try:
        while True:
            print(ENTERED_ITEMS % len(items))
            item = input("> ").strip()
            if item == "":
                continue

            items.append(item)
    except KeyboardInterrupt:
        return items


# Input:  int -> 10
# Output: int -> 3
#
def get_random_number(limit):
    return int(random() * limit)


# Input:      list, str
# User_input: str
# Output:     list
#
def regex_replace(five_elements_on_data, origin_path) -> list:
    proceed_to_apply_changes = False

    while True:
        print("\n" + origin_path)

        text_to_replace = input(ENTER_THE_TEXT_TO_REPLACE)
        replacement = input(ENTER_THE_REPLACEMENT_TEXT)

        if text_to_replace == "" or replacement == "":
            break

        print(str(origin_path) + " -> " + str(sub(text_to_replace, replacement, origin_path)))
        for element in five_elements_on_data:
            print(str(element.get_file_path()) + " -> " + sub(text_to_replace, replacement, str(element.get_file_path())))

        print("\n" + ARE_THE_REPLACEMENTS_OKAY)
        option = choose(["1", "2", "3"])
        if option == "1":
            proceed_to_apply_changes = True
            break
        elif option == "2":
            break

    if proceed_to_apply_changes:
        return [text_to_replace, replacement]
    return ["", ""]


def replace_all_coincidences_on_data(db_data, origin_path, text_to_replace, replacement) -> list:
    origin_path = sub(text_to_replace, replacement, origin_path)
    i = 0
    while i < len(db_data):
        original_element_path = str(db_data[i].get_file_path())
        modified_element_path = sub(text_to_replace, replacement, original_element_path)
        db_data[i].set_file_path(modified_element_path)
        i += 1

    return [db_data, origin_path]
