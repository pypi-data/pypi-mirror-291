"""functions for work with pickle"""

import logging
import pickle
from pathlib import Path

from classes import NotesBook


def save_notes(notebook: NotesBook, filename: str = "notesbook.pkl") -> None:
    """
    Save data to a pickle file.

    Args:
        notebook (NotesBook): The object to be saved (e.g., an instance of NotesBook).
        filename (str): The name of the file to save the data to.
        Default is "NotesBook.pkl".

    Raises:
        Exception: If an error occurs during the saving process, it will be logged.
    """
    try:
        with Path(filename).open("wb") as f:
            pickle.dump(notebook, f)
        logging.info("Data successfully saved to %s", filename)
    except Exception as e:
        logging.error("Error occurred while saving data to %s: %s", filename, e)


def load_notes(filename: str = "notesbook.pkl") -> NotesBook:
    """
    Load data from a pickle file.

    Args:
        filename (str): The name of the file to load the data from.
        Default is "NotesBook.pkl".

    Returns:
        Any: The loaded data, or a new instance of NotesBook
        if the file is not found or an error occurs.
    """
    file_path = Path(filename)
    if not file_path.exists():
        logging.warning(
            "File %s not found. Returning a new NotesBook instance.", filename
        )
        return NotesBook()

    try:
        with file_path.open("rb") as f:
            data = pickle.load(f)
        logging.info("Data successfully loaded from %s", filename)
        return data
    except (pickle.UnpicklingError, EOFError) as e:
        logging.error("Error occurred while loading data from %s: %s", filename, e)
        return NotesBook()
    except Exception as e:
        logging.critical(
            "Unknown error occurred while loading data from %s: %s", filename, e
        )
        return NotesBook()
