"""
Performance Monitoring Middleware

Tracks API latency for all Flask endpoints.
Adds performance metrics to headers and logs for analysis.

Features:
- Automatic request timing
- X-Response-Time header
- Async logging of performance metrics
- Slow endpoint detection (>100ms threshold)
"""
import time
from flask import request, g
from functools import wraps


def setup_middleware(app):
    """
    Register performance monitoring middleware with Flask app.

    Usage:
        from utils.middleware import setup_middleware
        setup_middleware(app)

    Args:
        app: Flask application instance
    """

    @app.before_request
    def before_request():
        """Record request start time"""
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        """
        Calculate request latency and add to response headers.
        Log performance metrics asynchronously.
        """
        if hasattr(g, 'start_time'):
            # Calculate latency
            latency_ms = (time.time() - g.start_time) * 1000

            # Add latency header to response
            response.headers['X-Response-Time-Ms'] = f'{latency_ms:.2f}'

            # Log performance (async, non-blocking)
            try:
                from utils.logger_service import log_performance_async
                from flask import session

                user_id = session.get('user_id', 'anonymous')
                endpoint = request.endpoint or request.path
                method = request.method
                status_code = response.status_code

                log_performance_async(
                    endpoint=endpoint,
                    latency_ms=latency_ms,
                    method=method,
                    status_code=status_code,
                    user_id=user_id
                )

                # Warn if slow request (>100ms threshold)
                if latency_ms > 100:
                    print(f"[Performance] Slow request: {method} {endpoint} - {latency_ms:.1f}ms")

            except Exception as e:
                # Don't fail request if logging fails
                print(f"[Performance] Failed to log: {e}")

        return response

    print("[Middleware] Performance monitoring enabled")


def measure_latency(f):
    """
    Decorator to measure function latency.

    Usage:
        @measure_latency
        def my_function():
            ...

    Returns function result with latency measurement logged.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time()

        # Execute function
        result = f(*args, **kwargs)

        # Calculate latency
        latency_ms = (time.time() - start) * 1000

        # Log latency
        print(f"[Latency] {f.__name__}: {latency_ms:.2f}ms")

        return result

    return decorated_function


def track_slow_queries(threshold_ms=100):
    """
    Decorator to track slow database queries or API calls.

    Usage:
        @track_slow_queries(threshold_ms=50)
        def expensive_operation():
            ...

    Args:
        threshold_ms: Threshold in milliseconds to log warning
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            latency_ms = (time.time() - start) * 1000

            if latency_ms > threshold_ms:
                print(f"[SlowQuery] {f.__name__} took {latency_ms:.1f}ms (threshold: {threshold_ms}ms)")

            return result
        return decorated_function
    return decorator
