"""Functions for validation inputs

    Returns:
        bool: returns result of expretions True or False
    """

from datetime import datetime
from classes.notes_book import NotesBook
import re


def input_name_validation(user_input):
    """validation input data for add name

    Args:
        user_input (str): user input in string format

    Returns:
        str: returns user input if passed validation
    """
    if len(user_input) > 0:
        return user_input


def input_number_validation(user_input):
    """validation input data for add number

    Args:
        user_input (str): user input in string format

    Returns:
        str: returns user input if passed validation
    """

    pattern = r"(^[+0-9]{1,3})*([0-9]{10,11}$)"
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match:
        return user_input


def input_email_validation(user_input):
    """validation input data for add email

    Args:
        user_input (str): user input in string format

    Returns:
        str: returns user input if passed validation
    """
    pattern = r"\w+@\w+\.\w+"
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match:
        return user_input


def input_address_validation(user_input):
    """validation input data for add address

    Args:
        user_input (str): user input in string format

    Returns:
        str: returns user input if passed validation
    """
    if len(user_input) > 0:
        return user_input


def input_birthday_validation(user_input):
    """validation input data for add bitrhday

    Args:
        user_input (str): user input in string format

    Returns:
        bool: returns result of expretions True or False
    """
    res = True
    try:
        res = bool(datetime.strptime(user_input, "%d.%m.%Y"))
        return res
    except ValueError:
        res = False
        return res

def input_note_validation(note_name: str, book: NotesBook):
    if book.find(note_name) is not None:
        return True
    else: 
        return False

def input_tag_validation(tag: str):
    """
    Validates a tag input by checking if it matches the expected format.

    Args:
        tag (str): The tag to validate.

    Returns:
        bool: True if the tag is valid, False otherwise.
    """
    return re.match(r"#\w+", tag)