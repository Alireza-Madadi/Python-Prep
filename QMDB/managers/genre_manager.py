from sqlalchemy import select, func
from sqlalchemy.orm import Session

from QMDB.models import Genre, MovieGenre


class GenreManager:
    """
    Manages all database operations for the Genre model.
    
    This class encapsulates the logic for creating, retrieving,
    updating, and deleting (CRUD) genres, as well as
    running complex queries related to genres.
    """
    def __init__(self, session: Session):
        """
        Initializes the GenreManager with a database session.

        Args:
            session (Session): The SQLAlchemy session to be used for 
                             database operations.
        """
        self.session = session

    def create(self, name: str) -> Genre:
        """
        Creates a new genre record in the database.

        Args:
            name (str): The unique name for the new genre.

        Returns:
            Genre: The newly created Genre object.
        """
        new_genre =Genre(name=name)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre
        
    def get(self, genre_id: int) -> Genre | None:
        """
        Retrieves a specific genre by its primary key.

        Args:
            genre_id (int): The ID of the genre to retrieve.

        Returns:
            Genre | None: The Genre object if found, otherwise None.
        """
        return self.session.get(Genre, genre_id)

    def get_all(self) -> list[Genre]:
        """
        Retrieves all genres from the database.

        Returns:
            list[Genre]: A list of all Genre objects.
        """
        return self.session.execute(select(Genre)).scalars().all()

    def get_genre_by_name(self, name: str) -> Genre | None:
        """
        Finds a genre by its unique name.

        Args:
            name (str): The name of the genre to find.

        Returns:
            Genre | None: The Genre object if found, otherwise None.
        """
        return self.session.execute(select(Genre).where(Genre.name ==name)).scalar_one_or_none()

    def update(self, genre_id: int, new_name: str) -> Genre:
        """
        Updates the name of an existing genre.

        Args:
            genre_id (int): The ID of the genre to update.
            new_name (str): The new name for the genre.

        Returns:
            Genre: The updated Genre object.
        """
        genre =self.session.get(Genre, genre_id)
        if genre:
            genre.name =new_name
            self.session.commit()
        return genre

    def delete(self, genre_id: int) -> bool:
        """
        Deletes a genre from the database.

        Args:
            genre_id (int): The ID of the genre to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        genre =self.session.get(Genre, genre_id)
        if genre:
            self.session.delete(genre)
            self.session.commit()
            return True
        return False

    def get_genres_with_most_movies(self) -> list[tuple]:
        """
        Gets a list of genres, ordered by the number of movies
        associated with them (descending).

        Returns:
            list[tuple]: A list of tuples, where each tuple contains
                         (Genre object, movie_count).
        """
        stmt =select(Genre, func.count(MovieGenre.movie_id)).join(MovieGenre, isouter=True).group_by(Genre.id).order_by(func.count(MovieGenre.movie_id).desc())
        return self.session.execute(stmt).all()

