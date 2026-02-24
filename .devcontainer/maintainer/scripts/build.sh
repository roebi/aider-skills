#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="aider-skills-dev"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
CONTAINERFILE="$SCRIPT_DIR/../Containerfile"

command -v podman &>/dev/null && RUNTIME="podman" || RUNTIME="docker"
echo "==> Runtime: $RUNTIME"

$RUNTIME build \
  --file "$CONTAINERFILE" \
  --tag "$IMAGE_NAME:latest" \
  "$REPO_ROOT"

echo "==> Built: $IMAGE_NAME:latest"
echo "    Next: .devcontainer/maintainer/scripts/run.sh"

