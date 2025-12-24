# A/B Test Design: Movie Recommendation System

## Executive Summary

This document outlines the A/B test design for evaluating two recommendation algorithms in a Netflix-style movie recommendation system. The test compares a **Control variant** (random recommendations) against a **Treatment variant** (popularity-based recommendations) to determine which approach yields higher user engagement.

---

## 1. Hypothesis

**Null Hypothesis (H0):** Popularity-based recommendations do not improve user engagement metrics (CTR and CVR) compared to random recommendations.

**Alternative Hypothesis (H1):** Popularity-based recommendations significantly increase user engagement metrics (CTR and CVR) compared to random recommendations.

---

## 2. Test Design

### 2.1 Randomization Unit

**Unit of randomization:** Individual users (identified by `user_id`)

**Assignment method:** Hash-based deterministic assignment
- User ID is hashed using MD5
- Hash value modulo 2 determines variant assignment
- Ensures consistent variant assignment for repeat visits
- Expected 50/50 split between Control and Treatment

### 2.2 Variants

| Variant | Description | Algorithm |
|---------|-------------|-----------|
| **Control** | Baseline recommendations | Random selection of 12 movies from catalog |
| **Treatment** | Popularity-based recommendations | Top 12 movies ranked by average user rating |

### 2.3 Traffic Allocation

- **Control:** 50% of users
- **Treatment:** 50% of users

---

## 3. Metrics

### 3.1 Primary Metrics

#### Click-Through Rate (CTR)
- **Definition:** Percentage of recommendations that receive clicks
- **Formula:** `CTR = (Number of Clicks / Number of Impressions) × 100%`
- **Success criterion:** Treatment CTR > Control CTR with statistical significance

#### Conversion Rate (CVR)
- **Definition:** Percentage of clicks that result in ratings (conversions)
- **Formula:** `CVR = (Number of Ratings / Number of Clicks) × 100%`
- **Success criterion:** Treatment CVR > Control CVR with statistical significance

### 3.2 Secondary Metrics

- **User engagement:** Number of movies rated per user
- **Session duration:** Time spent browsing recommendations
- **Rating distribution:** Distribution of 1-5 star ratings

### 3.3 Guardrail Metrics

Metrics to ensure the Treatment variant doesn't degrade user experience:

1. **Response Latency:** Recommendation API response time
   - **Threshold:** Must not increase by more than 100ms
   - **Rationale:** Slow recommendations hurt user experience

2. **Catalog Coverage:** Percentage of unique movies recommended
   - **Threshold:** Must not decrease by more than 20%
   - **Rationale:** Over-recommending popular movies reduces diversity

3. **Novelty Score:** Percentage of recommendations for less-popular items
   - **Threshold:** Must maintain at least 30% novelty
   - **Rationale:** Users should discover new movies, not just blockbusters

---

## 4. Power Analysis & Sample Size

### 4.1 Assumptions

- **Baseline CTR (Control):** 10% (conservative estimate)
- **Minimum Detectable Effect (MDE):** 20% relative improvement
  - Target Treatment CTR: 12% (10% × 1.2)
- **Statistical significance level (α):** 0.05 (5% Type I error rate)
- **Statistical power (1 - β):** 0.80 (80% power to detect true effect)

### 4.2 Sample Size Calculation

Using standard A/B test sample size formula for proportions:

```
n = 2 × [(Z_α/2 + Z_β)^2 × p(1-p)] / (MDE^2)

Where:
- Z_α/2 = 1.96 (for α = 0.05, two-tailed)
- Z_β = 0.84 (for β = 0.20, i.e., 80% power)
- p = 0.10 (baseline CTR)
- MDE = 0.02 (absolute effect size: 12% - 10%)
```

**Required sample size per variant:**
- Approximately **1,500 impressions per variant**
- Total: **3,000 impressions** (across both variants)

**Estimated runtime:**
- If 50 users participate with 2 sessions each
- Each session generates 12 impressions
- Total: 50 × 2 × 12 = **1,200 impressions**
- Need approximately **3-4 demo sessions** to reach sample size

### 4.3 MDE Illustration

| Metric | Control (Baseline) | MDE (Absolute) | Treatment (Target) | Relative Lift |
|--------|-------------------|----------------|-------------------|---------------|
| CTR | 10% | +2% | 12% | +20% |
| CVR | 30% | +6% | 36% | +20% |

---

## 5. Sanity Checks

### 5.1 Sample Ratio Mismatch (SRM)

**Check:** Verify that variant assignment is approximately 50/50

**Formula:**
```
Expected ratio: 50% Control, 50% Treatment
Tolerance: ±5%
```

**Action if SRM detected:**
- Investigate hash-based assignment logic
- Check for logging errors
- Review user filtering criteria

### 5.2 Data Quality Checks

1. **Logging completeness:** Verify all events (impression, click, conversion) are logged
2. **Timestamp accuracy:** Ensure events are logged in correct chronological order
3. **User ID consistency:** Check for duplicate or missing user IDs

---

## 6. Statistical Testing

### 6.1 Hypothesis Test for CTR

**Test:** Two-proportion z-test

**Null hypothesis:** `CTR_treatment - CTR_control = 0`

**Formula:**
```
z = (p_treatment - p_control) / SE

Where:
SE = sqrt[p_pooled × (1 - p_pooled) × (1/n_control + 1/n_treatment)]
p_pooled = (x_control + x_treatment) / (n_control + n_treatment)
```

**Decision rule:**
- If p-value < 0.05: Reject H0 (statistically significant difference)
- If p-value ≥ 0.05: Fail to reject H0 (no significant difference)

### 6.2 Confidence Intervals

Report 95% confidence intervals for lift:

```
Lift = (Treatment - Control) / Control × 100%

95% CI = Lift ± 1.96 × SE_lift
```

---

## 7. Instrumentation & Logging

### 7.1 Event Types

| Event | Trigger | Data Logged |
|-------|---------|-------------|
| **Impression** | Recommendations displayed to user | `timestamp, user_id, variant, movie_ids` |
| **Click** | User clicks on movie card | `timestamp, user_id, variant, movie_id` |
| **Conversion** | User rates movie (1-5 stars) | `timestamp, user_id, variant, movie_id, rating` |

### 7.2 Log Files

All events are logged to CSV files in `data/logs/`:
- `impressions.csv`
- `clicks.csv`
- `conversions.csv`

---

## 8. Analysis Plan

### 8.1 Data Collection Period

- **Minimum duration:** Until sample size requirements are met
- **Recommended duration:** 1-2 weeks for classroom demo
- **Data cutoff:** Analyze data at end of collection period (no peeking)

### 8.2 Analysis Steps

1. **Data validation:** Run sanity checks (SRM, data quality)
2. **Descriptive statistics:** Calculate CTR and CVR for both variants
3. **Hypothesis testing:** Run two-proportion z-tests for primary metrics
4. **Effect size estimation:** Calculate lift and confidence intervals
5. **Guardrail checks:** Verify latency, coverage, and novelty metrics
6. **Interpretation:** Make recommendation to launch or iterate

### 8.3 Decision Framework

| Outcome | CTR Result | CVR Result | Guardrails | Decision |
|---------|-----------|-----------|------------|----------|
| **Win** | Significant improvement | Significant improvement | Pass | Launch Treatment |
| **Partial Win** | Significant improvement | No change | Pass | Consider launch |
| **No Effect** | No change | No change | Pass | Keep Control |
| **Loss** | Significant degradation | Any result | Fail | Keep Control |

---

## 9. Limitations & Caveats

### 9.1 Synthetic Data

This A/B test uses **demo interactions** rather than real user traffic:
- Users are students/instructors manually clicking and rating
- Sample sizes are small compared to production systems
- Behavior may not reflect real-world usage patterns

**Implication:** Results demonstrate A/B testing methodology but may not generalize to production.

### 9.2 Simplified Algorithms

- **Control:** Random recommendations (not a realistic baseline)
- **Treatment:** Simple popularity-based (not personalized)

**Implication:** Real-world systems would use more sophisticated algorithms (collaborative filtering, deep learning).

### 9.3 Selection Bias

- Demo users may have different preferences than general population
- Users know they're in a test, which may influence behavior (Hawthorne effect)

---

## 10. Next Steps

### 10.1 After Test Completion

1. Generate static HTML report with:
   - Metrics visualization (CTR/CVR charts)
   - Statistical test results (p-values, confidence intervals)
   - Guardrail metrics
   - Recommendations

2. Present findings to stakeholders

3. Decide on next iteration:
   - If Treatment wins: Consider more sophisticated algorithms (collaborative filtering, LightGCN)
   - If no effect: Investigate why popularity-based failed
   - Run follow-up tests with different algorithms

### 10.2 Future Experiments

- **Personalization:** Test collaborative filtering vs. popularity-based
- **Diversity:** Test diversity-optimized recommendations vs. pure popularity
- **Cold start:** Test strategies for new users with no history
- **Multi-armed bandit:** Dynamic traffic allocation based on real-time performance

---

## References

1. Kohavi, R., & Longbotham, R. (2017). *Online Controlled Experiments and A/B Testing*. Encyclopedia of Machine Learning and Data Mining.

2. Deng, A., Xu, Y., Kohavi, R., & Walker, T. (2013). *Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data*. WSDM 2013.

3. Fabijan, A., et al. (2019). *Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners*. KDD 2019.

---

**Document version:** 1.0
**Last updated:** 2024
**Author:** BA Project Team
