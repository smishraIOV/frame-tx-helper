---
name: validate-eip
description: Validate an Ethereum EIP's Rootstock status rule by rule against rskj code and RSKIPs, then record the result in the generators. Use when checking, correcting or adding a row in eip8141-deps.md or rsk-eip-status.md, or when asked whether Rootstock implements an EIP.
---

# Validate an EIP's Rootstock status

Goal: a status for one EIP that a reviewer can trust, with every claim backed by a line of code at the pinned rskj commit or by an RSKIP. Most past mistakes in this project came from shortcuts: a quick look that found nothing, an activation check taken as proof of the whole EIP, or a cited line that sat in the wrong method. Don't take those shortcuts.

## Inputs

- The EIP number. Read its spec from a local `ethereum/EIPs` clone (`EIPS/eip-<n>.md`), not from memory.
- `sources.json`: the pinned rskj commit and RSKIPs commit/PR heads. Cite only those.
- `readme.md` → **Assumptions**: settled project decisions (typed txs coming via RSKIP-543/545/546, storage rent rejected, no EIP-2929, blobs optional). Apply them in the *Under assumptions* column; never reopen them.
- Local clones: `../rskj` and `../RSKIPs`.

## Procedure

1. **Split the spec into numbered rules.** Read the Specification section and list every normative rule as (a), (b), (c)… An EIP is rarely one rule: EIP-2 has four, EIP-161 four, EIP-3860 four. Note which rules don't apply to Rootstock (difficulty formula, beacon chain, slots) and why.
2. **Find the code path for each rule** in rskj (paths under `rskj-core/src/main/java/`):
   - Opcodes: `org/ethereum/vm/VM.java` (the `executeOpcode` switch and `do<OPCODE>()` methods), `org/ethereum/vm/OpCode.java`.
   - Gas constants: `org/ethereum/vm/GasCost.java`; limits: `org/ethereum/config/Constants.java`.
   - Contract creation: check **both paths**. Creation transactions go through `org/ethereum/core/TransactionExecutor.java` (`create()`, `createContract()`), and `CREATE`/`CREATE2` through `org/ethereum/vm/program/Program.java` (`createContract()`). They often differ (EIP-2, 161, 684).
   - Calls and refunds: `Program.java` (`callToAddress`, `suicide`), `TransactionExecutor.java` (`finalization`, `refundGas`).
   - Transactions and signatures: `org/ethereum/core/Transaction.java`; account state: `org/ethereum/db/MutableRepository.java`, `org/ethereum/core/Repository.java`.
   - Precompiles: `org/ethereum/vm/PrecompiledContracts.java`, `co/rsk/pcc/`.
   - Block-level rules: `co/rsk/validators/`. Transaction-pool-only rules: `co/rsk/net/handler/txvalidator/`, `co/rsk/net/handler/TxPendingValidator.java`, `co/rsk/core/bc/PendingState.java`. **A pool-only check is not adoption**: it doesn't bind other nodes (EIP-2681, 7825).
3. **Find the activation.** Look for an `activations.isActive(RSKIP<n>)` gate on each rule's code path. Map RSKIP → network upgrade with `rskj-core/src/main/resources/reference.conf` (`consensusRules`), and upgrade → mainnet height with `config/main.conf` (`hardforkActivationHeights`). Code with no gate has applied since genesis. Different rules can activate in different upgrades: date the status by the upgrade that completed it, and say which rule came when (EIP-2: rule (3) for `CREATE` only since RSKIP-453, Lovell).
4. **Read the RSKIP**, if there is one (`../RSKIPs/IPs/RSKIP<n>.md`, or the PR head named in `sources.json`). Record its status (Adopted / Draft / Withdrawn…) and any stated deviation from the EIP. An RSKIP that is Draft activates nothing.
5. **Search for evidence of absence properly** before writing "No":
   - Run multi-ref searches under `bash -c '...'`. zsh doesn't word-split `$REFS`, so a git grep over several branches silently fails.
   - Run a **control** first, a search that must hit (EIP-3198 → RSKIP-412). If the control finds nothing, the method is broken and a "no hits" result means nothing.
   - Search all RSKIPs refs: `git for-each-ref refs/heads refs/remotes/origin`, then `git grep -i -E "eip[- ]?<n>([^0-9]|$)" $REFS -- IPs`, plus feature keywords (opcode or precompile names).
   - Search rskj sources for the feature (opcode name, constant, precompile address). rskj commit messages and branch names rarely name EIPs, so a miss there is not evidence.
6. **Check every cited line**, including the method it's in. `sed -n '<n>p'` shows the line but not its context; a citation to the `GAS` opcode was once offered as evidence for `CREATE`. `scripts/check_citations.py` prints the enclosing method for every citation.
7. **Classify** the EIP using the project's status definitions:
   - **Yes**: every applicable rule holds on mainnet.
   - **Partial**: some rules hold; the evidence says which.
   - **Partial (WIP)**: covered only by a Draft RSKIP; nothing active yet.
   - **Adapted**: same goal, Rootstock-specific design (EIP-100's difficulty formula).
   - **No**: not active on mainnet, including pool-only rules.
   - **N/A**: doesn't apply to Rootstock (beacon chain, difficulty bomb, slots, reverted EIPs).
   - **?**: not verified. If any claim was taken on trust, the row is `?` with the claim kept in the evidence; don't upgrade it on a hunch.
   - A deviation that only shows up in edge cases still makes the status Partial, but say how theoretical it is (EIP-684: needs a hash collision).
8. **Write the evidence** as (a)/(b)/(c), one clause per rule, each with a code link or RSKIP. Name divergences explicitly ("**Divergence:** no 63/64 rule"). Add a **Watch:** note when an open RSKIP or EIP would change the picture (EIP-6780 with RSKIP-701 and EIP-4758).
9. **Record it in the generators, never in the `.md` files:**
   - `rsk-eip-status.md` rows live in `scripts/build_status.py` (`R`), built with `code(path, line)` and `rskip(n, upgrade)` links.
   - `eip8141-deps.md` rows live in `scripts/build_deps.py` (`RSK`, with the *Under assumptions* column in `ASSUMED`), as plain backtick citations like `` `Program.java:592` ``.
   - Update both when the EIP is in both. Use `scripts/set_entries.py` to replace whole entries and remove the EIP from `UNVERIFIED`.
   - Review notes and observations go in `notes/eip8141.md`.
10. **Regenerate and check**: `scripts/regen.sh <EIPs clone>`. It refuses if the generated notes were edited by hand, and it must end with `0 problem(s)` from the citation check. Look at the `git diff` of the generated files: only the intended rows (plus derived lists, graph labels and summary counts) should change.
11. **Commit** each finished EIP, or small group, on its own: what changed, the status before → after, and the key evidence. Use the attribution line from the session instructions. Stage only the files you changed; never stage the user's uncommitted edits, and never push.

## Report back

For each EIP give a short table (rule → finding → code reference), the status before → after, and anything that needs the user's decision rather than a code check (for example, whether a pool-only rule should count). If a step needs clarification, skip that EIP, say so, and move on.
