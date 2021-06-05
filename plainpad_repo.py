from termcolor import colored
from pandas.core.frame import DataFrame
from numpy import RAISE, add, uint
import pandas as pd
import os
import time

CWD = os.getcwd()
DATA_NAME = 'data.csv'
DATA_PATH = os.path.join(CWD, DATA_NAME)
COLUMNS = ['Id', 'Name', 'Content', 'Date']


def data_exists() -> bool:
    """Check wheter data.csv file exists or not

    Returns:
        bool: True if data.csv file exists
    """
    return os.path.exists(DATA_PATH)


def create_data() -> None:
    """Create data.csv in `DATA_PATH`
    """
    if not data_exists():
        columns = ",".join(COLUMNS)
        with open(DATA_PATH, 'w') as data:
            # Writing colums since pandas can not parse empty file
            print(columns, file=data)


def note_exists(note_id: int) -> bool:
    """Check whether note exists in data.csv with id of `note_id`

    Args:
        note_id (int): Id of note that's being checked

    Returns:
        bool: True if note exists
    """
    df = get_notes()
    df = df.loc[df['Id'] == note_id]
    return not df.empty


def add_note(note_name: str, note_content: str) -> None:
    """Add a new note to the end of data.csv

    Args:
        note_name (str): Name of the new note
        note_content (str): Content of the new note

    Raises:
        Exception: If `note_name` is empty or only contains spaces
    """
    if note_name.isspace() or len(note_name) == 0:
        raise Exception('`note_name` can not be empty.')

    note_id = gen_unique_id()
    note_name = '"{}"'.format(note_name)
    note_content = '"{}"'.format(note_content)
    note_date = time.time()
    note_rows = [[note_id, note_name, note_content, note_date]]
    note = pd.DataFrame(note_rows, columns=COLUMNS)
    notes = get_notes()
    notes = notes.append(note, ignore_index=True)
    notes.to_csv(DATA_PATH, index=False, columns=COLUMNS)


def get_notes() -> DataFrame:
    """Read notes from data.csv

    Returns:
        DataFrame: Notes
    """
    return pd.read_csv(DATA_PATH)


def get_note_index(note_id: int) -> int:
    """Get note index in notes table

    Args:
        note_id (int): Note id

    Returns:
        int: Note index
    """
    if note_exists(note_id):
        df = get_notes()
        index = df[((df['Id'] == note_id))].index
        return index
    return -1


def get_note(note_id: int) -> DataFrame:
    """Return one note by `note_id`

    Args:
        note_id (int): Note id

    Returns:
        DataFrame: Note
    """
    df = get_notes()
    df = df.loc[df['Id'] == note_id]
    return df


def gen_unique_id() -> int:
    """Generate a unique id for a new note

    Returns:
        int: A unique id obtained by getting the biggest id of notes added by 1
    """
    notes = get_notes()
    count = len(notes.index)
    if count > 0:
        return int(notes.loc[notes['Id'].idxmax()]['Id']) + 1
    return 0


def find_notes(text: str) -> DataFrame:
    """Find notes whose names contain `text`

    Args:
        text (str): The text used to filter note names

    Returns:
        DataFrame: All notes whose names contain `text`
    """
    df = get_notes()
    df = df[df['Name'].str.contains(
        text, regex=False, case=False, na=False)]
    return df


def remove_note(note_id: int) -> bool:
    """Remove a note with its id

    Args:
        note_id (int): Note id

    Returns:
        bool: True if note existed and removed; Otherwise, False
    """
    if note_exists(note_id):
        index = get_note_index(note_id)
        notes = get_notes()
        notes = notes.drop(index)
        notes.to_csv(DATA_PATH, index=False, columns=COLUMNS)
        return True

    return False


def update_note(note_id: int, note_name: str, note_content: str) -> bool:
    """Update a note

    Args:
        note_id (int): Id of note that's being updated
        note_name (str): Note new name
        note_content (str): Note new content

    Raises:
        Exception: If `note_name` is empty or only contains spaces

    Returns:
        bool: True if note existed and updated
    """
    if note_exists(note_id):
        if note_name.isspace() and len(note_name) == 0:
            raise Exception('`note_name` can not be empty.')

        index = get_note_index(note_id)
        notes = get_notes()
        notes.iloc[index, 1] = '"{}"'.format(note_name)
        notes.iloc[index, 2] = note_content
        notes.to_csv(DATA_PATH, index=False, columns=COLUMNS)
        return True
    return False
