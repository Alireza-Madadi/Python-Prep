import unittest
import hashlib
from secure_auth_system.main import Account, Site, welcome, change_password

class TestAccount(unittest.TestCase):
    """
    Tests the Account class, including all validation logic.
    """

    def test_account_creation_success(self):
        """Tests successful creation of a valid account."""
        acc = Account("Ali_Babaei", "ValidPass123", "0030376459", "09121212121", "test@example.com")
        self.assertEqual(acc.username, "Ali_Babaei")
        self.assertEqual(acc.phone, "09121212121")
        # Check if password was hashed
        self.assertNotEqual(acc.password, "ValidPass123")
        self.assertEqual(len(acc.password), 64) # SHA-256 length

    def test_invalid_username(self):
        """Tests that invalid usernames raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Invalid username."):
            Account("invalidusername", "ValidPass123", "0030376459", "09121212121", "test@example.com")
        with self.assertRaisesRegex(ValueError, "Invalid username."):
            Account("Ali_Babaei_Extra", "ValidPass123", "0030376459", "09121212121", "test@example.com")

    def test_invalid_password(self):
        """Tests that weak passwords raise ValueError."""
        # Too short
        with self.assertRaisesRegex(ValueError, "Invalid password."):
            Account("Ali_Babaei", "short", "0030376459", "09121212121", "test@example.com")
        # No uppercase
        with self.assertRaisesRegex(ValueError, "Invalid password."):
            Account("Ali_Babaei", "noupper123", "0030376459", "09121212121", "test@example.com")
        # No digit
        with self.assertRaisesRegex(ValueError, "Invalid password."):
            Account("Ali_Babaei", "NoDigitHere", "0030376459", "09121212121", "test@example.com")

    def test_invalid_national_id(self):
        """Tests that invalid national IDs raise ValueError."""
        # Wrong length
        with self.assertRaisesRegex(ValueError, "Invalid national id."):
            Account("Ali_Babaei", "ValidPass123", "123", "09121212121", "test@example.com")
        # Fails checksum
        with self.assertRaisesRegex(ValueError, "Invalid national id."):
            Account("Ali_Babaei", "ValidPass123", "0030376458", "09121212121", "test@example.com")

    def test_invalid_phone(self):
        """Tests that invalid phone numbers raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Invalid phone number."):
            Account("Ali_Babaei", "ValidPass123", "0030376459", "09121212", "test@example.com")
        with self.assertRaisesRegex(ValueError, "Invalid phone number."):
            Account("Ali_Babaei", "ValidPass123", "0030376459", "1234567890", "test@example.com")

    def test_invalid_email(self):
        """Tests that invalid emails raise ValueError."""
        with self.assertRaisesRegex(ValueError, "Invalid email."):
            Account("Ali_Babaei", "ValidPass123", "0030376459", "09121212121", "not-an-email")
        with self.assertRaisesRegex(ValueError, "Invalid email."):
            Account("Ali_Babaei", "ValidPass123", "0030376459", "09121212121", "test@domain.toolong")

    def test_phone_normalization(self):
        """Tests that +98 numbers are normalized to 09..."""
        acc = Account("Ali_Babaei", "ValidPass123", "0030376459", "+989121212121", "test@example.com")
        self.assertEqual(acc.phone, "09121212121")


class TestSite(unittest.TestCase):
    """
    Tests the Site class for registration, login, and logout logic.
    """
    
    def setUp(self):
        """Set up a new site and a valid user for each test."""
        self.site = Site("salib.net")
        self.user1 = Account("Test_User", "ValidPass1T", "0030376459", "09121212121", "test@example.com")
        self.user1_hash = hashlib.sha256("ValidPass1T".encode("utf-8")).hexdigest()

    def test_init_site(self):
        """Tests the site constructor."""
        self.assertEqual(self.site.url, "salib.net")
        self.assertListEqual(self.site.registered_users, [])
        self.assertListEqual(self.site.active_users, [])

    def test_register_success(self):
        """Tests successful user registration."""
        result = self.site.register(self.user1)
        self.assertEqual(result, "Register successful.")
        self.assertIn(self.user1, self.site.registered_users)

    def test_register_duplicate(self):
        """Tests that registering a duplicate user raises an error."""
        self.site.register(self.user1)
        with self.assertRaisesRegex(ValueError, "User already registered."):
            self.site.register(self.user1)

    def test_login_success(self):
        """Tests successful login with username and email."""
        self.site.register(self.user1)
        
        # Test login with username
        result_user = self.site.login(username="Test_User", password="ValidPass1T")
        self.assertEqual(result_user, "Login successful.")
        self.assertIn(self.user1, self.site.active_users)
        
        self.site.logout(self.user1) # Log out before next test
        
        # Test login with email
        result_email = self.site.login(email="test@example.com", password="ValidPass1T")
        self.assertEqual(result_email, "Login successful.")
        self.assertIn(self.user1, self.site.active_users)

    def test_login_failure(self):
        """Tests various failed login attempts."""
        self.site.register(self.user1)
        
        # Wrong password
        result_wrong_pass = self.site.login(username="Test_User", password="WrongPassword")
        self.assertEqual(result_wrong_pass, "Invalid login.")
        self.assertNotIn(self.user1, self.site.active_users)

        # User not found
        result_not_found = self.site.login(username="Fake_User", password="ValidPass1T")
        self.assertEqual(result_not_found, "Invalid login.")

    def test_login_already_active(self):
        """Tests that logging in twice returns 'User already logged in'."""
        self.site.register(self.user1)
        self.site.login(username="Test_User", password="ValidPass1T")
        result = self.site.login(username="Test_User", password="ValidPass1T")
        self.assertEqual(result, "User already logged in.")
        self.assertEqual(self.site.active_users.count(self.user1), 1) # Still only logged in once

    def test_logout(self):
        """Tests successful and unsuccessful logout."""
        self.site.register(self.user1)
        
        # Test logout when not logged in
        result_not_logged_in = self.site.logout(self.user1)
        self.assertEqual(result_not_logged_in, "User is not logged in.")
        
        # Test successful logout
        self.site.login(username="Test_User", password="ValidPass1T")
        self.assertIn(self.user1, self.site.active_users)
        result_success = self.site.logout(self.user1)
        self.assertEqual(result_success, "Logout successful.")
        self.assertNotIn(self.user1, self.site.active_users)


class TestDecorators(unittest.TestCase):
    """
    Tests the custom decorators @show_welcome and @verify_change_password.
    """
    
    def setUp(self):
        self.user = Account("SeyedAli_Babaei", "ValidPass123", "0030376459", "09121212121", "test@example.com")
        self.original_hash = self.user.password

    def test_show_welcome_decorator(self):
        """Tests the @show_welcome name formatting."""
        # Test long name truncation
        self.user.username = "This_Is_A_Very_Long_Username" # <--- FIX: Use a name that IS > 15 chars
        result_long = welcome(self.user)
        # FIX: The string 'This Is A Very ' is 15 chars. So the result is '...Very ...' not '...Very L...'
        self.assertEqual(result_long, "Welcome to our website This Is A Very ...!") 

        # Test short name
        self.user.username = "Ali_Babaei"
        result_short = welcome(self.user)
        self.assertEqual(result_short, "Welcome to our website Ali Babaei!") # <--- FIX: This is the correct non-truncated string

    def test_change_password_decorator_success(self):
        """Tests that the decorator allows a password change with the correct old password."""
        result = change_password(self.user, old_password="ValidPass123", new_password="NewValidPass456")
        self.assertEqual(result, "Your password has been changed successfully.")
        # Check that the hash actually changed
        self.assertNotEqual(self.original_hash, self.user.password)
        # Check that the new hash is correct
        new_hash = hashlib.sha256("NewValidPass456".encode("utf-8")).hexdigest()
        self.assertEqual(self.user.password, new_hash)

    def test_change_password_decorator_failure(self):
        """Tests that the decorator blocks a password change with the wrong old password."""
        with self.assertRaisesRegex(ValueError, "Incorrect old password."):
            change_password(self.user, old_password="WRONG_OLD_PASS", new_password="NewValidPass456")
        
        # Verify that the password did NOT change
        self.assertEqual(self.original_hash, self.user.password)

    def test_change_password_decorator_invalid_new(self):
        """Tests that the decorator blocks an invalid NEW password."""
        with self.assertRaisesRegex(ValueError, "Invalid password."):
            change_password(self.user, old_password="ValidPass123", new_password="short")
        
        # Verify that the password did NOT change
        self.assertEqual(self.original_hash, self.user.password)


if __name__ == '__main__':
    unittest.main()


