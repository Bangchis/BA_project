"""
Mock Recommender Systems
- Control: Matrix Factorization
- Treatment: LightGCN
"""
import random
import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')


class MovieDataset:
    """Simple movie dataset handler"""

    def __init__(self):
        self.movies = None
        self.load_data()

    def load_data(self):
        """Load movie metadata"""
        movies_file = DATA_DIR / 'movies.csv'

        if movies_file.exists():
            self.movies = pd.read_csv(movies_file)
        else:
            # Create sample data if file doesn't exist
            self.movies = self._create_sample_data()

    def _create_sample_data(self):
        """Create sample movie data for demo with real TMDB poster URLs"""
        sample_movies = [
            {
                'movieId': 1,
                'title': 'The Shawshank Redemption (1994)',
                'genres': 'Drama',
                'avg_rating': 4.5,
                'poster_url': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
            },
            {
                'movieId': 2,
                'title': 'The Godfather (1972)',
                'genres': 'Crime|Drama',
                'avg_rating': 4.4,
                'poster_url': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
            },
            {
                'movieId': 3,
                'title': 'The Dark Knight (2008)',
                'genres': 'Action|Crime|Drama',
                'avg_rating': 4.3,
                'poster_url': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'
            },
            {
                'movieId': 4,
                'title': 'Pulp Fiction (1994)',
                'genres': 'Crime|Drama|Thriller',
                'avg_rating': 4.3,
                'poster_url': 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg'
            },
            {
                'movieId': 5,
                'title': 'Forrest Gump (1994)',
                'genres': 'Comedy|Drama|Romance',
                'avg_rating': 4.2,
                'poster_url': 'https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg'
            },
            {
                'movieId': 6,
                'title': 'Inception (2010)',
                'genres': 'Action|Mystery|Sci-Fi',
                'avg_rating': 4.2,
                'poster_url': 'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg'
            },
            {
                'movieId': 7,
                'title': 'The Matrix (1999)',
                'genres': 'Action|Sci-Fi|Thriller',
                'avg_rating': 4.1,
                'poster_url': 'https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg'
            },
            {
                'movieId': 8,
                'title': 'Interstellar (2014)',
                'genres': 'Adventure|Drama|Sci-Fi',
                'avg_rating': 4.1,
                'poster_url': 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg'
            },
            {
                'movieId': 9,
                'title': 'Fight Club (1999)',
                'genres': 'Drama|Thriller',
                'avg_rating': 4.0,
                'poster_url': 'https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg'
            },
            {
                'movieId': 10,
                'title': 'The Lord of the Rings (2001)',
                'genres': 'Adventure|Fantasy',
                'avg_rating': 4.0,
                'poster_url': 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg'
            },
            {
                'movieId': 11,
                'title': 'Parasite (2019)',
                'genres': 'Comedy|Drama|Thriller',
                'avg_rating': 3.9,
                'poster_url': 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg'
            },
            {
                'movieId': 12,
                'title': 'Avengers: Endgame (2019)',
                'genres': 'Action|Adventure|Sci-Fi',
                'avg_rating': 3.9,
                'poster_url': 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg'
            },
            {
                'movieId': 13,
                'title': 'Joker (2019)',
                'genres': 'Crime|Drama|Thriller',
                'avg_rating': 3.8,
                'poster_url': 'https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg'
            },
            {
                'movieId': 14,
                'title': 'Spider-Man: No Way Home (2021)',
                'genres': 'Action|Adventure|Sci-Fi',
                'avg_rating': 3.8,
                'poster_url': 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg'
            },
            {
                'movieId': 15,
                'title': 'Dune (2021)',
                'genres': 'Action|Adventure|Drama|Sci-Fi',
                'avg_rating': 3.7,
                'poster_url': 'https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg'
            },
            {
                'movieId': 16,
                'title': 'Everything Everywhere All at Once (2022)',
                'genres': 'Action|Comedy|Sci-Fi',
                'avg_rating': 3.9,
                'poster_url': 'https://image.tmdb.org/t/p/w500/w3LxiVYdWWRvEVdn5RYq6jIqkb1.jpg'
            },
            {
                'movieId': 17,
                'title': 'The Grand Budapest Hotel (2014)',
                'genres': 'Comedy|Drama',
                'avg_rating': 3.7,
                'poster_url': 'https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg'
            },
            {
                'movieId': 18,
                'title': 'Whiplash (2014)',
                'genres': 'Drama|Music',
                'avg_rating': 3.8,
                'poster_url': 'https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg'
            },
            {
                'movieId': 19,
                'title': 'Her (2013)',
                'genres': 'Drama|Romance|Sci-Fi',
                'avg_rating': 3.6,
                'poster_url': 'https://image.tmdb.org/t/p/w500/eCOtqtfvn7mxGl6nfmq4b1exJRc.jpg'
            },
            {
                'movieId': 20,
                'title': 'La La Land (2016)',
                'genres': 'Comedy|Drama|Musical|Romance',
                'avg_rating': 3.6,
                'poster_url': 'https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg'
            },
        ]
        return pd.DataFrame(sample_movies)

    def get_all_movies(self):
        """Return all movies"""
        return self.movies.to_dict('records')

    def get_movie_by_id(self, movie_id):
        """Get movie details by ID"""
        movie = self.movies[self.movies['movieId'] == int(movie_id)]
        if not movie.empty:
            return movie.iloc[0].to_dict()
        return None


# Global dataset instance
dataset = MovieDataset()


def extract_genre_preferences(rated_movies_dict):
    """
    Extract genre preferences from user's rated movies.

    Args:
        rated_movies_dict: {movie_id: rating} dictionary

    Returns:
        Dictionary of {genre: preference_score}
    """
    genre_scores = {}

    if not rated_movies_dict:
        return genre_scores

    for movie_id, rating in rated_movies_dict.items():
        movie = dataset.get_movie_by_id(int(movie_id))
        if not movie:
            continue

        genres = movie.get('genres', '').split('|')

        # Weight by rating (5★ = 1.0, 1★ = 0.2)
        weight = float(rating) / 5.0

        for genre in genres:
            genre = genre.strip()
            if genre:
                genre_scores[genre] = genre_scores.get(genre, 0) + weight

    return genre_scores


def score_movie_by_preference(movie, genre_preferences, variant='control'):
    """
    Score a movie based on genre preferences and variant type.

    Args:
        movie: Movie dictionary
        genre_preferences: Genre preference scores from extract_genre_preferences()
        variant: 'control' or 'treatment'

    Returns:
        Float score (0.0 to 1.0)
    """
    if not genre_preferences:
        # No preferences yet - use default scoring
        if variant == 'treatment':
            return movie.get('avg_rating', 3.0) / 5.0
        else:
            return random.random()

    # Calculate genre match score
    genre_match_score = 0
    movie_genres = movie.get('genres', '').split('|')

    for genre in movie_genres:
        genre = genre.strip()
        genre_match_score += genre_preferences.get(genre, 0)

    # Normalize (max score ~5.0 if all genres match highly)
    genre_match_score = min(genre_match_score / 5.0, 1.0)

    # Combine with popularity
    popularity_score = movie.get('avg_rating', 3.0) / 5.0

    if variant == 'treatment':
        # LightGCN: More weight on genre matching (60%) + popularity (40%)
        return (genre_match_score * 0.6) + (popularity_score * 0.4)
    else:
        # Matrix Factorization: Less weight on genre matching (30%) + randomness (70%)
        return (genre_match_score * 0.3) + (random.random() * 0.7)


def get_control_recommendations(user_id, n=12, rated_movies=None):
    """
    Control: Matrix Factorization (with pseudo-personalization if user has ratings)

    Args:
        user_id: User identifier
        n: Number of recommendations
        rated_movies: Dictionary of {movie_id: rating} for personalization

    Returns:
        List of movie dictionaries
    """
    all_movies = dataset.get_all_movies()

    # Filter out already-rated movies
    if rated_movies:
        rated_ids = set(int(mid) for mid in rated_movies.keys())
        candidates = [m for m in all_movies if m['movieId'] not in rated_ids]

        # Extract genre preferences
        genre_prefs = extract_genre_preferences(rated_movies)

        # Score movies with slight genre bias
        for movie in candidates:
            movie['_score'] = score_movie_by_preference(movie, genre_prefs, variant='control')

        # Sort by score and return top N
        candidates.sort(key=lambda m: m['_score'], reverse=True)
        result = candidates[:n]

        # Clean up temporary score field
        for m in result:
            m.pop('_score', None)

        return result
    else:
        # No ratings yet - pure random
        return random.sample(all_movies, min(n, len(all_movies)))


def get_treatment_recommendations(user_id, n=12, rated_movies=None):
    """
    Treatment: LightGCN (with genre personalization)

    Args:
        user_id: User identifier
        n: Number of recommendations
        rated_movies: Dictionary of {movie_id: rating} for personalization

    Returns:
        List of movie dictionaries
    """
    all_movies = dataset.get_all_movies()

    # Filter out already-rated movies
    if rated_movies:
        rated_ids = set(int(mid) for mid in rated_movies.keys())
        candidates = [m for m in all_movies if m['movieId'] not in rated_ids]

        # Extract genre preferences
        genre_prefs = extract_genre_preferences(rated_movies)

        # Score movies with genre + popularity
        for movie in candidates:
            movie['_score'] = score_movie_by_preference(movie, genre_prefs, variant='treatment')

        # Sort by score and return top N
        candidates.sort(key=lambda m: m['_score'], reverse=True)
        result = candidates[:n]

        # Clean up temporary score field
        for m in result:
            m.pop('_score', None)

        return result
    else:
        # No ratings yet - pure popularity
        movies = dataset.movies.copy()
        if 'avg_rating' in movies.columns:
            movies = movies.sort_values('avg_rating', ascending=False)
        return movies.head(n).to_dict('records')


def get_recommendations(user_id, variant, n=12, rated_movies=None):
    """
    Get recommendations based on assigned variant (with personalization)

    Args:
        user_id: User identifier
        variant: 'control' or 'treatment'
        n: Number of recommendations
        rated_movies: Dictionary of {movie_id: rating} for personalization

    Returns:
        List of movie dictionaries
    """
    if variant == 'treatment':
        return get_treatment_recommendations(user_id, n, rated_movies)
    else:
        return get_control_recommendations(user_id, n, rated_movies)
