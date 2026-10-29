"""Check every rskj code citation in the generated files against the pinned commit in sources.json.

Usage: python3.15 -I scripts/check_citations.py [--rskj PATH] [--quiet] [files...]

Finds GitHub links (.../rsksmart/rskj/blob/<sha>/<path>#L<n>) and plain citations (`Name.java:123`,
`Name.java:89-91`, and a bare `:428` meaning "same file as the previous citation on this line").
For each one it reads the file at the pinned commit with `git show`, so the local checkout's state
doesn't matter, and prints the enclosing method and the cited line so the claim can be eyeballed.
A citation is a problem if its commit isn't the pinned one, the file doesn't exist, the file name
is ambiguous, or the line is out of range. Exits 1 if there are problems.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCES = json.loads((REPO / "sources.json").read_text(encoding="utf-8"))
PINNED = SOURCES["rskj"]["commit"]

ap = argparse.ArgumentParser()
ap.add_argument("--rskj", default=str(REPO.parent / "rskj"), help="path to an rskj clone (default: ../rskj)")
ap.add_argument("--quiet", action="store_true", help="print only problems and the summary")
ap.add_argument("files", nargs="*", default=["rsk-eip-status.md", "eip8141-deps.md"])
args = ap.parse_args()

LINK = re.compile(r"https://github\.com/rsksmart/rskj/blob/([0-9a-f]+)/([^)#\s]+?\.java)(?:#L(\d+))?\)")
PLAIN = re.compile(r"`([A-Za-z0-9_]+\.java):(\d+)(?:-(\d+))?`")
BARE = re.compile(r"`:(\d+)`")
METHOD = re.compile(r"^\s*(?:@\w+\s*)*(?:(?:public|private|protected|static|final|synchronized|default|abstract)\s+)+"
                    r"[\w<>\[\],.? ]+?\s+(\w+)\s*\(")
TYPE = re.compile(r"^\s*(?:public\s+|private\s+|protected\s+)?(?:static\s+)?(?:final\s+)?(?:abstract\s+)?(class|enum|interface)\s+(\w+)")

_files, _trees = {}, {}


def git(*a):
    return subprocess.run(["git", "-C", args.rskj, *a], capture_output=True, text=True)


def content(sha, path):
    key = (sha, path)
    if key not in _files:
        r = git("show", f"{sha}:{path}")
        _files[key] = r.stdout.split("\n") if r.returncode == 0 else None
    return _files[key]


def resolve(sha, name):
    if sha not in _trees:
        r = git("ls-tree", "-r", "--name-only", sha)
        _trees[sha] = [p for p in r.stdout.split("\n") if p.endswith(".java")] if r.returncode == 0 else []
    hits = [p for p in _trees[sha] if p.endswith("/" + name) and "/src/main/" in p]
    return hits


def enclosing(lines, n):
    for i in range(n - 1, -1, -1):
        m = METHOD.match(lines[i])
        if m:
            return m.group(1) + "()"
        t = TYPE.match(lines[i])
        if t:
            return f"{t.group(1)} {t.group(2)}"
    return "?"


problems, checked = [], 0


def check(src, sha, path, first, last=None):
    global checked
    checked += 1
    where = f"{path.split('/')[-1]}:{first}" + (f"-{last}" if last else "")
    if not sha.startswith(PINNED[:7]) and not PINNED.startswith(sha[:7]):
        problems.append(f"{src}: {where} cites commit {sha}, not the pinned {PINNED}")
    lines = content(PINNED, path)
    if lines is None:
        problems.append(f"{src}: {path} does not exist at {PINNED}")
        return
    if first is None:
        if not args.quiet:
            print(f"  {where:<42} (file only)")
        return
    end = last or first
    if not 1 <= first <= end <= len(lines):
        problems.append(f"{src}: {where} is out of range ({len(lines)} lines)")
        return
    if not args.quiet:
        print(f"  {where:<42} [{enclosing(lines, first)}] {lines[first - 1].strip()[:90]}")


for name in args.files:
    text = (REPO / name).read_text(encoding="utf-8")
    if not args.quiet:
        print(f"== {name}")
    seen = set()
    for lineno, line in enumerate(text.split("\n"), 1):
        src = f"{name}:{lineno}"
        last_path = None
        # Walk citations left to right so a bare `:N` binds to the previous file on the line.
        tokens = sorted(
            [(m.start(), "link", m) for m in LINK.finditer(line)]
            + [(m.start(), "plain", m) for m in PLAIN.finditer(line)]
            + [(m.start(), "bare", m) for m in BARE.finditer(line)],
            key=lambda t: t[0],
        )
        for _, kind, m in tokens:
            if kind == "link":
                sha, path, ln = m.group(1), m.group(2), m.group(3)
                last_path = path
                key = (sha, path, ln)
                if key not in seen:
                    seen.add(key)
                    check(src, sha, path, int(ln) if ln else None)
            elif kind == "plain":
                fname, a, b = m.group(1), int(m.group(2)), m.group(3)
                hits = resolve(PINNED, fname)
                if len(hits) != 1:
                    problems.append(f"{src}: `{fname}` matches {len(hits)} files at {PINNED}")
                    continue
                last_path = hits[0]
                key = (PINNED, hits[0], a, b)
                if key not in seen:
                    seen.add(key)
                    check(src, PINNED, hits[0], a, int(b) if b else None)
            elif last_path:
                key = (PINNED, last_path, m.group(1))
                if key not in seen:
                    seen.add(key)
                    check(src, PINNED, last_path, int(m.group(1)))

for p in problems:
    print("PROBLEM", p)
print(f"{checked} citations checked against rskj {PINNED}: {len(problems)} problem(s).")
sys.exit(1 if problems else 0)
