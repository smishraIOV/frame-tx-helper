---
name: rsk-evidence-search
description: Search rskj, RSKIPs and EIPs for evidence in a way that can be trusted - correct shell, control searches, full upstream coverage, GitHub API for remote state. Use before claiming that an RSKIP or rskj code does or doesn't exist for a feature, when reading an RSKIP PR, or when checking whether local clones are current.
---

# Search for Rootstock evidence you can trust

A search that silently fails looks exactly like a search that found nothing. Twice in this project a "no hits" result turned out to mean nothing: once because the shell broke the command, once because the clone searched was a fork missing most upstream branches. Every rule below comes from one of those.

## Rules

1. **Never fetch an SSH remote; use the GitHub API instead.** Fetching from this shell has no SSH credentials, so `git fetch` on a `git@github.com:` (or `ssh://`) remote fails. Check `git -C <repo> remote get-url <remote>` first. For remote state (branch heads, PR heads, PR state, branch lists) call `https://api.github.com/...` from Python (`urllib`, unauthenticated, rate-limited). Public HTTPS remotes may be fetched or cloned.
2. **Know which repo a clone actually points at.** The local clones are not upstream:
   - `../RSKIPs`: `origin` is the fork `smishraIOV/RSKIPs` (SSH), with roughly a third of upstream's branch names.
   - `../rskj`: `origin` is `rsksmart/rskj` (HTTPS); `myiov` (SSH) and `jurajpiar` are forks.
   - `.` (frame-tx-helper): `origin` is SSH, so the user pushes; never push.
3. **Search upstream in full for absence claims.** For RSKIPs, use an HTTPS mirror of `rsksmart/RSKIPs` in the scratchpad (`git clone --mirror https://github.com/rsksmart/RSKIPs.git`). It contains every branch and every `refs/pull/<n>/head`, so it includes PRs opened from forks. Record the scope (number of refs, what they are) in `sources.json` → `no_rskip_search`.
4. **Run multi-ref git commands under bash.** zsh doesn't word-split an unquoted `$REFS`, so `git grep ... $REFS` gets one bogus argument and fails. Wrap the whole search in `bash -c '...'`. Don't use `set -- $VAR` to split in zsh either.
5. **Run a control before trusting "no hits."** Search first for something that must match, with the same command and refs:
   - EIP-3198 → RSKIP-412 (`eip[- ]?3198([^0-9]|$)`).
   - Extra positives: EIP-2537 → RSKIP-188; `swapn|dupn` → RSKIP-191.
   If the control misses, the method is broken: fix it before reading any other result.
6. **Search EIP numbers and features.** RSKIPs don't always cite the EIP number. Use `eip[- ]?<n>([^0-9]|$)` (case-insensitive) and also feature keywords: opcode names, precompile names, "calldata floor", "access list", and so on. In rskj, search `rskj-core/src/main` for the opcode, constant or precompile address. Write regexes so a keyword can't match inside another one (`p256` matches `secp256k1`; use `secp256r1|p-?256[^k]`).
7. **Don't treat rskj commit messages or branch names as evidence.** A control showed rskj commits rarely name EIPs (`--grep=3198` finds nothing even though RSKIP-412 implements it), so a miss there proves nothing.
8. **Read RSKIP PRs at their head commit.** PR branches often live in another repo. Get `head.repo.full_name` and `head.sha` from `GET /repos/rsksmart/RSKIPs/pulls/<n>`, then the file from `https://raw.githubusercontent.com/<head repo>/<sha>/IPs/RSKIP<n>.md`, or from `refs/pull/<n>/head` in the mirror. Record the head in `sources.json` → `rskip_prs`.
9. **Check that clones are current before citing them.**
   - `python3.15 -I scripts/check_sources.py` reports whether the pinned rskj commit and PR heads in `sources.json` have moved.
   - For a local clone with an HTTPS `origin`, compare `git rev-parse HEAD` with `origin/<branch>`, fetching only that HTTPS remote. For anything else, compare against the API.
   - A clone that is behind means re-checking cited lines: `scripts/check_citations.py` reads every citation at the pinned commit.
10. **Cite what you actually searched.** In the generated files and commit messages, name the repo, the refs or commit, the date and the control. "No RSKIP" is only as strong as that scope. If the scope changes, update `sources.json` so both legends follow.

## Quick reference

```bash
# RSKIPs: all upstream branches + PR heads, with a control (scratchpad mirror)
bash -c '
cd <scratchpad>/dl/RSKIPs-upstream.git
REFS=$(git for-each-ref --format="%(refname)" refs/heads "refs/pull/*/head")
echo "refs: $(echo "$REFS" | wc -l)"
hits() { git grep -l -i -E "$1" $REFS -- IPs | cut -d: -f2 | sort -u | tr "\n" " "; }
echo "control: $(hits "eip[- ]?3198([^0-9]|$)")"   # must list IPs/RSKIP412.md
echo "EIP-<n>: $(hits "eip[- ]?<n>([^0-9]|$)")"'
```

```python
# Remote state via the GitHub API (never fetch an SSH remote)
import json, urllib.request
pr = json.load(urllib.request.urlopen("https://api.github.com/repos/rsksmart/RSKIPs/pulls/701", timeout=20))
print(pr["state"], pr["head"]["repo"]["full_name"], pr["head"]["sha"])
```
