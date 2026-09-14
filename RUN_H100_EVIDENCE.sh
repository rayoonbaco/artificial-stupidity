#!/usr/bin/env bash
set -u

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR" || exit 1

echo "Artificial Stupidity: predeclared H100 evidence run"
echo "This takes roughly 50-65 minutes and always creates a downloadable evidence ZIP."

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh || exit 1
  export PATH="/root/.local/bin:$PATH"
fi

uv sync || exit 1
uv run python benchmark/h100_evidence_runner.py
status=$?

echo
echo "Runner exit code: $status"
echo "An ESCALATE exit is expected when empirical checks pass because only a human can authorize KEEP."
exit "$status"
