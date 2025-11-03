# QMDB: SQLAlchemy ORM & Query Engine

A Python project demonstrating advanced SQLAlchemy usage, database design with ORM, complex querying, and the "Manager Pattern".

This project was developed as part of the **Quera College Advanced Python and Object-Oriented Thinking** course, showcasing the ability to build a robust, testable, and clean data-access layer for an application similar to IMDB.

## Core Concepts Demonstrated

This project showcases proficiency in several key backend technologies and design patterns:

* **SQLAlchemy ORM:** Defining database schema (Movies, Users, Genres, Reviews) as Python classes in `models.py`.

* **Complex Relationships:** Implementation of:

  * **One-to-Many:** `User` to `Review`, `Movie` to `Review`.

  * **Many-to-Many:** `Movie` to `Genre` (using an association table).

* **Manager Pattern:** Encapsulating all database logic (CRUD operations and complex queries) within dedicated `Manager` classes (`/managers`). This keeps the database logic clean, testable, and separate from potential application logic.

* **Advanced Queries:** Writing complex, efficient queries using SQLAlchemy's core functions, including:

  * `func.avg` and `func.count` for statistical analysis.

  * `group_by` for aggregating data.

  * `order_by` and `limit` for sorting and pagination.

  * `join` for combining data across related models.

* **Unit Testing:** A complete test suite built with Python's `unittest` module. The tests use an **in-memory SQLite database** (`sqlite:///:memory:`) to ensure fast, isolated, and reliable testing of all manager methods and statistical queries.

## Tech Stack

* **Python 3**

* **SQLAlchemy** (for ORM and Querying)

* **unittest** (for Testing)

## How to Install

This project is a library (a data-access layer) and isn't meant to be "run" directly. You can install its dependencies using:

```bash
# Navigate to the project directory
cd Python-Prep/QMDB

# Install dependencies
pip install -r requirements.txt
## How to Run Tests

A comprehensive test suite is included to validate all database logic.

To run all tests for **this specific project**, navigate to the root directory of this repository (`Python-Prep/`) and use the `unittest discover` command with the `-s` flag to specify the starting directory:

```bash
# From the root "Python-Prep" directory:
python -m unittest discover -s QMDB

##Project Structure
Python-Prep/
│
├── QMDB/                 # Main project package
│   ├── __init__.py       # Makes 'QMDB' a Python package
│   ├── models.py         # Defines all SQLAlchemy ORM models (Tables)
│   ├── requirements.txt  # Project dependencies
│   │
│   ├── managers/         # Encapsulates all database logic
│   │   ├── __init__.py
│   │   ├── genre_manager.py
│   │   ├── movie_manager.py
│   │   ├── review_manager.py
│   │   └── user_manager.py
│   │
│   └── test/             # Contains all unit tests
│       ├── __init__.py   # Makes 'test' a sub-package
│       └── tests.py  # The main test suite
│