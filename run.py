# Import the required modules
import sqlite3  # Used to create and manage the database for storing usernames and passwords
import os       # Used to clear the therminal
from random import randrange  # Used to generate random passwords
from prettytable import PrettyTable  # Used to create a visually appealing table for displaying results

# Table schema for storing username and password information.
TABLE = "credentials"
# The table will have four columns: id, username, password, and service.
DATABASE = f"""CREATE TABLE IF NOT EXISTS {TABLE}
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL,
                  service TEXT NOT NULL);"""

def create_db():
    """
    Creates an SQLite database in memory and sets up the required table.

    This function establishes a connection to an in-memory SQLite database,
    creates a table 'credentials' with columns 'id', 'username', 'password', and 'service',
    and returns the connection to the newly created database.

    Returns:
        sqlite3.connect: A connection to the in-memory SQLite database.
    """
    print(f"Creating database on computer's memory.\n")
    connector = sqlite3.connect(":memory:")
    cursor = connector.cursor()
    cursor.execute(DATABASE)
    return connector

def get_column_names(database):
    column_dict = {}
    with database:
        cursor = database.cursor()
        cursor.execute(f"PRAGMA table_info({TABLE})")
        for column_info in cursor.fetchall()[1:]:
            column_name = column_info[1]
            column_dict[column_name] = ""
    return column_dict

def get_database_values(database, key=None, value=None):
    with database: 
        cursor = database.cursor()
        if key and value:
            cursor.execute(f"SELECT * FROM {TABLE} WHERE {key} = {value}")
        else:
            cursor.execute(f"SELECT * FROM {TABLE}")
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        table = PrettyTable(column_names)
        for row in results:
            table.add_row(row)
        return table
        
def prompt_values(database):
    column_dict = get_column_names(database)
    for key,value in column_dict.items():
        while True:   
            column_dict[key] = input(f"Please type the {key}: ")
            if len(column_dict[key]) > 64:
                print(f"Please use less than 64 characters for {key}")
            else:
                break
    new_entry = tuple(value for value in column_dict.values())
    return new_entry

def entry_exist(cursor):
    if cursor.fetchone() is None:
        return False
    else:
        return True

def request_id(database, message):
    action = message.lower().split()[0]
    while True:
        print(f"LockMinder {message}")
        entry_id = input(f"Please enter the ID of the account you'd like to {action}, or type 0 to return to the main menu: ")
        if entry_id == "0":
            display_menu(database)
        try:
            entry_id = int(entry_id)
            return entry_id
        except ValueError:
            os.system('clear')
            print("Invalid id. Please enter an integer number.")

def check_entry(database, entry_id):
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM {TABLE} WHERE id = {entry_id}")
    if not entry_exist(cursor):
        os.system('clear')
        print(f"There is no entry number {entry_id}")
        return False
    else:
        return True

# "1": add an account
def add_account(database):
    print("LockMinder Add Account\n")
    new_entry = prompt_values(database)
    with database: 
        cursor = database.cursor()
        cursor.execute(f"INSERT INTO {TABLE} (username, password, service) VALUES (?, ?, ?)", new_entry)
        last_row_id = cursor.lastrowid
        print(f"Your account is now added to the credentials list.")
        row = get_database_values(database, key="id", value=last_row_id)
        print(row)
    display_menu(database) if replay_display_menu() else None

# "2": view all accounts
def view_all_accounts(database):
    print("LockMinder view all accounts\n")
    rows = get_database_values(database)
    print(rows)
    display_menu(database) if replay_display_menu() else None

# "3": update an account
def update_account(database, description):
    while True:
        entry_id = request_id(database, description)
        with database:
            cursor = database.cursor()
            cursor.execute(f"SELECT * FROM {TABLE} WHERE id = {entry_id}")
            if check_entry(database, entry_id):
                new_entry = prompt_values(database)
                cursor.execute(f"UPDATE {TABLE} SET username = ?, password = ?, service = ? WHERE id = {entry_id}", new_entry)
                row = get_database_values(database, key="id", value=entry_id)
                print(f"Your account is now updated on the credentials list.")
                print(row)
                break
    display_menu(database) if replay_display_menu() else None

# "4": delete an account
def delete_account(database):
    print("LockMinder update an account\n")
    entry_id = request_id("Please type the account ID that you want to delete: ")
    with database:
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM {TABLE} WHERE id = {entry_id}")
        if not entry_exist(cursor):
            print(f"There is no entry number {entry_id}")
        else:
            
            cursor.execute(f"DELETE FROM {TABLE} WHERE id = {entry_id};") 
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
    entry_id = request_id("Please type the account ID that you want to retrieve: ")
    with database:
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM {TABLE} WHERE id = {entry_id}")
        if not entry_exist(cursor):
            print(f"There is no entry number {entry_id}")
        else:
            row = get_database_values(database, key="id", value=entry_id) 
            print(row)
    display_menu(database) if replay_display_menu() else None

def replay_display_menu():
    """Asks the user if they want to go back to the main menu.

        Returns:
            bool: True if the user wants to go back (chooses 'Y'), False if they do not want to go back (chooses 'N').

        The function repeatedly prompts the user with a question asking if they would like to return
        to the main menu. The user's input is converted to uppercase using the 'upper()' method for case-insensitive comparison.
        If the user chooses 'Y', the function returns True, indicating they want to go back, and exits the loop.
        If the user chooses 'N', the function returns False, indicating they do not want to go back, and exits the loop.
    """
    while True:
        repeat = input("Would you like to go back to the main menu? (Y / N): ").upper()
        if repeat == "Y":
            return True
        elif repeat == "N":
            return False

def display_menu(database):
    """Displays the LockMinder menu and handles user input for various options.

    Parameters:
        database (object): The database object or connection needed for the menu functions.

    The function displays a menu with options and descriptions using PrettyTable.
    It continuously prompts the user to select an option until a valid choice is made.
    Once a valid option is chosen, the corresponding function for that option is executed.
    The user can exit the menu by selecting '0', which calls the 'exit' function.
    """
    options = {
            "1": [add_account, "Add an account"],
            "2": [view_all_accounts, "View all accounts"],
            "3": [update_account, "Update an account"],
            "4": [delete_account, "Delete an account"],
            "5": [generate_password, "Generate a password"],
            "6": [retrieve_password, "Retrieve a password"],
            "0": [exit, "Exit."]
        }
    while True:
        print_menu(options)
        choice = input("Select one of the options: ")

        if choice in options:
            os.system('clear')
            options[choice][0](database, options[choice][1])
            break
        else:
            os.system('clear')
            print("Please select a valid option.")

def print_menu(options):
    """Prints the LockMinder menu with options and their descriptions.

    Parameters:
        options (dict): A dictionary containing menu options and their descriptions.
                        The keys are option numbers (e.g., "1", "2", etc.).
                        The values are lists with two elements:
                            1. The function to call for the option.
                            2. The description of the option.

    The function creates a PrettyTable and populates it with the option numbers and descriptions.
    It then prints the table to display the LockMinder menu with all available options.
    """
    print("LockMinder Menu:")
    menu = PrettyTable(["OPTION", "DESCRIPTION"])
    for key, value in options.items():
        menu.add_row([key, value[1]])
    print(menu)

def main():
    print("Welcome to LockMinder\n")
    database = create_db()
    display_menu(database)

main()