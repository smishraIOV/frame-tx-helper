# Prep for Frame txs on Roostock

Initial exploration to scope the work needed to implement frame transactions [EIP-8141](https://eips.ethereum.org/EIPS/eip-8141) on rootstock. 

## Prepwork
* Task 1: List all EIP dependencies of EIP-8141
    - let us do this iteratively, but limit the depth to two levels to start with
    - extended to depth 3, where the tree closes: depth 4+ adds nothing (33 EIPs in total, including the ones 8141 only cites)
* Task 2: Separately, list all EIPs that have been activated on Rootstock.
    - One way of doing this to first group EIPs by the ethereum hard forks in which they were activated
    - then, for each of these EIPs, we check if there are corresponding RSKIPs (activation height) or direct code implementation (e.g. commit)
    - it is possible that some implementations of EIPs are partial

## Assumptions (2026-10-27)
Working assumptions for scoping. The per-EIP effect is in the "Under assumptions" column of `eip8141-deps.md`.

1. **Typed transactions will be activated:** RSKIP-543 (EIP-2718 envelope), RSKIP-545 (EIP-7702 set-code) and RSKIP-546 (Type 1/2 encodings). Their latest versions are open PRs [#708](https://github.com/rsksmart/RSKIPs/pull/708) (543), [#710](https://github.com/rsksmart/RSKIPs/pull/710) (545) and [#709](https://github.com/rsksmart/RSKIPs/pull/709) (546). RSKIP-544 (EIP-3541) is already active since Vetiver.
2. **All storage rent RSKIPs count as rejected** (07, 17, 21, 27, 52, 61, 113, 240). Storage rent can't be used as a reason to skip an EIP.
3. **No EIP-2929 gas differences on Rootstock.** EIP-8141 gas will be defined without warm/cold access pricing, with our own rationale.
4. **Blobs aren't critical to frame transactions.** If needed, EIP-4844 can be activated via RSKIP-558.

## Files
* `eip8141-deps.md`: EIP-8141 dependency tree and Rootstock status (Task 1)
* `rsk-eip-status.md`: Ethereum Core EIPs by hard fork vs Rootstock, with RSKIP, upgrade, height and evidence (Task 2)
* `notes/eip8141.md`: the Observations section of `eip8141-deps.md`, including review notes. Edit notes here, not in the generated file.
* `sources.json`: the pinned sources both files cite (rskj commit, RSKIPs commit and PR heads, EIPs fetch date). Update it when re-pinning.
* `scripts/`: the two files above are generated; edit the generators, not the `.md` files. They need a shallow clone of `ethereum/EIPs` and a sibling `../rskj` clone.
    - `scripts/regen.sh <EIPs>`: regenerates both files and checks every citation. It refuses to run if the generated Observations were edited by hand (move the edits into `notes/eip8141.md`). Set `PYTHON` to choose the interpreter (default `python3.15`).
    - `build_deps.py`, `build_status.py`: the generators.
    - `check_citations.py`: reads every cited rskj file at the pinned commit and prints the enclosing method and line; flags wrong commits, missing files and out-of-range lines.
    - `check_sources.py`: reports whether anything in `sources.json` has moved upstream (GitHub API).
    - `set_entries.py`: replaces whole status entries in a generator from a small edits file.

## Next steps
1. Validate the findings from Task 2 in rsk-eip-status.md
2. Classify EIPs dependenies as hard or soft pre-requisite.
    - e.g. EIPs related to changes in calldata cost are not hard blockers.
    - but dependencies related to post quantum approaches will be hard ones 