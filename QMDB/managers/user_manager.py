from sqlalchemy import func, select
from sqlalchemy.orm import Session

from QMDB.models import Review, User


class UserManager:
    """
    Manages all database operations for the User model.
    
    This class encapsulates the logic for CRUD operations on users,
    as well as user verification and statistical queries.
    """
    def __init__(self, session: Session):
        """
        Initializes the UserManager with a database session.

        Args:
            session (Session): The SQLAlchemy session to be used for 
                             database operations.
        """
        self.session = session

    def create(self, name: str, email: str) -> User:
        """
        Creates a new user record in the database.

        Args:
            name (str): The user's display name.
            email (str): The user's unique email address.

        Returns:
            User: The newly created User object.
        """
        user =User(name=name, email =email)
        self.session.add(user)
        self.session.commit()
        return user

    def get(self, user_id: int) -> User | None:
        """
        Retrieves a specific user by their primary key.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The User object if found, otherwise None.
        """
        return self.session.get(User, user_id)

    def get_all(self) -> list[User]:
        """
        Retrieves all users from the database.

        Returns:
            list[User]: A list of all User objects.
        """
        return self.session.execute(select(User)).scalars().all()
        
    def get_user_by_email(self, email: str) -> User | None:
        """
        Finds a user by their unique email address.

        Args:
            email (str): The email address to search for.

        Returns:
            User | None: The User object if found, otherwise None.
        """
        return self.session.execute(select(User).where(User.email ==email)).scalar_one_or_none()

    def get_most_active_users(self, limit=5) -> list[tuple]:
        """
        Finds the most active users based on the number of reviews they
        have written.

        Args:
            limit (int, optional): The number of users to return. Defaults to 5.

        Returns:
            list[tuple]: A list of tuples, where each tuple contains
                         (user_id, review_count).
        """
        return self.session.execute(select(Review.user_id, func.count(Review.id)).group_by(Review.user_id).order_by(func.count(Review.id).desc()).limit(limit)).all()

    def update(self, user_id: int, update_data: dict) -> User:
        """
        Updates a user's attributes (e.g., name, email).

        Args:
            user_id (int): The ID of the user to update.
            update_data (dict): A dictionary of fields to update.

        Returns:
            User: The updated User object.
        """
        user =self.session.get(User, user_id)
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            self.session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        """
        Deletes a user from the database.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        user =self.session.get(User, user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def verify_user(self, user_id: int) -> User:
        """
        Marks a user as verified.

        Args:
            user_id (int): The ID of the user to verify.

        Returns:
            User: The updated, verified User object.
        """
        user =self.session.get(User, user_id)
        if user:
            user.is_verified =True
            self.session.commit()
        return user

