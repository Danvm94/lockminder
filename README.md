# LockMinder
![LockMinder](./readme/initial.png)

LockMinder is a user-friendly password manager software that helps you securely store and manage your account credentials. With an intuitive menu-based interface, you can easily add, view, update, and delete accounts in the encrypted SQLite database. LockMinder also offers a password generation tool for creating strong and randomized passwords. Simplify your digital life and keep your passwords safe with LockMinder.

Note: For security purposes on demonstration, LockMinder currently operates with an in-memory database, ensuring that no data is saved outside the application. Please be aware that any added account information will not persist beyond the current session.

## Demo
Experience LockMinder in action by visiting our live demo deployed on Heroku. Simply access the following URL to explore the software's functionality: [LockMinder](https://lockminder-4bcc151d4d1c.herokuapp.com/)
- - - 
# Contents
* [Technologies Used](#technologies-used)
    * [Language](#language)
    * [Libraries](#libraries)
    * [Frameworks & Tools](#frameworks--tools)
* [User Experience](#user-experience-ux)
* [Design](#design)
  * [Flowchart](#flowchart)
  * [Existing Features](#existing-features)
  * [Future Implementations](#future-implementations)
* [Deployment](#deployment)
  * [Heroku Deployment](#heroku-deployment)
  * [Run locally](#run-locally)
  * [Create data model and integrate using an API](#create-data-model-and-integrate-using-an-api)
* [Testing](#testing)
* [Credits](#credits)
- - - 

# Technologies Used
## Language
* ![Python](https://img.shields.io/badge/Python-3.x-yellow?logo=python&logoColor=yellow)

Python was the chosen language for this project.

## Libraries
* ![SQLite3](https://img.shields.io/badge/SQLite3-Library-yellow?logo=sqlite&logoColor=white
) 

    The "SQLite3" was used as the database management system to securely store and manage account credentials in the project.

* ![os](https://img.shields.io/badge/OS-Library-yellow?logo=linux&logoColor=white) 

    The "OS" library was used to clear the Python terminal, providing a clean and user-friendly interface for the project.

* ![Random](https://img.shields.io/badge/Random-Library-yellow)

    The "random" library was used for the password generator to create strong and randomized passwords in the project.

* ![prettytable](https://img.shields.io/badge/prettytable-Library-yellow)

    The "prettytable" feature was used to format and display tabular data in a visually appealing manner in the project.

## Frameworks & Tools
* ![Heroku Deployed](https://img.shields.io/badge/Heroku-Deployed-yellow?logo=heroku&logoColor=white)

    Heroku was used to deploy a live view of the project

* ![Git Version Control](https://img.shields.io/badge/Git-Version%20Control-yellow?logo=git&logoColor=white)

    Git was used for version control in the project, enabling efficient tracking of changes.

* ![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-yellow?logo=github&logoColor=white)

    GitHub was used as the repository for this project.

For this project a [Code Institute template](https://github.com/Code-Institute-Org/python-essentials-template), was utilized. It provided all the necessary files to run the mock terminal in the browser, facilitating the development process.
- - - 
# User Experience (UX)

## The ideal users for this website is:
* Individuals who are looking for a secure and user-friendly password manager to store and manage their account credentials.

* Users who require a reliable and convenient method to generate strong and randomized passwords for various online services.

## User stories:
* As a user, I want to create an account in the password manager to securely store my login credentials for various online services.

* As a user, I want the password manager to generate strong and unique passwords for accounts to enhance security.

* As a user, I want the ability to view and manage all my stored account credentials in a well-organized and user-friendly interface.

* As a user, I want the option to update or change passwords for my accounts when needed, ensuring my information remains up-to-date.

* As a user, I want the password manager to provide a simple and efficient way to delete accounts that I no longer need.

## How to use:
