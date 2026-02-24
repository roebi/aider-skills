#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing aider-skills in editable (dev) mode ..."
pip install -e ".[dev]" --quiet

echo "==> Confirming CLI entry point ..."
aider-skills --version

echo "==> Dev environment ready!"
echo "    Run: aider-skills --help"
echo "    Run: pytest"
