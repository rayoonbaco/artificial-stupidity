"""Public, read-only demonstration of the Artificial Stupidity evidence gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

from gate.as_gate import evaluate


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "gate" / "examples"
CONFIG_PATH = ROOT / "gate" / "gate_config.json"


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


CONFIG = _load_json(CONFIG_PATH)
BASELINE = _load_json(EXAMPLES / "baseline.json")
SCENARIO_FILES = {
    "keep": "candidate_keep.json",
    "reject": "candidate_reject.json",
    "escalate": "candidate_escalate.json",
}
SCENARIOS = {name: _load_json(EXAMPLES / filename) for name, filename in SCENARIO_FILES.items()}
SCENARIO_EVIDENCE = {
    name: _load_json(EXAMPLES / f"evidence_{name}.json") for name in SCENARIO_FILES
}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self'; script-src 'self'; "
        "img-src 'self' data:; connect-src 'self'"
    )
    return response


@app.get("/")
def index():
    initial = evaluate(
        BASELINE, SCENARIOS["escalate"], CONFIG, SCENARIO_EVIDENCE["escalate"]
    ).to_dict()
    return render_template(
        "index.html",
        baseline=BASELINE,
        scenarios=SCENARIOS,
        initial=initial,
        config=CONFIG,
    )


@app.post("/api/evaluate")
def api_evaluate():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object."}), 400
    scenario = payload.get("scenario")
    if scenario not in SCENARIOS:
        return jsonify({"error": "Choose a published demonstration scenario."}), 400
    try:
        decision = evaluate(
            BASELINE, SCENARIOS[scenario], CONFIG, SCENARIO_EVIDENCE[scenario]
        )
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": f"Evidence could not be trusted: {exc}"}), 422
    return jsonify(decision.to_dict())


@app.get("/api/scenarios")
def api_scenarios():
    return jsonify({"baseline": BASELINE, "scenarios": SCENARIOS})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
