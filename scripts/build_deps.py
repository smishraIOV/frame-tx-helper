"""Build the EIP-8141 dependency tree (depth <= 2) and emit eip8141-deps.md.

Usage: python3.15 -I build_deps.py <EIPs-repo> <out.md>
"""
import re
import sys
from pathlib import Path

eips_dir = Path(sys.argv[1]) / "EIPS"
out_path = Path(sys.argv[2])

ROOT, MAX_DEPTH = 8141, 3  # the tree closes at depth 3; depth 4+ adds nothing
SOFT = [2, 2929, 3651, 6780, 7819, 7843, 7997, 8038]  # cited in the 8141 body, not in `requires`
EIP_URL = "https://eips.ethereum.org/EIPS/eip-{}"

FORK = {
    2: "Homestead", 161: "Spurious Dragon", 684: "Retroactive (all forks)", 1052: "Constantinople",
    2200: "Istanbul", 2718: "Berlin", 2929: "Berlin", 2930: "Berlin", 1559: "London", 3529: "London",
    3541: "London", 3607: "Retroactive (all forks)", 4895: "Shanghai", 3651: "Shanghai", 4788: "Cancun",
    4844: "Cancun", 6780: "Cancun", 7623: "Prague", 7702: "Prague", 7594: "Fusaka", 7825: "Fusaka",
    2780: "Glamsterdam (scheduled)", 7708: "Glamsterdam (scheduled)", 7778: "Glamsterdam (scheduled)",
    7843: "Glamsterdam (scheduled)", 7928: "Glamsterdam (scheduled)", 7976: "Glamsterdam (scheduled)",
    7997: "Glamsterdam (scheduled)", 8037: "Glamsterdam (scheduled)", 8038: "Glamsterdam (scheduled)",
    8246: "Glamsterdam (scheduled)", 7819: "—", 2681: "Retroactive (all forks)", 8141: "— (not in Glamsterdam meta EIP-7773)",
}

# Rootstock status: (Yes / Partial / No / N/A / ?, evidence). Sources: rskj master 1e95a3b, RSKIPs a389ec2.
RSK = {
    8141: ("No", "No RSKIP."),
    2: ("Yes", "Complete since Lovell. (1) 53000 gas for contract-creation txs and (2) low-s signatures (`Transaction.java:321`) from genesis; (3) failed code deposit leaves no empty contract: top-level creates from genesis (`TransactionExecutor` rollback), internal CREATE/CREATE2 only since RSKIP-453 (Lovell, block 7,338,024; `Program.java:738`). (4) Difficulty formula: N/A, RSK uses its own."),
    161: ("Partial", "Only rule (a), and only for CREATE/CREATE2: new contracts start at nonce 1 since RSKIP-125 (Wasabi; `Program.java:592`); contract-creation txs still start at 0 (`TransactionExecutor.java:403`). (b) 25000 new-account gas is charged even for zero value (`VM.java:1734`, `:1797`). (c) A zero-value transfer creates an empty account (`MutableRepository.java:322`). (d) No end-of-tx deletion of touched empty accounts; only SUICIDE deletions (`TransactionExecutor.java:622`)."),
    684: ("Yes", "`Program.java:547` `addressCollisionException`."),
    2681: ("No", "No consensus rule or RSKIP: nonces are `BigInteger` and block validation only checks equality (`BlockTxsValidationRule.java:89-91`); CREATE/CREATE2 has no nonce-cap check (`Program.java:472`). Only the tx pool (`TxPendingValidator.java:66`) and block-building sort (`PendingState.java:194`) reject nonces over 8 bytes, which still allows 2^64-1 (the EIP forbids it)."),
    1052: ("Yes", "RSKIP-140 (Papyrus), fixed by RSKIP-169 (Iris)."),
    1559: ("Partial", "No 1559 fee market or Type-2 tx. Closest analogue since genesis: a consensus-enforced block floor, header `minimumGasPrice` (`BlockHeader.java:127`). Every tx must pay at least it (`TxsMinGasPriceRule`), and it can only move a bounded step from the parent (`PrevMinGasPriceRule`). It's miner-voted, not burnt, with no gas-target elasticity. BASEFEE (EIP-3198, RSKIP-412) returns it (`VM.java:1101`). RSKIP-546 (Type 1/2) is Draft."),
    2200: ("No", "Flat SSTORE costs in `GasCost.java`."),
    2718: ("No", "RSKIP-543 Typed Transaction Envelope: Draft."),
    2780: ("No", "No RSKIP."),
    2929: ("No", "Not adopted; see RSKIP-239 (Reprice Trie Read Opcodes, cites 2929)."),
    2930: ("No", "No access-list code anywhere in rskj; needs 2718. RSKIP-546 (Draft) covers the Type-1 envelope."),
    3529: ("No", "Pre-London refunds still in `GasCost.java` (REFUND_SSTORE 15000, SUICIDE_REFUND 24000)."),
    3541: ("Yes", "RSKIP-544, Vetiver (block 8,804,200)."),
    3607: ("No", "No sender-code check: `TransactionExecutor.init()` (`TransactionExecutor.java:162`) checks initcode size, gas, nonce, balance and addresses only; the pool's `TxValidatorAccountStateValidator` only checks the sender exists and isn't deleted. RSKIP-545 (PR #710) says it isn't needed for 7702 on RSK."),
    3651: ("No", "Needs 2929."),
    4788: ("N/A", "Beacon-chain specific."),
    4844: ("No", "RSKIP-558 Blob Carrying Transactions: Draft."),
    4895: ("N/A", "Beacon-chain specific."),
    6780: ("No", "Pre-Cancun SELFDESTRUCT: `Program.suicide` always deletes the account (`Program.java:434`), with no same-tx check; balance is burnt when the beneficiary is the contract itself (`:428`); SUICIDE_REFUND still paid (`TransactionExecutor.java:693`). No RSKIP."),
    7594: ("No", "PeerDAS; only referenced by RSKIP-558 (Draft). No blobs on RSK."),
    7623: ("No", "No RSKIP."),
    7702: ("No", "RSKIP-545 Set Code for EOAs: Draft."),
    7708: ("No", "No RSKIP."),
    7778: ("No", "No RSKIP."),
    7819: ("No", "No RSKIP."),
    7825: ("No", "No consensus per-tx cap: execution only checks the tx against the remaining block gas (`TransactionExecutor.java:265`). The 2^60 `Constants.TRANSACTION_GAS_CAP` is used only by the pool (`TxValidatorGasLimitValidator.java:40`); 7825's cap is 2^24. RSKIP-144 sublist limits (Reed 8.1.0, not scheduled on mainnet) are a different rule."),
    7843: ("N/A?", "SLOTNUM is beacon-slot based; RSK would need an equivalent or a no-op."),
    7928: ("No", "No RSKIP."),
    7976: ("No", "No RSKIP."),
    7997: ("?", "No RSKIP; check whether an equivalent factory is deployed on RSK."),
    8037: ("No", "No RSKIP."),
    8038: ("No", "No RSKIP."),
    8246: ("No", "No RSKIP."),
}


# Status under the project assumptions in `## Project assumptions` (user decisions, 2026-10-27).
# Anything not listed keeps its current RSK status.
PR = "https://github.com/rsksmart/RSKIPs/pull/{}"
ASSUMED = {
    2718: ("Assumed", f"RSKIP-543 ([PR #708]({PR.format(708)}))."),
    7702: ("Assumed", f"RSKIP-545 ([PR #710]({PR.format(710)}))."),
    1559: ("Partial", f"Type-2 encoding via RSKIP-546 ([PR #709]({PR.format(709)})); base fee effectively zero, no dynamic fee market."),
    2930: ("Partial", "Type-1 encoding and access-list gas via RSKIP-546; the access list has no effect on execution (no 2929)."),
    4844: ("If needed", "Can be activated via RSKIP-558; not critical for frame txs."),
    7594: ("Not needed", "Only matters if blobs are used; PeerDAS is DA-layer networking."),
    2929: ("Won't", "Project decision: 2929 gas differences not implemented; 8141 gas defined with RSK rationale."),
    3651: ("Won't", "Only meaningful with 2929."),
    8038: ("Replace", "Assumes 2929-style state-access pricing; replace with RSK 8141 gas rationale."),
    3607: ("Not needed", "RSKIP-545: RSK doesn't check sender code, so no 7702 exception needed. 8141's own sender rules still need to be checked."),
}


def preamble(n):
    text = (eips_dir / f"eip-{n}.md").read_text(encoding="utf-8")
    block = re.match(r"---\n(.*?)\n---", text, re.S).group(1)
    pre = dict(l.split(":", 1) for l in block.splitlines() if ":" in l)
    pre = {k.strip().lower(): v.strip() for k, v in pre.items()}
    pre["requires"] = [int(x) for x in re.findall(r"\d+", pre.get("requires", ""))]
    return pre


# BFS over `requires` so each node gets its shallowest depth.
meta = {ROOT: preamble(ROOT)}
depth = {ROOT: 0}
edges = []
frontier = [ROOT]
for d in range(1, MAX_DEPTH + 1):
    nxt = []
    for parent in frontier:
        for child in meta[parent]["requires"]:
            edges.append((parent, child))
            if child not in depth:
                depth[child] = d
                meta[child] = preamble(child)
                nxt.append(child)
    frontier = nxt
hard = set(depth) - {ROOT}

soft_only = [n for n in SOFT if n not in hard]
for n in soft_only:
    depth[n] = 1
    meta[n] = preamble(n)

# Requires of the deepest nodes that we did not expand (beyond MAX_DEPTH).
beyond = sorted({c for n in hard if depth[n] == MAX_DEPTH for c in meta[n]["requires"] if c not in depth})


def link(n):
    return f"[{n}]({EIP_URL.format(n)})"


def kind(n):
    if n in hard and n in SOFT:
        return "hard + cited"
    return "hard" if n in hard else "soft"


out = []
w = out.append
w("# EIP-8141 (Frame Transaction): dependency tree and Rootstock status\n")
w(f"EIP-8141 is **{meta[ROOT]['status']}** (created {meta[ROOT].get('created')}). This is Task 1 in `readme.md`: `requires:` walked to depth {MAX_DEPTH}, "
  "plus the EIPs that are only cited in the 8141 body (\"soft\", not expanded).\n")
w("Sources: `ethereum/EIPs` (fetched 2026-10-27) for preambles and the hardfork metas (7600 Pectra, 7607 Fusaka, 7773 Glamsterdam); "
  "`rsksmart/rskj` master `1e95a3b` and `rsksmart/RSKIPs` `a389ec2` for Rootstock status. See `rsk-eip-status.md` for the wider evidence.\n")
w("Legend: **hard** = reached through `requires`; **soft** = only cited in the 8141 body; **hard + cited** = both. "
  "RSK: Yes / Partial / No / N/A / ? (not verified). ⚠ = not Final yet, so the spec can still change.\n")
w("**No RSKIP** means no RSKIP on any of the 95 branches of `rsksmart/RSKIPs` cites the EIP or its feature, and rskj `master` has no matching code (checked 2026-10-28, with a control search that does find EIP-3198 in RSKIP-412).\n")

w("## Project assumptions\n")
w("Decided 2026-10-27 (see the notes under Observations). The `Under assumptions` column below applies them; the `RSK` column stays as today's mainnet state.\n")
w(f"1. **Typed transactions will be activated:** RSKIP-543 (2718 envelope), RSKIP-545 (7702 set-code) and RSKIP-546 (Type 1/2 encodings). Their latest versions are open PRs [#708]({PR.format(708)}) (543), [#710]({PR.format(710)}) (545) and [#709]({PR.format(709)}) (546). RSKIP-544 (EIP-3541) is already active since Vetiver.")
w("2. **Storage rent RSKIPs count as rejected:** 07, 17 (already Rejected); 21, 27, 52, 61, 113 (Withdrawn); 240 (Deferred). Storage rent can't be used as a reason to skip an EIP.")
w("3. **No EIP-2929 gas differences on Rootstock.** 8141 gas will be defined without warm/cold access pricing, with our own rationale.")
w("4. **Blobs aren't critical to frame txs.** If needed, EIP-4844 can be activated via RSKIP-558.\n")

w("## Nodes\n")
w("| Depth | EIP | Title | Dep | EIP status | Ethereum fork | Required by | RSK | RSK evidence | Under assumptions |")
w("|---|---|---|---|---|---|---|---|---|---|")
parents = {}
for p, c in edges:
    parents.setdefault(c, set()).add(p)
order = sorted(depth, key=lambda n: (depth[n], kind(n) == "soft", n))
for n in order:
    if n == ROOT:
        continue
    st = meta[n]["status"]
    warn = "" if st == "Final" else " ⚠"
    by = ", ".join(str(p) for p in sorted(parents.get(n, []))) or "8141 (body)"
    r, ev = RSK.get(n, ("?", ""))
    a = ASSUMED.get(n)
    assumed = f"**{a[0]}**: {a[1]}" if a else "same"
    w(f"| {depth[n]} | {link(n)} | {meta[n]['title']} | {kind(n)} | {st}{warn} | {FORK.get(n, '?')} | {by} | **{r}** | {ev} | {assumed} |")
w("")
w(f"Not expanded (`requires` of depth-{MAX_DEPTH} nodes): {', '.join(link(n) for n in beyond) or 'none; the tree is complete'}.\n")

w("## Graph\n")
w("```mermaid")
w("graph LR")
status_class = {"Yes": "yes", "Partial": "partial", "No": "no"}
for n in order:
    tag = "EIP-8141 (root)" if n == ROOT else f"RSK: {RSK.get(n, ('?',))[0]}"
    w(f'  E{n}["{n}<br/>{meta[n]["title"][:28]}<br/><i>{tag}</i>"]')
seen = set()
for p, c in edges:
    if (p, c) not in seen:
        seen.add((p, c))
        w(f"  E{p} --> E{c}")
for n in SOFT:
    w(f"  E{ROOT} -.-> E{n}")
# Border-only styling: fill and text colours come from the viewer's theme, so the graph reads in light and dark mode.
w("  classDef yes stroke:#2e9e44,stroke-width:3px")
w("  classDef partial stroke:#d4a017,stroke-width:3px")
w("  classDef no stroke:#d64545,stroke-width:3px")
w("  classDef other stroke:#8a8a8a,stroke-width:2px,stroke-dasharray:4 3")
w("  classDef root stroke:#3b82f6,stroke-width:4px")
w(f"  class E{ROOT} root")
for n in order:
    if n != ROOT:
        w(f"  class E{n} {status_class.get(RSK.get(n, ('?',))[0], 'other')}")
w("```\n")
w("Solid arrows = `requires`; dashed = cited in the body only. Each box shows its Rootstock status; the border repeats it: green = on RSK, amber = partial, red = missing, grey dashed = N/A or unverified, blue = EIP-8141.\n")

w("## What's missing on Rootstock\n")
missing = [n for n in order if n != ROOT and RSK.get(n, ("?",))[0] in ("No", "Partial", "?")]
hard1 = [n for n in missing if n in hard and depth[n] == 1]
hard2 = [n for n in missing if n in hard and depth[n] >= 2]
softm = [n for n in missing if n not in hard]
w(f"- **Direct requirements (depth 1), {len(hard1)}:** " + ", ".join(f"{link(n)} ({RSK[n][0]})" for n in hard1) + ".")
w(f"- **Transitive (depth 2–{MAX_DEPTH}), {len(hard2)}:** " + ", ".join(f"{link(n)} ({RSK[n][0]})" for n in hard2) + ".")
w(f"- **Soft (cited only), {len(softm)}:** " + ", ".join(f"{link(n)} ({RSK[n][0]})" for n in softm) + ".")
present = [n for n in order if n != ROOT and RSK.get(n, ("?",))[0] == "Yes"]
w(f"- **Already on RSK:** " + ", ".join(link(n) for n in present) + ".\n")

w("### Remaining work under the project assumptions\n")
resolved = {"Assumed", "If needed", "Not needed", "Won't", "N/A"}
def eff(n):
    return ASSUMED[n][0] if n in ASSUMED else RSK.get(n, ("?",))[0]
todo = [n for n in order if n != ROOT and eff(n) not in resolved | {"Yes"}]
spec = [n for n in todo if eff(n) in ("No", "Replace", "Partial")]
unk = [n for n in todo if eff(n) in ("?", "N/A?")]
w(f"After applying the assumptions, **{len(spec)}** EIPs still need an RSK decision or an RSKIP, and **{len(unk)}** are unverified or need a substitute.\n")
w("- **Needs a decision or RSKIP:** " + ", ".join(f"{link(n)} ({eff(n)})" for n in spec) + ".")
w("- **Unverified or needs a substitute:** " + ", ".join(f"{link(n)} ({eff(n)})" for n in unk) + ".\n")

w("### Observations\n")
w("- **Rootstock has no typed transactions at all.** No 2718 handling in rskj master, and none of RSKIP-543/545/546 is in `ConsensusRule.java`. EIP-2718 is the base of the tree: 1559, 2930, 4844, 7702 and 8141 itself all depend on it. RSKIP-543/545/546 (envelope, 7702, Type 1/2) exist but are Draft, so they're the natural first step.")
w("  * @claude: For this project, assume that RSKIP-543, 545, and 546 will be activated. ")
w("  * For the present, the lates versions of these RSKIPS live as PRs 708, 709, and 710 ")
w("  * → Applied as assumption 1 (PR #708 = RSKIP-543, #709 = RSKIP-546, #710 = RSKIP-545). "
  "RSKIP-546 gives 1559 and 2930 their encodings only: base fee is effectively zero, and the access list is charged for bandwidth but doesn't affect execution.")
w("- **Gas-model conflicts.** 2929, 2930, 3529 and 3651, plus the newer 2780, 7778, 8037 and 8038, all assume Ethereum's access-list, refund and state-gas model. Rootstock's storage rent design deliberately did not adopt 2929. Each of these needs an explicit RSK decision: adopt, adapt, or define 8141 gas without it.")
w("  * @claude: For this project, treat all storage rent related RSKIPs as rejected. ")
w("  * @claude: for the present, assume that gas price difference from eip-2929 will not be implemented on Rootstock. We will define 8141 gas without it - with our own rationale.")
w("  * → Applied as assumptions 2 and 3. 2929 and 3651 become Won't, and 8038 becomes Replace. "
  "Still open: 3529 (refund reduction), 2200, and the newer gas EIPs 2780, 7778, 7623, 7976 and 8037. These are 2929-independent and need individual decisions as part of the RSK 8141 gas rationale. "
  "EIP-161 (required by 7702 and 8037) is only partly active: new contracts start at nonce 1, but none of the empty-account rules apply, so zero-value calls still create accounts. That matters for 8037's state-creation charging, and it needs a decision like the gas EIPs above.")
w("- **Blob dependencies.** 4844 and 7594 are in `requires` mainly for BLOBHASH and the blob-wrapper format. Rootstock has no blobs (RSKIP-558 is Draft). We need to establish whether 8141 can work on RSK without them, for example with zero blobs per frame tx.")
w("  * @claude: blobs are not critical to frame transactions. For this project we can assume that if needed, eip-4844 can be activated on Rootstock (RSKIP-558)")
w("  * → Applied as assumption 4: 4844 is If needed, 7594 is Not needed.")
w("- **Beacon-chain items (4788, 4895, 7843 SLOTNUM)** don't map to Rootstock and need an RSK-specific substitute or exclusion.")
w("- **Moving targets.** 8141 is Draft, and 2780, 7708, 7778, 7843, 7928, 7976, 7997, 8037, 8038 and 8246 are Last Call. Most are scheduled for Glamsterdam, so their specs may still change.")
w("- **Still to verify:** 7997, marked `?` above. Resolved: 3607 (not adopted, not needed per RSKIP-545) and 161 (Partial: nonce rule only, checked rule by rule).")

out_path.write_text("\n".join(out) + "\n", encoding="utf-8")
print("hard:", sorted(hard))
print("soft-only:", soft_only)
print("beyond:", beyond)
print("nodes:", len(depth) - 1, "missing:", len(missing))
