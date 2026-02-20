import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import pandas as pd
import json
from pathlib import Path


class InteractiveROIDashboard:
    """
    Create interactive web dashboard for ROI analysis.
    """

    def __init__(self, data_file, summary_file):
        """Initialize dashboard"""
        self.data_file = Path(data_file)
        self.summary_file = Path(summary_file)

        if not self.data_file.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_file}")
        if not self.summary_file.exists():
            raise FileNotFoundError(f"Summary file not found: {self.summary_file}")

        self.df = pd.read_csv(self.data_file)
        self.df["month"] = pd.to_datetime(self.df["month"], errors="coerce")

        with open(self.summary_file, "r") as f:
            self.summary = json.load(f)

        # Ensure derived columns exist
        self.df["total_benefits"] = self.df["incident_savings"] + self.df["productivity_gain"] + self.df["compliance_savings"]
        self.df["net_benefits"] = self.df["total_benefits"] - self.df["program_cost"]
        self.df["monthly_roi_pct"] = (self.df["net_benefits"] / self.df["program_cost"]) * 100

        self.df["cumulative_costs"] = self.df["program_cost"].cumsum()
        self.df["cumulative_benefits"] = self.df["total_benefits"].cumsum()
        self.df["cumulative_net_benefits"] = self.df["net_benefits"].cumsum()
        self.df["cumulative_roi_pct"] = (self.df["cumulative_net_benefits"] / self.df["cumulative_costs"]) * 100

        # Initialize Dash app
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        """Define dashboard layout"""
        total_investment = self.summary.get("total_investment", 0)
        total_benefits = self.summary.get("total_benefits", 0)
        total_net = self.summary.get("total_net_benefits", 0)
        final_roi = self.summary.get("final_cumulative_roi_pct", 0)
        payback = self.summary.get("months_to_payback", "N/A")

        min_month = 0
        max_month = len(self.df) - 1

        self.app.layout = html.Div([
            html.H1("Security Culture Program ROI Dashboard"),

            html.Div([
                html.Div([
                    html.H3("Final ROI"),
                    html.H2(f"{final_roi:.2f}%")
                ], style={"padding": "10px", "border": "1px solid #ddd", "borderRadius": "8px", "width": "23%"}),

                html.Div([
                    html.H3("Total Investment"),
                    html.H2(f"${total_investment:,.2f}")
                ], style={"padding": "10px", "border": "1px solid #ddd", "borderRadius": "8px", "width": "23%"}),

                html.Div([
                    html.H3("Total Benefits"),
                    html.H2(f"${total_benefits:,.2f}")
                ], style={"padding": "10px", "border": "1px solid #ddd", "borderRadius": "8px", "width": "23%"}),

                html.Div([
                    html.H3("Payback (Months)"),
                    html.H2(f"{payback}")
                ], style={"padding": "10px", "border": "1px solid #ddd", "borderRadius": "8px", "width": "23%"}),
            ], style={"display": "flex", "gap": "10px", "marginBottom": "20px"}),

            html.Div([
                html.Label("Select Chart Type:"),
                dcc.Dropdown(
                    id="chart-type",
                    options=[
                        {"label": "Monthly ROI (%)", "value": "monthly_roi"},
                        {"label": "Cumulative ROI (%)", "value": "cumulative_roi"},
                        {"label": "Costs vs Benefits", "value": "costs_benefits"},
                        {"label": "Security Metrics", "value": "security_metrics"}
                    ],
                    value="monthly_roi",
                    clearable=False
                )
            ], style={"marginBottom": "20px"}),

            html.Div([
                html.Label("Select Time Period (Month Index Range):"),
                dcc.RangeSlider(
                    id="month-range",
                    min=min_month,
                    max=max_month,
                    step=1,
                    value=[min_month, max_month],
                    marks={i: str(i + 1) for i in range(min_month, max_month + 1, 3)}
                )
            ], style={"marginBottom": "20px"}),

            dcc.Graph(id="main-chart"),

            html.H2("Data Table"),
            dash_table.DataTable(
                id="data-table",
                columns=[{"name": c, "id": c} for c in self.df.columns],
                page_size=10,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "fontFamily": "Arial", "fontSize": "12px"},
                style_header={"fontWeight": "bold"}
            )
        ], style={"padding": "20px"})

    def setup_callbacks(self):
        """Setup interactive callbacks"""

        @self.app.callback(
            Output("main-chart", "figure"),
            Output("data-table", "data"),
            Input("chart-type", "value"),
            Input("month-range", "value")
        )
        def update_outputs(chart_type, month_range):
            start, end = month_range
            filtered = self.df.iloc[start:end + 1].copy()

            # Data table output
            table_data = filtered.copy()
            table_data["month"] = table_data["month"].dt.strftime("%Y-%m-%d")

            if chart_type == "monthly_roi":
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=filtered["month"],
                    y=filtered["monthly_roi_pct"],
                    mode="lines+markers",
                    name="Monthly ROI (%)"
                ))
                fig.add_hline(y=0, line_dash="dash")
                fig.update_layout(
                    title="Monthly ROI (%)",
                    xaxis_title="Month",
                    yaxis_title="ROI (%)"
                )
                return fig, table_data.to_dict("records")

            if chart_type == "cumulative_roi":
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=filtered["month"],
                    y=filtered["cumulative_roi_pct"],
                    mode="lines+markers",
                    name="Cumulative ROI (%)"
                ))
                fig.add_hline(y=0, line_dash="dash")
                fig.update_layout(
                    title="Cumulative ROI (%)",
                    xaxis_title="Month",
                    yaxis_title="ROI (%)"
                )
                return fig, table_data.to_dict("records")

            if chart_type == "costs_benefits":
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=filtered["month"],
                    y=filtered["program_cost"],
                    name="Program Cost"
                ))
                fig.add_trace(go.Bar(
                    x=filtered["month"],
                    y=filtered["total_benefits"],
                    name="Total Benefits"
                ))
                fig.update_layout(
                    barmode="group",
                    title="Program Costs vs Total Benefits",
                    xaxis_title="Month",
                    yaxis_title="USD"
                )
                return fig, table_data.to_dict("records")

            if chart_type == "security_metrics":
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=filtered["month"],
                    y=filtered["phishing_success_rate"] * 100,
                    mode="lines+markers",
                    name="Phishing Success Rate (%)"
                ))
                fig.add_trace(go.Scatter(
                    x=filtered["month"],
                    y=filtered["security_incidents"],
                    mode="lines+markers",
                    name="Security Incidents (count)"
                ))
                fig.add_trace(go.Scatter(
                    x=filtered["month"],
                    y=filtered["compliance_rate"] * 100,
                    mode="lines+markers",
                    name="Compliance Rate (%)"
                ))
                fig.update_layout(
                    title="Security Metrics Over Time",
                    xaxis_title="Month"
                )
                return fig, table_data.to_dict("records")

            # Fallback
            return go.Figure(), table_data.to_dict("records")

    def run(self, port=8050):
        """Run the dashboard server"""
        self.app.run_server(host="0.0.0.0", port=port, debug=True)


def main():
    """Launch interactive dashboard"""
    dashboard = InteractiveROIDashboard(
        "../data/security_metrics.csv",
        "../reports/roi_summary.json"
    )
    dashboard.run(port=8050)


if __name__ == "__main__":
    main()
