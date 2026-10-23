## ⚠️Tangerine Whistle

### Run
```bash
uv run execute remote -rA -vv --fork=Prague \
    --rpc-endpoint=http://localhost:37546/ \
    --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
    --rpc-chain-id=298 \
    --seed-account-sweep-amount='1_000_000 ether' \
    --default-max-fee-per-blob-gas=710_000_000_000 \
    --tx-wait-timeout=15 \
    "tests/tangerine_whistle/"
```

### Running with geth
```bash
#Geth run
docker run --name geth --publish 8545:8545 --detach registry.hub.docker.com/ethereum/client-go:v1.17.5 --dev --verbosity 3 --http --http.api eth --http.addr 0.0.0.0 --rpc.txfeecap 1000
#Tests run
uv run execute remote -rA -vv --fork=Prague \
    --rpc-endpoint=http://localhost:8545/ \
    --rpc-seed-key=0xb71c71a67e1177ad4e901695e1b4b9ee17ae16c6668d313eac2f96dbcda3f291 \
    --rpc-chain-id=1337 \
    --seed-account-sweep-amount='1_000_000 ether' \
    --default-max-fee-per-blob-gas=710 \
    --tx-wait-timeout=15 \
    --max-tx-per-batch=1 \
    "tests/tangerine_whistle/"
```

### Run Results
```
SKIPPED [64] tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py:299: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [64] tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py:423: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [272] tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py:560: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [272] tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py:669: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [40] tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py:779: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [8] tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py:927: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [2] tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py:1136: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [2] tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py:1241: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
======================================================================================= 724 skipped, 1 warning in 0.38s =======================================================================================
```