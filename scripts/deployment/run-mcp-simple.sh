#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

exec /usr/bin/env python3 -u "$REPO_ROOT/scripts/mcp-server-simple.py"


