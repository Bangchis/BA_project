"""
BA Project: Netflix-style Recommender System with A/B Testing
Main Flask Application (Enhanced with Performance Monitoring & Async Logging)
"""
from flask import Flask, render_template, session, request, jsonify
import os
from datetime import datetime
import secrets

# Import routes
from routes import main, analytics

# Import performance middleware
from utils.middleware import setup_middleware

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Register blueprints
app.register_blueprint(main.bp)
app.register_blueprint(analytics.bp)

# Setup performance monitoring middleware
# Tracks API latency and adds X-Response-Time-Ms header
setup_middleware(app)

# Create necessary directories
os.makedirs('data/logs', exist_ok=True)
os.makedirs('static/images/posters', exist_ok=True)

@app.before_request
def setup_session():
    """Initialize session variables"""
    if 'user_id' not in session:
        session['user_id'] = None
    if 'variant' not in session:
        session['variant'] = None

@app.context_processor
def inject_now():
    """Inject current datetime into all templates"""
    return {'now': datetime.now()}

if __name__ == '__main__':
    print("=" * 60)
    print("  Netflix-Style Recommender System with A/B Testing")
    print("  (Enhanced: Async Logging + Performance Monitoring)")
    print("=" * 60)
    print("\n  📍 Running on: http://localhost:5000")
    print("  📊 Dashboard: http://localhost:5000/dashboard")
    print("\n  ⚡ Features:")
    print("    - Zero-latency async logging (<5ms)")
    print("    - API performance tracking")
    print("    - Consistent hashing (sticky sessions)")
    print("\n" + "=" * 60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
