# Ethereum EIPs by hard fork vs Rootstock

Task 2 in `readme.md`: every Core EIP in each Ethereum hard fork, its Rootstock status, the RSK network upgrade and mainnet activation height, and the evidence. Code links point at [`rsksmart/rskj@1e95a3b03`](https://github.com/rsksmart/rskj/tree/1e95a3b03) (origin/master, 2026-10-16). RSKIP statuses come from `rsksmart/RSKIPs` `a389ec2`, plus open PR heads as of 2026-10-28 (#701 RSKIP-701 `658944d`, #708 RSKIP-543, #709 RSKIP-546, #710 RSKIP-545 `4a8a1d9`); fork lists come from the hardfork meta EIPs, linked per section.

**RSK status:** **Yes** = fully active · **Partial** = some of it active (the evidence says which part) · **Adapted** = same goal, RSK-specific design · **No** = not active · **N/A** = doesn't apply to Rootstock (beacon chain, difficulty bomb, reverted) · **?** = not verified · **Partial (WIP)** = only covered by a Draft RSKIP that is work in progress; nothing active yet. Rows marked **Unverified** were taken on trust (a brief citation, not a rule-by-rule check) and show **?** until validated; the claimed status is kept in the evidence. The *Under assumptions* column applies the project assumptions in `readme.md` where they change the picture.

**No RSKIP** means no RSKIP on any of the 95 branches of `rsksmart/RSKIPs` cites the EIP or its feature, and rskj `master` has no matching code (checked 2026-10-28, with a control search that does find EIP-3198 in RSKIP-412).

## Summary

| Fork | Core EIPs | Yes | Partial | Partial (WIP) | Adapted | No | N/A | ? |
|---|---|---|---|---|---|---|---|---|
| Homestead | 2 | 2 |  |  |  |  |  |  |
| Tangerine Whistle | 1 |  | 1 |  |  |  |  |  |
| Spurious Dragon | 4 | 3 | 1 |  |  |  |  |  |
| Byzantium | 9 | 7 |  |  | 1 |  | 1 |  |
| Constantinople | 5 | 2 | 1 |  |  |  | 2 |  |
| Istanbul | 6 | 4 | 1 |  |  |  |  | 1 |
| Muir Glacier | 1 |  |  |  |  |  | 1 |  |
| Berlin | 4 |  |  |  |  | 3 |  | 1 |
| London | 5 | 2 |  | 1 |  |  | 1 | 1 |
| Arrow Glacier | 1 |  |  |  |  |  | 1 |  |
| Gray Glacier | 1 |  |  |  |  |  | 1 |  |
| Paris (The Merge) | 2 |  |  |  |  |  | 2 |  |
| Shanghai | 5 | 1 |  |  |  |  | 2 | 2 |
| Cancun (Dencun) | 6 | 2 |  |  |  | 3 | 1 |  |
| Prague (Pectra) | 10 |  |  |  |  | 5 | 5 |  |
| Osaka (Fusaka) | 9 |  |  |  |  | 7 | 1 | 1 |
| Amsterdam (Glamsterdam, scheduled) | 18 |  |  |  |  | 12 | 6 |  |
| Retroactive | 4 |  | 1 |  |  | 2 |  | 1 |
| **Total** | **93** | **23** | **5** | **1** | **1** | **32** | **24** | **7** |

Of the 69 EIPs that apply to Rootstock, 23 are fully active, 6 are partial or adapted, 1 is partial only through Draft RSKIP work, 32 are missing, and 7 still need verifying. Rootstock tracks Ethereum's EVM opcode and precompile additions closely up to Cancun (except blobs), but appears to have skipped the gas-model changes since Berlin (2929, 2930, 3529, 2200, 1884 repricing; several still unverified) and has no typed transactions.

## Homestead

Meta: [EIP-606](https://eips.ethereum.org/EIPS/eip-606).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [2](https://eips.ethereum.org/EIPS/eip-2) | Homestead Hard-fork Changes | **Yes** | Lovell | 7,338,024 | Complete since Lovell. From genesis: (1) contract-creation tx cost 53000 [`GasCost.java:84`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/GasCost.java#L84); (2) low-s rule [`Transaction.java:321`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/Transaction.java#L321); (3) top-level creates roll back on failed code deposit [`TransactionExecutor.java:471`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L471). Internal CREATE/CREATE2 left an empty account until [RSKIP-453](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP453.md) (Lovell) ([`Program.java:738`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L738), [`Program.java:756`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L756)). (4) Difficulty formula: N/A, RSK uses its own. |  |
| [7](https://eips.ethereum.org/EIPS/eip-7) | DELEGATECALL | **Yes** | Genesis | 0 | DELEGATECALL [`OpCode.java:669`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/OpCode.java#L669); value handling fixed by [RSKIP-103](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP103.md) (Orchid 0.6.0). |  |

## Tangerine Whistle

Meta: [EIP-608](https://eips.ethereum.org/EIPS/eip-608).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [150](https://eips.ethereum.org/EIPS/eip-150) | Gas cost changes for IO-heavy operations | **Partial** | Genesis | 0 | Gas repricing matches: CALL 700, BALANCE 400, EXTCODESIZE/COPY 700, SLOAD 200, SELFDESTRUCT 5000 ([`GasCost.java:52`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/GasCost.java#L52)). **Divergence:** no 63/64 rule; the callee gets min(remaining, requested) gas, so a call can forward all remaining gas ([`VM.java:1659`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1659)); CREATE also passes all remaining gas ([`Program.java:523`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L523)). `getCallStackDepth` added by [RSKIP-203](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP203.md) (Arrowhead). |  |

## Spurious Dragon

Meta: [EIP-607](https://eips.ethereum.org/EIPS/eip-607).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [155](https://eips.ethereum.org/EIPS/eip-155) | Simple replay attack protection | **Yes** | Genesis | 0 | Signing payload is rlp(..., chainId, 0, 0) ([`Transaction.java:468`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/Transaction.java#L468)); v = chainId*2 + 35 + recId ([`Transaction.java:445`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/Transaction.java#L445)); txs accepted with chain ID 0 or the network's ([`Transaction.java:325`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/Transaction.java#L325)). Mainnet chain ID 30. |  |
| [160](https://eips.ethereum.org/EIPS/eip-160) | EXP cost increase | **Yes** | Genesis | 0 | `EXP_BYTE_GAS = 50` [`GasCost.java:90`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/GasCost.java#L90). |  |
| [161](https://eips.ethereum.org/EIPS/eip-161) | State trie clearing (invariant-preserving alternative) | **Partial** | Wasabi | 1,591,000 | Only rule (a), and only for CREATE/CREATE2: new contracts start at nonce 1 via [RSKIP-125](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP125.md) (Wasabi) ([`Program.java:592`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L592)); contract-creation txs still start at 0 ([`TransactionExecutor.java:403`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L403)). (b) 25000 new-account gas is charged even for zero value ([`VM.java:1734`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1734), [`VM.java:1797`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1797)). (c) A zero-value transfer creates an empty account ([`MutableRepository.java:322`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/db/MutableRepository.java#L322)). (d) No end-of-tx deletion of touched empty accounts; only SUICIDE deletions ([`TransactionExecutor.java:622`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L622)). |  |
| [170](https://eips.ethereum.org/EIPS/eip-170) | Contract code size limit | **Yes** | Genesis | 0 | `MAX_CONTRACT_SIZE = 0x6000` [`Constants.java:55`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/config/Constants.java#L55), enforced in [`TransactionExecutor.java:529`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L529). |  |

## Byzantium

Meta: [EIP-609](https://eips.ethereum.org/EIPS/eip-609).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [100](https://eips.ethereum.org/EIPS/eip-100) | Change difficulty adjustment to target mean block time including uncles | **Adapted** | Genesis | 0 | Rootstock uses its own uncle-aware difficulty formula ([`DifficultyCalculator.java:77`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/core/DifficultyCalculator.java#L77)), not EIP-100's. |  |
| [140](https://eips.ethereum.org/EIPS/eip-140) | REVERT instruction | **Yes** | Genesis | 0 | REVERT (no activation gate, [`VM.java:2133`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L2133)) returns data and flags the result reverted ([`VM.java:1752`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1752)); a reverted child call rolls back state and refunds its remaining gas ([`Program.java:962`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L962)); a reverted top-level tx rolls back without forfeiting leftover gas ([`TransactionExecutor.java:471`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L471)). |  |
| [196](https://eips.ethereum.org/EIPS/eip-196) | Precompiled contracts for addition and scalar multiplication on the elliptic curve alt_bn128 | **Yes** | Papyrus | 2,392,700 | alt_bn128 ADD/MUL enabled by [RSKIP-137](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP137.md) (Papyrus) ([`PrecompiledContracts.java:145`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/PrecompiledContracts.java#L145)). |  |
| [197](https://eips.ethereum.org/EIPS/eip-197) | Precompiled contracts for optimal ate pairing check on the elliptic curve alt_bn128 | **Yes** | Papyrus | 2,392,700 | alt_bn128 pairing enabled by [RSKIP-137](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP137.md) (Papyrus). |  |
| [198](https://eips.ethereum.org/EIPS/eip-198) | Big integer modular exponentiation | **Yes** | Genesis | 0 | MODEXP is a genesis precompile; EIP-198 pricing (`GQUAD_DIVISOR = 20`, [`PrecompiledContracts.java:462`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/PrecompiledContracts.java#L462)). |  |
| [211](https://eips.ethereum.org/EIPS/eip-211) | New opcodes: RETURNDATASIZE and RETURNDATACOPY | **Yes** | Iris | 3,614,800 | RETURNDATASIZE/COPY present with no activation gate ([`VM.java:1927`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1927)); out-of-bounds copy throws ([`VM.java:974`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L974)). Complete since [RSKIP-171](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP171.md) (Iris), which states full EIP-211 compatibility by clearing the buffer in call-like opcodes that don't create a frame ([`Program.java:915`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L915)). |  |
| [214](https://eips.ethereum.org/EIPS/eip-214) | New opcode STATICCALL | **Yes** | Orchid | 729,000 | STATICCALL gated by [RSKIP-91](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP91.md) (Orchid) ([`VM.java:2126`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L2126)). |  |
| [649](https://eips.ethereum.org/EIPS/eip-649) | Metropolis Difficulty Bomb Delay and Block Reward Reduction | **N/A** |  |  | Ethereum difficulty-bomb schedule; Rootstock has no difficulty bomb. |  |
| [658](https://eips.ethereum.org/EIPS/eip-658) | Embedding transaction status code in receipts | **Yes** | Genesis | 0 | Receipt status byte [`TransactionReceipt.java:45`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionReceipt.java#L45). |  |

## Constantinople

Meta: [EIP-1013](https://eips.ethereum.org/EIPS/eip-1013).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [145](https://eips.ethereum.org/EIPS/eip-145) | Bitwise shifting instructions in EVM | **Yes** | Wasabi | 1,591,000 | SHL/SHR/SAR via [RSKIP-120](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP120.md) (Wasabi) ([`VM.java:1870`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1870)). |  |
| [1014](https://eips.ethereum.org/EIPS/eip-1014) | Skinny CREATE2 | **Yes** | Wasabi | 1,591,000 | CREATE2 via [RSKIP-125](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP125.md) (Wasabi) ([`VM.java:2115`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L2115)). |  |
| [1052](https://eips.ethereum.org/EIPS/eip-1052) | EXTCODEHASH opcode | **Partial** | Iris | 3,614,800 | EXTCODEHASH via [RSKIP-140](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP140.md) (Papyrus), corrected by [RSKIP-169](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP169.md) (Iris): gas 400, 0 for non-existent accounts, empty-code hash for accounts without code ([`MutableRepository.java:217`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/db/MutableRepository.java#L217)). Deviation: EIP-1052 returns 0 for EIP-161 *empty* accounts; RSK returns the empty-code hash, and RSK does create empty accounts (161 rule c). |  |
| [1234](https://eips.ethereum.org/EIPS/eip-1234) | Constantinople Difficulty Bomb Delay and Block Reward Adjustment | **N/A** |  |  | Ethereum difficulty-bomb schedule; Rootstock has no difficulty bomb. |  |
| [1283](https://eips.ethereum.org/EIPS/eip-1283) | Net gas metering for SSTORE without dirty maps | **N/A** |  |  | Reverted in Ethereum by Petersburg before activation. |  |

## Petersburg

Meta: [EIP-1716](https://eips.ethereum.org/EIPS/eip-1716). Only removes EIP-1283 from Constantinople; nothing to adopt.

## Istanbul

Meta: [EIP-1679](https://eips.ethereum.org/EIPS/eip-1679).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [152](https://eips.ethereum.org/EIPS/eip-152) | Add BLAKE2 compression function `F` precompile | **Yes** | Iris | 3,614,800 | BLAKE2F via [RSKIP-153](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP153.md) (Iris); input validation tightened by [RSKIP-552](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP552.md) (Vetiver). |  |
| [1108](https://eips.ethereum.org/EIPS/eip-1108) | Reduce alt_bn128 precompile gas costs | **Yes** | Papyrus | 2,392,700 | All EIP-1108 prices, with no activation gate: ADD 150 ([`BN128Addition.java:53`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/pcc/altBN128/BN128Addition.java#L53)), MUL 6000 ([`BN128Multiplication.java:53`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/pcc/altBN128/BN128Multiplication.java#L53)), pairing 45000 + 34000/pair ([`BN128Pairing.java:58`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/pcc/altBN128/BN128Pairing.java#L58)). The precompiles only exist since [RSKIP-137](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP137.md) (Papyrus), so RSK never charged pre-1108 prices. |  |
| [1344](https://eips.ethereum.org/EIPS/eip-1344) | ChainID opcode | **Yes** | Papyrus | 2,392,700 | CHAINID via [RSKIP-152](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP152.md) (Papyrus) ([`VM.java:1956`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1956)). |  |
| [1884](https://eips.ethereum.org/EIPS/eip-1884) | Repricing for trie-size-dependent opcodes | **Partial** | Papyrus | 2,392,700 | Only SELFBALANCE, via [RSKIP-151](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP151.md) (Papyrus) ([`VM.java:1962`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1962)); SLOAD/BALANCE/EXTCODEHASH repricing not adopted. |  |
| [2028](https://eips.ethereum.org/EIPS/eip-2028) | Transaction data gas cost reduction | **Yes** | Arrowhead | 6,223,700 | Non-zero calldata byte costs 16 (was 68) via [RSKIP-400](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP400.md) (Arrowhead) ([`Transaction.java:230`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/Transaction.java#L230), [`GasCost.java:80`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/GasCost.java#L80)). |  |
| [2200](https://eips.ethereum.org/EIPS/eip-2200) | Structured Definitions for Net Gas Metering | **?** |  |  | **Unverified** (claimed No): Flat SSTORE costs ([`GasCost.java:39`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/GasCost.java#L39)). |  |

## Muir Glacier

Meta: [EIP-2387](https://eips.ethereum.org/EIPS/eip-2387).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [2384](https://eips.ethereum.org/EIPS/eip-2384) | Muir Glacier Difficulty Bomb Delay | **N/A** |  |  | Ethereum difficulty-bomb schedule; Rootstock has no difficulty bomb. |  |

## Berlin

Meta: [EIP-7568](https://eips.ethereum.org/EIPS/eip-7568).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [2565](https://eips.ethereum.org/EIPS/eip-2565) | ModExp Gas Cost | **No** |  |  | MODEXP keeps EIP-198 pricing (`GQUAD_DIVISOR = 20`). |  |
| [2718](https://eips.ethereum.org/EIPS/eip-2718) | Typed Transaction Envelope | **No** |  |  | No typed txs in rskj. [RSKIP-543](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP543.md) Draft ([PR #708](https://github.com/rsksmart/RSKIPs/pull/708)). | Assumed active |
| [2929](https://eips.ethereum.org/EIPS/eip-2929) | Gas cost increases for state access opcodes | **?** |  |  | **Unverified** (claimed No): Not adopted; project decision not to adopt (`readme.md` assumption 3). | Won't (project decision) |
| [2930](https://eips.ethereum.org/EIPS/eip-2930) | Optional access lists | **No** |  |  | No access-list code in rskj. [RSKIP-546](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP546.md) ([PR #709](https://github.com/rsksmart/RSKIPs/pull/709), Draft) only specifies the access list's RLP shape. | Partial: RSKIP-546: access list RLP shape only; charged gas, no impact on execution. |

## London

Meta: [EIP-7568](https://eips.ethereum.org/EIPS/eip-7568).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [1559](https://eips.ethereum.org/EIPS/eip-1559) | Fee market change for ETH 1.0 chain | **Partial (WIP)** |  |  | Partial through [RSKIP-546](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP546.md) ([PR #709](https://github.com/rsksmart/RSKIPs/pull/709), Draft): Type-2 encoding only; base fee effectively zero, no dynamic fee market. | Partial: Type-2 encoding, zero base fee |
| [3198](https://eips.ethereum.org/EIPS/eip-3198) | BASEFEE opcode | **Yes** | Arrowhead | 6,223,700 | BASEFEE via [RSKIP-412](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP412.md) (Arrowhead) ([`VM.java:1950`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1950)); returns the block's `minimumGasPrice` ([`VM.java:1101`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L1101)). |  |
| [3529](https://eips.ethereum.org/EIPS/eip-3529) | Reduction in refunds | **?** |  |  | **Unverified** (claimed No): Pre-London refunds ([`GasCost.java:61`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/GasCost.java#L61): REFUND_SSTORE 15000, SUICIDE_REFUND 24000). |  |
| [3541](https://eips.ethereum.org/EIPS/eip-3541) | Reject new contract code starting with the 0xEF byte | **Yes** | Vetiver | 8,804,200 | [RSKIP-544](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP544.md) (Vetiver), on both paths: CREATE/CREATE2 ([`Program.java:712`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L712)) and contract-creation txs ([`TransactionExecutor.java:541`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L541)). |  |
| [3554](https://eips.ethereum.org/EIPS/eip-3554) | Difficulty Bomb Delay to December 2021 | **N/A** |  |  | Ethereum difficulty-bomb schedule; Rootstock has no difficulty bomb. |  |

## Arrow Glacier

Meta: [EIP-7568](https://eips.ethereum.org/EIPS/eip-7568).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [4345](https://eips.ethereum.org/EIPS/eip-4345) | Difficulty Bomb Delay to June 2022 | **N/A** |  |  | Ethereum difficulty-bomb schedule; Rootstock has no difficulty bomb. |  |

## Gray Glacier

Meta: [EIP-7568](https://eips.ethereum.org/EIPS/eip-7568).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [5133](https://eips.ethereum.org/EIPS/eip-5133) | Delaying Difficulty Bomb to mid-September 2022 | **N/A** |  |  | Ethereum difficulty-bomb schedule; Rootstock has no difficulty bomb. |  |

## Paris (The Merge)

Meta: [EIP-7568](https://eips.ethereum.org/EIPS/eip-7568).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [3675](https://eips.ethereum.org/EIPS/eip-3675) | Upgrade consensus to Proof-of-Stake | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [4399](https://eips.ethereum.org/EIPS/eip-4399) | Supplant DIFFICULTY opcode with PREVRANDAO | **N/A** |  |  | Rootstock is merge-mined PoW; DIFFICULTY ([`OpCode.java:260`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/OpCode.java#L260)) keeps its meaning. |  |

## Shanghai

Meta: [EIP-7568](https://eips.ethereum.org/EIPS/eip-7568).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [3651](https://eips.ethereum.org/EIPS/eip-3651) | Warm COINBASE | **?** |  |  | **Unverified** (claimed No): Only meaningful with 2929. | Won't (needs 2929) |
| [3855](https://eips.ethereum.org/EIPS/eip-3855) | PUSH0 instruction | **Yes** | Arrowhead | 6,223,700 | PUSH0 via [RSKIP-398](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP398.md) (Arrowhead) ([`VM.java:2064`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L2064)). |  |
| [3860](https://eips.ethereum.org/EIPS/eip-3860) | Limit and meter initcode | **?** | Lovell | 7,338,024 | **Unverified** (claimed Yes): Initcode limit/metering via [RSKIP-438](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP438.md) (Lovell) (`MAX_INITCODE_SIZE`, [`Constants.java:56`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/config/Constants.java#L56)). |  |
| [4895](https://eips.ethereum.org/EIPS/eip-4895) | Beacon chain push withdrawals as operations | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [6049](https://eips.ethereum.org/EIPS/eip-6049) | Deprecate SELFDESTRUCT | **N/A** |  |  | Deprecation notice only; no consensus change. |  |

## Cancun (Dencun)

Meta: [EIP-7569](https://eips.ethereum.org/EIPS/eip-7569).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [1153](https://eips.ethereum.org/EIPS/eip-1153) | Transient storage opcodes | **Yes** | Lovell | 7,338,024 | TLOAD/TSTORE via [RSKIP-446](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP446.md) (Lovell) ([`VM.java:2041`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L2041)). |  |
| [4788](https://eips.ethereum.org/EIPS/eip-4788) | Beacon block root in the EVM | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [4844](https://eips.ethereum.org/EIPS/eip-4844) | Shard Blob Transactions | **No** |  |  | [RSKIP-558](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP558.md) Draft. | If needed (RSKIP-558) |
| [5656](https://eips.ethereum.org/EIPS/eip-5656) | MCOPY - Memory copying instruction | **Yes** | Lovell | 7,338,024 | MCOPY via [RSKIP-445](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP445.md) (Lovell) ([`VM.java:2107`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/VM.java#L2107)). |  |
| [6780](https://eips.ethereum.org/EIPS/eip-6780) | SELFDESTRUCT only in same transaction | **No** |  |  | Pre-Cancun SELFDESTRUCT: always deletes the account, with no same-tx check ([`Program.java:434`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L434)); burns the balance when the beneficiary is the contract itself ([`Program.java:428`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L428)); SUICIDE_REFUND still paid ([`TransactionExecutor.java:693`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L693)). No RSKIP. **Watch:** [RSKIP-701](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP701.md) ([PR #701](https://github.com/rsksmart/RSKIPs/pull/701), Draft) is proposed for Cardamom with 543/545/546 ([RSKIP-694](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP694.md)). It keeps RSKIP-545 delegated accounts and nonces on SELFDESTRUCT, diverging further from 6780. On Ethereum, [EIP-4758](https://eips.ethereum.org/EIPS/eip-4758) (Stagnant) would make SELFDESTRUCT balance-only. |  |
| [7516](https://eips.ethereum.org/EIPS/eip-7516) | BLOBBASEFEE instruction | **No** |  |  | Blob-specific; Rootstock has no blobs ([RSKIP-558](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP558.md) Draft). |  |

## Prague (Pectra)

Meta: [EIP-7600](https://eips.ethereum.org/EIPS/eip-7600).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [2537](https://eips.ethereum.org/EIPS/eip-2537) | Precompile for BLS12-381 curve operations | **No** |  |  | [RSKIP-188](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP188.md) (BLS12-381 precompiles) Withdrawn. |  |
| [2935](https://eips.ethereum.org/EIPS/eip-2935) | Serve historical block hashes from state | **No** |  |  | No RSKIP; BLOCKHASH not served from state. |  |
| [6110](https://eips.ethereum.org/EIPS/eip-6110) | Supply validator deposits on chain | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [7002](https://eips.ethereum.org/EIPS/eip-7002) | Execution layer triggerable withdrawals | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [7251](https://eips.ethereum.org/EIPS/eip-7251) | Increase the MAX_EFFECTIVE_BALANCE | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [7549](https://eips.ethereum.org/EIPS/eip-7549) | Move committee index outside Attestation | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [7623](https://eips.ethereum.org/EIPS/eip-7623) | Increase calldata cost | **No** |  |  | No RSKIP. |  |
| [7685](https://eips.ethereum.org/EIPS/eip-7685) | General purpose execution layer requests | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [7691](https://eips.ethereum.org/EIPS/eip-7691) | Blob throughput increase | **No** |  |  | Blob-specific; Rootstock has no blobs ([RSKIP-558](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP558.md) Draft). |  |
| [7702](https://eips.ethereum.org/EIPS/eip-7702) | Set Code for EOAs | **No** |  |  | [RSKIP-545](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP545.md) Draft ([PR #710](https://github.com/rsksmart/RSKIPs/pull/710)). | Assumed active |

## Osaka (Fusaka)

Meta: [EIP-7607](https://eips.ethereum.org/EIPS/eip-7607).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [7594](https://eips.ethereum.org/EIPS/eip-7594) | PeerDAS - Peer Data Availability Sampling | **No** |  |  | Blob-specific; Rootstock has no blobs ([RSKIP-558](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP558.md) Draft). |  |
| [7823](https://eips.ethereum.org/EIPS/eip-7823) | Set upper bounds for MODEXP | **?** |  |  | **Unverified** (claimed No): No RSKIP; MODEXP input bounds unchanged. |  |
| [7825](https://eips.ethereum.org/EIPS/eip-7825) | Transaction Gas Limit Cap | **No** |  |  | No consensus per-tx cap: execution only checks the tx against the remaining block gas ([`TransactionExecutor.java:265`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L265)). The 2^60 cap is pool-only ([`TxValidatorGasLimitValidator.java:40`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/net/handler/txvalidator/TxValidatorGasLimitValidator.java#L40)); 7825's cap is 2^24. [RSKIP-144](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP144.md) sublist limits (Reed 8.1.0, not scheduled on mainnet) are a different rule. |  |
| [7883](https://eips.ethereum.org/EIPS/eip-7883) | ModExp Gas Cost Increase | **No** |  |  | No RSKIP; MODEXP keeps EIP-198 pricing. |  |
| [7917](https://eips.ethereum.org/EIPS/eip-7917) | Deterministic proposer lookahead | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [7918](https://eips.ethereum.org/EIPS/eip-7918) | Blob base fee bounded by execution cost | **No** |  |  | Blob-specific; Rootstock has no blobs ([RSKIP-558](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP558.md) Draft). |  |
| [7934](https://eips.ethereum.org/EIPS/eip-7934) | RLP Execution Block Size Limit | **No** |  |  | No RSKIP. |  |
| [7939](https://eips.ethereum.org/EIPS/eip-7939) | Count leading zeros (CLZ) opcode | **No** |  |  | No RSKIP; no CLZ in `OpCode.java`. |  |
| [7951](https://eips.ethereum.org/EIPS/eip-7951) | Precompile for secp256r1 Curve Support | **No** |  |  | No RSKIP; no secp256r1 precompile (Rootstock has secp256k1 add/mul via RSKIP-516, Reed). |  |

## Amsterdam (Glamsterdam, scheduled)

Meta: [EIP-7773](https://eips.ethereum.org/EIPS/eip-7773).

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [2780](https://eips.ethereum.org/EIPS/eip-2780) | Resource-Based Intrinsic Transaction Gas (Last Call) | **No** |  |  | No RSKIP. |  |
| [7688](https://eips.ethereum.org/EIPS/eip-7688) | Forward Compatible Consensus Data Structures (Review) | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [7708](https://eips.ethereum.org/EIPS/eip-7708) | ETH Transfers Emit a Log (Last Call) | **No** |  |  | No RSKIP. |  |
| [7732](https://eips.ethereum.org/EIPS/eip-7732) | Enshrined Proposer-Builder Separation (Last Call) | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [7778](https://eips.ethereum.org/EIPS/eip-7778) | Block Gas Accounting without Refunds (Last Call) | **No** |  |  | No RSKIP. |  |
| [7843](https://eips.ethereum.org/EIPS/eip-7843) | SLOTNUM Opcode (Last Call) | **N/A** |  |  | SLOTNUM is beacon-slot based; would need an RSK equivalent. |  |
| [7928](https://eips.ethereum.org/EIPS/eip-7928) | Block-Level Access Lists (Last Call) | **No** |  |  | No RSKIP. |  |
| [7954](https://eips.ethereum.org/EIPS/eip-7954) | Increase Maximum Contract Size (Last Call) | **No** |  |  | No RSKIP. |  |
| [7976](https://eips.ethereum.org/EIPS/eip-7976) | Increase Calldata Floor Cost (Last Call) | **No** |  |  | No RSKIP. |  |
| [7981](https://eips.ethereum.org/EIPS/eip-7981) | Increase Access List Cost (Last Call) | **No** |  |  | No RSKIP. |  |
| [7997](https://eips.ethereum.org/EIPS/eip-7997) | Deterministic Factory Contract (Last Call) | **No** |  |  | No RSKIP. |  |
| [8024](https://eips.ethereum.org/EIPS/eip-8024) | Backward Compatible SWAPN, DUPN, EXCHANGE (Last Call) | **No** |  |  | No RSKIP. Rootstock's old DUPN/SWAPN at 0xa8/0xa9 ([`OpCode.java:630`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/OpCode.java#L630)) are disabled by [RSKIP-191](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP191.md) (Iris). |  |
| [8037](https://eips.ethereum.org/EIPS/eip-8037) | State Creation Gas Cost Increase (Last Call) | **No** |  |  | No RSKIP. |  |
| [8038](https://eips.ethereum.org/EIPS/eip-8038) | State-Access Gas Cost Update (Last Call) | **No** |  |  | No RSKIP. |  |
| [8045](https://eips.ethereum.org/EIPS/eip-8045) | Exclude Slashed Validators from Proposing (Last Call) | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [8061](https://eips.ethereum.org/EIPS/eip-8061) | Increase Exit and Consolidation Churn (Last Call) | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |
| [8246](https://eips.ethereum.org/EIPS/eip-8246) | Remove SELFDESTRUCT Burn (Last Call) | **No** |  |  | No RSKIP. |  |
| [8282](https://eips.ethereum.org/EIPS/eip-8282) | Builder Execution Requests (Last Call) | **N/A** |  |  | Ethereum consensus layer / beacon chain; no Rootstock equivalent. |  |

## Retroactive (all forks)

Rules Ethereum applies from genesis, not tied to one upgrade.

| EIP | Title | RSK | RSK upgrade | Mainnet height | Evidence | Under assumptions |
|---|---|---|---|---|---|---|
| [684](https://eips.ethereum.org/EIPS/eip-684) | Revert creation in case of collision | **Partial** | Wasabi | 1,591,000 | CREATE/CREATE2 only, since [RSKIP-125](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP125.md) (Wasabi): fails on an address with code or non-zero nonce ([`Program.java:572`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L572)) or deleted earlier in the block ([`Program.java:543`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L543)). Contract-creation txs have no collision check: the account is re-created, keeping only its balance ([RSKIP-174](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP174.md) (Iris); [`TransactionExecutor.java:403`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L403)). A collision there would need a hash collision, so the gap is theoretical. |  |
| [2681](https://eips.ethereum.org/EIPS/eip-2681) | Limit account nonce to 2^64-1 | **No** |  |  | No consensus rule or RSKIP: nonces are `BigInteger` and block validation only checks equality ([`BlockTxsValidationRule.java:89`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/validators/BlockTxsValidationRule.java#L89)); CREATE/CREATE2 has no nonce-cap check ([`Program.java:472`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/vm/program/Program.java#L472)). Only the tx pool ([`TxPendingValidator.java:66`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/net/handler/TxPendingValidator.java#L66)) and block-building sort ([`PendingState.java:194`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/core/bc/PendingState.java#L194)) reject nonces over 8 bytes, which still allows 2^64-1 (the EIP forbids it). Related: [RSKIP-545](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP545.md) requires set-code authorization nonces < 2^64-1. |  |
| [3607](https://eips.ethereum.org/EIPS/eip-3607) | Reject transactions from senders with deployed code | **No** |  |  | No sender-code check in [`TransactionExecutor.init()`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/org/ethereum/core/TransactionExecutor.java#L162) or the pool's [`TxValidatorAccountStateValidator.java`](https://github.com/rsksmart/rskj/blob/1e95a3b03/rskj-core/src/main/java/co/rsk/net/handler/txvalidator/TxValidatorAccountStateValidator.java); [RSKIP-545](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP545.md) notes this and doesn't need it. | Not needed (RSKIP-545) |
| [7610](https://eips.ethereum.org/EIPS/eip-7610) | Revert creation in case of non-empty storage (Last Call) | **?** |  |  | Collision on non-empty storage: not checked. |  |

## Rootstock upgrades that brought in Ethereum EIPs

| RSK upgrade | Mainnet height | EIPs |
|---|---|---|
| Genesis | 0 | 7, 100, 140, 150, 155, 160, 170, 198, 658 |
| Orchid | 729,000 | 214 |
| Wasabi | 1,591,000 | 145, 161, 684, 1014 |
| Papyrus | 2,392,700 | 196, 197, 1108, 1344, 1884 |
| Iris | 3,614,800 | 152, 211, 1052 |
| Arrowhead | 6,223,700 | 2028, 3198, 3855 |
| Lovell | 7,338,024 | 2, 1153, 3860?, 5656 |
| Vetiver | 8,804,200 | 3541 |

`?` after an EIP = claimed, not yet verified.

