# Quick Start Guide

Get the Netflix-style A/B testing app running in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
cd "/mnt/c/Users/Admin/Desktop/code python/BA_project"
pip install -r requirements.txt
```

## Step 2: Run the App (30 seconds)

```bash
python3 app.py
```

You should see:
```
============================================================
  Netflix-Style Recommender System with A/B Testing
============================================================

  📍 Running on: http://localhost:5000
  📊 Dashboard: http://localhost:5000/dashboard
```

## Step 3: Open in Browser

Open your browser and go to:
- **Home**: http://localhost:5000
- **Dashboard**: http://localhost:5000/dashboard

## Step 4: Demo Workflow (3 minutes)

### A. Login
1. Click "Login" button in navbar
2. Enter user ID (e.g., "alice")
3. You'll see your assigned variant (Control or Treatment)

### B. Browse Recommendations
1. After login, you'll see 12 movie recommendations
2. **Control users** see Matrix Factorization recommendations
3. **Treatment users** see LightGCN recommendations

### C. Interact with Movies
1. Click any movie card → Opens detail modal
2. Rate the movie (1-5 stars) → Logs conversion
3. Repeat with multiple movies

### D. View Analytics
1. Open dashboard in new tab: http://localhost:5000/dashboard
2. See real-time metrics update:
   - CTR (Click-Through Rate)
   - CVR (Conversion Rate)
   - Lift (Treatment vs Control)
3. Dashboard auto-refreshes every 5 seconds

## Step 5: Demo with Multiple Users

To simulate A/B test properly:

1. **Logout** and login with different user IDs:
   - user1, user2, user3, etc.
   - alice, bob, charlie, etc.

2. **Vary behavior**:
   - Some users click many movies
   - Some users rate movies
   - Some users just browse

3. **Check variant distribution**:
   - Dashboard shows ~50% Control, ~50% Treatment
   - If distribution is skewed, check SRM alert

## Sample User IDs

Hash-based assignment ensures:
- **Control**: user1, user3, user5, user7, alice, charlie, eve
- **Treatment**: user2, user4, user6, user8, bob, david, frank

## Expected Metrics (Hypothetical)

After 20-30 interactions:

| Variant | CTR | CVR |
|---------|-----|-----|
| Control (Random) | ~8-12% | ~25-35% |
| Treatment (Popular) | ~15-20% | ~30-40% |

**Lift**: +30-50% improvement in CTR for Treatment

## Troubleshooting

### "Port 5000 already in use"
Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### "No recommendations showing"
1. Make sure you clicked "Login" first
2. Check browser console for errors (F12)

### "Dashboard shows 0 metrics"
1. Login and browse recommendations first
2. Click movies and rate them
3. Refresh dashboard

## Next Steps

1. Read full A/B test design: [docs/AB_Test_Design.md](docs/AB_Test_Design.md)
2. Customize recommendations: Edit `utils/recommender.py`
3. Add more movies: Modify sample data in `utils/recommender.py`
4. Export results: Check log files in `data/logs/`

## Pro Tips

- Use **Incognito/Private windows** to simulate different users quickly
- **Don't reload page** while logged in (session will reset)
- **Logout properly** before switching users
- **Monitor dashboard** in separate tab while interacting

---

**Ready to impress your instructor?** Follow this guide and you'll have a fully functional A/B test demo in minutes!
