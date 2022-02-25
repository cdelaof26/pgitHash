from tools.lang import ITEM_NOT_FOUND
from tools.lang import SELECT_AN_OPTION
from tools.lang import PRESS_CTRL_C_TO_EXIT
from tools.lang import ENTERED_ITEMS

from sys import stdout
from os import get_terminal_size

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


# Input:      str
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
