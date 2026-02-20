// Simple tooltip helper
const tooltip = document.getElementById("tooltip");
function showTooltip(html, x, y) {
  tooltip.innerHTML = html;
  tooltip.style.left = (x + 12) + "px";
  tooltip.style.top = (y + 12) + "px";
  tooltip.style.opacity = 1;
}
function hideTooltip() {
  tooltip.style.opacity = 0;
}

// Load and process behavior data
async function loadData() {
  // Fetch data from JSON file
  const resp = await fetch("dashboard_data.json", { cache: "no-store" });
  if (!resp.ok) {
    throw new Error("Failed to load dashboard_data.json");
  }
  const data = await resp.json();

  // Basic validation
  if (!data.summary || !data.departments || !data.risk || !data.phishing) {
    throw new Error("dashboard_data.json missing required sections");
  }

  return data;
}

// Create metric cards
function createMetricCards(data) {
  const metricsDiv = document.getElementById("metrics");
  metricsDiv.innerHTML = "";

  const s = data.summary;

  const cards = [
    { title: "Employees Analyzed", value: s.total_employees, subtext: "Total records in dataset" },
    { title: "Avg Pre Score", value: s.pre_avg, subtext: "Average before training" },
    { title: "Avg Post Score", value: s.post_avg, subtext: "Average after training" },
    { title: "Avg Improvement", value: s.improvement_avg, subtext: "Post - Pre average" },
    { title: "Avg Behavior Score", value: s.behavior_avg, subtext: "0 (worst) to 10 (best)" },
    { title: "Password Compliance", value: s.password_compliance_rate_pct + "%", subtext: "Yes rate" },
    { title: "MFA Enabled", value: s.mfa_enabled_rate_pct + "%", subtext: "Yes rate" },
    { title: "Phishing Pass (Sim 3)", value: s.phishing_pass_rate_pct.sim3 + "%", subtext: "Latest simulation pass rate" },
  ];

  cards.forEach(c => {
    const el = document.createElement("div");
    el.className = "metric-card";
    el.innerHTML = `
      <h3>${c.title}</h3>
      <p class="value">${c.value}</p>
      <div class="subtext">${c.subtext}</div>
    `;
    metricsDiv.appendChild(el);
  });
}

// Create knowledge improvement chart
function createKnowledgeChart(data) {
  const container = d3.select("#knowledge-chart");
  container.html("");

  const s = data.summary;

  // Set up SVG dimensions
  const width = 900;
  const height = 320;
  const margin = { top: 20, right: 20, bottom: 50, left: 60 };

  const svg = container.append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`);

  // Data for bars
  const bars = [
    { label: "Avg Pre", value: s.pre_avg },
    { label: "Avg Post", value: s.post_avg },
    { label: "Avg Improvement", value: s.improvement_avg },
  ];

  // Scales
  const x = d3.scaleBand()
    .domain(bars.map(d => d.label))
    .range([margin.left, width - margin.right])
    .padding(0.25);

  const y = d3.scaleLinear()
    .domain([0, 100])
    .nice()
    .range([height - margin.bottom, margin.top]);

  // Axes
  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x));

  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y));

  // Bars
  svg.selectAll("rect.bar")
    .data(bars)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("x", d => x(d.label))
    .attr("y", d => y(d.value))
    .attr("width", x.bandwidth())
    .attr("height", d => (height - margin.bottom) - y(d.value))
    .on("mousemove", (event, d) => {
      showTooltip(`<strong>${d.label}</strong><br/>Value: ${d.value}`, event.pageX, event.pageY);
    })
    .on("mouseleave", hideTooltip);

  // Labels
  svg.selectAll("text.value-label")
    .data(bars)
    .enter()
    .append("text")
    .attr("class", "value-label")
    .attr("x", d => x(d.label) + x.bandwidth() / 2)
    .attr("y", d => y(d.value) - 6)
    .attr("text-anchor", "middle")
    .style("font-size", "12px")
    .text(d => d.value);
}

// Create department performance chart
function createDepartmentChart(data) {
  const container = d3.select("#department-chart");
  container.html("");

  // Aggregate by department already provided
  const rows = data.departments.map(d => ({
    Department: d.Department,
    behavior_avg: +d.behavior_avg,
    improvement_avg: +d.improvement_avg,
    employees: +d.employees
  }));

  // Sort by behavior score
  rows.sort((a, b) => b.behavior_avg - a.behavior_avg);

  const width = 900;
  const height = 420;
  const margin = { top: 20, right: 30, bottom: 40, left: 140 };

  const svg = container.append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`);

  const y = d3.scaleBand()
    .domain(rows.map(d => d.Department))
    .range([margin.top, height - margin.bottom])
    .padding(0.2);

  const x = d3.scaleLinear()
    .domain([0, 10])
    .nice()
    .range([margin.left, width - margin.right]);

  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x));

  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y));

  // Color code by performance level
  function perfColor(v) {
    if (v >= 7.5) return "#2ca02c"; // green-ish
    if (v >= 5.0) return "#ff7f0e"; // orange-ish
    return "#d62728";               // red-ish
  }

  svg.selectAll("rect.deptbar")
    .data(rows)
    .enter()
    .append("rect")
    .attr("class", "deptbar")
    .attr("x", x(0))
    .attr("y", d => y(d.Department))
    .attr("height", y.bandwidth())
    .attr("width", d => x(d.behavior_avg) - x(0))
    .attr("fill", d => perfColor(d.behavior_avg))
    .on("mousemove", (event, d) => {
      showTooltip(
        `<strong>${d.Department}</strong><br/>
         Behavior Avg: ${d.behavior_avg.toFixed(2)}<br/>
         Improvement Avg: ${d.improvement_avg.toFixed(2)}<br/>
         Employees: ${d.employees}`,
        event.pageX, event.pageY
      );
    })
    .on("mouseleave", hideTooltip);

  // Value labels
  svg.selectAll("text.deptlabel")
    .data(rows)
    .enter()
    .append("text")
    .attr("x", d => x(d.behavior_avg) + 6)
    .attr("y", d => y(d.Department) + y.bandwidth() / 2 + 4)
    .style("font-size", "12px")
    .text(d => d.behavior_avg.toFixed(2));
}

// Create risk distribution pie chart
function createRiskChart(data) {
  const container = d3.select("#risk-chart");
  container.html("");

  const counts = data.risk.risk_level_counts; // {Low:..., Medium:..., High:...}
  const entries = Object.entries(counts).map(([k, v]) => ({ level: k, count: +v }));

  const width = 600;
  const height = 360;
  const radius = Math.min(width, height) / 2 - 20;

  const svg = container.append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const color = d3.scaleOrdinal()
    .domain(entries.map(d => d.level))
    .range(["#2ca02c", "#ff7f0e", "#d62728"]); // green/yellow/red feel

  const pie = d3.pie().value(d => d.count);
  const arc = d3.arc().innerRadius(0).outerRadius(radius);

  const total = d3.sum(entries, d => d.count);

  svg.selectAll("path")
    .data(pie(entries))
    .enter()
    .append("path")
    .attr("d", arc)
    .attr("fill", d => color(d.data.level))
    .attr("stroke", "white")
    .attr("stroke-width", 2)
    .on("mousemove", (event, d) => {
      const pct = total ? (d.data.count / total * 100) : 0;
      showTooltip(`<strong>${d.data.level}</strong><br/>Count: ${d.data.count}<br/>${pct.toFixed(1)}%`, event.pageX, event.pageY);
    })
    .on("mouseleave", hideTooltip)
    .on("click", (event, d) => {
      alert(`Clicked risk level: ${d.data.level}\nEmployees: ${d.data.count}`);
    });

  // Labels
  svg.selectAll("text")
    .data(pie(entries))
    .enter()
    .append("text")
    .attr("transform", d => `translate(${arc.centroid(d)})`)
    .attr("text-anchor", "middle")
    .style("font-size", "12px")
    .style("fill", "white")
    .text(d => {
      const pct = total ? (d.data.count / total * 100) : 0;
      return pct >= 8 ? `${pct.toFixed(0)}%` : "";
    });

  // Legend
  const legend = container.append("div").attr("class", "legend");
  entries.forEach(e => {
    const item = legend.append("div").attr("class", "legend-item");
    item.append("span").attr("class", "legend-swatch").style("background", color(e.level));
    item.append("span").text(`${e.level} (${e.count})`);
  });
}

// Create phishing progression line chart
function createPhishingChart(data) {
  const container = d3.select("#phishing-chart");
  container.html("");

  const p = data.phishing.overall_pass_rates_pct;
  const points = [
    { sim: "Sim 1", value: +p.sim1_pass_rate_pct },
    { sim: "Sim 2", value: +p.sim2_pass_rate_pct },
    { sim: "Sim 3", value: +p.sim3_pass_rate_pct }
  ];

  const width = 900;
  const height = 320;
  const margin = { top: 20, right: 20, bottom: 50, left: 60 };

  const svg = container.append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`);

  const x = d3.scalePoint()
    .domain(points.map(d => d.sim))
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

  const line = d3.line()
    .x(d => x(d.sim))
    .y(d => y(d.value));

  svg.append("path")
    .datum(points)
    .attr("fill", "none")
    .attr("stroke-width", 3)
    .attr("d", line);

  svg.selectAll("circle")
    .data(points)
    .enter()
    .append("circle")
    .attr("cx", d => x(d.sim))
    .attr("cy", d => y(d.value))
    .attr("r", 6)
    .on("mousemove", (event, d) => {
      showTooltip(`<strong>${d.sim}</strong><br/>Pass Rate: ${d.value.toFixed(1)}%`, event.pageX, event.pageY);
    })
    .on("mouseleave", hideTooltip);

  svg.selectAll("text.phishlabel")
    .data(points)
    .enter()
    .append("text")
    .attr("class", "phishlabel")
    .attr("x", d => x(d.sim))
    .attr("y", d => y(d.value) - 10)
    .attr("text-anchor", "middle")
    .style("font-size", "12px")
    .text(d => `${d.value.toFixed(1)}%`);
}

// Initialize dashboard
async function initDashboard() {
  try {
    const data = await loadData();
    createMetricCards(data);
    createKnowledgeChart(data);
    createDepartmentChart(data);
    createRiskChart(data);
    createPhishingChart(data);

    // Auto-refresh every 60 seconds (optional)
    if (window.__refreshInterval) clearInterval(window.__refreshInterval);
    window.__refreshInterval = setInterval(async () => {
      const d = await loadData();
      createMetricCards(d);
      createKnowledgeChart(d);
      createDepartmentChart(d);
      createRiskChart(d);
      createPhishingChart(d);
    }, 60000);

  } catch (e) {
    console.error(e);
    alert("Dashboard initialization failed: " + e.message);
  }
}

// Refresh button
document.addEventListener("DOMContentLoaded", () => {
  initDashboard();
  const btn = document.getElementById("refresh");
  if (btn) btn.addEventListener("click", initDashboard);
});
