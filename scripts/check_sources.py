"""Report whether the sources pinned in sources.json have moved upstream.

Usage: python3.15 -I scripts/check_sources.py

Compares the pinned rskj commit with the head of its branch, and each RSKIPs PR head with the PR's
current head (and state). Uses the public GitHub API without authentication, so it's rate-limited.
Exits 1 if anything has moved, 2 if GitHub couldn't be reached.
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCES = json.loads((REPO / "sources.json").read_text(encoding="utf-8"))


def api(path):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def same(a, b):
    n = min(len(a), len(b))
    return a[:n] == b[:n]


moved = 0
try:
    rskj = SOURCES["rskj"]
    head = api(f"repos/{rskj['repo']}/commits/{rskj['branch']}")
    sha, date = head["sha"], head["commit"]["committer"]["date"][:10]
    ok = same(rskj["commit"], sha)
    moved += not ok
    print(f"{'ok   ' if ok else 'MOVED'} {rskj['repo']} {rskj['branch']}: pinned {rskj['commit']} ({rskj['date']}), upstream {sha[:9]} ({date})")

    for p in SOURCES["rskip_prs"]:
        pr = api(f"repos/{SOURCES['rskips']['repo']}/pulls/{p['pr']}")
        sha = pr["head"]["sha"]
        state = "merged" if pr.get("merged_at") else pr["state"]
        ok = same(p["head"], sha) and state == "open"
        moved += not ok
        print(f"{'ok   ' if ok else 'MOVED'} PR #{p['pr']} (RSKIP-{p['rskip']}): pinned {p['head']} ({p['checked']}), "
              f"upstream {sha[:7]} ({pr['updated_at'][:10]}), {state}")

    eips = api("repos/ethereum/EIPs/commits/master")
    print(f"info  ethereum/EIPs: fetched {SOURCES['ethereum_eips']['fetched']}, master now {eips['sha'][:7]} "
          f"({eips['commit']['committer']['date'][:10]}); refetch to pick up EIP status changes")
except (urllib.error.URLError, KeyError, TimeoutError) as e:
    print(f"could not reach GitHub: {e}")
    sys.exit(2)

print(f"{moved} source(s) moved since they were pinned." if moved else "All pinned sources are current.")
sys.exit(1 if moved else 0)
