# frame-tx-helper

Scoping work for EIP-8141 (Frame Transaction) on Rootstock. See `readme.md` for the tasks.

- Treat the **Assumptions** section in `readme.md` as settled. Don't re-raise storage rent or EIP-2929 adoption as open questions, and apply the assumptions when classifying EIP status.
- Back every Rootstock status claim with evidence: an RSKIP, an rskj file/line, or a commit. Local clones are at `../rskj` and `../RSKIPs`.
- Run Python with Homebrew `python3.15` (`/opt/homebrew/bin/python3.15 -I`), not the system `python3`.
- Never fetch from an SSH remote (`git@github.com:` or `ssh://`); use the GitHub API for remote state instead. `../RSKIPs` and this repo have SSH `origin` remotes; `../RSKIPs` is a fork, so search upstream `rsksmart/RSKIPs` through an HTTPS mirror clone. See the `rsk-evidence-search` skill.
