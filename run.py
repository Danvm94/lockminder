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
    """
    Retrieve column names of the 'credentials' table from the specified database.

    This function queries the SQLite database to fetch the column names of the 'credentials' table.
    It returns a dictionary with the column names as keys and empty strings as values.
    The 'ID' column is excluded from the returned dictionary.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.

    Returns:
        dict: A dictionary containing column names (excluding 'ID') as keys with empty strings as values.
    """
    column_dict = {}
    with database:
        cursor = database.cursor()
        cursor.execute(f"PRAGMA table_info({TABLE})")
        for column_info in cursor.fetchall()[1:]:
            column_name = column_info[1]
            column_dict[column_name] = ""
    return column_dict

def get_database_values(database, key=None, value=None):
    """
    Retrieve data from the 'credentials' table in the specified database.

    This function queries the SQLite database to fetch data from the 'credentials' table.
    If both 'key' and 'value' are provided, it filters the results based on the given key-value pair.
    Otherwise, it fetches all data from the table.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        key (str, optional): The column name to filter the results. Defaults to None.
        value (str, optional): The value to match in the specified column. Defaults to None.

    Returns:
        PrettyTable: A PrettyTable object containing the fetched data as rows and column names as headers.
    """
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
    """
    Prompt the user to enter values for each column in the 'credentials' table.

    This function interacts with the user to gather values for each column in the 'credentials' table.
    It fetches the column names and initializes a dictionary with the column names as keys and empty strings as values.
    The user is prompted to enter data for each column, and the input is validated to ensure it does not exceed 64 characters.
    Once all values are obtained, a tuple containing the user-provided values is returned.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.

    Returns:
        tuple: A tuple containing the user-provided values for each column in the 'credentials' table.
    """
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

def entry_exist(cursor, entry_id):
    """
    Check if an entry with the given ID exists in the database.

    This function checks if an entry with the specified ID exists in the database
    by using the provided cursor to fetch the corresponding data. If the entry is not found,
    it prints a message indicating that it does not exist and returns False. Otherwise, it
    returns True.

    Args:
        cursor (sqlite3.Cursor): The cursor to execute the database query.
        entry_id (int): The ID of the entry to check for existence.

    Returns:
        bool: True if the entry with the given ID exists, False otherwise.
    """
    if cursor.fetchone() is None:
        print(f"There is no entry number {entry_id}")
        return False
    else:
        return True

def request_id(database, message):
    """
    Request the user to input the ID of the account.

    This function displays a prompt to the user with the given 'message', which indicates
    the action they should perform (e.g., "Add an account," "Update an account," etc.).
    The user is asked to enter the ID of the account they want to perform the action on,
    or they can type '0' to return to the main menu.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        message (str): The action message to be displayed, such as "Add an account."

    Returns:
        int: The ID of the account entered by the user, or 0 to return to the main menu.
    """
    action = message.lower().split()[0]
    while True:
        print(f"LockMinder {message}\n")
        entry_id = input(f"Please enter the ID of the account you'd like to {action}, or type 0 to return to the main menu: ")
        if entry_id == "0":
            os.system('clear')
            display_menu(database)
        try:
            entry_id = int(entry_id)
            return entry_id
        except ValueError:
            os.system('clear')
            print("Invalid id. Please enter an integer number.")

def check_entry(database, entry_id):
    """
    Check if an entry with the given ID exists in the database.

    This function checks if an entry with the specified ID exists in the 'credentials' table
    of the specified database by executing an SQL query with the given 'entry_id'. If the entry
    does not exist, it prints a message and returns False. Otherwise, it returns True.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        entry_id (int): The ID of the entry to check for existence.

    Returns:
        bool: True if the entry with the given ID exists, False otherwise.
    """
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM {TABLE} WHERE id = {entry_id}")
    if not entry_exist(cursor, entry_id):
        os.system("clear")
        print(f"There is no entry number {entry_id}")
        return False
    else:
        return True

# "1": add an account
def add_account(database, message):
    print(f"LockMinder {message}\n")
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
def view_all_accounts(database, description):
    print(f"LockMinder {description}\n")
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
                row = get_database_values(database, key="id", value=entry_id)
                print(row)
                new_entry = prompt_values(database)
                cursor.execute(f"UPDATE {TABLE} SET username = ?, password = ?, service = ? WHERE id = {entry_id}", new_entry)
                row = get_database_values(database, key="id", value=entry_id)
                print(f"Your account is now updated on the credentials list.")
                print(row)
                break
    display_menu(database) if replay_display_menu() else None

# "4": delete an account
def delete_account(database, description):
    while True:
        entry_id = request_id(database, description)
        with database:
            cursor = database.cursor()
            cursor.execute(f"SELECT * FROM {TABLE} WHERE id = {entry_id}")
            if check_entry(database, entry_id):
                row = get_database_values(database, key="id", value=entry_id)
                print(row)            
                cursor.execute(f"DELETE FROM {TABLE} WHERE id = {entry_id};")
                print(f"The entry number {entry_id} is now deleted.") 
                break
    display_menu(database) if replay_display_menu() else None
    
# "5": generate a password
def generate_password(database, description):
    print(f"LockMinder {description}\n")
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
def retrieve_password(database, description):
    while True:
        entry_id = request_id(database, description)
        with database:
            cursor = database.cursor()
            cursor.execute(f"SELECT * FROM {TABLE} WHERE id = {entry_id}")
            if check_entry(database, entry_id):
                row = get_database_values(database, key="id", value=entry_id) 
                print(row)
                break
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
            os.system("clear")
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
        if choice == "0":
            options[choice][0]()
        elif choice in options:
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