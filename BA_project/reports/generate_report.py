"""
Generate Static HTML Report for A/B Test Results
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.metrics import calculate_metrics, check_srm, calculate_lift
from datetime import datetime

def generate_html_report():
    """Generate a static HTML report with A/B test results"""

    metrics = calculate_metrics()
    srm = check_srm(metrics)
    lift = calculate_lift(metrics)

    # Calculate totals
    total_users = metrics['control']['users'] + metrics['treatment']['users']
    total_impressions = metrics['control']['impressions'] + metrics['treatment']['impressions']
    total_clicks = metrics['control']['clicks'] + metrics['treatment']['clicks']
    total_conversions = metrics['control']['conversions'] + metrics['treatment']['conversions']

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A/B Test Report - Netflix Recommender</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            background: linear-gradient(135deg, #E50914 0%, #B20710 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            border-radius: 12px;
            margin-bottom: 2rem;
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .section {{
            background: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        h2 {{
            color: #E50914;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #E50914;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 1.5rem 0;
        }}

        .metric-card {{
            background: #f9f9f9;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #E50914;
        }}

        .metric-label {{
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 0.5rem;
        }}

        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #333;
        }}

        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}

        .comparison-table th,
        .comparison-table td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        .comparison-table th {{
            background: #f5f5f5;
            font-weight: 600;
        }}

        .control-badge {{
            background: #3b82f6;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }}

        .treatment-badge {{
            background: #10b981;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }}

        .lift-positive {{
            color: #10b981;
            font-weight: bold;
        }}

        .lift-negative {{
            color: #ef4444;
            font-weight: bold;
        }}

        .alert {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }}

        .alert-title {{
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}

        footer {{
            text-align: center;
            color: #666;
            margin-top: 3rem;
            padding: 2rem;
            border-top: 1px solid #ddd;
        }}

        @media print {{
            body {{
                background: white;
            }}
            .section {{
                box-shadow: none;
                border: 1px solid #ddd;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>A/B Test Report</h1>
            <p class="subtitle">Netflix-Style Recommender System</p>
            <p class="subtitle">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>

        <!-- Executive Summary -->
        <div class="section">
            <h2>Executive Summary</h2>
            <p>
                This A/B test evaluated two recommendation algorithms: <strong>Control (Matrix Factorization)</strong> vs
                <strong>Treatment (LightGCN)</strong>. The test ran with {total_users} users
                generating {total_impressions} impressions, {total_clicks} clicks, and {total_conversions} conversions.
            </p>

            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Users</div>
                    <div class="metric-value">{total_users}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Impressions</div>
                    <div class="metric-value">{total_impressions}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Clicks</div>
                    <div class="metric-value">{total_clicks}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Conversions</div>
                    <div class="metric-value">{total_conversions}</div>
                </div>
            </div>
        </div>

        <!-- SRM Check -->
        {"<div class='section'><div class='alert'><div class='alert-title'>⚠️ Sample Ratio Mismatch Detected</div><p>" + srm['message'] + "</p></div></div>" if srm['has_srm'] else ""}

        <!-- Variant Comparison -->
        <div class="section">
            <h2>Variant Comparison</h2>

            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th><span class="control-badge">CONTROL</span> Matrix Factorization</th>
                        <th><span class="treatment-badge">TREATMENT</span> LightGCN</th>
                        <th>Lift</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Users</strong></td>
                        <td>{metrics['control']['users']}</td>
                        <td>{metrics['treatment']['users']}</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td><strong>Impressions</strong></td>
                        <td>{metrics['control']['impressions']}</td>
                        <td>{metrics['treatment']['impressions']}</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td><strong>Clicks</strong></td>
                        <td>{metrics['control']['clicks']}</td>
                        <td>{metrics['treatment']['clicks']}</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td><strong>Conversions</strong></td>
                        <td>{metrics['control']['conversions']}</td>
                        <td>{metrics['treatment']['conversions']}</td>
                        <td>-</td>
                    </tr>
                    <tr style="background: #f9f9f9;">
                        <td><strong>CTR (Click-Through Rate)</strong></td>
                        <td>{metrics['control']['ctr']*100:.2f}%</td>
                        <td>{metrics['treatment']['ctr']*100:.2f}%</td>
                        <td class="{'lift-positive' if lift['ctr'] > 0 else 'lift-negative'}">
                            {'+' if lift['ctr'] > 0 else ''}{lift['ctr']:.2f}%
                        </td>
                    </tr>
                    <tr style="background: #f9f9f9;">
                        <td><strong>CVR (Conversion Rate)</strong></td>
                        <td>{metrics['control']['cvr']*100:.2f}%</td>
                        <td>{metrics['treatment']['cvr']*100:.2f}%</td>
                        <td class="{'lift-positive' if lift['cvr'] > 0 else 'lift-negative'}">
                            {'+' if lift['cvr'] > 0 else ''}{lift['cvr']:.2f}%
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Key Findings -->
        <div class="section">
            <h2>Key Findings</h2>
            <ul style="line-height: 2;">
                <li>
                    <strong>CTR Lift:</strong> Treatment variant showed
                    <span class="{'lift-positive' if lift['ctr'] > 0 else 'lift-negative'}">
                        {'+' if lift['ctr'] > 0 else ''}{lift['ctr']:.2f}%
                    </span>
                    change in click-through rate
                </li>
                <li>
                    <strong>CVR Lift:</strong> Treatment variant showed
                    <span class="{'lift-positive' if lift['cvr'] > 0 else 'lift-negative'}">
                        {'+' if lift['cvr'] > 0 else ''}{lift['cvr']:.2f}%
                    </span>
                    change in conversion rate
                </li>
                <li>
                    <strong>Sample Ratio:</strong> Control {srm['control_ratio']*100:.1f}% vs Treatment {srm['treatment_ratio']*100:.1f}%
                </li>
            </ul>
        </div>

        <!-- Recommendations -->
        <div class="section">
            <h2>Recommendations</h2>
            <p>
                Based on the test results:
            </p>
            <ul style="line-height: 2;">
                {'<li><strong>Launch Treatment:</strong> LightGCN shows improvement in key metrics. Deploy to production.</li>' if lift['ctr'] > 10 and lift['cvr'] > 0 else ''}
                {'<li><strong>Iterate:</strong> Results are inconclusive. Consider running a longer test or trying different hyperparameters.</li>' if lift['ctr'] < 10 and lift['ctr'] > -10 else ''}
                {'<li><strong>Keep Control:</strong> Treatment variant did not improve metrics. Maintain Matrix Factorization.</li>' if lift['ctr'] < -5 else ''}
                <li><strong>Next Steps:</strong> Consider testing deeper GNN architectures (NGCF, PinSage)</li>
                <li><strong>Sample Size:</strong> Collect more data to increase statistical power (current: {total_impressions} impressions)</li>
            </ul>
        </div>

        <footer>
            <p><strong>BA Project - Business Analysis Course</strong></p>
            <p>Netflix-Style Recommender System with A/B Testing Framework</p>
            <p style="margin-top: 1rem; font-size: 0.9rem; color: #999;">
                For detailed methodology, see <a href="../docs/AB_Test_Design.md" style="color: #E50914;">AB_Test_Design.md</a>
            </p>
        </footer>
    </div>
</body>
</html>
    """

    # Save report
    report_path = 'reports/ab_test_report.html'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Report generated successfully: {report_path}")
    print(f"📊 Open in browser: file://{os.path.abspath(report_path)}")

    return report_path


if __name__ == '__main__':
    generate_html_report()
