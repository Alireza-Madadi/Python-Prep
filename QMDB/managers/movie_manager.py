from datetime import datetime
from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session

from QMDB.models import Movie, Genre, Review


class MovieManager:
    """
    Manages all database operations for the Movie model.
    
    This class encapsulates the logic for CRUD operations on movies,
    managing their relationships (like genres and reviews),
    and running complex statistical queries.
    """
    def __init__(self, session: Session) -> None:
        """
        Initializes the MovieManager with a database session.

        Args:
            session (Session): The SQLAlchemy session to be used for 
                             database operations.
        """
        self.session = session

    def create(self, title: str, release_year: int) -> Movie:
        """
        Creates a new movie record in the database.

        Args:
            title (str): The title of the movie.
            release_year (int): The release year of the movie.

        Returns:
            Movie: The newly created Movie object.
        """
        new_movie =Movie(title=title, release_year=release_year)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def get(self, movie_id: int) -> Movie | None:
        """
        Retrieves a specific movie by its primary key.

        Args:
            movie_id (int): The ID of the movie to retrieve.

        Returns:
            Movie | None: The Movie object if found, otherwise None.
        """
        return self.session.get(Movie, movie_id)

    def get_all(self) -> list[Movie]:
        """
        Retrieves all movies from the database.

        Returns:
            list[Movie]: A list of all Movie objects.
        """
        return self.session.execute(select(Movie)).scalars().all()

    def add_genre(self, movie_id: int, genre: Genre) -> Movie:
        """
        Associates a genre with a specific movie (Many-to-Many).

        Args:
            movie_id (int): The ID of the movie.
            genre (Genre): The Genre object to add.

        Returns:
            Movie: The updated Movie object with the new genre association.
        """
        movie =self.get(movie_id)
        movie.genres.append(genre)
        self.session.commit()
        return movie

    def get_reviews(self, movie_id: int) -> list[Review]:
        """
        Retrieves all reviews for a specific movie.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            list[Review]: A list of Review objects related to the movie.
        """
        movie = self.get(movie_id)
        return movie.reviews


    def get_average_rating(self, movie_id: int) -> float | None:
        """
        Calculates the average rating for a specific movie.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            float | None: The average rating, or None if no reviews exist.
        """
        q =select(func.avg(Review.rating)).where(Review.movie_id ==movie_id)
        return self.session.execute(q).scalar_one_or_none()

    def update(self, movie_id: int, update_data: dict) -> Movie:
        """
        Updates a movie's attributes (e.g., title, year).

        Args:
            movie_id (int): The ID of the movie to update.
            update_data (dict): A dictionary of fields to update.

        Returns:
            Movie: The updated Movie object.
        """
        movie =self.session.get(Movie, movie_id)
        if movie:
            for key, value in update_data.items():
                setattr(movie, key, value)
            self.session.commit()
        return movie

    def delete(self, movie_id: int) -> bool:
        """
        Deletes a movie from the database.

        Args:
            movie_id (int): The ID of the movie to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        movie =self.session.get(Movie, movie_id)
        if movie:
            self.session.delete(movie)
            self.session.commit()
            return True
        return False

    def remove_genre(self, movie_id: int, genre: Genre) -> Movie:
        """
        Removes a genre association from a specific movie.

        Args:
            movie_id (int): The ID of the movie.
            genre (Genre): The Genre object to remove.

        Returns:
            Movie: The updated Movie object.
        """
        movie =self.session.get(Movie, movie_id)
        movie.genres.remove(genre)
        self.session.commit()
        return movie

    def get_top_movies_by_rating(self, limit: int = 10) -> list[tuple]:
        """
        Gets a list of movies ranked by their average rating (descending).

        Args:
            limit (int, optional): The number of movies to return. Defaults to 10.

        Returns:
            list[tuple]: A list of tuples, where each tuple contains
                         (Movie object, average_rating).
        """
        stmt =select(Movie, func.avg(Review.rating)).join(Review, isouter=True).group_by(Movie.id).order_by(func.avg(Review.rating).desc()).limit(limit)
        return self.session.execute(stmt).all()

    def get_movies_by_genre(self, genre_name: str) -> list[Movie]:  
        """
        Finds all movies associated with a specific genre name.

        Args:
            genre_name (str): The name of the genre to filter by.

        Returns:
            list[Movie]: A list of Movie objects matching the genre.
        """
        stmt =select(Movie).join(Movie.genres).where(Genre.name ==genre_name)
        return self.session.execute(stmt).scalars().all()

    def get_top_rated_movies_by_genre(self) -> list[tuple]:
        """
        Gets a list of movies and their average ratings, grouped by genre.
        Used for statistical analysis (e.g., "What is the top-rated
        movie in each genre?").

        Returns:
            list[tuple]: A list of tuples containing
                         (genre_name, movie_title, average_rating).
        """
        stmt =select(Genre.name, Movie.title, func.avg(Review.rating)).join(Genre.movies).join(Movie.reviews, isouter=True).group_by(Genre.name, Movie.title).order_by(Genre.name, func.avg(Review.rating).desc())
        return self.session.execute(stmt).all()

