# Changelog

- `# Run On Hedera:` comments added where the 'static change' is done on test cases. List of changes:
  1. `Run On Hedera: a nonzero value transfer below 1 tinybar` - Hedera's EVM counts value in tinybars. One tinybar is 10_000_000_000 wei, and the node rejects any nonzero transfer smaller than that. 
  2. `Run On Hedera: a post-state balance assertion` - Adapt balance check to match (1) changes
  3. gas_price/max_fee_per_gas/max_priority_fee_per_gas difference - Do not use static gas_price for Hedera
  4. `Run On Hedera: increase funding because of "Insufficient funds for transfer"` - Requires more balance for some tests
  5. `Run On Hedera: round up to the nearest whole tinybar` - Hedera only tracks balances in whole tinybars.
  6. `Run On Hedera: Useful for viewing and debugging JSON-RPC Relay errors` - Debug purpose
  7. `Run On Hedera: the Hedera network's block gas limit is fixed at 150_000_000` - static change for gas limit test
- `# TODO Fix On Hedera:` comments added where fixes are required on Hedera for the core spec test framework to work or tests are skipped because of idenfied/triage issue
- `# Fixed In Test:` comments added where a genuine test bug (not a Hedera behavior difference) was found and fixed while running against Hedera

## Skipped tests

1. All tests that are not supported by Hedera, skipped with a reason at [Skip List](docs/hedera/hedera_skips.toml)
2. All other skipped tests are skipped and managed by repo owners

# Require Fix On Hedera

[List of all the failures](docs/hedera/hedera_failures.md)

# Fork Groups Runs

✅ - Fully passing on Hedera

▶️️ - Contains 'Skip Temporary' failures group that are skipped

⚠️ - Contains failures that are still require a fix

## ▶️️ [Prague](docs/hedera/hedera_prague.md)
## ▶️️ [Cancun](docs/hedera/hedera_cancun.md)
## ⚠️ [Shanghai](docs/hedera/hedera_shanghai.md)
## ✅ [Paris](docs/hedera/hedera_paris.md)
## ✅ [London](docs/hedera/hedera_london.md)
## ✅ [Berlin](docs/hedera/hedera_berlin.md)
## ✅ [Istanbul](docs/hedera/hedera_istanbul.md)
## ▶️️ [Constantinople](docs/hedera/hedera_constantinople.md)
## ✅ [Byzantium](docs/hedera/hedera_byzantium.md)
## ▶️️ [Tangerine Whistle](docs/hedera/hedera_tangerine_whistle.md)
## ✅ [Homestead](docs/hedera/hedera_homestead.md)
## ⚠️ [Frontier](docs/hedera/hedera_frontier.md)
