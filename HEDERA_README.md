# Hedera Execution Spec Tests

## Table of Contents

- [Purpose](#purpose)
- [How it works](#how-it-works)
- [Running locally](#running-locally)
- [CI (TODO)](#ci-todo)
- [Where to look](#where-to-look)
- [Changelog](#changelog)
  - [Skipped tests](#skipped-tests)
- [Require Fix On Hedera](#require-fix-on-hedera)
- [Fork Groups Runs](#fork-groups-runs)

This is a fork of [ethereum/execution-specs](https://github.com/ethereum/execution-specs)
(which hosts the Ethereum Execution Spec Tests, EEST) adapted to run against a
Hedera network.

## Purpose

Hedera exposes an Ethereum-compatible EVM through the JSON-RPC Relay, but the
network is not a 1:1 Ethereum client (for example, balances are tracked in
tinybars). The goal of this fork is to:

1. **Confirm Hedera <> Ethereum equivalence** by running the official Ethereum
   consensus tests against Hedera, fork by fork.
2. **Track incompatibilities**: every test that does not pass is classified,
   documented and linked to an issue, so we know exactly where Hedera differs.
3. **Detect new incompatibilities** by re-running the suite in CI (planned), so a
   Hedera change that breaks equivalence shows up as a new failure instead of
   going unnoticed.

## How it works

- Tests are executed with `uv run execute remote`, which builds the test
  transactions, sends them over JSON-RPC (to the Relay of a local Hedera node,
  or any other Ethereum node, e.g. geth, as a reference) and checks the
  resulting post-state against the test expectations.
- Every test run is classified into one of three outcomes:
    - **Passes** as is.
    - **Passes after a small adaptation** of the test or framework, marked with
      `# Run On Hedera:` (see [Changelog](#changelog)).
    - **Does not pass**: either skipped through the [Skip List](docs/hedera/hedera_skips.toml)
      with a reason, or listed in [Require Fix On Hedera](#require-fix-on-hedera).
- The skip list is loaded by the `hedera_skips` pytest plugin. Each entry skips
  every test whose node id starts with the given `prefix`, and states the reason
  and the [skip group](#skipped-tests).
- Per-fork run commands and results live in `docs/hedera/hedera_<fork>.md` (see
  [Fork Groups Runs](#fork-groups-runs)). Each file has the exact command to run
  that fork, an optional geth reference run, and the results per test folder.

## Running locally

1. Start a local Hedera node with the JSON-RPC Relay (the docs use
   `http://localhost:37546/`, chain id `298`). For this you can
   use [evm-functional-testing](https://github.com/hashgraph/hedera-evm-testing/tree/main/evm-functional-testing) with a
   command `./test.sh solo start --profile spec`.
   See [evm-functional-testing/README.md](https://github.com/hashgraph/hedera-evm-testing/blob/main/evm-functional-testing/README.md)
   for more details.
2. Run a fork, for example:

```bash
uv run execute remote -rA -vv --fork=Prague \
    --rpc-endpoint=http://localhost:37546/ \
    --rpc-seed-key=<funded account private key> \
    --rpc-chain-id=298 \
    --seed-account-sweep-amount='1_000_000 ether' \
    --default-max-fee-per-blob-gas=710_000_000_000 \
    --tx-wait-timeout=15 \
    "tests/prague/"
```

The exact command and flags for each fork are in its `docs/hedera/hedera_<fork>.md`.

## CI (TODO)

The suite is intended to run in CI against a Hedera node to continuously verify
Hedera <> Ethereum equivalence.

## Where to look

| What                                | Where                                                            |
|-------------------------------------|------------------------------------------------------------------|
| Changes made to tests and framework | [Changelog](#changelog)                                          |
| Tests skipped on Hedera and why     | [docs/hedera/hedera_skips.toml](docs/hedera/hedera_skips.toml)   |
| Known failures needing a Hedera fix | [docs/hedera/hedera_failures.md](docs/hedera/hedera_failures.md) |
| Per-fork commands and results       | [Fork Groups Runs](#fork-groups-runs)                            |

## Changelog

- `# Run On Hedera:` comments added where the 'static change' is done on test cases. List of changes:
    1. `Run On Hedera: a nonzero value transfer below 1 tinybar` - Hedera's EVM counts value in tinybars. One tinybar is
       10_000_000_000 wei, and the node rejects any nonzero transfer smaller than that.
    2. `Run On Hedera: a post-state balance assertion` - Adapt balance check to match (1) changes
    3. gas_price/max_fee_per_gas/max_priority_fee_per_gas difference - Do not use static gas_price for Hedera
    4. `Run On Hedera: increase funding because of "Insufficient funds for transfer"` - Requires more balance for some
       tests
    5. `Run On Hedera: round up to the nearest whole tinybar` - Hedera only tracks balances in whole tinybars.
    6. `Run On Hedera: Useful for viewing and debugging JSON-RPC Relay errors` - Debug purpose
    7. `Run On Hedera: the Hedera network's block gas limit is fixed at 150_000_000` - static change for gas limit test
- `# TODO Fix On Hedera:` comments added where fixes are required on Hedera for the core spec test framework to work or
  tests are skipped because of idenfied/triage issue
- `# Fixed In Test:` comments added where a genuine test bug (not a Hedera behavior difference) was found and fixed
  while running against Hedera

### Skipped tests

1. All tests that are not supported by Hedera, skipped with a reason at [Skip List](docs/hedera/hedera_skips.toml).
   All Hedera skips have related **Skip Groups:**
    1. `ACCEPTED_INCOMPATIBILITY`: These are the acknowledged incompatibilities, like type3 transactions where we will
       not be compatible.
    2. `UNKNOWN_INCOMPATIBILITY`: Detected, unknown reason, needs investigation.
    3. `KNOWN_INCOMPATIBILITY`: Detected, known reasoning, fix pending. Example: Pectra EIP-7702.
    4. `FRAMEWORK_BUG`: Skipped due to a framework bug.

2. All other skipped tests are skipped and managed by original ethereum spec test repo community

## Require Fix On Hedera

[List of all the failures](docs/hedera/hedera_failures.md)

## Fork Groups Runs

✅ - Fully passing on Hedera

▶️️ - Contains 'Skip Temporary' failures group that are skipped

⚠️ - Contains failures that are still require a fix

### ▶️️ [Prague](docs/hedera/hedera_prague.md)

### ▶️️ [Cancun](docs/hedera/hedera_cancun.md)

### ⚠️ [Shanghai](docs/hedera/hedera_shanghai.md)

### ✅ [Paris](docs/hedera/hedera_paris.md)

### ✅ [London](docs/hedera/hedera_london.md)

### ✅ [Berlin](docs/hedera/hedera_berlin.md)

### ✅ [Istanbul](docs/hedera/hedera_istanbul.md)

### ▶️️ [Constantinople](docs/hedera/hedera_constantinople.md)

### ✅ [Byzantium](docs/hedera/hedera_byzantium.md)

### ▶️️ [Tangerine Whistle](docs/hedera/hedera_tangerine_whistle.md)

### ✅ [Homestead](docs/hedera/hedera_homestead.md)

### ⚠️ [Frontier](docs/hedera/hedera_frontier.md)
