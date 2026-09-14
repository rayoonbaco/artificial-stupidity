let scenarios = {};
let baseline = {};
let selected = "escalate";

const copy = {
  KEEP: "The measured gain clears the configured rules with complete supporting evidence.",
  REJECT: "The candidate does not clear the gate's automatic rejection rules.",
  ESCALATE: "Evidence is promising, but automatic acceptance pauses for human judgment."
};

function showScenario(name) {
  selected = name;
  const candidate = scenarios[name];
  document.querySelectorAll("[data-scenario]").forEach((button) => {
    button.classList.toggle("active", button.dataset.scenario === name);
  });
  document.getElementById("candidate-bpb").textContent = candidate.val_bpb.toFixed(6);
  document.getElementById("candidate-memory").textContent = `${candidate.peak_vram_mb.toFixed(1)} MB`;
  document.getElementById("candidate-complexity").textContent = `${candidate.complexity_delta_lines} lines`;
}

function renderDecision(result) {
  const card = document.getElementById("decision");
  card.className = `decision decision-${result.action.toLowerCase()}`;
  document.getElementById("decision-action").textContent = result.action;
  document.getElementById("decision-summary").textContent = copy[result.action];
  document.getElementById("decision-index").textContent = `${["keep", "reject", "escalate"].indexOf(selected) + 1}`.padStart(2, "0") + " / 03";
  const reasons = document.getElementById("decision-reasons");
  reasons.replaceChildren(...result.reasons.map((reason) => {
    const item = document.createElement("li");
    item.textContent = reason;
    return item;
  }));
  document.getElementById("fact-gain").textContent = result.facts.val_bpb_improvement.toFixed(6);
  document.getElementById("fact-coverage").textContent = `${Math.round(result.facts.evidence_coverage * 100)}%`;
  document.getElementById("fact-memory").textContent = `${(result.facts.memory_growth_fraction * 100).toFixed(2)}%`;
}

document.querySelectorAll("[data-scenario]").forEach((button) => {
  button.addEventListener("click", () => showScenario(button.dataset.scenario));
});

document.getElementById("run-gate").addEventListener("click", async () => {
  const button = document.getElementById("run-gate");
  const error = document.getElementById("api-error");
  button.disabled = true;
  button.firstChild.textContent = "Evaluating evidence ";
  error.hidden = true;
  try {
    const response = await fetch("/api/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ baseline, candidate: scenarios[selected] })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "The gate could not run.");
    renderDecision(result);
  } catch (problem) {
    error.textContent = problem.message;
    error.hidden = false;
  } finally {
    button.disabled = false;
    button.firstChild.textContent = "Run independent gate ";
  }
});

fetch("/api/scenarios")
  .then((response) => response.json())
  .then((data) => {
    scenarios = data.scenarios;
    baseline = data.baseline;
    showScenario("escalate");
  })
  .catch(() => {
    document.getElementById("api-error").textContent = "The example evidence could not be loaded.";
    document.getElementById("api-error").hidden = false;
    document.getElementById("run-gate").disabled = true;
  });
