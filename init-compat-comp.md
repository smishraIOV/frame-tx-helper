# Initial compatibility comparison: Ethereum EIPs vs Rootstock

Source: Deleted file. originally from (organization) google sheet `Final EIPs vs RSKIPs - EIP Adoption.csv` (undated; it ends at EIP-7636). This file checks whether that deleted CSV is a reasonable starting point for Task 2 in `readme.md`, then reproduces it with two added columns.

Evidence comes from local clones: `rsksmart/rskj` master `3dc9d97` (2026-09-09), `rsksmart/RSKIPs` `a389ec2` (2026-10-21), and `ethereum/EIPs` + `ethereum/ERCs` (fetched 2026-10-27) for EIP status and category.

## 1. Evaluation summary

**Verdict: usable as a seed for Core EIPs only, and only after correcting it. Do not treat it as authoritative.** It predates the Lovell (7.0.0) and Vetiver (9.0.0) upgrades and has several outright errors in Core rows. About half the rows are ERCs or Meta EIPs, where "adopted by a chain" does not apply.

| Metric | Value |
|---|---|
| Data rows | 212 |
| Status counts | Not Yet Adopted: 183, Adopted: 24, Partially Adopted: 3, Won't Be Adopted: 2 |
| Category counts (from EIP preamble) | ERC: 105, Core: 61, Meta: 15, Interface: 14, Networking: 14, Informational: 3 |
| Final non-ERC EIPs ≤ 7636 on eips.ethereum.org | 120 |
| ...of which missing from CSV | 14 (Core: 9) |
| Final Core EIPs after 7636 (not covered) | 11 |
| CSV rows whose EIP is not (now) Final | 1 |
| Core rows in CSV | 61 |
| Core rows checked against rskj/RSKIPs | 30 → **9 wrong**, 2 suspect |
| Eval flags | n/a: 162, ok: 19, unverified: 18, wrong: 9, suspect: 4 |

### Findings

**A. Coverage and staleness**
- The CSV stops at EIP-7636. It doesn't cover Pectra, Fusaka, or later work. Rootstock-side, it misses Lovell (RSKIP-438/445/446, height 7,338,024) and Vetiver (RSKIP-544, height 8,804,200).
- Final Core EIPs ≤ 7636 missing from the CSV: [2537](https://eips.ethereum.org/EIPS/eip-2537), [2935](https://eips.ethereum.org/EIPS/eip-2935), [6110](https://eips.ethereum.org/EIPS/eip-6110), [6916](https://eips.ethereum.org/EIPS/eip-6916), [7002](https://eips.ethereum.org/EIPS/eip-7002), [7251](https://eips.ethereum.org/EIPS/eip-7251), [7549](https://eips.ethereum.org/EIPS/eip-7549), [7594](https://eips.ethereum.org/EIPS/eip-7594), [7623](https://eips.ethereum.org/EIPS/eip-7623).
- Final Core EIPs after 7636: [7685](https://eips.ethereum.org/EIPS/eip-7685), [7691](https://eips.ethereum.org/EIPS/eip-7691), [7702](https://eips.ethereum.org/EIPS/eip-7702), [7823](https://eips.ethereum.org/EIPS/eip-7823), [7825](https://eips.ethereum.org/EIPS/eip-7825), [7883](https://eips.ethereum.org/EIPS/eip-7883), [7917](https://eips.ethereum.org/EIPS/eip-7917), [7918](https://eips.ethereum.org/EIPS/eip-7918), [7934](https://eips.ethereum.org/EIPS/eip-7934), [7939](https://eips.ethereum.org/EIPS/eip-7939), [7951](https://eips.ethereum.org/EIPS/eip-7951).
- Of EIP-8141's 13 required EIPs, the CSV covers only [1559](https://eips.ethereum.org/EIPS/eip-1559), [2718](https://eips.ethereum.org/EIPS/eip-2718), [3529](https://eips.ethereum.org/EIPS/eip-3529), [3607](https://eips.ethereum.org/EIPS/eip-3607), [4844](https://eips.ethereum.org/EIPS/eip-4844); missing: [2780](https://eips.ethereum.org/EIPS/eip-2780), [7594](https://eips.ethereum.org/EIPS/eip-7594), [7702](https://eips.ethereum.org/EIPS/eip-7702), [7708](https://eips.ethereum.org/EIPS/eip-7708), [7778](https://eips.ethereum.org/EIPS/eip-7778), [7825](https://eips.ethereum.org/EIPS/eip-7825), [7976](https://eips.ethereum.org/EIPS/eip-7976), [8037](https://eips.ethereum.org/EIPS/eip-8037).
- Rows that are not Final today: 7636 (Withdrawn).

**B. Scope and semantics**
- ERCs are mixed in with protocol EIPs and the status is applied inconsistently: ERC-20 is "Adopted" but ERC-721 is "Not Yet Adopted", though any EVM chain supports both. Hardfork-meta EIPs (606–609, 779, 1013, 1679, 1716, 2387, 7568, 7569) are listed as "Not Yet Adopted", which doesn't mean anything for a meta EIP.
- Many "Adopted" rows have no RSKIP. Some really are genesis behaviour inherited from EthereumJ (DELEGATECALL, EIP-150/160 costs, MODEXP). Others came in through an RSKIP that the CSV doesn't list (CHAINID → RSKIP-152; alt_bn128 → RSKIP-137).

**C. Errors in Core rows (verified)**
- EIP-7 (wrong): DELEGATECALL present since genesis (`OpCode.java:669`, rskj `VM.java` `doCALL`). Should be Adopted.
- EIP-5656 (wrong): MCOPY: RSKIP-445, Lovell (`VM.java:2107`). Should be Adopted.
- EIP-3198 (wrong): BASEFEE implemented by RSKIP-412, Arrowhead (`VM.java:1950`). Should be Adopted / RSKIP-412.
- EIP-1153 (wrong): TLOAD/TSTORE: RSKIP-446, Lovell (`VM.java:2041`). Should be Adopted.
- EIP-2200 (wrong): Note says 'Only SELFBALANCE implemented', but SELFBALANCE is from EIP-1884. No evidence of 2200 net gas metering (`GasCost.SSTORE` flat).
- EIP-684 (wrong): Create-collision revert exists (`Program.java:547`, `addressCollisionException`). Likely Adopted.
- EIP-214 (wrong): STATICCALL gated by RSKIP-91 (`VM.java:2126`), Orchid (rskj `reference.conf`). Should be Adopted / RSKIP-91.
- EIP-3860 (wrong): Initcode limit/metering: RSKIP-438 (Adopted), Lovell. Should be Adopted.
- EIP-3541 (wrong): RSKIP-544 (Adopted), Vetiver (height 8,804,200). Post-dates the CSV.
- EIP-1559 (suspect): RSKIP-412 is BASEFEE, which is EIP-3198 (per `ConsensusRule.java` comment), not EIP-1559. No 1559 fee market. RSKIP-543/545/546 (typed tx / Type 2) are Draft.
- EIP-1884 (suspect): SELFBALANCE (part of EIP-1884) is RSKIP-151, Papyrus (`VM.java:1962`). Should be Partially Adopted.

**D. Structure**
- The CSV has no Ethereum-fork column, no RSK upgrade or activation height, and no evidence links. The `Fork` column below is added for Core rows and comes from the hardfork meta EIPs.

### Recommendation for Task 2

Seed Task 2 from **rskj** instead: `ConsensusRule.java`, `reference.conf` (RSKIP → upgrade) and `main.conf` (upgrade → height), joined with the RSKIPs that cite an EIP (`grep EIP- IPs/*.md`). Use the CSV only to cross-check the Core rows, and drop ERCs and Meta EIPs.

RSK mainnet upgrade heights (`rskj-core/src/main/resources/config/main.conf`): Orchid 729,000 · Wasabi 1,591,000 · Papyrus 2,392,700 · Iris 3,614,800 · Hop 4,598,500 · Fingerroot 5,468,000 · Arrowhead 6,223,700 · Lovell 7,338,024 · Reed 8,052,200 · Vetiver 8,804,200 · Cardamom (not scheduled).

## 2. Extracted table

The columns `EIP` through `Notes` reproduce the CSV verbatim. `Category` and `Fork` are added, and `Eval flag` / `Eval comment` give the result of this review. Flags: **ok** = confirmed against rskj/RSKIPs · **wrong** = contradicted by evidence · **suspect** = incomplete or inconsistent · **unverified** = Core row not yet checked · **n/a** = ERC/Meta/Interface/Networking.

| EIP | Title | Category | Fork | Status on RSK | RSKIP(s) | RSKIP title(s) | Notes | Eval flag | Eval comment |
|---|---|---|---|---|---|---|---|---|---|
| [2](https://eips.ethereum.org/EIPS/eip-2) | Homestead Hard-fork Changes | Core | Homestead | Adopted |  |  |  | **unverified** |  |
| [4](https://eips.ethereum.org/EIPS/eip-4) | EIP Classification | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5](https://eips.ethereum.org/EIPS/eip-5) | Gas Usage for `RETURN` and `CALL*` | Core |  | Not Yet Adopted |  |  |  | **unverified** |  |
| [6](https://eips.ethereum.org/EIPS/eip-6) | Renaming SUICIDE opcode | Interface |  | Adopted |  |  |  | **n/a** |  |
| [7](https://eips.ethereum.org/EIPS/eip-7) | DELEGATECALL | Core | Homestead | Not Yet Adopted |  |  |  | **wrong** | DELEGATECALL present since genesis (`OpCode.java:669`, rskj `VM.java` `doCALL`). Should be Adopted. |
| [8](https://eips.ethereum.org/EIPS/eip-8) | devp2p Forward Compatibility Requirements for Homestead | Networking | Homestead | Not Yet Adopted |  |  |  | **n/a** |  |
| [20](https://eips.ethereum.org/EIPS/eip-20) | Token Standard | ERC |  | Adopted |  |  |  | **n/a** |  |
| [55](https://eips.ethereum.org/EIPS/eip-55) | Mixed-case checksum address encoding | ERC |  | Partially Adopted | [60](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP60.md) | Checksum Address Encoding | Implemented algorithm is compatible by using a null prefix | **n/a** |  |
| [100](https://eips.ethereum.org/EIPS/eip-100) | Change difficulty adjustment to target mean block time including uncles | Core | Byzantium | Adopted |  |  |  | **unverified** |  |
| [137](https://eips.ethereum.org/EIPS/eip-137) | Ethereum Domain Name Service - Specification | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [140](https://eips.ethereum.org/EIPS/eip-140) | REVERT instruction | Core | Byzantium | Adopted |  |  |  | **unverified** |  |
| [141](https://eips.ethereum.org/EIPS/eip-141) | Designated invalid EVM instruction | Core |  | Adopted |  |  |  | **unverified** |  |
| [145](https://eips.ethereum.org/EIPS/eip-145) | Bitwise shifting instructions in EVM | Core | Constantinople | Adopted | [120](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP120.md) | Shifting opcodes |  | **ok** | RSKIP-120, Wasabi. |
| [150](https://eips.ethereum.org/EIPS/eip-150) | Gas cost changes for IO-heavy operations | Core | Tangerine Whistle | Adopted |  |  |  | **ok** | EIP-150 costs in `GasCost.java` (BALANCE 400, SLOAD 200, EXTCODESIZE 700). |
| [152](https://eips.ethereum.org/EIPS/eip-152) | Add BLAKE2 compression function `F` precompile | Core | Istanbul | Adopted | [153](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP153.md) | Add BLAKE2 Compression Function F Precompile |  | **ok** | RSKIP-153, Iris; input validation tightened by RSKIP-552, Vetiver. |
| [155](https://eips.ethereum.org/EIPS/eip-155) | Simple replay attack protection | Core | Spurious Dragon | Adopted |  |  |  | **unverified** |  |
| [158](https://eips.ethereum.org/EIPS/eip-158) | State clearing | Core |  | Not Yet Adopted |  |  |  | **unverified** |  |
| [160](https://eips.ethereum.org/EIPS/eip-160) | EXP cost increase | Core | Spurious Dragon | Adopted |  |  |  | **ok** | `GasCost.EXP_BYTE_GAS = 50`. |
| [161](https://eips.ethereum.org/EIPS/eip-161) | State trie clearing (invariant-preserving alternative) | Core | Spurious Dragon | Won't Be Adopted |  |  |  | **unverified** |  |
| [162](https://eips.ethereum.org/EIPS/eip-162) | Initial ENS Hash Registrar | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [165](https://eips.ethereum.org/EIPS/eip-165) | Standard Interface Detection | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [170](https://eips.ethereum.org/EIPS/eip-170) | Contract code size limit | Core | Spurious Dragon | Adopted |  |  |  | **unverified** |  |
| [173](https://eips.ethereum.org/EIPS/eip-173) | Contract Ownership Standard | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [181](https://eips.ethereum.org/EIPS/eip-181) | ENS support for reverse resolution of Ethereum addresses | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [190](https://eips.ethereum.org/EIPS/eip-190) | Ethereum Smart Contract Packaging Standard | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [191](https://eips.ethereum.org/EIPS/eip-191) | Signed Data Standard | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [196](https://eips.ethereum.org/EIPS/eip-196) | Precompiled contracts for addition and scalar multiplication on the elliptic curve alt_bn128 | Core | Byzantium | Adopted |  |  |  | **ok** | Adopted, but missing RSKIP: alt_bn128 precompiles enabled by RSKIP-137, Papyrus (`PrecompiledContracts.java`). |
| [197](https://eips.ethereum.org/EIPS/eip-197) | Precompiled contracts for optimal ate pairing check on the elliptic curve alt_bn128 | Core | Byzantium | Adopted |  |  |  | **ok** | Adopted, but missing RSKIP: RSKIP-137, Papyrus. |
| [198](https://eips.ethereum.org/EIPS/eip-198) | Big integer modular exponentiation | Core | Byzantium | Adopted |  |  |  | **ok** | MODEXP is a genesis precompile (`PrecompiledContracts.GENESIS_ADDRESSES`). |
| [211](https://eips.ethereum.org/EIPS/eip-211) | New opcodes: RETURNDATASIZE and RETURNDATACOPY | Core | Byzantium | Adopted | [171](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP171.md) | Clean EVM Internal Buffer in Call-like Opcodes | This implementation allows for full compatibility with the EIP | **ok** | Opcodes present (`OpCode.java:229`); RSKIP-171 buffer fix, Iris. |
| [214](https://eips.ethereum.org/EIPS/eip-214) | New opcode STATICCALL | Core | Byzantium | Not Yet Adopted |  |  |  | **wrong** | STATICCALL gated by RSKIP-91 (`VM.java:2126`), Orchid (rskj `reference.conf`). Should be Adopted / RSKIP-91. |
| [223](https://eips.ethereum.org/EIPS/eip-223) | Token with transaction handling model | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [225](https://eips.ethereum.org/EIPS/eip-225) | Clique proof-of-authority consensus protocol | Core |  | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [234](https://eips.ethereum.org/EIPS/eip-234) | Add `blockHash` to JSON-RPC filter options. | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [600](https://eips.ethereum.org/EIPS/eip-600) | Ethereum purpose allocation for Deterministic Wallets | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [601](https://eips.ethereum.org/EIPS/eip-601) | Ethereum hierarchy for deterministic wallets | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [606](https://eips.ethereum.org/EIPS/eip-606) | Hardfork Meta: Homestead | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [607](https://eips.ethereum.org/EIPS/eip-607) | Hardfork Meta: Spurious Dragon | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [608](https://eips.ethereum.org/EIPS/eip-608) | Hardfork Meta: Tangerine Whistle | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [609](https://eips.ethereum.org/EIPS/eip-609) | Hardfork Meta: Byzantium | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [627](https://eips.ethereum.org/EIPS/eip-627) | Whisper Specification | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [649](https://eips.ethereum.org/EIPS/eip-649) | Metropolis Difficulty Bomb Delay and Block Reward Reduction | Core | Byzantium | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [658](https://eips.ethereum.org/EIPS/eip-658) | Embedding transaction status code in receipts | Core | Byzantium | Adopted |  |  |  | **unverified** |  |
| [681](https://eips.ethereum.org/EIPS/eip-681) | URL Format for Transaction Requests | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [684](https://eips.ethereum.org/EIPS/eip-684) | Revert creation in case of collision | Core |  | Not Yet Adopted |  |  |  | **wrong** | Create-collision revert exists (`Program.java:547`, `addressCollisionException`). Likely Adopted. |
| [695](https://eips.ethereum.org/EIPS/eip-695) | Create `eth_chainId` method for JSON-RPC | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [706](https://eips.ethereum.org/EIPS/eip-706) | DEVp2p snappy compression | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [712](https://eips.ethereum.org/EIPS/eip-712) | Typed structured data hashing and signing | Interface |  | Not Yet Adopted |  |  |  | **suspect** | RSKIP-712 (RSK typed structured data signing) is Adopted (UI layer). |
| [721](https://eips.ethereum.org/EIPS/eip-721) | Non-Fungible Token Standard | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [747](https://eips.ethereum.org/EIPS/eip-747) | wallet_watchAsset RPC Method | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [777](https://eips.ethereum.org/EIPS/eip-777) | Token Standard | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [778](https://eips.ethereum.org/EIPS/eip-778) | Ethereum Node Records (ENR) | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [779](https://eips.ethereum.org/EIPS/eip-779) | Hardfork Meta: DAO Fork | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [820](https://eips.ethereum.org/EIPS/eip-820) | Pseudo-introspection Registry Contract | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [868](https://eips.ethereum.org/EIPS/eip-868) | Node Discovery v4 ENR Extension | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1013](https://eips.ethereum.org/EIPS/eip-1013) | Hardfork Meta: Constantinople | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1014](https://eips.ethereum.org/EIPS/eip-1014) | Skinny CREATE2 | Core | Constantinople | Adopted | [125](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP125.md) | Create2 |  | **ok** | RSKIP-125, Wasabi (`VM.java:2115`). |
| [1046](https://eips.ethereum.org/EIPS/eip-1046) | tokenURI Interoperability | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1052](https://eips.ethereum.org/EIPS/eip-1052) | EXTCODEHASH opcode | Core | Constantinople | Adopted | [140](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP140.md) | EXTCODEHASH opcode |  | **ok** | RSKIP-140, Papyrus; corrected by RSKIP-169, Iris. |
| [1108](https://eips.ethereum.org/EIPS/eip-1108) | Reduce alt_bn128 precompile gas costs | Core | Istanbul | Adopted |  |  |  | **ok** | Adopted; EIP-1108 prices used (e.g. MUL = 6000, `BN128Multiplication.java:53`), activated with RSKIP-137. |
| [1153](https://eips.ethereum.org/EIPS/eip-1153) | Transient storage opcodes | Core | Cancun | Not Yet Adopted |  |  |  | **wrong** | TLOAD/TSTORE: RSKIP-446, Lovell (`VM.java:2041`). Should be Adopted. |
| [1155](https://eips.ethereum.org/EIPS/eip-1155) | Multi Token Standard | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1167](https://eips.ethereum.org/EIPS/eip-1167) | Minimal Proxy Contract | ERC |  | Adopted | [159](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP159.md) | Minimal Proxy Contract |  | **n/a** |  |
| [1193](https://eips.ethereum.org/EIPS/eip-1193) | Ethereum Provider JavaScript API | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1234](https://eips.ethereum.org/EIPS/eip-1234) | Constantinople Difficulty Bomb Delay and Block Reward Adjustment | Core | Constantinople | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [1271](https://eips.ethereum.org/EIPS/eip-1271) | Standard Signature Validation Method for Contracts | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1283](https://eips.ethereum.org/EIPS/eip-1283) | Net gas metering for SSTORE without dirty maps | Core | Constantinople | Not Yet Adopted |  |  |  | **unverified** |  |
| [1328](https://eips.ethereum.org/EIPS/eip-1328) | WalletConnect URI Format | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1344](https://eips.ethereum.org/EIPS/eip-1344) | ChainID opcode | Core | Istanbul | Adopted |  |  |  | **ok** | Adopted, but missing RSKIP: CHAINID is RSKIP-152, Papyrus (`VM.java:1956`). |
| [1363](https://eips.ethereum.org/EIPS/eip-1363) | Payable Token | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1559](https://eips.ethereum.org/EIPS/eip-1559) | Fee market change for ETH 1.0 chain | Core | London | Partially Adopted | [412](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP412.md) | BASEFEE instruction | EIP1559 contains more changes that BASEFEE alone | **suspect** | RSKIP-412 is BASEFEE, which is EIP-3198 (per `ConsensusRule.java` comment), not EIP-1559. No 1559 fee market. RSKIP-543/545/546 (typed tx / Type 2) are Draft. |
| [1679](https://eips.ethereum.org/EIPS/eip-1679) | Hardfork Meta: Istanbul | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1716](https://eips.ethereum.org/EIPS/eip-1716) | Hardfork Meta: Petersburg | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [1820](https://eips.ethereum.org/EIPS/eip-1820) | Pseudo-introspection Registry Contract | ERC |  | Not Yet Adopted |  |  |  | **suspect** | RSKIP-148 (ERC1820 registry) is Adopted (DApp layer). |
| [1884](https://eips.ethereum.org/EIPS/eip-1884) | Repricing for trie-size-dependent opcodes | Core | Istanbul | Won't Be Adopted |  |  | Storage rent does not require this change | **suspect** | SELFBALANCE (part of EIP-1884) is RSKIP-151, Papyrus (`VM.java:1962`). Should be Partially Adopted. |
| [1967](https://eips.ethereum.org/EIPS/eip-1967) | Proxy Storage Slots | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2028](https://eips.ethereum.org/EIPS/eip-2028) | Transaction data gas cost reduction | Core | Istanbul | Adopted | [400](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP400.md) | Calldata gas cost reduction |  | **ok** | RSKIP-400, Arrowhead. |
| [2098](https://eips.ethereum.org/EIPS/eip-2098) | Compact Signature Representation | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2124](https://eips.ethereum.org/EIPS/eip-2124) | Fork identifier for chain compatibility checks | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2135](https://eips.ethereum.org/EIPS/eip-2135) | Consumable Interface (Tickets, etc) | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2159](https://eips.ethereum.org/EIPS/eip-2159) | Common Prometheus Metrics Names for Clients | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2200](https://eips.ethereum.org/EIPS/eip-2200) | Structured Definitions for Net Gas Metering | Core | Istanbul | Partially Adopted |  |  | Only SELFBALANCE implemented | **wrong** | Note says 'Only SELFBALANCE implemented', but SELFBALANCE is from EIP-1884. No evidence of 2200 net gas metering (`GasCost.SSTORE` flat). |
| [2228](https://eips.ethereum.org/EIPS/eip-2228) | Canonicalize the name of network ID 1 and chain ID 1 | Informational |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2255](https://eips.ethereum.org/EIPS/eip-2255) | Wallet Permissions System | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2309](https://eips.ethereum.org/EIPS/eip-2309) | ERC-721 Consecutive Transfer Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2364](https://eips.ethereum.org/EIPS/eip-2364) | eth/64: forkid-extended protocol handshake | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2384](https://eips.ethereum.org/EIPS/eip-2384) | Muir Glacier Difficulty Bomb Delay | Core | Muir Glacier | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [2387](https://eips.ethereum.org/EIPS/eip-2387) | Hardfork Meta: Muir Glacier | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2464](https://eips.ethereum.org/EIPS/eip-2464) | eth/65: transaction announcements and retrievals | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2481](https://eips.ethereum.org/EIPS/eip-2481) | eth/66 request identifier | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2535](https://eips.ethereum.org/EIPS/eip-2535) | Diamonds, Multi-Facet Proxy | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2565](https://eips.ethereum.org/EIPS/eip-2565) | ModExp Gas Cost | Core | Berlin | Not Yet Adopted |  |  | Is not implemented due to RSK's modexp | **unverified** |  |
| [2612](https://eips.ethereum.org/EIPS/eip-2612) | Permit Extension for EIP-20 Signed Approvals | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2678](https://eips.ethereum.org/EIPS/eip-2678) | Revised Ethereum Smart Contract Packaging Standard (EthPM v3) | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2681](https://eips.ethereum.org/EIPS/eip-2681) | Limit account nonce to 2^64-1 | Core |  | Not Yet Adopted |  |  |  | **unverified** |  |
| [2696](https://eips.ethereum.org/EIPS/eip-2696) | JavaScript `request` method RPC transport | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2700](https://eips.ethereum.org/EIPS/eip-2700) | JavaScript Provider Event Emitter | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2718](https://eips.ethereum.org/EIPS/eip-2718) | Typed Transaction Envelope | Core | Berlin | Not Yet Adopted |  |  | Is not implemented can be done in the future. Required for 7702 | **ok** | Still not active; RSKIP-543 (Typed Tx Envelope) and RSKIP-546 (Type 1/2) are Draft. |
| [2771](https://eips.ethereum.org/EIPS/eip-2771) | Secure Protocol for Native Meta Transactions | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2929](https://eips.ethereum.org/EIPS/eip-2929) | Gas cost increases for state access opcodes | Core | Berlin | Not Yet Adopted |  |  | Is not implemented due to storage rent | **ok** | Not active; see RSKIP-239 (reprice trie read opcodes, references 2929). |
| [2930](https://eips.ethereum.org/EIPS/eip-2930) | Optional access lists | Core | Berlin | Not Yet Adopted |  |  | It not necessary until 2929 is adopted | **unverified** |  |
| [2976](https://eips.ethereum.org/EIPS/eip-2976) | Typed Transactions over Gossip | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2981](https://eips.ethereum.org/EIPS/eip-2981) | NFT Royalty Standard | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [2982](https://eips.ethereum.org/EIPS/eip-2982) | Serenity Phase 0 | Informational |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [3156](https://eips.ethereum.org/EIPS/eip-3156) | Flash Loans | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [3198](https://eips.ethereum.org/EIPS/eip-3198) | BASEFEE opcode | Core | London | Not Yet Adopted |  |  |  | **wrong** | BASEFEE implemented by RSKIP-412, Arrowhead (`VM.java:1950`). Should be Adopted / RSKIP-412. |
| [3448](https://eips.ethereum.org/EIPS/eip-3448) | MetaProxy Standard | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [3475](https://eips.ethereum.org/EIPS/eip-3475) | Abstract Storage Bonds | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [3525](https://eips.ethereum.org/EIPS/eip-3525) | Semi-Fungible Token | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [3529](https://eips.ethereum.org/EIPS/eip-3529) | Reduction in refunds | Core | London | Not Yet Adopted |  |  |  | **ok** | Not adopted: pre-London refunds still in `GasCost.java` (REFUND_SSTORE 15000, SUICIDE_REFUND 24000). |
| [3541](https://eips.ethereum.org/EIPS/eip-3541) | Reject new contract code starting with the 0xEF byte | Core | London | Not Yet Adopted |  |  | Required for 7702 | **wrong** | RSKIP-544 (Adopted), Vetiver (height 8,804,200). Post-dates the CSV. |
| [3554](https://eips.ethereum.org/EIPS/eip-3554) | Difficulty Bomb Delay to December 2021 | Core | London | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [3607](https://eips.ethereum.org/EIPS/eip-3607) | Reject transactions from senders with deployed code | Core |  | Not Yet Adopted |  |  | Required for 7702 | **unverified** |  |
| [3643](https://eips.ethereum.org/EIPS/eip-3643) | T-REX - Token for Regulated EXchanges | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [3651](https://eips.ethereum.org/EIPS/eip-3651) | Warm COINBASE | Core | Shanghai | Not Yet Adopted |  |  |  | **unverified** |  |
| [3668](https://eips.ethereum.org/EIPS/eip-3668) | CCIP Read: Secure offchain data retrieval | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [3675](https://eips.ethereum.org/EIPS/eip-3675) | Upgrade consensus to Proof-of-Stake | Core | Paris | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [3855](https://eips.ethereum.org/EIPS/eip-3855) | PUSH0 instruction | Core | Shanghai | Adopted | [398](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP398.md) | PUSH0 instruction |  | **ok** | RSKIP-398, Arrowhead (`VM.java:2064`). |
| [3860](https://eips.ethereum.org/EIPS/eip-3860) | Limit and meter initcode | Core | Shanghai | Not Yet Adopted |  |  |  | **wrong** | Initcode limit/metering: RSKIP-438 (Adopted), Lovell. Should be Adopted. |
| [4345](https://eips.ethereum.org/EIPS/eip-4345) | Difficulty Bomb Delay to June 2022 | Core | Arrow Glacier | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [4399](https://eips.ethereum.org/EIPS/eip-4399) | Supplant DIFFICULTY opcode with PREVRANDAO | Core | Paris | Not Yet Adopted |  |  |  | **unverified** |  |
| [4400](https://eips.ethereum.org/EIPS/eip-4400) | EIP-721 Consumable Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4519](https://eips.ethereum.org/EIPS/eip-4519) | Non-Fungible Tokens Tied to Physical Assets | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4626](https://eips.ethereum.org/EIPS/eip-4626) | Tokenized Vaults | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4736](https://eips.ethereum.org/EIPS/eip-4736) | Consensus Layer Withdrawal Protection | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4788](https://eips.ethereum.org/EIPS/eip-4788) | Beacon block root in the EVM | Core | Cancun | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [4804](https://eips.ethereum.org/EIPS/eip-4804) | Web3 URL to EVM Call Message Translation | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4834](https://eips.ethereum.org/EIPS/eip-4834) | Hierarchical Domains | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4844](https://eips.ethereum.org/EIPS/eip-4844) | Shard Blob Transactions | Core | Cancun | Not Yet Adopted |  |  |  | **ok** | Not active; RSKIP-558 (Blob txs) is Draft. |
| [4881](https://eips.ethereum.org/EIPS/eip-4881) | Deposit Contract Snapshot Interface | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4895](https://eips.ethereum.org/EIPS/eip-4895) | Beacon chain push withdrawals as operations | Core | Shanghai | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [4906](https://eips.ethereum.org/EIPS/eip-4906) | EIP-721 Metadata Update Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4907](https://eips.ethereum.org/EIPS/eip-4907) | Rental NFT, an Extension of EIP-721 | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4910](https://eips.ethereum.org/EIPS/eip-4910) | Royalty Bearing NFTs | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4938](https://eips.ethereum.org/EIPS/eip-4938) | eth/67 - Removal of GetNodeData | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [4955](https://eips.ethereum.org/EIPS/eip-4955) | Vendor Metadata Extension for NFTs | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5006](https://eips.ethereum.org/EIPS/eip-5006) | Rental NFT, NFT User Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5007](https://eips.ethereum.org/EIPS/eip-5007) | Time NFT, ERC-721 Time Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5023](https://eips.ethereum.org/EIPS/eip-5023) | Shareable Non-Fungible Token | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5133](https://eips.ethereum.org/EIPS/eip-5133) | Delaying Difficulty Bomb to mid-September 2022 | Core | Gray Glacier | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [5169](https://eips.ethereum.org/EIPS/eip-5169) | Client Script URI for Token Contracts | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5192](https://eips.ethereum.org/EIPS/eip-5192) | Minimal Soulbound NFTs | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5202](https://eips.ethereum.org/EIPS/eip-5202) | Blueprint contract format | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5219](https://eips.ethereum.org/EIPS/eip-5219) | Contract Resource Requests | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5267](https://eips.ethereum.org/EIPS/eip-5267) | Retrieval of EIP-712 domain | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5313](https://eips.ethereum.org/EIPS/eip-5313) | Light Contract Ownership | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5375](https://eips.ethereum.org/EIPS/eip-5375) | NFT Author Information and Consent | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5380](https://eips.ethereum.org/EIPS/eip-5380) | ERC-721 Entitlement Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5484](https://eips.ethereum.org/EIPS/eip-5484) | Consensual Soulbound Tokens | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5489](https://eips.ethereum.org/EIPS/eip-5489) | NFT Hyperlink Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5507](https://eips.ethereum.org/EIPS/eip-5507) | Refundable Tokens | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5521](https://eips.ethereum.org/EIPS/eip-5521) | Referable NFT | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5528](https://eips.ethereum.org/EIPS/eip-5528) | Refundable Fungible Token | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5564](https://eips.ethereum.org/EIPS/eip-5564) | Stealth Addresses | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5570](https://eips.ethereum.org/EIPS/eip-5570) | Digital Receipt Non-Fungible Tokens | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5585](https://eips.ethereum.org/EIPS/eip-5585) | ERC-721 NFT Authorization | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5606](https://eips.ethereum.org/EIPS/eip-5606) | Multiverse NFTs | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5615](https://eips.ethereum.org/EIPS/eip-5615) | ERC-1155 Supply Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5646](https://eips.ethereum.org/EIPS/eip-5646) | Token State Fingerprint | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5656](https://eips.ethereum.org/EIPS/eip-5656) | MCOPY - Memory copying instruction | Core | Cancun | Not Yet Adopted |  |  |  | **wrong** | MCOPY: RSKIP-445, Lovell (`VM.java:2107`). Should be Adopted. |
| [5679](https://eips.ethereum.org/EIPS/eip-5679) | Token Minting and Burning | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5725](https://eips.ethereum.org/EIPS/eip-5725) | Transferable Vesting NFT | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5732](https://eips.ethereum.org/EIPS/eip-5732) | Commit Interface | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5749](https://eips.ethereum.org/EIPS/eip-5749) | The 'window.evmproviders' object | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5750](https://eips.ethereum.org/EIPS/eip-5750) | General Extensibility for Method Behaviors | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5757](https://eips.ethereum.org/EIPS/eip-5757) | Process for Approving External Resources | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5773](https://eips.ethereum.org/EIPS/eip-5773) | Context-Dependent Multi-Asset Tokens | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [5793](https://eips.ethereum.org/EIPS/eip-5793) | eth/68 - Add tx type to tx announcement | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6049](https://eips.ethereum.org/EIPS/eip-6049) | Deprecate SELFDESTRUCT | Meta | Shanghai | Not Yet Adopted |  |  |  | **n/a** |  |
| [6059](https://eips.ethereum.org/EIPS/eip-6059) | Parent-Governed Nestable Non-Fungible Tokens | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6066](https://eips.ethereum.org/EIPS/eip-6066) | Signature Validation Method for NFTs | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6105](https://eips.ethereum.org/EIPS/eip-6105) | No Intermediary NFT Trading Protocol | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6122](https://eips.ethereum.org/EIPS/eip-6122) | Forkid checks based on timestamps | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6147](https://eips.ethereum.org/EIPS/eip-6147) | Guard of NFT/SBT, an Extension of ERC-721 | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6150](https://eips.ethereum.org/EIPS/eip-6150) | Hierarchical NFTs | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6220](https://eips.ethereum.org/EIPS/eip-6220) | Composable NFTs utilizing Equippable Parts | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6239](https://eips.ethereum.org/EIPS/eip-6239) | Semantic Soulbound Tokens | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6381](https://eips.ethereum.org/EIPS/eip-6381) | Public Non-Fungible Token Emote Repository | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6454](https://eips.ethereum.org/EIPS/eip-6454) | Minimal Transferable NFT detection interface | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6492](https://eips.ethereum.org/EIPS/eip-6492) | Signature Validation for Predeploy Contracts | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6538](https://eips.ethereum.org/EIPS/eip-6538) | Stealth Meta-Address Registry | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6672](https://eips.ethereum.org/EIPS/eip-6672) | Multi-redeemable NFTs | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6780](https://eips.ethereum.org/EIPS/eip-6780) | SELFDESTRUCT only in same transaction | Core | Cancun | Not Yet Adopted |  |  |  | **ok** | Not adopted (no same-tx restriction visible in `VM.doSUICIDE`); light check. |
| [6808](https://eips.ethereum.org/EIPS/eip-6808) | Fungible Key Bound Token | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6809](https://eips.ethereum.org/EIPS/eip-6809) | Non-Fungible Key Bound Token | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6953](https://eips.ethereum.org/EIPS/eip-6953) | Network Upgrade Activation Triggers | Informational |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6963](https://eips.ethereum.org/EIPS/eip-6963) | Multi Injected Provider Discovery | Interface |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [6982](https://eips.ethereum.org/EIPS/eip-6982) | Efficient Default Lockable Tokens | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7007](https://eips.ethereum.org/EIPS/eip-7007) | Verifiable AI-Generated Content Token | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7044](https://eips.ethereum.org/EIPS/eip-7044) | Perpetually Valid Signed Voluntary Exits | Core | Cancun | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [7045](https://eips.ethereum.org/EIPS/eip-7045) | Increase max attestation inclusion slot | Core | Cancun | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [7053](https://eips.ethereum.org/EIPS/eip-7053) | Interoperable Digital Media Indexing | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7066](https://eips.ethereum.org/EIPS/eip-7066) | Lockable Extension for ERC-721 | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7092](https://eips.ethereum.org/EIPS/eip-7092) | Financial Bonds | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7160](https://eips.ethereum.org/EIPS/eip-7160) | ERC-721 Multi-Metadata Extension | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7201](https://eips.ethereum.org/EIPS/eip-7201) | Namespaced Storage Layout | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7231](https://eips.ethereum.org/EIPS/eip-7231) | Identity-aggregated NFT | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7329](https://eips.ethereum.org/EIPS/eip-7329) | ERC/EIP Repository split | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7401](https://eips.ethereum.org/EIPS/eip-7401) | Parent-Governed Non-Fungible Tokens Nesting | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7409](https://eips.ethereum.org/EIPS/eip-7409) | Public Non-Fungible Tokens Emote Repository | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7432](https://eips.ethereum.org/EIPS/eip-7432) | Non-Fungible Token Roles | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7439](https://eips.ethereum.org/EIPS/eip-7439) | Prevent ticket touting | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7514](https://eips.ethereum.org/EIPS/eip-7514) | Add Max Epoch Churn Limit | Core | Cancun | Not Yet Adopted |  |  |  | **n/a** | Specific to Ethereum PoW difficulty bomb or PoS beacon chain; doesn't apply to RSK. |
| [7516](https://eips.ethereum.org/EIPS/eip-7516) | BLOBBASEFEE instruction | Core | Cancun | Not Yet Adopted |  |  |  | **unverified** |  |
| [7528](https://eips.ethereum.org/EIPS/eip-7528) | ETH (Native Asset) Address Convention | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7535](https://eips.ethereum.org/EIPS/eip-7535) | Native Asset ERC-4626 Tokenized Vault | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7540](https://eips.ethereum.org/EIPS/eip-7540) | Asynchronous ERC-4626 Tokenized Vaults | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7568](https://eips.ethereum.org/EIPS/eip-7568) | Hardfork Meta Backfill - Berlin to Shapella | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7569](https://eips.ethereum.org/EIPS/eip-7569) | Hardfork Meta - Dencun | Meta |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7575](https://eips.ethereum.org/EIPS/eip-7575) | Multi-Asset ERC-4626 Vaults | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7588](https://eips.ethereum.org/EIPS/eip-7588) | Blob Transactions Metadata JSON Schema | ERC |  | Not Yet Adopted |  |  |  | **n/a** |  |
| [7636](https://eips.ethereum.org/EIPS/eip-7636) | Extension of EIP-778 for "client" ENR Entry | Networking |  | Not Yet Adopted |  |  |  | **n/a** |  |

## 3. EIP-8141 dependencies not in the CSV

| EIP | Title | Status (eips.ethereum.org) | Category | RSK |
|---|---|---|---|---|
| [2780](https://eips.ethereum.org/EIPS/eip-2780) | Resource-Based Intrinsic Transaction Gas | Last Call | Core | no RSKIP found |
| [7594](https://eips.ethereum.org/EIPS/eip-7594) | PeerDAS - Peer Data Availability Sampling | Final | Core | referenced by RSKIP-558 (Draft) |
| [7702](https://eips.ethereum.org/EIPS/eip-7702) | Set Code for EOAs | Final | Core | RSKIP-545 (Draft) |
| [7708](https://eips.ethereum.org/EIPS/eip-7708) | ETH Transfers Emit a Log | Last Call | Core | no RSKIP found |
| [7778](https://eips.ethereum.org/EIPS/eip-7778) | Block Gas Accounting without Refunds | Last Call | Core | no RSKIP found |
| [7825](https://eips.ethereum.org/EIPS/eip-7825) | Transaction Gas Limit Cap | Final | Core | no RSKIP found |
| [7976](https://eips.ethereum.org/EIPS/eip-7976) | Increase Calldata Floor Cost | Last Call | Core | no RSKIP found |
| [8037](https://eips.ethereum.org/EIPS/eip-8037) | State Creation Gas Cost Increase | Last Call | Core | no RSKIP found |

