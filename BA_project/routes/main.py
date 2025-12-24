"""
Main Routes: Home page and recommendations
"""
from flask import Blueprint, render_template, request, session, jsonify
from utils.ab_testing import assign_variant, log_impression, log_click, log_conversion
from utils.recommender import get_recommendations, dataset

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page - Netflix-style landing"""
    return render_template('index.html')


@bp.route('/login', methods=['POST'])
def login():
    """Simple user login - just set user_id"""
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID required'}), 400

    # Assign variant based on user_id
    variant = assign_variant(user_id)

    # Store in session
    session['user_id'] = user_id
    session['variant'] = variant
    session['rated_movies'] = {}  # Initialize empty ratings dict

    return jsonify({
        'success': True,
        'user_id': user_id,
        'variant': variant
    })


@bp.route('/recommendations')
def recommendations():
    """Get personalized recommendations based on variant"""
    user_id = session.get('user_id')
    variant = session.get('variant')
    rated_movies = session.get('rated_movies', {})  # Get rated movies from session

    if not user_id or not variant:
        return jsonify({'error': 'Please login first'}), 401

    # Get personalized recommendations (filters out rated movies)
    recs = get_recommendations(user_id, variant, n=12, rated_movies=rated_movies)

    # Log impression
    movie_ids = [movie['movieId'] for movie in recs]
    log_impression(user_id, variant, movie_ids)

    return jsonify({
        'recommendations': recs,
        'variant': variant,
        'personalized': len(rated_movies) > 0,  # Indicate if personalized
        'num_ratings': len(rated_movies)
    })


@bp.route('/click', methods=['POST'])
def click():
    """Log movie click event"""
    data = request.get_json()
    movie_id = data.get('movie_id')

    user_id = session.get('user_id')
    variant = session.get('variant')

    if not user_id or not variant:
        return jsonify({'error': 'Not logged in'}), 401

    if not movie_id:
        return jsonify({'error': 'Movie ID required'}), 400

    # Log click
    log_click(user_id, variant, movie_id)

    # Get movie details
    movie = dataset.get_movie_by_id(movie_id)

    return jsonify({
        'success': True,
        'movie': movie
    })


@bp.route('/rate', methods=['POST'])
def rate():
    """Log movie rating (conversion event)"""
    data = request.get_json()
    movie_id = data.get('movie_id')
    rating = data.get('rating')

    user_id = session.get('user_id')
    variant = session.get('variant')

    if not user_id or not variant:
        return jsonify({'error': 'Not logged in'}), 401

    if not movie_id or not rating:
        return jsonify({'error': 'Movie ID and rating required'}), 400

    # Validate rating
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({'error': 'Rating must be 1-5'}), 400

    # Store rating in session for personalization
    if 'rated_movies' not in session:
        session['rated_movies'] = {}
    session['rated_movies'][str(movie_id)] = rating
    session.modified = True  # Mark session as modified

    # Log conversion
    log_conversion(user_id, variant, movie_id, rating)

    return jsonify({
        'success': True,
        'message': f'Rated movie {movie_id} with {rating} stars',
        'should_refresh': True,  # Signal to frontend to refresh recommendations
        'num_ratings': len(session['rated_movies'])
    })


@bp.route('/logout')
def logout():
    """Clear session"""
    session.clear()
    return jsonify({'success': True})
