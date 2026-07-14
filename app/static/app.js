async function getJson(url, options) {
  const response = await fetch(url, options);
  return response.json();
}

function metricCard(label, value) {
  return `<div class="card"><span>${label}</span><strong>${value}</strong></div>`;
}

async function loadDashboard() {
  const metricsEl = document.getElementById("metrics");
  if (!metricsEl) return;
  const [metrics, runs, risks] = await Promise.all([
    getJson("/dashboard"),
    getJson("/runs"),
    getJson("/risks")
  ]);
  metricsEl.innerHTML = [
    metricCard("Total runs", metrics.total_agent_runs),
    metricCard("Successful", metrics.successful_runs),
    metricCard("Failed", metrics.failed_runs),
    metricCard("Avg latency ms", metrics.average_tool_latency_ms),
    metricCard("Estimated cost", `$${metrics.estimated_total_cost}`),
    metricCard("High-risk prompts", metrics.high_risk_prompts)
  ].join("");
  document.getElementById("runs").innerHTML = runs.map((run) => `
    <div class="run-row">
      <strong>#${run.id} ${run.agent_name}</strong>
      <span class="badge">${run.status}</span>
      <p>${run.user_request_summary}</p>
      <a href="/trace.html">Inspect trace</a>
    </div>
  `).join("") || "<p>No runs yet.</p>";
  document.getElementById("risks").innerHTML = risks.map((risk) => `
    <div class="risk-row">
      <strong class="${risk.risk_level === "critical" ? "danger" : ""}">${risk.risk_level}: ${risk.risk_type}</strong>
      <p>Run #${risk.run_id} - ${risk.explanation}</p>
    </div>
  `).join("") || "<p>No risk flags yet.</p>";
}

const generateButton = document.getElementById("generateData");
if (generateButton) {
  generateButton.addEventListener("click", async () => {
    await getJson("/synthetic/generate", { method: "POST" });
    await loadDashboard();
  });
}

const traceButton = document.getElementById("loadTrace");
if (traceButton) {
  traceButton.addEventListener("click", async () => {
    const runId = document.getElementById("traceRunId").value;
    const data = await getJson(`/runs/${runId}`);
    document.getElementById("traceOutput").textContent = JSON.stringify(data, null, 2);
  });
}

loadDashboard();
