from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

class MovieGenre(Base):
    """
    Association table for the many-to-many relationship 
    between Movie and Genre.
    """
    __tablename__ ="moviegenres"
    movie_id: Mapped[int] =mapped_column(ForeignKey("movies.id"), primary_key=True)
    genre_id: Mapped[int] =mapped_column(ForeignKey("genres.id"), primary_key=True)

class Movie(Base):
    """
    Represents a Movie in the database.

    Attributes:
        id (int): Primary key.
        title (str): The title of the movie.
        release_year (int): The release year of the movie.
    
    Relationships:
        genres (List[Genre]): Many-to-Many relationship with Genre.
        reviews (List[Review]): One-to-Many relationship with Review.
    """
    __tablename__ ="movies"
    id: Mapped[int] =mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] =mapped_column(nullable=False)
    release_year: Mapped[int] =mapped_column(nullable=True)
    
    # Relationships
    genres: Mapped[List["Genre"]] =relationship(secondary="moviegenres", back_populates="movies")
    reviews: Mapped[List["Review"]] =relationship(back_populates="movie")

class User(Base):
    """
    Represents a User (reviewer) in the database.

    Attributes:
        id (int): Primary key.
        name (str): User's display name.
        email (str): User's unique email address.
        is_verified (bool): Flag for email verification.
        created_at (datetime): Timestamp of user creation.
        
    Relationships:
        reviews (List[Review]): One-to-Many relationship with Review.
    """
    __tablename__ ="users"
    id: Mapped[int] =mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] =mapped_column(nullable=False)
    email: Mapped[str] =mapped_column(nullable=False, unique=True)
    is_verified: Mapped[bool] =mapped_column(default=False)
    created_at: Mapped[datetime] =mapped_column(default=datetime.now)
    
    # Relationships
    reviews: Mapped[List["Review"]] =relationship(back_populates="user")

class Genre(Base):
    """
    Represents a movie Genre (e.g., "Sci-Fi", "Comedy").

    Attributes:
        id (int): Primary key.
        name (str): The unique name of the genre.
        
    Relationships:
        movies (List[Movie]): Many-to-Many relationship with Movie.
    """
    __tablename__ ="genres"
    id: Mapped[int] =mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] =mapped_column(nullable=False, unique=True)
    
    # Relationships
    movies: Mapped[List["Movie"]] =relationship(secondary="moviegenres", back_populates="genres")

class Review(Base):
    """
    Represents a Review for a Movie, written by a User.

    Attributes:
        id (int): Primary key.
        rating (int): The rating given (e.g., 1-5).
        comment (str): The text content of the review.
        created_at (datetime): Timestamp of review creation.
        updated_at (datetime): Timestamp of last review update.
        
    Relationships:
        movie (Movie): Many-to-One relationship with Movie.
        user (User): Many-to-One relationship with User.
    """
    __tablename__ ="review"
    id: Mapped[int] =mapped_column(primary_key=True, autoincrement=True)
    
    # Foreign Key to Movie
    movie_id: Mapped[int] =mapped_column(ForeignKey("movies.id"))
    movie: Mapped[Movie] =relationship(back_populates="reviews")
    
    # Foreign Key to User
    user_id: Mapped[int] =mapped_column(ForeignKey("users.id"))
    user: Mapped[User] =relationship(back_populates="reviews")
    
    rating: Mapped[int] =mapped_column(nullable=False)
    comment: Mapped[str] =mapped_column(nullable=True)
    created_at: Mapped[datetime] =mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] =mapped_column(default=datetime.now, onupdate=datetime.now)

