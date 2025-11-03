# Secure Account Management System

A Python project demonstrating a secure, object-oriented approach to user account management, input validation, and authentication.

This project was developed as part of the **Quera College Advanced Python and Object-Oriented Thinking** course. It showcases the principles of building a robust and secure data model for handling sensitive user information.

## Core Concepts Demonstrated

This project showcases proficiency in several critical backend and security concepts:

- **Object-Oriented Programming (OOP):** The entire logic is encapsulated in two main classes, Account (representing the user data model) and Site (representing the application logic).
- **Secure Password Hashing:** Uses Python's hashlib library to **hash** (not encrypt) passwords with SHA-256 before they are stored, ensuring that plain-text passwords are never saved.
- **Advanced Input Validation:** Implements rigorous server-side validation for all user inputs:
  - **Regex (Regular Expressions):** Used to validate complex patterns for usernames (^\[a-zA-Z\]+\_\[a-zA-Z\]+), phone numbers (^(\\+98|0)9\\d{9}\$), and emails.
  - **Algorithmic Validation:** Implements the checksum algorithm for validating 10-digit Iranian National IDs.
- **Custom Python Decorators:** Demonstrates advanced Python usage by creating custom decorators from scratch:
  - @show_welcome: Intercepts a function call to format a user's name for a welcome message.
  - @verify_change_password: Acts as a security middleware, verifying the user's old password before allowing the password change function to execute.
- **Unit Testing:** A comprehensive test suite built with unittest that covers:
  - All successful and failing validation cases (e.g., invalid email, weak password).
  - Core Site logic (register, login, logout, duplicate user).
  - Security logic for the decorators (e.g., blocking a password change with the wrong old password).

## Tech Stack

- **Python 3**
- **hashlib** (for SHA-256 password hashing)
- **re** (for regex-based validation)
- **unittest** (for Testing)

## How to Run Tests

This project is a library and is best verified using its test suite.

To run all tests, navigate to the **root directory** of this repository (Python-Prep/) and use the unittest discover command with the -s flag:

\# From the root "Python-Prep" directory:  
python -m unittest discover -s secure_auth_system  

## Project Structure

Python-Prep/  
│  
└── secure_auth_system/  
├── \__init_\_.py # Makes 'secure_auth_system' a Python package  
├── README.md # This README file  
├── requirements.txt # (Empty, uses standard libraries)  
├── main.py # Contains Account, Site, and decorator logic  
│  
└── test/  
├── \__init_\_.py # Makes 'test' a sub-package  
└── test_sample.py # The main test suite