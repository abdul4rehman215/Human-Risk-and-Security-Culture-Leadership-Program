from flask import Flask, render_template, jsonify
from culture_analyzer import SecurityCultureAnalyzer
from trend_analyzer import SecurityCultureTrendAnalyzer

app = Flask(__name__, template_folder='../templates', static_folder='../static')

culture_analyzer = SecurityCultureAnalyzer()
trend_analyzer = SecurityCultureTrendAnalyzer()


@app.route('/')
def dashboard():
    """Render main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/culture-metrics')
def get_culture_metrics():
    """
    API endpoint for current culture metrics.

    Generates comprehensive report and returns JSON.
    Handles errors appropriately.
    """
    try:
        report = culture_analyzer.generate_comprehensive_report(days_back=90)
        culture_analyzer.save_report_to_json(report, filename='data/culture_report.json')
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/trend-data')
def get_trend_data():
    """
    API endpoint for trend data.

    Generates trend report and returns JSON.
    """
    try:
        report = trend_analyzer.generate_trend_report(months_back=6)
        trend_analyzer.save_report_to_json(report, filename='data/trend_report.json')
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/department-metrics')
def get_department_metrics():
    """
    API endpoint for department-specific metrics.

    Extracts department data from the comprehensive report and formats
    it for visualization.
    """
    try:
        report = culture_analyzer.generate_comprehensive_report(days_back=90)

        training_by_dept = report.get("training_effectiveness", {}).get("score_by_department", {})
        click_by_dept = report.get("phishing_resilience", {}).get("click_rate_by_department", {})
        report_by_dept = report.get("phishing_resilience", {}).get("report_rate_by_department", {})
        culture_by_dept = report.get("culture_score", {}).get("culture_by_department", {})

        # Union of department keys
        departments = (
            set(training_by_dept.keys())
            | set(click_by_dept.keys())
            | set(report_by_dept.keys())
            | set(culture_by_dept.keys())
        )

        formatted = []
        for dept in sorted(departments):
            formatted.append({
                "department": dept,
                "avg_training_score": float(training_by_dept.get(dept, 0)),
                "phishing_click_rate": float(click_by_dept.get(dept, 0)),
                "phishing_report_rate": float(report_by_dept.get(dept, 0)),
                "culture_score": float(culture_by_dept.get(dept, 0))
            })

        return jsonify({
            "generated_from_period_days": report.get("metadata", {}).get("period_days", 90),
            "departments": formatted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
