// Dashboard JavaScript with D3.js visualizations
class SecurityCultureDashboard {
 constructor() {
  this.tooltip = d3.select("body")
   .append("div")
   .attr("class", "tooltip");

  this.loadData();
 }

 async loadData() {
  try {
   const [cultureRes, trendRes, deptRes] = await Promise.all([
    fetch('/api/culture-metrics'),
    fetch('/api/trend-data'),
    fetch('/api/department-metrics')
   ]);

   const cultureData = await cultureRes.json();
   const trendData = await trendRes.json();
   const deptData = await deptRes.json();

   if (cultureData.error || trendData.error || deptData.error) {
    console.error("API error:", cultureData.error || trendData.error || deptData.error);
    return;
   }

   const generatedAt = cultureData?.metadata?.generated_at_utc || "Unknown";
   document.getElementById("lastUpdated").textContent =
    `Last Updated (UTC): ${generatedAt}`;

   this.renderKPIs(cultureData);
   this.renderTrainingChart(deptData);
   this.renderPhishingChart(trendData);
   this.renderCultureTrendChart(trendData);
   this.renderDepartmentComparison(deptData);

  } catch (err) {
   console.error("Failed to load dashboard data:", err);
  }
 }

 renderKPIs(data) {
  const kpiContainer = document.getElementById("kpi-container");
  kpiContainer.innerHTML = "";

  const trainingAvg = data?.training_effectiveness?.average_score ?? 0;
  const trainingCount = data?.training_effectiveness?.completion_count ?? 0;

  const clickRate = data?.phishing_resilience?.click_rate ?? 0;
  const reportRate = data?.phishing_resilience?.report_rate ?? 0;

  const cultureScore = data?.culture_score?.overall_culture_score ?? 0;
  const awarenessScore = data?.culture_score?.awareness_score ?? 0;
  const behaviorScore = data?.culture_score?.behavior_score ?? 0;

  const incidents = data?.incident_summary?.total_incidents ?? 0;

  const kpis = [
   { label: "Avg Training Score (90d)", value: `${trainingAvg.toFixed(2)}%` },
   { label: "Training Completions (90d)", value: `${trainingCount}` },
   { label: "Phishing Click Rate (90d)", value: `${clickRate.toFixed(2)}%` },
   { label: "Phishing Report Rate (90d)", value: `${reportRate.toFixed(2)}%` },
   { label: "Overall Culture Score (90d)", value: `${cultureScore.toFixed(2)}/10` },
   { label: "Awareness Score (90d)", value: `${awarenessScore.toFixed(2)}/10` },
   { label: "Behavior Score (90d)", value: `${behaviorScore.toFixed(2)}/10` },
   { label: "Incidents Logged (90d)", value: `${incidents}` }
  ];

  kpis.forEach(kpi => {
   const div = document.createElement("div");
   div.className = "kpi-item";

   const value = document.createElement("div");
   value.className = "kpi-value";
   value.textContent = kpi.value;

   const label = document.createElement("div");
   label.className = "kpi-label";
   label.textContent = kpi.label;

   div.appendChild(value);
   div.appendChild(label);
   kpiContainer.appendChild(div);
  });
 }

 renderTrainingChart(deptData) {
  const svg = d3.select("#training-svg");
  svg.selectAll("*").remove();

  const departments = (deptData?.departments || []).map(d => ({
   department: d.department,
   avg_training_score: +d.avg_training_score
  }));

  const width = svg.node().clientWidth || 600;
  const height = 300;
  const margin = { top: 20, right: 20, bottom: 60, left: 50 };

  svg.attr("viewBox", `0 0 ${width} ${height}`);

  const x = d3.scaleBand()
   .domain(departments.map(d => d.department))
   .range([margin.left, width - margin.right])
   .padding(0.2);

  const y = d3.scaleLinear()
   .domain([0, 100])
   .nice()
   .range([height - margin.bottom, margin.top]);

  svg.append("g")
   .attr("transform", `translate(0,${height - margin.bottom})`)
   .call(d3.axisBottom(x))
   .selectAll("text")
   .attr("transform", "rotate(-30)")
   .style("text-anchor", "end");

  svg.append("g")
   .attr("transform", `translate(${margin.left},0)`)
   .call(d3.axisLeft(y));

  svg.selectAll(".bar")
   .data(departments)
   .enter()
   .append("rect")
   .attr("x", d => x(d.department))
   .attr("y", d => y(d.avg_training_score))
   .attr("width", x.bandwidth())
   .attr("height", d => (height - margin.bottom) - y(d.avg_training_score))
   .attr("fill", "#667eea");
 }

 renderPhishingChart(trendData) {
  const svg = d3.select("#phishing-svg");
  svg.selectAll("*").remove();

  const monthly = trendData?.phishing_trends?.monthly || [];
  const data = monthly.map(d => ({
   month: d.month,
   click_rate: +d.click_rate,
   report_rate: +d.report_rate
  }));

  const width = svg.node().clientWidth || 600;
  const height = 300;
  const margin = { top: 20, right: 20, bottom: 60, left: 50 };

  svg.attr("viewBox", `0 0 ${width} ${height}`);

  const x = d3.scalePoint()
   .domain(data.map(d => d.month))
   .range([margin.left, width - margin.right]);

  const y = d3.scaleLinear()
   .domain([0, 100])
   .nice()
   .range([height - margin.bottom, margin.top]);

  svg.append("g")
   .attr("transform", `translate(0,${height - margin.bottom})`)
   .call(d3.axisBottom(x));

  svg.append("g")
   .attr("transform", `translate(${margin.left},0)`)
   .call(d3.axisLeft(y));

  const lineClick = d3.line()
   .x(d => x(d.month))
   .y(d => y(d.click_rate));

  const lineReport = d3.line()
   .x(d => x(d.month))
   .y(d => y(d.report_rate));

  svg.append("path")
   .datum(data)
   .attr("fill", "none")
   .attr("stroke", "#e74c3c")
   .attr("stroke-width", 2)
   .attr("d", lineClick);

  svg.append("path")
   .datum(data)
   .attr("fill", "none")
   .attr("stroke", "#2ecc71")
   .attr("stroke-width", 2)
   .attr("d", lineReport);
 }

 renderCultureTrendChart(trendData) {
  const svg = d3.select("#culture-svg");
  svg.selectAll("*").remove();

  const monthly = trendData?.culture_trends?.monthly || [];
  const data = monthly.map(d => ({
   month: d.month,
   culture_score: +d.culture_score
  }));

  const width = svg.node().clientWidth || 600;
  const height = 300;
  const margin = { top: 20, right: 20, bottom: 60, left: 50 };

  svg.attr("viewBox", `0 0 ${width} ${height}`);

  const x = d3.scalePoint()
   .domain(data.map(d => d.month))
   .range([margin.left, width - margin.right]);

  const y = d3.scaleLinear()
   .domain([0, 10])
   .nice()
   .range([height - margin.bottom, margin.top]);

  svg.append("g")
   .attr("transform", `translate(0,${height - margin.bottom})`)
   .call(d3.axisBottom(x));

  svg.append("g")
   .attr("transform", `translate(${margin.left},0)`)
   .call(d3.axisLeft(y));

  const line = d3.line()
   .x(d => x(d.month))
   .y(d => y(d.culture_score));

  svg.append("path")
   .datum(data)
   .attr("fill", "none")
   .attr("stroke", "#667eea")
   .attr("stroke-width", 2)
   .attr("d", line);
 }

 renderDepartmentComparison(deptData) {
  const svg = d3.select("#department-svg");
  svg.selectAll("*").remove();

  const departments = deptData?.departments || [];

  const metrics = [
   "avg_training_score",
   "phishing_click_rate",
   "phishing_report_rate",
   "culture_score"
  ];

  const width = svg.node().clientWidth || 600;
  const height = 300;
  const margin = { top: 30, right: 20, bottom: 70, left: 50 };

  svg.attr("viewBox", `0 0 ${width} ${height}`);

  const x = d3.scaleBand()
   .domain(departments.map(d => d.department))
   .range([margin.left, width - margin.right])
   .padding(0.2);

  const y = d3.scaleLinear()
   .domain([0, 100])
   .nice()
   .range([height - margin.bottom, margin.top]);

  svg.append("g")
   .attr("transform", `translate(0,${height - margin.bottom})`)
   .call(d3.axisBottom(x));

  svg.append("g")
   .attr("transform", `translate(${margin.left},0)`)
   .call(d3.axisLeft(y));
 }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
 new SecurityCultureDashboard();
});
