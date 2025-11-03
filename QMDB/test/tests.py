import unittest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# Import all models and managers using relative paths from the root
from QMDB.models import Base, Movie, Genre, Review, User
from QMDB.managers.movie_manager import MovieManager
from QMDB.managers.genre_manager import GenreManager
from QMDB.managers.review_manager import ReviewManager
from QMDB.managers.user_manager import UserManager


class TestManagerOperations(unittest.TestCase):
    """
    Test suite for all manager classes (User, Movie, Genre, Review).
    
    This class sets up an in-memory SQLite database for each test,
    populates it with seed data, and then runs tests against
    the manager methods to ensure all CRUD operations and
    statistical queries function as expected.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up the in-memory database engine once for the entire test class.
        """
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """
        Set up a fresh database session and all managers before each test.
        This ensures each test runs in isolation.
        
        Also, creates seed data (users, genres, movies, reviews)
        to test statistical queries against.
        """
        # Create a new session
        self.session = self.Session()
        
        # Re-create tables for a clean slate
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        # Initialize all managers with the new session
        self.movie_manager = MovieManager(self.session)
        self.genre_manager = GenreManager(self.session)
        self.review_manager = ReviewManager(self.session)
        self.user_manager = UserManager(self.session)

        # --- Seed Data ---
        # Create Users
        self.user1 = self.user_manager.create("Alice", "alice@example.com")
        self.user2 = self.user_manager.create("Bob", "bob@example.com")

        # Create Genres
        self.genre1 = self.genre_manager.create("Sci-Fi")
        self.genre2 = self.genre_manager.create("Action")

        # Create Movies
        self.movie1 = self.movie_manager.create("Inception", 2010) # Action
        self.movie2 = self.movie_manager.create("The Matrix", 1999) # Sci-Fi
        self.movie3 = self.movie_manager.create("Dune", 2021) # Sci-Fi

        # Create Relationships
        self.movie_manager.add_genre(self.movie1.id, self.genre2)
        self.movie_manager.add_genre(self.movie2.id, self.genre1)
        self.movie_manager.add_genre(self.movie3.id, self.genre1)

        # Create Reviews
        # Movie 1 (Inception) - Avg: 8.0
        self.review_manager.create(self.movie1.id, self.user1.id, 9, "Amazing!")
        self.review_manager.create(self.movie1.id, self.user2.id, 7, "Good.")
        
        # Movie 2 (The Matrix) - Avg: 10.0
        self.review_manager.create(self.movie2.id, self.user1.id, 10, "Perfect!")
        
        # Movie 3 (Dune) - Avg: 5.0
        self.review_manager.create(self.movie3.id, self.user2.id, 5, "A bit slow.")
        
        # User 1 (Alice) has 2 reviews (Avg: 9.5)
        # User 2 (Bob) has 2 reviews (Avg: 6.0)

    def tearDown(self):
        """
        Close the session and roll back any changes after each test.
        """
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        """
        Drop all tables after all tests are done.
        """
        Base.metadata.drop_all(cls.engine)

    def test_create_and_get_methods(self):
        """
        Tests the basic create() and get() methods for all managers.
        """
        # Test creating and getting a user
        user = self.user_manager.create("Charlie", "charlie@example.com")
        self.assertIsNotNone(user.id)
        fetched_user = self.user_manager.get(user.id)
        self.assertEqual(fetched_user.name, "Charlie")

        # Test getting a genre by name
        fetched_genre = self.genre_manager.get_genre_by_name("Sci-Fi")
        self.assertEqual(fetched_genre.id, self.genre1.id)

        # Test getting all movies
        all_movies = self.movie_manager.get_all()
        self.assertEqual(len(all_movies), 3)

        # Test getting reviews by user
        user1_reviews = self.review_manager.get_reviews_by_user(self.user1.id)
        self.assertEqual(len(user1_reviews), 2)
        self.assertEqual(user1_reviews[0].rating, 9)
        self.assertEqual(user1_reviews[1].rating, 10)

    def test_relationship_methods(self):
        """
        Tests methods that manage model relationships, like add_genre.
        """
        # Test add_genre and get_movies_by_genre
        movie = self.movie_manager.create("Interstellar", 2014)
        self.movie_manager.add_genre(movie.id, self.genre1) # Add "Sci-Fi"
        
        scifi_movies = self.movie_manager.get_movies_by_genre("Sci-Fi")
        self.assertEqual(len(scifi_movies), 3) # Matrix, Dune, Interstellar
        self.assertIn(movie, scifi_movies)
        self.assertIn(self.movie2, scifi_movies)

    def test_statistical_queries(self):
        """
        Tests the complex statistical and aggregation queries.
        """
        # Test MovieManager: get_top_movies_by_rating
        # Expected: Matrix (10.0), Inception (8.0), Dune (5.0)
        top_movies = self.movie_manager.get_top_movies_by_rating(limit=3)
        self.assertEqual(len(top_movies), 3)
        self.assertEqual(top_movies[0][0].title, "The Matrix") # Movie object
        self.assertEqual(top_movies[0][1], 10.0) # Avg rating
        self.assertEqual(top_movies[1][0].title, "Inception")
        self.assertEqual(top_movies[1][1], 8.0)
        self.assertEqual(top_movies[2][0].title, "Dune")
        self.assertEqual(top_movies[2][1], 5.0)

        # Test UserManager: get_most_active_users
        # Expected: Alice (2 reviews), Bob (2 reviews)
        active_users = self.user_manager.get_most_active_users(limit=2)
        self.assertEqual(len(active_users), 2)
        user_ids = {u[0] for u in active_users}
        review_counts = {u[1] for u in active_users}
        self.assertIn(self.user1.id, user_ids)
        self.assertIn(self.user2.id, user_ids)
        self.assertEqual(review_counts, {2}) # Both have 2 reviews

        # Test ReviewManager: get_average_rating_by_user
        # Expected: Alice (9.5), Bob (6.0)
        avg_ratings = self.review_manager.get_average_rating_by_user()
        self.assertEqual(len(avg_ratings), 2)
        for user_id, avg_rating in avg_ratings:
            if user_id == self.user1.id:
                self.assertEqual(avg_rating, 9.5)
            elif user_id == self.user2.id:
                self.assertEqual(avg_rating, 6.0)

        # Test GenreManager: get_genres_with_most_movies
        # Expected: Sci-Fi (2 movies), Action (1 movie)
        top_genres = self.genre_manager.get_genres_with_most_movies()
        self.assertEqual(len(top_genres), 2)
        self.assertEqual(top_genres[0][0].name, "Sci-Fi") # Genre object
        self.assertEqual(top_genres[0][1], 2) # Movie count
        self.assertEqual(top_genres[1][0].name, "Action")
        self.assertEqual(top_genres[1][1], 1)

    def test_update_and_delete_methods(self):
        """
        Tests the update and delete methods for all managers.
        """
        # MovieManager
        movie = self.movie_manager.create("Temp Movie", 2000)
        updated_movie = self.movie_manager.update(movie.id, {"title": "New Title"})
        self.assertEqual(updated_movie.title, "New Title")
        self.assertTrue(self.movie_manager.delete(movie.id))
        self.assertIsNone(self.movie_manager.get(movie.id))

        # GenreManager
        genre = self.genre_manager.create("Temp Genre")
        updated_genre = self.genre_manager.update(genre.id, "New Genre Name")
        self.assertEqual(updated_genre.name, "New Genre Name")
        self.assertTrue(self.genre_manager.delete(genre.id))
        self.assertIsNone(self.genre_manager.get(genre.id))

        # ReviewManager
        review = self.review_manager.create(self.movie1.id, self.user1.id, 1, "Bad!")
        updated_review = self.review_manager.update(review.id, {"rating": 2})
        self.assertEqual(updated_review.rating, 2)
        self.assertTrue(self.review_manager.delete(review.id))
        self.assertIsNone(self.review_manager.get(review.id))

        # UserManager
        user = self.user_manager.create("Temp User", "temp@example.com")
        updated_user = self.user_manager.update(user.id, {"name": "Robert"})
        self.assertEqual(updated_user.name, "Robert")
        self.assertTrue(self.user_manager.delete(user.id))
        self.assertIsNone(self.user_manager.get(user.id))


if __name__ == "__main__":
    unittest.main()

