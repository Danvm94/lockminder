# sqlite3 used to store the username and passwords information
import sqlite3
# os library to check if file exists
import os
from random import randrange

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

# "1": add an account
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

# "2": view all accounts
def view_all_accounts(database):
    print("LockMinder view all accounts\n")
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM {TABLE}")
    rows = cursor.fetchall()
    for row in rows:
        id, username, password, service = row
        print(f"ID: {id} - Service: {service} - Username: {username} - Password: *******")
    display_menu(database) if replay_display_menu() else None

# "3": update an account
def update_account(database):
    print("LockMinder update an account\n")
    entry_id = int(input("Please type the account ID that you want to update: "))
    cursor = database.cursor()
    service = input("Please type the service name:\n")
    username = input("Please type the service username:\n")
    password = input("Please type the service password:\n")
    new_entry = (username, password, service, entry_id)
    cursor.execute(f"UPDATE {TABLE} SET username = ?, password = ?, service = ? WHERE id = ?", new_entry)
    database.commit()
    cursor.close()
    print(f"Your {service} account is now updated on the credentials list.")

# "4": delete an account
def delete_account(database):
    print("LockMinder update an account\n")
    entry_id = int(input("Please type the account ID that you want to delete: "))
    cursor = database.cursor()
    cursor.execute(f"DELETE FROM {TABLE} WHERE id = {entry_id};")
    database.commit()
    display_menu(database) if replay_display_menu() else None
    
# "5": generate a password
def generate_password(database):
    print("LockMinder password generator\n")
    password_length = int(input("Please type the password length (min: 1 | max: 50): "))
    new_password = ""
    for char in range(password_length):
        new_dec_char = randrange(33, 126)
        new_char = chr(new_dec_char)
        new_password += new_char
    print("Follow the new password below:\n")
    print(new_password)
    display_menu(database) if replay_display_menu() else None

# "6": retrieve a password
def retrieve_password(database):
    print("LockMinder retrieve a password\n")
    entry_id = int(input("Please type the account ID that you want to retrieve: "))
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM {TABLE} WHERE id={entry_id}")
    rows = cursor.fetchall()
    for row in rows:
        id, username, password, service = row
        print(f"ID: {id} - Service: {service} - Username: {username} - Password: {password}")
        
    display_menu(database) if replay_display_menu() else None

def replay_display_menu():
        repeat = input("Would you like to go back to the main menu? (Y / N): ")
        if repeat == "Y":
            return True
        else:
            return False

def display_menu(database):
    while True:
        options = {
        "1": add_account,
        "2": view_all_accounts,
        "3": update_account,
        "4": delete_account,
        "5": generate_password,
        "6": retrieve_password,
        }
        print("LockMinder Menu:")
        print("1. Add an account")
        print("2. View all accounts")
        print("3. Update an account")
        print("4. Delete an account")
        print("5. Generate a password")
        print("6. Retrieve a password")
        print("0. Exit")
        choice = input("Select one of the options: ")
        if choice in options:
            options[choice](database)
            break

def main():
    print("Welcome to LockMinder\n")
    check_db_presence(DATABASE_PATH)
    database = connect_db(DATABASE_PATH)
    display_menu(database)

main()