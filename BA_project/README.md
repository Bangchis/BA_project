# Netflix-Style Recommender System with A/B Testing

A beautiful Netflix-inspired movie recommendation system with built-in A/B testing framework for Business Analysis course.

![Netflix UI](https://img.shields.io/badge/UI-Netflix--Style-E50914?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?style=for-the-badge)

## Features

- **Netflix-Style UI**: Beautiful dark theme with movie cards, hero banner, and smooth animations
- **A/B Testing Framework**: Hash-based variant assignment with event logging
- **Real-time Analytics Dashboard**: Live CTR/CVR metrics with lift analysis
- **Interactive Demo**: Click movies, rate them, and see metrics update in real-time
- **Two Recommendation Variants**:
  - **Control**: Random movie recommendations
  - **Treatment**: Popularity-based recommendations (by average rating)

## Project Structure

```
BA_project/
├── app.py                          # Main Flask application
├── routes/
│   ├── main.py                    # Home and recommendation routes
│   └── analytics.py               # Dashboard and metrics routes
├── templates/
│   ├── base.html                  # Base template with Netflix navbar
│   ├── index.html                 # Netflix-style home page
│   └── dashboard.html             # A/B testing analytics dashboard
├── static/
│   ├── css/
│   │   └── netflix.css           # Custom Netflix styling
│   └── images/
│       └── posters/               # Movie poster images
├── data/
│   ├── movies.csv                 # Movie metadata (auto-generated)
│   └── logs/                      # Event logs (CSV)
│       ├── impressions.csv        # Recommendation impressions
│       ├── clicks.csv             # Movie clicks
│       └── conversions.csv        # Movie ratings
├── utils/
│   ├── ab_testing.py              # Variant assignment & logging
│   ├── recommender.py             # Recommendation algorithms
│   └── metrics.py                 # CTR/CVR calculations
├── docs/
│   └── AB_Test_Design.md          # Complete A/B test documentation
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory**

```bash
cd "/mnt/c/Users/Admin/Desktop/code python/BA_project"
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
python app.py
```

4. **Open in browser**

```
Home page:      http://localhost:5000
Dashboard:      http://localhost:5000/dashboard
```

## Usage Guide

### 1. Login

- Click the "Login" button in the navbar
- Enter any user ID (e.g., "user123", "alice", "bob")
- You'll be automatically assigned to either Control or Treatment variant

### 2. Browse Recommendations

- After login, you'll see 12 movie recommendations
- Recommendations are based on your assigned variant:
  - **Control**: Random movies
  - **Treatment**: Popular movies (sorted by rating)

### 3. Interact with Movies

- **Click** on any movie card to view details
- **Rate** movies (1-5 stars) to log a conversion event
- All interactions are logged automatically

### 4. View Analytics

- Navigate to the Dashboard: [http://localhost:5000/dashboard](http://localhost:5000/dashboard)
- See real-time metrics:
  - **CTR (Click-Through Rate)**: % of recommendations clicked
  - **CVR (Conversion Rate)**: % of clicks that resulted in ratings
  - **Lift**: Percentage improvement of Treatment over Control
- Dashboard auto-refreshes every 5 seconds

## A/B Test Design

For complete A/B test methodology, see [docs/AB_Test_Design.md](docs/AB_Test_Design.md)

### Quick Overview

| Component | Details |
|-----------|---------|
| **Randomization Unit** | User ID (hash-based assignment) |
| **Variants** | Control (Random) vs Treatment (Popularity-based) |
| **Primary Metrics** | CTR, CVR |
| **Sample Size** | ~1,500 impressions per variant |
| **Guardrails** | Response latency, catalog coverage, novelty |

### Metrics Definitions

**CTR (Click-Through Rate)**
```
CTR = (Number of Clicks / Number of Impressions) × 100%
```

**CVR (Conversion Rate)**
```
CVR = (Number of Ratings / Number of Clicks) × 100%
```

**Lift**
```
Lift = ((Treatment Metric - Control Metric) / Control Metric) × 100%
```

## Demo Workflow

For classroom demonstrations:

1. **Setup**: Instructor runs the Flask app on local machine or shared server

2. **User Participation**:
   - Each student logs in with unique user ID
   - Students browse recommendations and rate movies
   - Aim for at least 20-30 participants

3. **Data Collection**:
   - All events logged to CSV files in `data/logs/`
   - No database required (simple CSV logging)

4. **Analysis**:
   - View real-time dashboard during demo
   - Export final metrics for presentation
   - Generate static HTML report (optional)

## API Endpoints

### Main Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/login` | POST | User login and variant assignment |
| `/recommendations` | GET | Get personalized recommendations |
| `/click` | POST | Log movie click event |
| `/rate` | POST | Log movie rating (conversion) |
| `/logout` | GET | Clear user session |

### Analytics Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard` | GET | Analytics dashboard page |
| `/api/metrics` | GET | Get current A/B test metrics (JSON) |
| `/api/recent-events` | GET | Get recent user events (JSON) |

## Data Files

### Log Files

All event logs are stored in `data/logs/` as CSV files:

**impressions.csv**
```csv
timestamp,user_id,variant,movie_id,rating,metadata
2024-01-01T12:00:00,user123,treatment,"1,2,3,4,5,6,7,8,9,10,11,12",,
```

**clicks.csv**
```csv
timestamp,user_id,variant,movie_id,rating,metadata
2024-01-01T12:01:00,user123,treatment,5,,
```

**conversions.csv**
```csv
timestamp,user_id,variant,movie_id,rating,metadata
2024-01-01T12:02:00,user123,treatment,5,5,
```

## Customization

### Adding More Movies

Edit `utils/recommender.py` and add movies to the sample data:

```python
sample_movies = [
    {'movieId': 21, 'title': 'Your Movie (2024)', 'genres': 'Drama', 'avg_rating': 4.0},
    # Add more...
]
```

### Changing Recommendation Algorithm

Modify the `get_treatment_recommendations()` function in `utils/recommender.py`:

```python
def get_treatment_recommendations(user_id, n=12):
    # Your custom algorithm here
    pass
```

### Adjusting Sample Size

Edit power analysis parameters in `docs/AB_Test_Design.md` and adjust expected sample sizes.

## Troubleshooting

### Port Already in Use

If port 5000 is occupied, change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### CSV Files Not Created

Ensure `data/logs/` directory exists:

```bash
mkdir -p data/logs
```

### No Recommendations Showing

Make sure you're logged in first. Check browser console for errors.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript
- **Data**: Pandas (CSV manipulation)
- **UI Icons**: Font Awesome
- **Fonts**: Google Fonts (Roboto)

## Screenshots

### Home Page (Netflix UI)
- Hero banner with featured content
- Login modal
- Movie recommendation grid with hover effects

### Analytics Dashboard
- Real-time CTR/CVR metrics
- Variant comparison
- Lift analysis
- Sample Ratio Mismatch (SRM) check
- Recent activity feed

## Academic Context

This project demonstrates:

1. **A/B Testing Methodology**: Proper experimental design with control/treatment variants
2. **Business Metrics**: CTR, CVR, and lift calculations
3. **Statistical Rigor**: Power analysis, sample size calculation, guardrail metrics
4. **Product Analytics**: Event logging, funnel analysis, user segmentation
5. **UI/UX Design**: Netflix-inspired user interface with modern web technologies

## Future Enhancements

- [ ] Integrate real MovieLens dataset (25M ratings)
- [ ] Add collaborative filtering (Matrix Factorization)
- [ ] Implement LightGCN for graph-based recommendations
- [ ] Export static HTML reports with charts (Plotly)
- [ ] Add statistical significance testing (z-test, p-values)
- [ ] Implement guardrail metric calculations (latency, diversity)
- [ ] Add user session replay functionality
- [ ] Support multiple concurrent A/B tests

## License

This project is created for educational purposes as part of a Business Analysis course.

## Authors

BA Project Team - 2024

## References

- Netflix UI Design: [Netflix](https://www.netflix.com)
- A/B Testing Best Practices: Kohavi et al. (2017)
- MovieLens Dataset: [GroupLens](https://grouplens.org/datasets/movielens/)

---

**Questions?** Check [docs/AB_Test_Design.md](docs/AB_Test_Design.md) for detailed methodology.

**Need help?** Review troubleshooting section or contact the development team.
