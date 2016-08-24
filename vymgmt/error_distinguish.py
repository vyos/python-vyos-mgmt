# Copyright (c) 2016 Hochikong


def distinguish_for_set(message):
    """Distinguish the error type,PathError or ValueError

    :param message: A error message string from VyOS
    :return: The type of error
    """
    path_error_string = ['Configuration path:', 'is not valid']
    value_error_string = ['Value validation failed']
    all_strings = [path_error_string, value_error_string]
    condition = 0
    for i in all_strings:
        for x in i:
            if x in message:
                condition += 1

    if condition == 2:
        return "ConfigPathError"
    elif condition == 1:
        return "ConfigValueError"
    else:
        return "NonsupportButError"


def distinguish_for_delete(message):
    """Distinguish the error type,PathError or ValueError

    :param message: A error message string from VyOS
    :return: The type of error
    """
    path_error_string = ['Configuration path:', 'is not valid', 'Delete failed']
    value_error_string = ['Nothing to delete', 'the specified value does not exist']
    all_strings = [path_error_string, value_error_string]
    condition = 0

    for i in all_strings:
        for x in i:
            if x in message:
                condition += 1

    if condition == 3:
        return "ConfigPathError"
    elif condition == 2:
        return "ConfigValueError"
    else:
        return "NonsupportButError"


def distinguish_for_commit(message):
    """Distinguish the error type

    :param message: A error message string from VyOS
    :return: The type of error
    """
    all_strings = ['Commit failed', 'due to another commit in progress']

    for i in all_strings:
        if i in message:
            if i == all_strings[0]:
                return "CommitFailed"
            if i == all_strings[1]:
                return "CommitConflict"
