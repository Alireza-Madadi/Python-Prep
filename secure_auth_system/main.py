import re
import hashlib
from functools import wraps

class Account:
    """
    Represents a user account with secure validation and password hashing.
    
    All data is validated upon initialization.
    """
    
    def __init__(self, username: str, password: str, national_id: str, phone: str, email: str) -> None:
        """
        Initializes a new Account.

        Args:
            username (str): The username (must be 'name_lastname').
            password (str): The plain-text password (must meet complexity rules).
            national_id (str): The 10-digit national ID.
            phone (str): The phone number (valid Iranian format).
            email (str): The email address.
            
        Raises:
            ValueError: If any validation fails.
        """
        self.username = self.username_validation(username)
        self.password = self.password_validation(password)  # Hashed password
        self.national_id = self.id_validation(national_id)
        self.phone = self.phone_validation(phone)
        self.email = self.email_validation(email)

    def username_validation(self, username: str) -> str:
        """Validates username format (e.g., 'firstname_lastname')."""
        pattern = r"^[a-zA-Z]+_[a-zA-Z]+"
        if not re.fullmatch(pattern, username):
            raise ValueError("Invalid username.")
        return username

    def password_validation(self, password: str) -> str:
        """
        Validates password complexity and returns its SHA-256 hash.
        Rules: min 8 chars, 1 uppercase, 1 lowercase, 1 digit.
        """
        if len(password) < 8 or \
           not re.search(r"[A-Z]", password) or \
           not re.search(r"[a-z]", password) or \
           not re.search(r"\d", password):
            raise ValueError("Invalid password.")
        # Hash the valid password for storage
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def id_validation(self, id_str: str) -> str:
        """Validates a 10-digit Iranian National ID using its checksum."""
        if id_str.isdigit() and len(id_str) == 10:
            s = 0
            for i in range(9):
                s += int(id_str[i]) * (10 - i)
            
            remainder = s % 11
            check_digit = int(id_str[9])
            
            if (remainder < 2 and remainder == check_digit) or \
               (remainder >= 2 and (11 - remainder) == check_digit):
                return id_str
        raise ValueError("Invalid national id.")

    def phone_validation(self, phone: str) -> str:
        """Validates Iranian phone number formats (09, +989, ...)."""
        pattern = r"^(\+98|0)9\d{9}$"
        if not re.fullmatch(pattern, phone):
            raise ValueError("Invalid phone number.")
        # Standardize phone number to 09... format
        if phone.startswith("+98"):
            phone = phone.replace("+98", "0")
        return phone

    def email_validation(self, email: str) -> str:
        """Validates email format using regex."""
        pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,5}$"
        if not re.fullmatch(pattern, email):
            raise ValueError("Invalid email.")
        return email

    def set_new_password(self, new_password: str) -> None:
        """
        Securely sets a new password after validating and hashing it.
        This is intended to be used with the @verify_change_password decorator.
        """
        self.password = self.password_validation(new_password)

    def __repr__(self):
        return f"<Account username='{self.username}'>"

    def __str__(self):
        return self.username

    def __eq__(self, other):
        """Two accounts are equal if their usernames are the same."""
        if isinstance(other, Account):
            return self.username == other.username
        return False


class Site:
    """
    Manages user registration, login, and logout for the website.
    """
    def __init__(self, url_address: str) -> None:
        self.url = url_address
        self.registered_users = []  # List[Account]
        self.active_users = []      # List[Account]

    def register(self, user: Account) -> str:
        """Registers a new user account."""
        if user in self.registered_users:
            raise ValueError("User already registered.")
        self.registered_users.append(user)
        return "Register successful."

    def login(self, username: str = None, email: str = None, password: str = None) -> str:
        """Logs in a user via username or email, and password."""
        if not password or (username is None and email is None):
            return "Invalid login." # Must provide password AND (user or email)
            
        hashpass = hashlib.sha256(password.encode("utf-8")).hexdigest()
        
        # Find the user first
        account_to_check = None
        for acc in self.registered_users:
            if username is not None and acc.username == username:
                account_to_check = acc
                break
            if email is not None and acc.email == email:
                account_to_check = acc
                break
        
        # If no user was found with that username/email
        if account_to_check is None:
            return "Invalid login." # <-- This fixes the security bug

        # Now check the password for the found user
        if hashpass == account_to_check.password:
            if account_to_check in self.active_users:
                return "User already logged in."
            else:
                self.active_users.append(account_to_check)
                return "Login successful."
        else:
            # User was found, but password was wrong
            return "Invalid login."

    def logout(self, user: Account) -> str:
        """Logs out an active user."""
        if user in self.active_users:
            self.active_users.remove(user)
            return "Logout successful."
        return "User is not logged in."

    def __repr__(self):
        return f"<Site url='{self.url}' users={len(self.registered_users)}>"

    def __str__(self):
        return self.url

# --- Decorators ---

def show_welcome(func):
    """
    Decorator: Formats the user's name before passing it to the function.
    Converts 'firstname_lastname' to 'Firstname Lastname' and truncates if > 15 chars.
    """
    @wraps(func)
    def wrapper(user: Account):
        formatted_name = user.username.replace("_", " ") # <--- FIX 1: Removed .title()
        if len(formatted_name) > 15:
            formatted_name = formatted_name[:15] + "..."
        return func(formatted_name)  # Pass the formatted string
    return wrapper

def verify_change_password(func):
    """
    Decorator: Acts as a security check for password changes.
    It verifies the old_password against the user's stored hash
    before allowing the wrapped function (which sets the new password) to run.
    """
    @wraps(func)
    def wrapper(user: Account, old_password: str, new_password: str):
        old_password_hash = hashlib.sha256(old_password.encode('utf-8')).hexdigest()
        if old_password_hash == user.password:
            # Old password is correct, proceed to change it
            return func(user, new_password)
        else:
            # Wrong old password, raise an error
            raise ValueError("Incorrect old password.")
    return wrapper

# --- Example Functions Using Decorators ---

@show_welcome
def welcome(formatted_username: str) -> str:
    """Example function that receives a formatted name from its decorator."""
    return f"Welcome to our website {formatted_username}!"

@verify_change_password
def change_password(user: Account, new_pass: str) -> str:
    """
    Example function to change a password.
    The @verify_change_password decorator will run first.
    """
    user.set_new_password(new_pass)
    return "Your password has been changed successfully."

