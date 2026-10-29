"""Task 2: Ethereum EIPs by hard fork vs Rootstock status. Emits rsk-eip-status.md.

Usage: python3.15 -I scripts/build_status.py <EIPs-repo> rsk-eip-status.md
"""
import re
import sys
from collections import Counter
from pathlib import Path

eips_dir = Path(sys.argv[1]) / "EIPS"
out_path = Path(sys.argv[2])

RSKJ = "1e95a3b03"  # rsksmart/rskj origin/master, 2026-10-16
EIP_URL = "https://eips.ethereum.org/EIPS/eip-{}"
RSKIP_URL = "https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP{:02d}.md"
PR_URL = "https://github.com/rsksmart/RSKIPs/pull/{}"
JAVA = "rskj-core/src/main/java/"


def code(path, line=None, label=None):
    """Link to a file (and line) in rskj at the pinned commit."""
    full = path if path.startswith("rskj-core/") else JAVA + path
    anchor = f"#L{line}" if line else ""
    text = label or (Path(path).name + (f":{line}" if line else ""))
    return f"[`{text}`](https://github.com/rsksmart/rskj/blob/{RSKJ}/{full}{anchor})"


def rskip(n, upgrade=None):
    s = f"[RSKIP-{n}]({RSKIP_URL.format(n)})"
    return f"{s} ({upgrade})" if upgrade else s


# Mainnet activation heights: rskj-core/src/main/resources/config/main.conf
HEIGHT = {
    "Genesis": 0, "Orchid": 729_000, "Orchid 0.6.0": 1_052_700, "Wasabi": 1_591_000, "Papyrus": 2_392_700,
    "Iris": 3_614_800, "Hop": 4_598_500, "Fingerroot": 5_468_000, "Arrowhead": 6_223_700,
    "Lovell": 7_338_024, "Reed": 8_052_200, "Vetiver": 8_804_200,
}

# Ethereum hard forks, in order, with their Core EIPs (hardfork meta EIPs 606, 607, 608, 609, 1013, 1716,
# 1679, 2387, 7568 + execution-specs for Berlin..Shanghai, 7569, 7600, 7607, 7773).
FORKS = [
    ("Homestead", 606, [2, 7]),
    ("Tangerine Whistle", 608, [150]),
    ("Spurious Dragon", 607, [155, 160, 161, 170]),
    ("Byzantium", 609, [100, 140, 196, 197, 198, 211, 214, 649, 658]),
    ("Constantinople", 1013, [145, 1014, 1052, 1234, 1283]),
    ("Petersburg", 1716, []),
    ("Istanbul", 1679, [152, 1108, 1344, 1884, 2028, 2200]),
    ("Muir Glacier", 2387, [2384]),
    ("Berlin", 7568, [2565, 2718, 2929, 2930]),
    ("London", 7568, [1559, 3198, 3529, 3541, 3554]),
    ("Arrow Glacier", 7568, [4345]),
    ("Gray Glacier", 7568, [5133]),
    ("Paris (The Merge)", 7568, [3675, 4399]),
    ("Shanghai", 7568, [3651, 3855, 3860, 4895, 6049]),
    ("Cancun (Dencun)", 7569, [1153, 4788, 4844, 5656, 6780, 7516]),
    ("Prague (Pectra)", 7600, [2537, 2935, 6110, 7002, 7251, 7549, 7623, 7685, 7691, 7702]),
    ("Osaka (Fusaka)", 7607, [7594, 7823, 7825, 7883, 7917, 7918, 7934, 7939, 7951]),
    ("Amsterdam (Glamsterdam, scheduled)", 7773,
     [2780, 7688, 7708, 7732, 7778, 7843, 7928, 7954, 7976, 7981, 7997, 8024, 8037, 8038, 8045, 8061, 8246, 8282]),
]
RETROACTIVE = [684, 2681, 3607, 7610]  # applied to all forks, not tied to one upgrade

N_A = "N/A"
BOMB = (N_A, "", "Ethereum difficulty-bomb schedule; Rootstock has no difficulty bomb.")
BEACON = (N_A, "", "Ethereum consensus layer / beacon chain; no Rootstock equivalent.")
BLOBS = ("No", "", "Blob-specific; Rootstock has no blobs ([RSKIP-558](" + RSKIP_URL.format(558) + ") Draft).")

# eip -> (status, RSK upgrade, evidence[, note on project assumptions])
# status: Yes | Partial | Adapted | No | Won't | N/A | ?
R = {
    # Homestead
    2: ("Yes", "Lovell", f"Complete since Lovell. From genesis: (1) contract-creation tx cost 53000 {code('org/ethereum/vm/GasCost.java', 84)}; "
        f"(2) low-s rule {code('org/ethereum/core/Transaction.java', 321)}; (3) top-level creates roll back on failed code deposit "
        f"{code('org/ethereum/core/TransactionExecutor.java', 471)}. Internal CREATE/CREATE2 left an empty account until "
        f"{rskip(453, 'Lovell')} ({code('org/ethereum/vm/program/Program.java', 738)}, {code('org/ethereum/vm/program/Program.java', 756)}). "
        "(4) Difficulty formula: N/A, RSK uses its own."),
    7: ("Yes", "Genesis", f"DELEGATECALL {code('org/ethereum/vm/OpCode.java', 669)}; value handling fixed by {rskip(103, 'Orchid 0.6.0')}."),
    # Tangerine Whistle
    150: ("Yes", "Genesis", f"EIP-150 costs in {code('org/ethereum/vm/GasCost.java')} (BALANCE 400, SLOAD 200, EXTCODESIZE 700); `getCallStackDepth` added by {rskip(203, 'Arrowhead')}."),
    # Spurious Dragon
    155: ("Yes", "Genesis", f"Chain ID in `v` {code('org/ethereum/core/Transaction.java', 73)}; mainnet chain ID 30."),
    160: ("Yes", "Genesis", f"`EXP_BYTE_GAS = 50` {code('org/ethereum/vm/GasCost.java', 90)}."),
    161: ("Partial", "Wasabi", f"Only rule (a), and only for CREATE/CREATE2: new contracts start at nonce 1 via {rskip(125, 'Wasabi')} "
          f"({code('org/ethereum/vm/program/Program.java', 592)}); contract-creation txs still start at 0 ({code('org/ethereum/core/TransactionExecutor.java', 403)}). "
          f"(b) 25000 new-account gas is charged even for zero value ({code('org/ethereum/vm/VM.java', 1734)}, {code('org/ethereum/vm/VM.java', 1797)}). "
          f"(c) A zero-value transfer creates an empty account ({code('org/ethereum/db/MutableRepository.java', 322)}). "
          f"(d) No end-of-tx deletion of touched empty accounts; only SUICIDE deletions ({code('org/ethereum/core/TransactionExecutor.java', 622)})."),
    170: ("Yes", "Genesis", f"`MAX_CONTRACT_SIZE = 0x6000` {code('org/ethereum/config/Constants.java', 55)}, enforced in {code('org/ethereum/core/TransactionExecutor.java', 529)}."),
    # Byzantium
    100: ("Adapted", "Genesis", f"Rootstock uses its own uncle-aware difficulty formula ({code('co/rsk/core/DifficultyCalculator.java', 77)}), not EIP-100's."),
    140: ("Yes", "Genesis", f"REVERT {code('org/ethereum/vm/VM.java', 2133)}."),
    196: ("Yes", "Papyrus", f"alt_bn128 ADD/MUL enabled by {rskip(137, 'Papyrus')} ({code('org/ethereum/vm/PrecompiledContracts.java', 145)})."),
    197: ("Yes", "Papyrus", f"alt_bn128 pairing enabled by {rskip(137, 'Papyrus')}."),
    198: ("Yes", "Genesis", f"MODEXP is a genesis precompile; EIP-198 pricing (`GQUAD_DIVISOR = 20`, {code('org/ethereum/vm/PrecompiledContracts.java', 462)})."),
    211: ("Yes", "Genesis", f"RETURNDATASIZE/COPY {code('org/ethereum/vm/OpCode.java', 229)}; buffer clean-up by {rskip(171, 'Iris')}."),
    214: ("Yes", "Orchid", f"STATICCALL gated by {rskip(91, 'Orchid')} ({code('org/ethereum/vm/VM.java', 2126)})."),
    649: BOMB,
    658: ("Yes", "Genesis", f"Receipt status byte {code('org/ethereum/core/TransactionReceipt.java', 45)}."),
    # Constantinople
    145: ("Yes", "Wasabi", f"SHL/SHR/SAR via {rskip(120, 'Wasabi')} ({code('org/ethereum/vm/VM.java', 1870)})."),
    1014: ("Yes", "Wasabi", f"CREATE2 via {rskip(125, 'Wasabi')} ({code('org/ethereum/vm/VM.java', 2115)})."),
    1052: ("Partial", "Iris", f"EXTCODEHASH via {rskip(140, 'Papyrus')}, corrected by {rskip(169, 'Iris')}: gas 400, 0 for non-existent accounts, "
           f"empty-code hash for accounts without code ({code('org/ethereum/db/MutableRepository.java', 217)}). Deviation: EIP-1052 returns 0 for EIP-161 *empty* accounts; "
           "RSK returns the empty-code hash, and RSK does create empty accounts (161 rule c)."),
    1234: BOMB,
    1283: (N_A, "", "Reverted in Ethereum by Petersburg before activation."),
    # Istanbul
    152: ("Yes", "Iris", f"BLAKE2F via {rskip(153, 'Iris')}; input validation tightened by {rskip(552, 'Vetiver')}."),
    1108: ("Yes", "Papyrus", f"EIP-1108 prices (e.g. MUL 6000, {code('co/rsk/pcc/altBN128/BN128Multiplication.java', 53)}), active with {rskip(137, 'Papyrus')}."),
    1344: ("Yes", "Papyrus", f"CHAINID via {rskip(152, 'Papyrus')} ({code('org/ethereum/vm/VM.java', 1956)})."),
    1884: ("Partial", "Papyrus", f"Only SELFBALANCE, via {rskip(151, 'Papyrus')} ({code('org/ethereum/vm/VM.java', 1962)}); SLOAD/BALANCE/EXTCODEHASH repricing not adopted."),
    2028: ("Yes", "Arrowhead", f"Calldata 16 gas/non-zero byte via {rskip(400, 'Arrowhead')}."),
    2200: ("No", "", f"Flat SSTORE costs ({code('org/ethereum/vm/GasCost.java', 39)})."),
    # Muir Glacier
    2384: BOMB,
    # Berlin
    2565: ("No", "", f"MODEXP keeps EIP-198 pricing (`GQUAD_DIVISOR = 20`)."),
    2718: ("No", "", f"No typed txs in rskj. {rskip(543)} Draft ([PR #708]({PR_URL.format(708)})).", "Assumed active"),
    2929: ("No", "", f"Not adopted; see {rskip(239)} (Reprice Trie Read Opcodes).", "Won't (project decision)"),
    2930: ("No", "", f"No access-list code in rskj. {rskip(546)} Draft ([PR #709]({PR_URL.format(709)})): encoding plus access-list gas only.", "Partial: encoding only"),
    # London
    1559: ("Partial", "Genesis", f"No 1559 fee market or Type-2 tx. Closest analogue since genesis: a consensus-enforced block floor, header `minimumGasPrice` "
           f"({code('org/ethereum/core/BlockHeader.java', 127)}). Every tx must pay at least it ({code('co/rsk/validators/TxsMinGasPriceRule.java', 33, 'TxsMinGasPriceRule')}), "
           f"and it can only move a bounded step from the parent ({code('co/rsk/validators/PrevMinGasPriceRule.java', 31, 'PrevMinGasPriceRule')}). "
           f"It's miner-voted, not burnt, with no gas-target elasticity. BASEFEE (EIP-3198) returns it ({code('org/ethereum/vm/VM.java', 1101)}). "
           f"Type-2 encoding in {rskip(546)} Draft.", "Partial: Type-2 encoding, zero base fee"),
    3198: ("Yes", "Arrowhead", f"BASEFEE via {rskip(412, 'Arrowhead')} ({code('org/ethereum/vm/VM.java', 1950)}); returns the block's `minimumGasPrice` ({code('org/ethereum/vm/VM.java', 1101)})."),
    3529: ("No", "", f"Pre-London refunds ({code('org/ethereum/vm/GasCost.java', 61)}: REFUND_SSTORE 15000, SUICIDE_REFUND 24000)."),
    3541: ("Yes", "Vetiver", f"{rskip(544, 'Vetiver')}, on both paths: CREATE/CREATE2 ({code('org/ethereum/vm/program/Program.java', 712)}) "
           f"and contract-creation txs ({code('org/ethereum/core/TransactionExecutor.java', 541)})."),
    3554: BOMB,
    # Arrow / Gray Glacier
    4345: BOMB,
    5133: BOMB,
    # Paris
    3675: BEACON,
    4399: (N_A, "", f"Rootstock is merge-mined PoW; DIFFICULTY ({code('org/ethereum/vm/OpCode.java', 260)}) keeps its meaning."),
    # Shanghai
    3651: ("No", "", "Only meaningful with 2929.", "Won't (needs 2929)"),
    3855: ("Yes", "Arrowhead", f"PUSH0 via {rskip(398, 'Arrowhead')} ({code('org/ethereum/vm/VM.java', 2064)})."),
    3860: ("Yes", "Lovell", f"Initcode limit/metering via {rskip(438, 'Lovell')} (`MAX_INITCODE_SIZE`, {code('org/ethereum/config/Constants.java', 56)})."),
    4895: BEACON,
    6049: (N_A, "", "Deprecation notice only; no consensus change."),
    # Cancun
    1153: ("Yes", "Lovell", f"TLOAD/TSTORE via {rskip(446, 'Lovell')} ({code('org/ethereum/vm/VM.java', 2041)})."),
    4788: BEACON,
    4844: ("No", "", f"{rskip(558)} Draft.", "If needed (RSKIP-558)"),
    5656: ("Yes", "Lovell", f"MCOPY via {rskip(445, 'Lovell')} ({code('org/ethereum/vm/VM.java', 2107)})."),
    6780: ("No", "", f"Pre-Cancun SELFDESTRUCT: always deletes the account, with no same-tx check ({code('org/ethereum/vm/program/Program.java', 434)}); "
           f"burns the balance when the beneficiary is the contract itself ({code('org/ethereum/vm/program/Program.java', 428)}); "
           f"SUICIDE_REFUND still paid ({code('org/ethereum/core/TransactionExecutor.java', 693)}). No RSKIP."),
    7516: BLOBS,
    # Prague
    2537: ("No", "", f"{rskip(188)} (BLS12-381 precompiles) Withdrawn."),
    2935: ("No", "", "No RSKIP; BLOCKHASH not served from state."),
    6110: BEACON, 7002: BEACON, 7251: BEACON, 7549: BEACON, 7685: BEACON,
    7623: ("No", "", "No RSKIP."),
    7691: BLOBS,
    7702: ("No", "", f"{rskip(545)} Draft ([PR #710]({PR_URL.format(710)})).", "Assumed active"),
    # Osaka
    7594: BLOBS,
    7823: ("No", "", "No RSKIP; MODEXP input bounds unchanged."),
    7825: ("No", "", f"No consensus per-tx cap: execution only checks the tx against the remaining block gas ({code('org/ethereum/core/TransactionExecutor.java', 265)}). "
           f"The 2^60 cap is pool-only ({code('co/rsk/net/handler/txvalidator/TxValidatorGasLimitValidator.java', 40)}); 7825's cap is 2^24. "
           f"{rskip(144)} sublist limits (Reed 8.1.0, not scheduled on mainnet) are a different rule."),
    7883: ("No", "", "No RSKIP; MODEXP keeps EIP-198 pricing."),
    7917: BEACON,
    7918: BLOBS,
    7934: ("No", "", "No RSKIP."),
    7939: ("No", "", "No RSKIP; no CLZ in `OpCode.java`."),
    7951: ("No", "", "No RSKIP; no secp256r1 precompile (Rootstock has secp256k1 add/mul via RSKIP-516, Reed)."),
    # Amsterdam (scheduled)
    7688: BEACON, 7732: BEACON, 8045: BEACON, 8061: BEACON, 8282: BEACON,
    7843: (N_A, "", "SLOTNUM is beacon-slot based; would need an RSK equivalent."),
    8024: ("No", "", f"No RSKIP. Rootstock's old DUPN/SWAPN at 0xa8/0xa9 ({code('org/ethereum/vm/OpCode.java', 630)}) are disabled by {rskip(191, 'Iris')}."),
    # Retroactive
    684: ("Partial", "Wasabi", f"CREATE/CREATE2 only, since {rskip(125, 'Wasabi')}: fails on an address with code or non-zero nonce "
          f"({code('org/ethereum/vm/program/Program.java', 572)}) or deleted earlier in the block ({code('org/ethereum/vm/program/Program.java', 543)}). "
          f"Contract-creation txs have no collision check: the account is re-created, keeping only its balance ({rskip(174, 'Iris')}; "
          f"{code('org/ethereum/core/TransactionExecutor.java', 403)}). A collision there would need a hash collision, so the gap is theoretical."),
    2681: ("No", "", f"No consensus rule or RSKIP: nonces are `BigInteger` and block validation only checks equality "
           f"({code('co/rsk/validators/BlockTxsValidationRule.java', 89)}); CREATE/CREATE2 has no nonce-cap check ({code('org/ethereum/vm/program/Program.java', 472)}). "
           f"Only the tx pool ({code('co/rsk/net/handler/TxPendingValidator.java', 66)}) and block-building sort ({code('co/rsk/core/bc/PendingState.java', 194)}) "
           "reject nonces over 8 bytes, which still allows 2^64-1 (the EIP forbids it)."),
    3607: ("No", "", f"No sender-code check in {code('org/ethereum/core/TransactionExecutor.java', 162, 'TransactionExecutor.init()')} "
           f"or the pool's {code('co/rsk/net/handler/txvalidator/TxValidatorAccountStateValidator.java')}; {rskip(545)} notes this and doesn't need it.", "Not needed (RSKIP-545)"),
    7610: ("?", "", "Collision on non-empty storage: not checked."),
}
for n in (2780, 7708, 7778, 7928, 7954, 7976, 7981, 7997, 8037, 8038, 8246):
    R.setdefault(n, ("No", "", "No RSKIP."))

# EIPs/ERCs outside the hard forks that Rootstock adopted through an RSKIP.
OTHER = [
    (55, f"{rskip(60)}: chain-ID-prefixed variant of the EIP-55 checksum."),
    (1167, f"{rskip(159)} (DApp layer)."),
    (1820, f"{rskip(148)} (DApp layer): ERC-1820 registry."),
    (712, f"{rskip(712)} (UI layer): RSK variant of typed-data signing."),
]


def title(n):
    p = eips_dir / f"eip-{n}.md"
    if not p.exists():
        return "?"
    m = re.search(r"^title:\s*(.+)$", p.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip().strip('"') if m else "?"


def status_of(n):
    p = eips_dir / f"eip-{n}.md"
    m = re.search(r"^status:\s*(.+)$", p.read_text(encoding="utf-8"), re.M) if p.exists() else None
    return m.group(1).strip() if m else "?"


def row(n):
    st, up, ev, *rest = R.get(n, ("?", "", "Not checked."))
    h = f"{HEIGHT[up]:,}" if up in HEIGHT else ""
    assumed = rest[0] if rest else ""
    warn = "" if status_of(n) == "Final" else f" ({status_of(n)})"
    return f"| [{n}]({EIP_URL.format(n)}) | {title(n)}{warn} | **{st}** | {up} | {h} | {ev} | {assumed} |"


HEADER = "| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |\n|---|---|---|---|---|---|---|"

out = []
w = out.append
w("# Ethereum EIPs by hard fork vs Rootstock\n")
w("Task 2 in `readme.md`: every Core EIP in each Ethereum hard fork, its Rootstock status, the RSK network upgrade and mainnet "
  "activation height, and the evidence. Code links point at "
  f"[`rsksmart/rskj@{RSKJ}`](https://github.com/rsksmart/rskj/tree/{RSKJ}) (origin/master, 2026-10-16). RSKIP statuses come from `rsksmart/RSKIPs` `a389ec2`; "
  "fork lists come from the hardfork meta EIPs, linked per section.\n")
w("**RSK status:** **Yes** = fully active · **Partial** = some of it active (the evidence says which part) · **Adapted** = same goal, RSK-specific design · "
  "**No** = not active · **N/A** = doesn't apply to Rootstock (beacon chain, difficulty bomb, reverted) · **?** = not verified. "
  "The *Under assumptions* column applies the project assumptions in `readme.md` where they change the picture.\n")
w("**No RSKIP** means no RSKIP on any of the 95 branches of `rsksmart/RSKIPs` cites the EIP or its feature, and rskj `master` has no matching code (checked 2026-10-28, with a control search that does find EIP-3198 in RSKIP-412).\n")

# Summary
counts = Counter()
per_fork = []
for name, meta_eip, nums in FORKS:
    c = Counter(R.get(n, ("?",))[0] for n in nums)
    per_fork.append((name, meta_eip, nums, c))
    counts.update(c)
counts.update(R.get(n, ("?",))[0] for n in RETROACTIVE)
cols = ["Yes", "Partial", "Adapted", "No", "N/A", "?"]
w("## Summary\n")
w("| Fork | Core EIPs | " + " | ".join(cols) + " |")
w("|---|---|" + "---|" * len(cols))
for name, meta_eip, nums, c in per_fork:
    if nums:
        w(f"| {name} | {len(nums)} | " + " | ".join(str(c.get(k, 0) or "") for k in cols) + " |")
rc = Counter(R.get(n, ("?",))[0] for n in RETROACTIVE)
w(f"| Retroactive | {len(RETROACTIVE)} | " + " | ".join(str(rc.get(k, 0) or "") for k in cols) + " |")
total = sum(len(n) for _, _, n, _ in per_fork) + len(RETROACTIVE)
w(f"| **Total** | **{total}** | " + " | ".join(f"**{counts.get(k, 0)}**" for k in cols) + " |\n")
applicable = total - counts[N_A]
w(f"Of the {applicable} EIPs that apply to Rootstock, {counts['Yes']} are fully active, {counts['Partial'] + counts['Adapted']} are partial or adapted, "
  f"{counts['No']} are missing, and {counts['?']} {'still needs' if counts['?'] == 1 else 'still need'} verifying. Rootstock tracks Ethereum's EVM opcode and precompile additions closely up to Cancun (except blobs), "
  "but skipped every gas-model change since Berlin (2929, 2930, 3529, 2200, 1884 repricing) and has no typed transactions.\n")

for name, meta_eip, nums, c in per_fork:
    if not nums:
        w(f"## {name}\n\nMeta: [EIP-{meta_eip}]({EIP_URL.format(meta_eip)}). Only removes EIP-1283 from Constantinople; nothing to adopt.\n")
        continue
    w(f"## {name}\n")
    w(f"Meta: [EIP-{meta_eip}]({EIP_URL.format(meta_eip)}).\n")
    w(HEADER)
    for n in nums:
        w(row(n))
    w("")

w("## Retroactive (all forks)\n")
w("Rules Ethereum applies from genesis, not tied to one upgrade.\n")
w(HEADER)
for n in RETROACTIVE:
    w(row(n))
w("")

w("## Other EIPs/ERCs adopted through an RSKIP\n")
w("Not part of an Ethereum hard fork, listed so the RSKIP → EIP mapping is complete.\n")
w("| EIP | Title | Rootstock |\n|---|---|---|")
for n, ev in OTHER:
    w(f"| [{n}]({EIP_URL.format(n)}) | {title(n)} | {ev} |")
w("")

w("## Rootstock upgrades that brought in Ethereum EIPs\n")
w("| RSK upgrade | Mainnet height | EIPs |\n|---|---|---|")
by_up = {}
for n, v in R.items():
    if v[1] and v[0] in ("Yes", "Partial", "Adapted"):
        by_up.setdefault(v[1], []).append(n)
for up in HEIGHT:
    if up in by_up:
        w(f"| {up} | {HEIGHT[up]:,} | " + ", ".join(str(n) for n in sorted(by_up[up])) + " |")
w("")

out_path.write_text("\n".join(out) + "\n", encoding="utf-8")
missing = sorted(n for _, _, ns, _ in per_fork for n in ns if n not in R)
print("total", total, dict(counts), "unlisted:", missing)
