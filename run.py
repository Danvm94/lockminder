# sqlite3 used to store the username and passwords information
import sqlite3
# os library to check if file exists
import os

# Specify the path and filename of the SQLite database file
DATABASE = '.\passwords.db'

def check_db_presence(database):
    """
    Check the presence of a database file at the specified path.
    Args:
        database (str): The path and filename of the database file.
    Returns:
        bool: True if the database file exists, False otherwise.
    """
    if not os.path.exists(database):
        print(f"There is no database file at the path provided: {database}")
        return False
    else:
        return True

def main():
    pass

