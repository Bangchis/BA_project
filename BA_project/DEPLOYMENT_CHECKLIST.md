# Deployment Checklist

Use this checklist before presenting your BA project.

## Pre-Presentation Setup (1 hour before)

### 1. Environment Setup
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Project folder accessible
- [ ] Terminal/command prompt ready

### 2. Test Run
- [ ] Run `python3 app.py` successfully
- [ ] App starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can access http://localhost:5000/dashboard
- [ ] No firewall blocking port 5000

### 3. Browser Setup
- [ ] Modern browser ready (Chrome, Firefox, Safari, Edge)
- [ ] Disable ad blockers (may interfere with JS)
- [ ] Clear browser cache
- [ ] Test in incognito/private mode
- [ ] Have multiple browser windows ready (for multi-user demo)

### 4. Network Setup (if sharing with class)
- [ ] Find your local IP address (`ipconfig` or `ifconfig`)
- [ ] Update app.py to use `host='0.0.0.0'` (already done)
- [ ] Share URL with classmates: `http://<your-ip>:5000`
- [ ] Test connection from another device

### 5. Presentation Materials
- [ ] README.md reviewed
- [ ] QUICKSTART.md ready for quick reference
- [ ] AB_Test_Design.md printed or open in tab
- [ ] PROJECT_SUMMARY.md for overview
- [ ] Screenshots taken (optional backup)

---

## During Presentation Checklist

### Part 1: Introduction (2 minutes)
- [ ] Explain project goal: Netflix-style recommender with A/B testing
- [ ] Show project structure briefly
- [ ] Mention technologies used (Flask, Tailwind CSS, etc.)

### Part 2: Live Demo - UI (5 minutes)
- [ ] Open home page: http://localhost:5000
- [ ] Show Netflix-style hero banner
- [ ] Demonstrate login modal
- [ ] Login as "alice"
- [ ] Show assigned variant badge
- [ ] Browse 12 recommendations
- [ ] Click a movie → show modal
- [ ] Rate a movie (5 stars)
- [ ] Repeat with 2-3 more movies

### Part 3: Live Demo - A/B Testing (5 minutes)
- [ ] Logout and login as "bob"
- [ ] Show different variant assignment
- [ ] Explain Control vs Treatment difference
- [ ] Click and rate more movies
- [ ] Open dashboard in new tab: http://localhost:5000/dashboard
- [ ] Show real-time metrics updating
- [ ] Point out CTR, CVR, Lift calculations
- [ ] Show variant distribution (should be ~50/50)

### Part 4: A/B Test Design (3 minutes)
- [ ] Open docs/AB_Test_Design.md
- [ ] Explain hypothesis
- [ ] Show metrics definitions (CTR, CVR)
- [ ] Mention power analysis and sample size
- [ ] Discuss guardrail metrics
- [ ] Show sanity checks (SRM)

### Part 5: Results & Insights (2 minutes)
- [ ] Generate static report: `python3 reports/generate_report.py`
- [ ] Open generated HTML report in browser
- [ ] Show metrics comparison table
- [ ] Discuss lift (Treatment vs Control)
- [ ] Present recommendations (launch/iterate/keep)

### Part 6: Technical Deep Dive (3 minutes) - Optional
- [ ] Show code structure (app.py, routes/, utils/)
- [ ] Explain hash-based variant assignment
- [ ] Show event logging (CSV files in data/logs/)
- [ ] Demonstrate metrics calculation logic
- [ ] Mention scalability considerations

### Part 7: Q&A (5 minutes)
Prepare answers for common questions:
- [ ] "Why hash-based assignment?" → Deterministic, no database needed
- [ ] "How do you ensure 50/50 split?" → Hash modulo 2
- [ ] "What if we had real users?" → Scale to database, add auth
- [ ] "Can you test more variants?" → Yes, extend to A/B/C/D tests
- [ ] "How to improve recommendations?" → Collaborative filtering, deep learning

---

## Post-Demo Checklist

### 1. Save Results
- [ ] Copy log files from data/logs/ to backup
- [ ] Save generated HTML report
- [ ] Take screenshots of dashboard
- [ ] Export metrics to CSV (if needed)

### 2. Cleanup (Optional)
- [ ] Clear log files for next demo: `rm data/logs/*.csv`
- [ ] Reset to clean state

### 3. Share Materials
- [ ] Push to GitHub (optional)
- [ ] Share report with instructor
- [ ] Provide documentation links

---

## Emergency Troubleshooting

### If app crashes during demo:

**Problem: Port 5000 in use**
```bash
# Quick fix: Use different port
# Edit app.py line: app.run(port=5001)
python3 app.py
```

**Problem: Module not found**
```bash
pip install -r requirements.txt
```

**Problem: Recommendations not showing**
- Make sure you're logged in
- Check browser console (F12) for errors
- Reload page

**Problem: Dashboard shows 0 metrics**
- Interact with recommendations first (click, rate)
- Refresh dashboard manually
- Check that log files exist in data/logs/

**Problem: Browser can't connect**
- Verify app is running (check terminal)
- Try http://127.0.0.1:5000 instead of localhost
- Disable VPN/firewall

---

## Presentation Tips

### Do's ✅
- ✅ Practice demo flow beforehand (run through 2-3 times)
- ✅ Have backup screenshots in case of technical issues
- ✅ Explain "why" not just "what" (business impact)
- ✅ Connect to course concepts (A/B testing, metrics, etc.)
- ✅ Be ready to show code if asked
- ✅ Mention limitations and future work

### Don'ts ❌
- ❌ Don't apologize for "simple" implementation
- ❌ Don't spend too long on tech stack details
- ❌ Don't skip the A/B test design explanation
- ❌ Don't forget to show the dashboard
- ❌ Don't ignore questions about methodology

---

## Audience Participation (Optional)

If instructor allows classmates to participate:

### Setup
1. Find your IP address:
   ```bash
   # Windows
   ipconfig

   # Mac/Linux
   ifconfig
   ```

2. Share URL: `http://<your-ip>:5000`

3. Ask classmates to:
   - Login with unique user IDs
   - Browse recommendations
   - Click and rate movies

### Expected Results
- With 20-30 participants:
  - 240-360 impressions
  - 30-60 clicks
  - 10-25 conversions
- Variant split: ~50% Control, 50% Treatment
- CTR: 10-20%
- CVR: 25-40%

### Monitor Progress
- Watch dashboard update in real-time
- Point out metrics increasing
- Show SRM check staying green
- Generate final report after participation

---

## Grading Rubric Alignment

Make sure to cover these points:

| Criteria | How This Project Addresses It |
|----------|------------------------------|
| **A/B Test Design** | Complete 20-page methodology document |
| **Implementation** | Fully functional web app with UI |
| **Metrics** | CTR, CVR, Lift calculations |
| **Logging** | CSV-based event tracking |
| **Dashboard** | Real-time analytics with auto-refresh |
| **Documentation** | README, Quick Start, Design Doc |
| **Presentation** | Live demo + static report |
| **Code Quality** | Modular, clean, well-commented |

---

## Time Management

**Total presentation time: 20-25 minutes**

| Section | Time | Priority |
|---------|------|----------|
| Introduction | 2 min | Required |
| UI Demo | 5 min | Required |
| A/B Testing Demo | 5 min | Required |
| Design Explanation | 3 min | Required |
| Results Report | 2 min | Required |
| Technical Details | 3 min | Optional |
| Q&A | 5 min | Required |

**Practice multiple times to stay within time limit!**

---

## Final Checks (5 minutes before)

- [ ] App is running (terminal shows Flask server)
- [ ] Browser tabs open (home + dashboard)
- [ ] Documentation ready (README, Design Doc)
- [ ] Backup plan ready (screenshots, slides)
- [ ] Confident and ready to explain methodology
- [ ] Water/coffee ready 😊

---

**You've got this! The project is complete and demo-ready.** 🎉

Remember: This is A/A+ level work. Present confidently!
