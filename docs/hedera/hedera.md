# Changelog

- Unsupported tests are skipped at `packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini`
- `# Run On Hedera:` comments added where the 'static change' is done on test cases
- `# TODO Fix On Hedera:` comments added where fixes are required on Hedera for the core spec test framework to work
- `# Fixed In Test:` comments added where a genuine test bug (not a Hedera behavior difference) was found and fixed while running against Hedera
- added `--env-gas-limit` flag. Override the environment gas limit used

# Require Fix On Hedera

1. `authorizationList` entries contain a duplicate snake_case `y_parity` field

   **Root cause:** The relay duplicates `yParity` as an extra snake_case `y_parity` field in `authorizationList` entries, which is otherwise rejected as an unexpected field. Likely because the mirror node returns `y_parity` and the relay doesn't drop it after formatting. Currently worked around client-side by dropping `y_parity` before validation (`packages/testing/src/execution_testing/test_types/transaction_types.py:90`).

2. Returned transaction hash doesn't match the hash computed from the transaction's own RLP data

   **Root cause:** Hedera has a bug that prevents the transaction hash it returns for a submitted transaction from matching the hash calculated from that transaction's own RLP encoding. The `assert self.transaction_hash == self.hash` check is disabled (replaced with a `print` warning) to work around this (`packages/testing/src/execution_testing/rpc/rpc_types.py:156`).

3. Multiple same-sender transactions in one JSON-RPC batch race on nonce sequencing

   **Root cause:** The local Hedera node's JSON-RPC relay doesn't handle multiple same-sender transactions submitted in one JSON-RPC batch call reliably — it races on nonce sequencing when 2+ transactions from the same account arrive together, causing "nonce too low"/"nonce too high" depending on timing. Sending them one at a time (waiting for each to land in a block before sending the next) sidesteps the race entirely.

   Example:
    1. frontier
   ```bash
   uv run execute remote -rA --verbose --fork=Prague \
       --rpc-endpoint=http://localhost:37546/ \
       --rpc-seed-key=0x748634984b480c75456a68ea88f31609cd3091e012e2834948a6da317b727c04 \
       --rpc-chain-id=298 \
       --seed-account-sweep-amount='1_000_000 ether' \
       --default-max-fee-per-blob-gas=710 \
       --tx-wait-timeout=15 \
       --env-gas-limit=15000000 \
       "tests/frontier/create/test_create_deposit_oog.py::test_create_deposit_oog[fork_Prague-create_opcode_CREATE2-state_test-enough_gas_True]"
   ```
   2. prague
    ```bash
    uv run execute remote -rA -v --fork=Prague \                                           
        --rpc-endpoint=http://localhost:37546/ \
        --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
        --rpc-chain-id=298 \
        --seed-account-sweep-amount='1_000_000 ether' \
        --default-max-fee-per-blob-gas=710_000_000_000 \
        --tx-wait-timeout=15 \
        "tests/prague/eip7623_increase_calldata_cost/test_execution_gas.py::TestGasConsumption::test_full_gas_consumption"
    ```

   Workaround: add `--max-tx-per-batch=1`.

4. Head block's reported `gasLimit` doesn't match the configured environment gas limit

   **Root cause:** The local Hedera node's head block reports a fixed `gasLimit` of `0x8f0d180` (150,000,000), regardless of the `--env-gas-limit` value passed to `execute remote` (e.g. `15000000`). The chain's actual block gas limit isn't adjustable via that flag, so tests relying on the environment gas limit matching the real network's block gas limit see a mismatch.

   Example:
   ```bash
   curl -s -X POST http://localhost:37546/ \
      -H "Content-Type: application/json" \
      -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}'
   {"jsonrpc":"2.0","result":{"timestamp":"0x6ab11f16","difficulty":"0x0","extraData":"0x","gasLimit":"0x8f0d180","baseFeePerGas":"0xa54f4c3c00","gasUsed":"0x0","logsBloom":"0x0...0","miner":"0x0...0","mixHash":"0x0...0","nonce":"0x0000000000000000","receiptsRoot":"0x0...0","sha3Uncles":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","size":"0x251","stateRoot":"0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421","totalDifficulty":"0x0","transactions":[],"transactionsRoot":"0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421","uncles":[],"withdrawals":[],"withdrawalsRoot":"0x0...0","number":"0x268d","hash":"0xc4f9131e5f230b182bde83dbd5199a263cb20252e1d1d46387064d5a81dc78f9","parentHash":"0x5885d271d77e19ffd3d00a18239a8980b58328f3f49f98d6700f642b793fc37f"},"id":1}
   ```

5. Large jumbo `EthereumTransaction` payloads are silently truncated on ingest, failing with `INVALID_TRANSACTION` / `BufferUnderflowException`

   **Root cause:** `DataBufferMarshaller` (`hedera-node/hedera-app/.../grpc/impl/netty/DataBufferMarshaller.java`) caches its read buffer in a **`static`** `ThreadLocal<BufferedData>`. The consensus node constructs two separate `DataBufferMarshaller` instances with different capacities — a small one for regular transactions (`MAX_TRANSACTION_SIZE + 1` = 133,121 bytes) and a large one for jumbo transactions (`jumboMaxTxnSize + 1`, e.g. 9,000,002 bytes) — but because the `ThreadLocal` field is `static`, both instances share the same per-thread cached buffer. gRPC dispatches calls across a shared Netty worker-thread pool, not partitioned by method, so on most worker threads a small/regular call (queries, node signature transactions, small `EthereumTransaction`s) runs first and permanently caches a 133,121-byte `ByteBuffer` for that thread — `ByteBuffer` capacity is fixed at allocation and `reset()` only rewinds position, it can't grow it.

   When a large jumbo `EthereumTransaction` later lands on one of these "poisoned" threads, its `DataBufferMarshaller.parse()` call finds the thread-local buffer already set (`if (buffer == null)` is false) and silently reuses the small, wrong-sized buffer instead of allocating one sized for jumbo. `buffer.writeBytes(stream, tooBigMessageSize)` internally bounds the read by `Math.min(maxLength, remaining())`, where `remaining()` reflects the small cached buffer's real capacity — so it reads only ~133KB and returns normally (loop condition satisfied, not a stream EOF) with no error. The parser downstream then sees the wire-format length-prefix correctly declaring the full (~1+ MB) message size against a buffer that only actually contains ~133KB, and throws `BufferUnderflowException`, surfaced by the SDK as a plain `INVALID_TRANSACTION` precheck status with no indication of a size/buffer problem.

   This reproduces deterministically regardless of network path (confirmed identical byte-exact truncation whether going through HAProxy or directly to the consensus node's gRPC port) since it's a pure in-process JVM bug, not a transport/proxy issue.

   Repro:
   ```bash
   uv run execute remote -rA -v --fork=Prague \
       --rpc-endpoint=http://localhost:37546/ \
       --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
       --rpc-chain-id=298 \
       --seed-account-sweep-amount='1_000_000 ether' \
       --default-max-fee-per-blob-gas=710_000_000_000 \
       --tx-wait-timeout=20 \
       "tests/prague/eip2537_bls_12_381_precompiles/test_bls12_pairing.py::test_valid_multi_inf"
   ```

   Workaround: Limiting data size, generated by the test

# Forks

## ⚠️[Prague](hedera_prague.md)
## ⚠️[Cancun](hedera_cancun.md)
## ⚠️[Shanghai](hedera_shanghai.md)
## ✅[Paris](hedera_paris.md)
## ✅[London](hedera_london.md)
## ✅[Berlin](hedera_berlin.md)
## ✅[Istanbul](hedera_istanbul.md)
## [Constantinople](hedera_constantinople.md)
## [Byzantium](hedera_byzantium.md)
## ❓[Tangerine Whistle](hedera_tangerine_whistle.md)
## ✅[Homestead](hedera_homestead.md)
## ❓️[Frontier](hedera_frontier.md)
