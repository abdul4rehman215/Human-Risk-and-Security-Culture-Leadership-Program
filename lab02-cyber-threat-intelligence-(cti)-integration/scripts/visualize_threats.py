#!/usr/bin/env python3
import json
from collections import Counter
from typing import Dict, List


def create_ascii_chart(data: Dict[str, int], title: str) -> str:
    """
    Create simple ASCII bar chart.

    Args:
        data: Dictionary with labels and values
        title: Chart title

    Returns:
        String with ASCII chart
    """
    if not data:
        return f"{title}\n(No data available)\n"

    max_value = max(data.values())
    scale_factor = 50 / max_value if max_value > 0 else 1

    lines = []
    lines.append(f"\n{title}")
    lines.append("-" * len(title))

    for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
        bar_length = int(value * scale_factor)
        bar = "#" * bar_length
        lines.append(f"{label:25} | {bar} ({value})")

    return "\n".join(lines)


def generate_html_dashboard():
    """
    Generate HTML dashboard with threat visualizations.

    Visualizations:
    - Threat level distribution (bar chart)
    - Indicator type breakdown (pie-style summary)
    - Priority score distribution (histogram-style counts)
    - Top sources (horizontal bar chart)
    """
    # Load master CTI dataset
    with open("output/master_cti_dataset.json", "r", encoding="utf-8") as f:
        data: List[dict] = json.load(f)

    total = len(data)

    # Calculate statistics for each visualization
    threat_levels = Counter([rec.get("threat_level", "Unknown") for rec in data])
    types = Counter([rec.get("type", "Unknown") for rec in data])
    sources = Counter([rec.get("source", "Unknown") for rec in data])

    # Priority score distribution (basic calculation from threat level)
    priority_scores = Counter()
    for rec in data:
        tl = rec.get("threat_level", "Low")
        if tl == "High":
            priority_scores["High (7-10)"] += 1
        elif tl == "Medium":
            priority_scores["Medium (4-6)"] += 1
        else:
            priority_scores["Low (1-3)"] += 1

    # Generate ASCII charts
    threat_chart = create_ascii_chart(dict(threat_levels), "Threat Level Distribution")
    type_chart = create_ascii_chart(dict(types), "Indicator Type Distribution")
    source_chart = create_ascii_chart(dict(sources), "Top Sources")
    priority_chart = create_ascii_chart(dict(priority_scores), "Priority Score Distribution")

    # Generate HTML with embedded CSS
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CTI Threat Intelligence Dashboard</title>
    <style>
        body {{
            font-family: monospace;
            background-color: #f4f4f4;
            padding: 20px;
        }}
        h1 {{
            color: #333;
        }}
        .section {{
            background: #ffffff;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }}
        pre {{
            background: #111;
            color: #0f0;
            padding: 10px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <h1>Cyber Threat Intelligence Dashboard</h1>
    <p>Total Indicators Processed: <strong>{total}</strong></p>

    <div class="section">
        <h2>Threat Level Distribution</h2>
        <pre>{threat_chart}</pre>
    </div>

    <div class="section">
        <h2>Indicator Type Breakdown</h2>
        <pre>{type_chart}</pre>
    </div>

    <div class="section">
        <h2>Priority Score Distribution</h2>
        <pre>{priority_chart}</pre>
    </div>

    <div class="section">
        <h2>Top Sources</h2>
        <pre>{source_chart}</pre>
    </div>
</body>
</html>
"""

    # Save to output/threat_dashboard.html
    output_file = "output/threat_dashboard.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Threat dashboard generated: {output_file}")


if __name__ == "__main__":
    generate_html_dashboard()
