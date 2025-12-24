"""
Metrics Calculation for A/B Testing
- CTR (Click-Through Rate)
- CVR (Conversion Rate)
- Sample sizes
- SRM (Sample Ratio Mismatch) check
"""
import csv
import pandas as pd
from pathlib import Path
from collections import defaultdict

LOG_DIR = Path('data/logs')


def read_log_file(event_type):
    """Read log file and return as DataFrame"""
    log_file = LOG_DIR / f'{event_type}s.csv'

    if not log_file.exists():
        return pd.DataFrame()

    return pd.read_csv(log_file)


def calculate_metrics():
    """
    Calculate A/B test metrics from log files

    Returns:
        Dictionary with metrics by variant
    """
    impressions = read_log_file('impression')
    clicks = read_log_file('click')
    conversions = read_log_file('conversion')

    metrics = {
        'control': {
            'impressions': 0,
            'clicks': 0,
            'conversions': 0,
            'ctr': 0.0,
            'cvr': 0.0,
            'users': 0
        },
        'treatment': {
            'impressions': 0,
            'clicks': 0,
            'conversions': 0,
            'ctr': 0.0,
            'cvr': 0.0,
            'users': 0
        }
    }

    # Count impressions by variant
    if not impressions.empty:
        impression_counts = impressions.groupby('variant').size()
        user_counts = impressions.groupby('variant')['user_id'].nunique()

        for variant in ['control', 'treatment']:
            if variant in impression_counts.index:
                metrics[variant]['impressions'] = int(impression_counts[variant])
                metrics[variant]['users'] = int(user_counts[variant])

    # Count clicks by variant
    if not clicks.empty:
        click_counts = clicks.groupby('variant').size()

        for variant in ['control', 'treatment']:
            if variant in click_counts.index:
                metrics[variant]['clicks'] = int(click_counts[variant])

    # Count conversions by variant
    if not conversions.empty:
        conversion_counts = conversions.groupby('variant').size()

        for variant in ['control', 'treatment']:
            if variant in conversion_counts.index:
                metrics[variant]['conversions'] = int(conversion_counts[variant])

    # Calculate rates
    for variant in ['control', 'treatment']:
        # CTR = clicks / impressions
        if metrics[variant]['impressions'] > 0:
            metrics[variant]['ctr'] = metrics[variant]['clicks'] / metrics[variant]['impressions']

        # CVR = conversions / clicks
        if metrics[variant]['clicks'] > 0:
            metrics[variant]['cvr'] = metrics[variant]['conversions'] / metrics[variant]['clicks']

    return metrics


def check_srm(metrics):
    """
    Check for Sample Ratio Mismatch (SRM)

    Expected ratio: 50/50 (due to hash-based assignment)

    Returns:
        Dictionary with SRM check results
    """
    control_users = metrics['control']['users']
    treatment_users = metrics['treatment']['users']
    total_users = control_users + treatment_users

    if total_users == 0:
        return {
            'has_srm': False,
            'message': 'No users yet',
            'control_ratio': 0,
            'treatment_ratio': 0
        }

    control_ratio = control_users / total_users
    treatment_ratio = treatment_users / total_users

    # Flag SRM if ratio deviates more than 5% from expected 50/50
    expected_ratio = 0.5
    tolerance = 0.05

    has_srm = (abs(control_ratio - expected_ratio) > tolerance or
               abs(treatment_ratio - expected_ratio) > tolerance)

    return {
        'has_srm': has_srm,
        'message': 'SRM detected! Check assignment logic.' if has_srm else 'No SRM detected',
        'control_ratio': round(control_ratio, 3),
        'treatment_ratio': round(treatment_ratio, 3),
        'expected_ratio': expected_ratio
    }


def get_recent_events(event_type, n=10):
    """Get recent events for display"""
    log_file = LOG_DIR / f'{event_type}s.csv'

    if not log_file.exists():
        return []

    df = pd.read_csv(log_file)
    return df.tail(n).to_dict('records')


def calculate_lift(metrics):
    """
    Calculate lift: (Treatment - Control) / Control

    Returns:
        Dictionary with lift percentages
    """
    lift = {}

    # CTR lift
    if metrics['control']['ctr'] > 0:
        lift['ctr'] = ((metrics['treatment']['ctr'] - metrics['control']['ctr']) /
                       metrics['control']['ctr']) * 100
    else:
        lift['ctr'] = 0

    # CVR lift
    if metrics['control']['cvr'] > 0:
        lift['cvr'] = ((metrics['treatment']['cvr'] - metrics['control']['cvr']) /
                       metrics['control']['cvr']) * 100
    else:
        lift['cvr'] = 0

    return lift
