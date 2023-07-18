# sqlite3 used to store the username and passwords information
import sqlite3
# os library to check if file exists
import os

# Specify the path and filename of the SQLite database file
DATABASE_PATH = 'passwords.db'
TABLE = "credentials"

def check_db_presence(database_path):
    """
    Check the presence of a database file and create it if it doesn't exist.
    Args:
        database (str): The path and filename of the database file.
    Returns:
        None
    """
    print(f"Checking for: {database_path} presence.\n")
    if not os.path.exists(database_path):
        print(f"There is no database file at the path provided: {database_path}.\n")
        create_db(database_path)
    else:
        print(f"Database presence confirmed: {database_path}.\n")

def create_db(database_path):
    """
    Create a new SQLite database with a 'credentials' table.
    Args:
        database (str): The path and filename of the database file.
    Returns:
        None
    """
    print(f"Creating: {database_path}.\n")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS {TABLE}
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  service TEXT NOT NULL);''')
    conn.close()

def connect_db(database_path):
    """
    Establish a connection to an SQLite database.
    Args:
        database_path (str): The path and filename of the database file.
    Returns:
        sqlite3.Connection: The connection object for the SQLite database.
    """
    connector = sqlite3.connect(database_path)
    return connector

def display_menu():
    options = {
    "1": test_print,
    "2": test_print,
    "3": test_print,
}
    print("LockMinder Menu:")
    print("1. Add an account and password")
    print("2. View all accounts")
    print("3. Update an account's password")
    print("4. Delete an account")
    print("5. Generate a password")
    print("6. Retrieve a password")
    print("0. Exit")
    choice = input("Select one of the options: ")
    options.get(choice, lambda: print("Invalid choice. Please try again."))()

def test_print():
    print("testing")

def main():
    print("Welcome to LockMinder\n")
    check_db_presence(DATABASE_PATH)
    database = connect_db(DATABASE_PATH)
    print(database.execute(f"SELECT * FROM {TABLE}").fetchall())
    
    


display_menu()

