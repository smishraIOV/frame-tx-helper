#!/bin/bash
# Regenerate eip8141-deps.md and rsk-eip-status.md, then check every rskj citation.
#
# Usage: scripts/regen.sh <path to an ethereum/EIPs clone>
#   PYTHON  interpreter to use (default: python3.15)
#   RSKJ    path to an rskj clone, passed to check_citations.py (default: ../rskj)
#
# Review notes for eip8141-deps.md live in notes/eip8141.md. If the Observations section of the
# generated file was edited by hand and no longer matches that file, this refuses to overwrite it.
set -euo pipefail

EIPS=${1:?usage: scripts/regen.sh <path to an ethereum/EIPs clone>}
PYTHON=${PYTHON:-python3.15}
cd "$(dirname "$0")/.."

if [ -f eip8141-deps.md ] && ! diff -q <(awk 'f; /^### Observations$/{f=1; getline}' eip8141-deps.md) notes/eip8141.md >/dev/null; then
  echo "eip8141-deps.md has Observations edits that aren't in notes/eip8141.md." >&2
  echo "Move them into notes/eip8141.md, then rerun. Diff (generated vs notes):" >&2
  diff <(awk 'f; /^### Observations$/{f=1; getline}' eip8141-deps.md) notes/eip8141.md >&2 || true
  exit 1
fi

"$PYTHON" -I scripts/build_deps.py "$EIPS" eip8141-deps.md >/dev/null
"$PYTHON" -I scripts/build_status.py "$EIPS" rsk-eip-status.md
"$PYTHON" -I scripts/check_citations.py --quiet ${RSKJ:+--rskj "$RSKJ"}
git diff --stat
