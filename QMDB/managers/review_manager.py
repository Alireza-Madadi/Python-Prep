from sqlalchemy import func, select
from sqlalchemy.orm import Session

from QMDB.models import Review


class ReviewManager:
    """
    Manages all database operations for the Review model.
    
    This class encapsulates the logic for CRUD operations on reviews
    and running complex queries related to user ratings and comments.
    """
    def __init__(self, session: Session):
        """
        Initializes the ReviewManager with a database session.

        Args:
            session (Session): The SQLAlchemy session to be used for 
                             database operations.
        """
        self.session = session

    def create(self, movie_id: int, user_id: int, rating: int, comment: str = None) -> Review:
        """
        Creates a new review record in the database.

        Args:
            movie_id (int): The ID of the movie being reviewed.
            user_id (int): The ID of the user writing the review.
            rating (int): The rating given (e.g., 1-5).
            comment (str, optional): The text comment. Defaults to None.

        Returns:
            Review: The newly created Review object.
        """
        new_review =Review(movie_id=movie_id, user_id =user_id, rating=rating, comment=comment)
        self.session.add(new_review)
        self.session.commit()
        return new_review

    def get(self, review_id: int) -> Review | None:
        """
        Retrieves a specific review by its primary key.

        Args:
            review_id (int): The ID of the review to retrieve.

        Returns:
            Review | None: The Review object if found, otherwise None.
        """
        return self.session.get(Review, review_id)
        
    def get_all(self) -> list[Review]:
        """
        Retrieves all reviews from the database.

        Returns:
            list[Review]: A list of all Review objects.
        """
        return self.session.execute(select(Review)).scalars().all()

    def get_reviews_by_user(self, user_id: int) -> list[Review]:
        """
        Retrieves all reviews written by a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[Review]: A list of reviews from that user.
        """
        return self.session.execute(select(Review).where(Review.user_id ==user_id)).scalars().all()

    def get_latest_reviews_for_movie_by_time(self, movie_id: int, limit: int = 5) -> list[Review]:
        """
        Gets the most recent reviews for a specific movie, ordered by creation time.

        Args:
            movie_id (int): The ID of the movie.
            limit (int, optional): The number of reviews to return. Defaults to 5.

        Returns:
            list[Review]: A list of the latest Review objects.
        """
        return self.session.execute(select(Review).where(Review.movie_id ==movie_id).order_by(Review.created_at.desc()).limit(limit)).scalars().all()

    def get_highest_rated_reviews(self, movie_id: int, limit: int = 5) -> list[Review]:
        """
        Gets the highest-rated reviews for a specific movie.

        Args:
            movie_id (int): The ID of the movie.
            limit (int, optional): The number of reviews to return. Defaults to 5.

        Returns:
            list[Review]: A list of the highest-rated Review objects.
        """
        return self.session.execute(select(Review).where(Review.movie_id ==movie_id).order_by(Review.rating.desc()).limit(limit)).scalars().all()

    def get_average_rating_by_user(self) -> list[tuple]:
        """
        Calculates the average rating given by each user.

        Returns:
            list[tuple]: A list of tuples, where each tuple contains
                         (user_id, average_rating).
        """
        return self.session.execute(select(Review.user_id, func.avg(Review.rating)).group_by(Review.user_id)).all()

    def update(self, review_id: int, update_data: dict) -> Review:
        """
        Updates a review's attributes (e.g., rating, comment).

        Args:
            review_id (int): The ID of the review to update.
            update_data (dict): A dictionary of fields to update.

        Returns:
            Review: The updated Review object.
        """
        review =self.session.get(Review, review_id)
        if review:
            for key, value in update_data.items():
                setattr(review, key, value)
            self.session.commit()
        return review

    def delete(self, review_id: int) -> bool:
        """
        Deletes a review from the database.

        Args:
            review_id (int): The ID of the review to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        review =self.session.get(Review, review_id)
        if review:
            self.session.delete(review)
            self.session.commit()
            return True
        return False

