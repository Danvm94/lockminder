# sqlite3 used to store the username and passwords information
import sqlite3
# os library to check if file exists
import os

# Specify the path and filename of the SQLite database file
DATABASE = 'passwords.db'

def check_db_presence(database):
    """
    Check the presence of a database file and create it if it doesn't exist.
    Args:
        database (str): The path and filename of the database file.
    Returns:
        None
    """
    print(f"Checking for: {database} presence.\n")
    if not os.path.exists(database):
        print(f"There is no database file at the path provided: {database}.\n")
        create_db(database)
    else:
        print(f"Database presence confirmed: {database}.\n")

def create_db(database):
    """
    Create a new SQLite database with a 'credentials' table.
    Args:
        database (str): The path and filename of the database file.
    Returns:
        None
    """
    print(f"Creating: {database}.\n")
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  service TEXT NOT NULL);''')
    conn.close()



def main():
    check_db_presence(DATABASE)

main()

