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
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE}
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL,
                  service TEXT NOT NULL);""")
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

def add_account(database):
    print("LockMinder Add Account\n")
    service = input("Please type the service name:\n")
    username = input("Please type the service username:\n")
    password = input("Please type the service password:\n")
    new_entry = (username, password, service)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO {TABLE} (username, password, service) VALUES (?, ?, ?)", new_entry)
    database.commit()
    cursor.close()
    print(f"Your {service} is now added to the credentials list.")
    display_menu(database) if replay_display_menu() else None

def view_all_accounts(database):
    print("LockMinder view all accounts\n")
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM {TABLE}")
    rows = cursor.fetchall()
    for row in rows:
        id, username, password, service = row
        print(f"ID: {id} - Service: {service} - Username: {username} - Password: *******")
    display_menu(database) if replay_display_menu() else None

def replay_display_menu():
        repeat = input("Would you like to go back to the main menu? (Y / N): ")
        if repeat == "Y":
            return True
        else:
            return False

def display_menu(database):
    options = {
    "1": add_account,
    "2": view_all_accounts,
    "3": add_account,
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
    options[choice](database)

def main():
    print("Welcome to LockMinder\n")
    check_db_presence(DATABASE_PATH)
    database = connect_db(DATABASE_PATH)
    display_menu(database)

main()