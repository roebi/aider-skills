#!/usr/bin/env bash
# Usage:
#   ./run.sh              — interactive shell
#   ./run.sh pytest       — run tests and exit
#   ./run.sh aider-skills --help
set -euo pipefail

IMAGE_NAME="aider-skills-dev"
CONTAINER_NAME="aider-skills-dev"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

command -v podman &>/dev/null && RUNTIME="podman" || RUNTIME="docker"
$RUNTIME rm -f "$CONTAINER_NAME" 2>/dev/null || true

if [ $# -eq 0 ]; then
  TTY_FLAGS=("-it"); EXEC_ARGS=("bash")
else
  TTY_FLAGS=("-i");  EXEC_ARGS=("$@")
fi

$RUNTIME run \
  "${TTY_FLAGS[@]}" \
  --rm \
  --name "$CONTAINER_NAME" \
  --volume "$REPO_ROOT:/workspace:z" \
  --workdir /workspace \
  --user vscode \
  "$IMAGE_NAME:latest" \
  "${EXEC_ARGS[@]}"
