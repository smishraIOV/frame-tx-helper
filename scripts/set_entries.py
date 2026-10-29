"""Replace whole dict entries in a generator and drop EIPs from its UNVERIFIED set.

Usage: python3.15 -I scripts/set_entries.py <generator.py> <edits.py>
<edits.py> defines ENTRIES = {eip: "    eip: (...),"} and VERIFIED = {eips to drop from UNVERIFIED}.
"""
import re
import sys
from pathlib import Path

target, edits = Path(sys.argv[1]), Path(sys.argv[2])
ns = {}
exec(edits.read_text(), ns)
s = target.read_text()
lines = s.split("\n")
for key, new in ns.get("ENTRIES", {}).items():
    start = next(i for i, l in enumerate(lines) if l.startswith(f"    {key}: ("))
    end = start
    while not lines[end].rstrip().endswith("),"):
        end += 1
    lines[start:end + 1] = new.split("\n")
s = "\n".join(lines)
drop = set(ns.get("VERIFIED", set()))
if drop:
    m = re.search(r"^UNVERIFIED = (?:\{([^}]*)\}|set\(\))", s, re.M)
    if not m:
        sys.exit("no UNVERIFIED set found in " + str(target))
    keep = [x.strip() for x in (m.group(1) or "").split(",") if x.strip() and int(x) not in drop]
    s = s[:m.start()] + ("UNVERIFIED = {" + ", ".join(keep) + "}" if keep else "UNVERIFIED = set()") + s[m.end():]
target.write_text(s)
print("ok", sorted(ns.get("ENTRIES", {})), "verified:", sorted(drop))
