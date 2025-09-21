#!/usr/bin/env bash
set -euo pipefail
MSG="${1:-chore: automated update}"; shift || true
GLOBS=("$@")
if [[ -z "${MACHINE_PAT:-}" ]]; then echo "MISSING MACHINE_PAT"; exit 1; fi
git config user.name  "${GIT_AUTHOR_NAME:-PPB Bot}"
git config user.email "${GIT_AUTHOR_EMAIL:-github93@wp.pl}"
git fetch --unshallow || true; git fetch --all --tags || true
git remote set-url origin "https://x-access-token:${MACHINE_PAT}@github.com/${GITHUB_REPOSITORY}.git"
shopt -s globstar nullglob
if [[ ${#GLOBS[@]} -gt 0 ]]; then for pattern in "${GLOBS[@]}"; do for f in $pattern; do git add -f "$f" || true; done; done
else git add -A; fi
if git diff --cached --quiet; then echo "Nothing to commit."; exit 0; fi
git commit -m "${MSG}"
BR="${GITHUB_REF_NAME:-main}"; git pull --rebase origin "$BR" || true; git push origin "HEAD:${BR}"
