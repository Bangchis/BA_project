"""
Analytics Routes: Dashboard and metrics
"""
from flask import Blueprint, render_template, jsonify, request, session
from utils.metrics import calculate_metrics, check_srm, get_recent_events, calculate_lift
from utils.logger_service import log_engagement_async

bp = Blueprint('analytics', __name__)


@bp.route('/dashboard')
def dashboard():
    """A/B Testing Dashboard"""
    return render_template('dashboard.html')


@bp.route('/api/metrics')
def get_metrics():
    """API endpoint to get current A/B test metrics"""
    metrics = calculate_metrics()
    srm = check_srm(metrics)
    lift = calculate_lift(metrics)

    return jsonify({
        'metrics': metrics,
        'srm': srm,
        'lift': lift
    })


@bp.route('/api/recent-events')
def recent_events():
    """Get recent events for activity feed"""
    impressions = get_recent_events('impression', n=5)
    clicks = get_recent_events('click', n=5)
    conversions = get_recent_events('conversion', n=5)

    return jsonify({
        'impressions': impressions,
        'clicks': clicks,
        'conversions': conversions
    })


@bp.route('/api/engagement', methods=['POST'])
def log_engagement():
    """
    Log user engagement event (dwell time tracking).

    Tracks how long users spend viewing movie modals - a key engagement metric.
    Uses async logging for zero-latency performance.

    Request body:
        {
            "movie_id": 123,
            "dwell_time_ms": 5000,
            "action": "close" | "rate" | "background_click"
        }
    """
    data = request.get_json()
    movie_id = data.get('movie_id')
    dwell_time_ms = data.get('dwell_time_ms')
    action = data.get('action', 'view')

    user_id = session.get('user_id')
    variant = session.get('variant')

    # Validation
    if not user_id or not variant:
        return jsonify({'error': 'Not logged in'}), 401

    if not movie_id or dwell_time_ms is None:
        return jsonify({'error': 'movie_id and dwell_time_ms required'}), 400

    # Log engagement asynchronously (non-blocking)
    log_engagement_async(user_id, variant, movie_id, dwell_time_ms, action)

    return jsonify({
        'success': True,
        'dwell_time_ms': dwell_time_ms,
        'action': action
    })
