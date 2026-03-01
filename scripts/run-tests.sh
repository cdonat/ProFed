#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

if [ ! -d ".venv" ]; then
  echo "Virtualenv not found. Run: uv venv && uv pip install -e .[dev]"
  exit 1
fi

source .venv/bin/activate
pytest "$@"
