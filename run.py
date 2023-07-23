# Import the required modules
# Used to create and manage the database for storing usernames and passwords
import sqlite3
# Used to clear the therminal
import os
# Used to generate random passwords
from random import randrange
# Used to create a visually appealing table for displaying results
from prettytable import PrettyTable

# Table schema for storing username and password information.
TABLE = "credentials"
# The table will have four columns: id, username, password, and service.
DATABASE = f"""CREATE TABLE IF NOT EXISTS {TABLE}
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL,
                  service TEXT NOT NULL);"""


def print_ascii_banner():
    """
    Display the ASCII banner from the 'welcome.txt' file.

    This function reads the content of the ASCII banner from the
    'welcome.txt' file and prints it to the console.
    If the 'welcome.txt' file is not found in the current
    directory, it will print an error message.

    Note:
        Ensure that the 'welcome.txt' file contains the properly
        formatted ASCII banner for correct display.
    """
    try:
        with open("./welcome.txt", "r") as file:
            banner = file.read()
            print(banner)
    except FileNotFoundError:
        print("Error: The banner file was not found.")


def create_db():
    """
    Creates an SQLite database in memory and sets up the required table.

    This function establishes a connection to an in-memory SQLite database,
    creates a table 'credentials' with columns:
    'id', 'username', 'password', and 'service',
    and returns the connection to the newly created database.

    Returns:
        sqlite3.connect: A connection to the in-memory SQLite database.
    """
    print(f"Creating database on computer's memory.\n")
    print("""Note: As this software is currently
running in a cloud environment,it is crucial not to
enter real user passwords, accounts, or any sensitive information.
The password manager is designed for demonstration purposes
and should not be used with actual personal data.\n""")
    connector = sqlite3.connect(":memory:")
    cursor = connector.cursor()
    cursor.execute(DATABASE)
    return connector


def get_column_names(database):
    """
    Retrieve column names of the 'credentials'
    table from the specified database.

    This function queries the SQLite database to fetch the column names of the
    'credentials' table.
    It returns a dictionary with the column names as keys and empty
    strings as values.
    The 'ID' column is excluded from the returned dictionary.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.

    Returns:
        dict: A dictionary containing column names (excluding 'ID') as keys
        with empty strings as values.
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

    This function queries the SQLite database to fetch data from the
    'credentials' table.
    If both 'key' and 'value' are provided, it filters the results
    based on the given key-value pair.
    Otherwise, it fetches all data from the table.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        key (str, optional): The column name to filter the results.
        Defaults to None.
        value (str, optional): The value to match in the specified column.
        Defaults to None.

    Returns:
        PrettyTable: A PrettyTable object containing the fetched data as rows
        and column names as headers.
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

    This function interacts with the user to gather values for each column
    in the 'credentials' table.
    It fetches the column names and initializes a dictionary with the column
    names as keys and empty strings as values.
    The user is prompted to enter data for each column, and the input is
    validated to ensure it does not exceed 64 characters.
    Once all values are obtained, a tuple containing the user-provided
    values is returned.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.

    Returns:
        tuple: A tuple containing the user-provided values for
        each column in the 'credentials' table.
    """
    column_dict = get_column_names(database)
    for key, value in column_dict.items():
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

    This function checks if an entry with the specified ID exists
    in the database
    by using the provided cursor to fetch the corresponding data.
    If the entry is not found,
    it prints a message indicating that it does not exist and returns False.
    Otherwise, it returns True.

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

    This function displays a prompt to the user
    with the given 'message', which indicates the action they should perform
    (e.g., "Add an account," "Update an account," etc.).
    The user is asked to enter the ID of the account they want
    to perform the action on, or they can type '0' to return to the main menu.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        message (str): The action message to be displayed,
        such as "Add an account."

    Returns:
        int: The ID of the account entered by the user,
        or 0 to return to the main menu.
    """
    action = message.lower().split()[0]
    while True:
        print(f"LockMinder {message}\n")
        entry_id = input(
            f"""Please enter the ID of the account you'd like to {action},
or type 0 to return to the main menu: """)
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

    This function checks if an entry with the specified ID exists
    in the 'credentials' table of the specified database by executing an
    SQL query with the given 'entry_id'. If the entry does not exist,
    it prints a message and returns False. Otherwise, it returns True.

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
    """
    Add a new account to the 'credentials' table in the specified database.

    This function displays a prompt message indicating the action of adding a
    new account based on the given 'message'.
    It then prompts the user to enter values for the 'username', 'password',
    and 'service' fields, and adds the new entry to the 'credentials' table.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        message (str): The action message to be displayed, such as
        "Add an account."

    Returns:
        None: This function does not return any value explicitly.
    """
    print(f"LockMinder {message}\n")
    new_entry = prompt_values(database)
    with database:
        cursor = database.cursor()
        query = (
                f"INSERT INTO {TABLE} "
                "(username, password, service) "
                "VALUES (?, ?, ?)"
        )
        cursor.execute(query, new_entry)
        last_row_id = cursor.lastrowid
        print(f"Your account is now added to the credentials list.")
        row = get_database_values(database, key="id", value=last_row_id)
        print(row)
    display_menu(database) if replay_display_menu() else None


# "2": view all accounts
def view_all_accounts(database, description):
    """
    View all accounts stored in the 'credentials' table.

    This function displays a prompt message indicating the action of
    viewing all accounts based on the given 'description'.
    It fetches all the records from the 'credentials' table in the specified
    database using the 'get_database_values' function and
    prints them to the console.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        description (str): The action message to be displayed,
        such as "View all accounts."

    Returns:
        None: This function does not return any value explicitly.
    """
    print(f"LockMinder {description}\n")
    rows = get_database_values(database)
    print(rows)
    display_menu(database) if replay_display_menu() else None


# "3": update an account
def update_account(database, description):
    """
    Update an existing account in the 'credentials' table.

    This function displays a prompt message indicating the action
    of update an account based on the given 'description'. It prompts the
    user to enter the ID of the account to update, validates its existence
    using the 'check_entry' function, and displays the current account details.
    The user is then asked to provide new values for the 'username',
    'password', and 'service' fields, and the corresponding entry in the
    'credentials' table is updated with the new data.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        description (str): The action message to be displayed,
        such as "Update an account."

    Returns:
        None: This function does not return any value explicitly.
    """
    while True:
        entry_id = request_id(database, description)
        with database:
            cursor = database.cursor()
            cursor.execute(f"SELECT * FROM {TABLE} WHERE id = {entry_id}")
            if check_entry(database, entry_id):
                row = get_database_values(database, key="id", value=entry_id)
                print(row)
                new_entry = prompt_values(database)
                query = (
                    f"UPDATE {TABLE} "
                    "SET username = ?, password = ?, service = ? "
                    "WHERE id = ?"
                )
                cursor.execute(query, (*new_entry, entry_id))
                row = get_database_values(database, key="id", value=entry_id)
                print(f"Your account is now updated on the credentials list.")
                print(row)
                break
    display_menu(database) if replay_display_menu() else None


# "4": delete an account
def delete_account(database, description):
    """
    Delete an existing account from the 'credentials' table.

    This function displays a message indicating the action of delete an account
    on the given 'description'. It prompts the user to enter the ID
    of the account to delete, validates its existence using the 'check_entry'
    function, and displays the details of the account. The user is then asked
    to confirm the deletion, and if confirmed, the corresponding entry in the
    'credentials' table is removed.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        description (str): The action message to be displayed,
        such as "Delete an account."

    Returns:
        None: This function does not return any value explicitly.
    """
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
    """
    Generate a random password and display it to the user.

    This function generates a random password of the specified length and
    displays it to the user based on the given 'description'.
    The user is prompted to enter the desired password length, and the
    generated password is then shown on the screen.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        description (str): The action message to be displayed,
        such as "Generate a password."

    Returns:
        None: This function does not return any value explicitly.
    """
    while True:
        print(f"LockMinder {description}\n")
        try:
            password_length = int(input(
                "Please type the password length (min: 1 | max: 50): "))
            if password_length < 1 or password_length > 50:
                os.system("clear")
                print("Invalid input. "
                      "Please enter an integer number from 1 to 50.")
            else:
                new_password = ""
                for char in range(password_length):
                    new_dec_char = randrange(33, 126)
                    new_char = chr(new_dec_char)
                    new_password += new_char
                print("Follow the new password below:\n")
                print(new_password)
                break
        except ValueError:
            os.system("clear")
            print("Invalid input. Please enter an integer number.")
    display_menu(database) if replay_display_menu() else None


# "6": retrieve a password
def retrieve_password(database, description):
    """
    Retrieve the password for an existing account from the 'credentials' table.

    This function allows the user to retrieve the password for an existing
    account from the 'credentials'. It prompts the user to enter the ID of the
    account to retrieve the password for, validates its existence
    using the 'check_entry' function, and displays the account details,
    including the password.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.
        description (str): The action message to be displayed,
        such as "Retrieve a password."

    Returns:
        None: This function does not return any value explicitly.
    """
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
            bool: True if the user wants to go back (chooses 'Y'),
            False if they do not want to go back (chooses 'N').

        The function repeatedly prompts the user with a question asking if they
        would like to return to the main menu. The user's input is converted to
        uppercase using the 'upper()' method for case-insensitive comparison.
        If the user chooses 'Y', the function returns True, indicating they
        want to go back, and exits the loop.
        If the user chooses 'N', the function returns False, indicating they
        do not want to go back, and exits the loop.
    """
    while True:
        repeat = input(
            "Would you like to go back to the main menu? (Y / N): ").upper()
        if repeat == "Y":
            os.system("clear")
            return True
        elif repeat == "N":
            return False


def display_menu(database):
    """
    Display the main menu of the LockMinder application.

    This function presents a menu of options to the user for managing accounts
    in the 'credentials' table.
    The user is repeatedly prompted to select an option until they choose
    a valid option.
    The available options are represented as a dictionary with keys as the menu
    choices and values as a list
    containing the corresponding function to execute and a description of the
    action for each option.
    The user's input is validated, and the selected function is executed
    based on the user's choice.

    Args:
        database (sqlite3.Connection): A connection to the SQLite database.

    Returns:
        None: This function does not return any value explicitly.
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
    """
    Print the main menu of the LockMinder application.

    This function receives a dictionary of menu options with keys as
    option numbers and values as a list containing the corresponding function
    and a description of the action for each option.
    The menu is displayed using the 'PrettyTable' library to provide a
    structured and readable format.
    Each option number and its associated description are displayed in a
    table format.

    Args:
        options (dict): A dictionary containing menu options with
        keys as option numbers and values as lists
        with the corresponding function and description for each option.

    Returns:
        None: This function does not return any value explicitly.
    """
    print("LockMinder Menu:")
    menu = PrettyTable(["OPTION", "DESCRIPTION"])
    for key, value in options.items():
        menu.add_row([key, value[1]])
    print(menu)


def main():
    """
    Entry point for the LockMinder application.

    This function serves as the starting point of the LockMinder application.
    It displays a welcome message and initializes the database by calling
    the 'create_db' function.
    The main menu is then displayed by calling the 'display_menu' function,
    allowing the user to interact with the application and manage accounts.

    Args:
        None

    Returns:
        None: This function does not return any value explicitly.
    """
    print_ascii_banner()
    database = create_db()
    display_menu(database)


main()
