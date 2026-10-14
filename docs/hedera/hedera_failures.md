# Require Fix On Hedera

## Summary 

| # | Title | Status | Issue | Comment |
|---|---|---|---|---|
| 1 | (Relay) `authorizationList` entries contain a duplicate snake_case `y_parity` field | Fixed | [hiero-ledger/hiero-json-rpc-relay#5858](https://github.com/hiero-ledger/hiero-json-rpc-relay/issues/5858) |
| 2 | (CN?) Returned transaction hash doesn't match the hash computed from the transaction's own RLP data | Issue | [hiero-ledger/hiero-consensus-node#27580](https://github.com/hiero-ledger/hiero-consensus-node/issues/27580) |
| 3 | (Relay) Multiple same-sender transactions in one JSON-RPC batch race on nonce sequencing | Awaiting Validation | — |
| 4 | (Relay) Head block's reported `gasLimit` doesn't match the configured environment gas limit | Expected Behaviour | [hiero-ledger/hiero-consensus-node#21633](https://github.com/hiero-ledger/hiero-consensus-node/issues/21633) (related) | Confuguring local Hedera MAX_TRANSACTION_GAS_LIMIT=15M |
| 5 | (CN) Large jumbo `EthereumTransaction` payloads are silently truncated on ingest, failing with `INVALID_TRANSACTION` / `BufferUnderflowException` | Issue | [hiero-ledger/hiero-consensus-node#27581](https://github.com/hiero-ledger/hiero-consensus-node/issues/27581) |
| 6 | (CN) `BALANCE`, `SELFBALANCE` and `CALLVALUE` opcodes return values in tinybar instead of wei | Issue | [hiero-ledger/hiero-consensus-node#27582](https://github.com/hiero-ledger/hiero-consensus-node/issues/27582) |
| 7 | (CN?) SELFDESTRUCT does not apply when triggered via internal CALL/CALLCODE/DELEGATECALL or during init code | Triage | — |
| 8 | (CN?) CALL/CALLCODE/DELEGATECALL into a SELFDESTRUCT-only contract reports failure | Triage | — |
| 9 | (Not supported on Hedera? Skip?) SELFDESTRUCT beneficiary must be an existing account on Hedera | Triage | — |
| 10 | (CN?) Warm-access gas cost not honored — repeat accesses (EIP-2929) and coinbase pre-warming (EIP-3651) | Issue | [hiero-ledger/hiero-consensus-node#21335](https://github.com/hiero-ledger/hiero-consensus-node/issues/21335) (COINBASE part only) |
| 11 | (CN?) BLOCKHASH returns 0 for genesis/recent blocks | Triage | — |
| 12 | (CN?) CALL with a nonzero value to a precompile address fails | Issue | https://github.com/hiero-ledger/hiero-consensus-node/issues/21332 | Seems like 'Expected Behaviour' but Hedera docs should be updated |
| 13 | (CN?) Gas-accounting precision mismatches in precompile/CALL cost measurement | Triage | — |
| 14 | Miscellaneous singleton failures — not yet root-caused | Triage | — |
| 15 | (Possible test-infra flake, not a confirmed Hedera bug) `test_tx_gas_limit` ERROR | Triage | — |
| 16 | (CN?) Out-of-gas transaction does not consume the full declared gas_limit | Triage | — |
| 17 | (Relay?) RPC rejects transaction — invalid yParity (-32000) | Triage | — |
| 18 | (Relay?) Zero-value r/s in authorization tuple serialized as empty '0x' | Triage | — |
| 19 | (CN?) Call to EIP-7702-delegated EOA rejected as INVALID_CONTRACT_ID | Triage | — |
| 20 | (Relay caching?) EIP-7702 authorization tuple does not bump authority nonce | Triage | — |
| 21 | (CN?) EIP-7702 authorization tuple does not write delegation designation code | Triage | — |
| 22 | (CN?) Delegated EOA used as transaction sender is not found as an existing account | Triage | — |
| 23 | (Relay/Mirror node) Account-state queries for a deleted (self-destructed) contract fail with `-32020` mirror node 500 | Triage | — |


## Details

---
1. ▶️ ️(Relay) `authorizationList` entries contain a duplicate snake_case `y_parity` field

   **Root cause:** The relay duplicates `yParity` as an extra snake_case `y_parity` field in `authorizationList` entries, which is otherwise rejected as an unexpected field. Likely because the mirror node returns `y_parity` and the relay doesn't drop it after formatting. Currently worked around client-side by dropping `y_parity` before validation (`packages/testing/src/execution_testing/test_types/transaction_types.py:90`).

   **Reproducer:** Comment the `model_config = CamelModel.model_config | {"extra": "ignore"}` under "# TODO Fix On Hedera: the relay duplicates `yParity` as `y_parity`" comment at `packages/testing/src/execution_testing/test_types/transaction_types.py`
   Execute: (it is failing for most of the `tests/prague/eip7702_set_code_tx/test_set_code_txs.py` tests) For example:
    ```bash
    uv run execute remote -rA -vv --fork=Prague \
        --rpc-endpoint=http://localhost:37546/ \
        --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
        --rpc-chain-id=298 \
        --seed-account-sweep-amount='1_000_000 ether' \
        --default-max-fee-per-blob-gas=710_000_000_000 \
        --tx-wait-timeout=15 \
        --max-tx-per-batch=1 \
        "tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_sponsored_set_code[fork_Prague-state_test-stop-tx_value_0]"
    ```
   
---
2. ⚠️(CN?) Returned transaction hash doesn't match the hash computed from the transaction's own RLP data

   **Root cause:** Hedera has a bug that prevents the transaction hash it returns for a submitted transaction from matching the hash calculated from that transaction's own RLP encoding. The `assert self.transaction_hash == self.hash` check is disabled (replaced with a `print` warning) to work around this (`packages/testing/src/execution_testing/rpc/rpc_types.py:156`).

   **Reproducer:** Uncomment the `assert self.transaction_hash == self.hash` under "# TODO Fix On Hedera: the hash calculated by the test client from the" comment at `packages/testing/src/execution_testing/rpc/rpc_types.py`
   Execute: is it failing for a lot of the tests, for example:
   ```bash
   uv run execute remote -rA -vv --fork=Prague \
      --rpc-endpoint=http://localhost:37546/ \
      --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
      --rpc-chain-id=298 \
      --seed-account-sweep-amount='1_000_000 ether' \
      --default-max-fee-per-blob-gas=710_000_000_000 \
      --tx-wait-timeout=15 \
      --max-tx-per-batch=1 \
      "tests/prague/eip7623_increase_calldata_cost/test_execution_gas.py::TestGasConsumption::test_full_gas_consumption[fork_Prague-state_test-extra_gas-type_4]"
   ```

---
3. ✅(Relay) Multiple same-sender transactions in one JSON-RPC batch race on nonce sequencing

   **Root cause:** The local Hedera node's JSON-RPC relay doesn't handle multiple same-sender transactions submitted in one JSON-RPC batch call reliably — it races on nonce sequencing when 2+ transactions from the same account arrive together, causing "nonce too low"/"nonce too high" depending on timing. Sending them one at a time (waiting for each to land in a block before sending the next) sidesteps the race entirely.

   (Fixed) Example:
    1. frontier
   ```bash
   uv run execute remote -rA -vv --fork=Prague \
       --rpc-endpoint=http://localhost:37546/ \
       --rpc-seed-key=0x748634984b480c75456a68ea88f31609cd3091e012e2834948a6da317b727c04 \
       --rpc-chain-id=298 \
       --seed-account-sweep-amount='1_000_000 ether' \
       --default-max-fee-per-blob-gas=710 \
       --tx-wait-timeout=15 \
       "tests/frontier/create/test_create_deposit_oog.py::test_create_deposit_oog[fork_Prague-create_opcode_CREATE2-state_test-enough_gas_True]"
   ```
    2. prague
    ```bash
    uv run execute remote -rA -vv --fork=Prague \
        --rpc-endpoint=http://localhost:37546/ \
        --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
        --rpc-chain-id=298 \
        --seed-account-sweep-amount='1_000_000 ether' \
        --default-max-fee-per-blob-gas=710_000_000_000 \
        --tx-wait-timeout=15 \
        "tests/prague/eip7623_increase_calldata_cost/test_execution_gas.py::TestGasConsumption::test_full_gas_consumption"
    ```

   With ENABLE_TX_POOL, ENABLE_NONCE_ORDERING enabled it ia failing with 'unexpected nonce for account + Transaction rejected: WRONG_NONCE' or 'Nonce too low' 

   Example:
   1. 'unexpected nonce for account + Transaction rejected: WRONG_NONCE'
   ```
   uv run execute remote -rA -vv --fork=Prague \
        --rpc-endpoint=http://localhost:37546/ \
        --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
        --rpc-chain-id=298 \
        --seed-account-sweep-amount='1_000_000 ether' \
        --default-max-fee-per-blob-gas=710_000_000_000 \
        --tx-wait-timeout=15 \
        "tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_sponsored_set_code[fork_Prague-state_test-stop-tx_value_0]"
   ```
   2. Nonce too low
   ```
   uv run execute remote -rA -vv --fork=Prague \
        --rpc-endpoint=http://localhost:37546/ \
        --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
        --rpc-chain-id=298 \
        --seed-account-sweep-amount='1_000_000 ether' \
        --default-max-fee-per-blob-gas=710_000_000_000 \
        --tx-wait-timeout=15 \
        "tests/prague/eip7623_increase_calldata_cost/test_execution_gas.py::TestGasConsumption::test_full_gas_consumption"
   ```

   Workaround: add `--max-tx-per-batch=1`.

---
4. ✅(Relay) Head block's reported `gasLimit` doesn't match the configured environment gas limit

   **Root cause:** The local Hedera node's head block reports a fixed `gasLimit` of `0x8f0d180` (150,000,000), regardless of the `--env-gas-limit` value passed to `execute remote` (e.g. `15000000`). The chain's actual block gas limit isn't adjustable via that flag, so tests relying on the environment gas limit matching the real network's block gas limit see a mismatch.

   Example:
   ```bash
   curl -s -X POST http://localhost:37546/ \
      -H "Content-Type: application/json" \
      -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}'
   {"jsonrpc":"2.0","result":{"timestamp":"0x6ab11f16","difficulty":"0x0","extraData":"0x","gasLimit":"0x8f0d180","baseFeePerGas":"0xa54f4c3c00","gasUsed":"0x0","logsBloom":"0x0...0","miner":"0x0...0","mixHash":"0x0...0","nonce":"0x0000000000000000","receiptsRoot":"0x0...0","sha3Uncles":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","size":"0x251","stateRoot":"0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421","totalDifficulty":"0x0","transactions":[],"transactionsRoot":"0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421","uncles":[],"withdrawals":[],"withdrawalsRoot":"0x0...0","number":"0x268d","hash":"0xc4f9131e5f230b182bde83dbd5199a263cb20252e1d1d46387064d5a81dc78f9","parentHash":"0x5885d271d77e19ffd3d00a18239a8980b58328f3f49f98d6700f642b793fc37f"},"id":1}
   ```

---
5. ⚠️(CN) Large jumbo `EthereumTransaction` payloads are silently truncated on ingest, failing with `INVALID_TRANSACTION` / `BufferUnderflowException`

   **Root cause:** `DataBufferMarshaller` (`hedera-node/hedera-app/.../grpc/impl/netty/DataBufferMarshaller.java`) caches its read buffer in a **`static`** `ThreadLocal<BufferedData>`. The consensus node constructs two separate `DataBufferMarshaller` instances with different capacities — a small one for regular transactions (`MAX_TRANSACTION_SIZE + 1` = 133,121 bytes) and a large one for jumbo transactions (`jumboMaxTxnSize + 1`, e.g. 9,000,002 bytes) — but because the `ThreadLocal` field is `static`, both instances share the same per-thread cached buffer. gRPC dispatches calls across a shared Netty worker-thread pool, not partitioned by method, so on most worker threads a small/regular call (queries, node signature transactions, small `EthereumTransaction`s) runs first and permanently caches a 133,121-byte `ByteBuffer` for that thread — `ByteBuffer` capacity is fixed at allocation and `reset()` only rewinds position, it can't grow it.

   When a large jumbo `EthereumTransaction` later lands on one of these "poisoned" threads, its `DataBufferMarshaller.parse()` call finds the thread-local buffer already set (`if (buffer == null)` is false) and silently reuses the small, wrong-sized buffer instead of allocating one sized for jumbo. `buffer.writeBytes(stream, tooBigMessageSize)` internally bounds the read by `Math.min(maxLength, remaining())`, where `remaining()` reflects the small cached buffer's real capacity — so it reads only ~133KB and returns normally (loop condition satisfied, not a stream EOF) with no error. The parser downstream then sees the wire-format length-prefix correctly declaring the full (~1+ MB) message size against a buffer that only actually contains ~133KB, and throws `BufferUnderflowException`, surfaced by the SDK as a plain `INVALID_TRANSACTION` precheck status with no indication of a size/buffer problem.

   This reproduces deterministically regardless of network path (confirmed identical byte-exact truncation whether going through HAProxy or directly to the consensus node's gRPC port) since it's a pure in-process JVM bug, not a transport/proxy issue.

   Repro:
   ```bash
   uv run execute remote -rA -vv --fork=Prague \
       --rpc-endpoint=http://localhost:37546/ \
       --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
       --rpc-chain-id=298 \
       --seed-account-sweep-amount='1_000_000 ether' \
       --default-max-fee-per-blob-gas=710_000_000_000 \
       --tx-wait-timeout=20 \
       "tests/prague/eip2537_bls_12_381_precompiles/test_bls12_pairing.py::test_valid_multi_inf"
   ```

   Workaround: Limiting data size, generated by the test

---
6. ⚠️(CN) `BALANCE`, `SELFBALANCE` and `CALLVALUE` opcodes return values in tinybar instead of wei

   **Root cause:** Hedera's EVM returns account balances and call values in tinybar (1 tinybar = 10_000_000_000 wei, i.e. 10^10 wei) rather than in wei, so the values seen by contract code are 10^10 times smaller than the Ethereum-spec values the tests expect. For example, an account funded with 0.29 ETH (`290_000_000_000_000_000` wei) reports `29_000_000` from `BALANCE`. The same conversion difference affects `SELFBALANCE` and `CALLVALUE`.

   Observed failure (`test_ext_code_on_self_delegating_set_code`):
   ```
   Storage.KeyValueMismatchError: incorrect value in address 0xb66d20c99ba38a82c001e8a4587b38ee91bc07be for key 0x...04:
   want 0x4064976a8dd0000 (dec:290000000000000000), got 0x1ba8140 (dec:29000000)
   ```

   **Reproducer:**
   ```bash
   uv run execute remote -rA -vv --fork=Prague \
       --rpc-endpoint=http://localhost:37546/ \
       --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
       --rpc-chain-id=298 \
       --seed-account-sweep-amount='1_000_000 ether' \
       --default-max-fee-per-blob-gas=710_000_000_000 \
       --tx-wait-timeout=15 \
       --max-tx-per-batch=1 \
       "tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_self_delegating_set_code[fork_Prague-state_test-self_sponsored_tx]"
   ```

   Marked in the tests with `# TODO Fix On Hedera: BALANCE return value in tinybar, 10_000_000_000 wei = 1 tinybar` (`tests/prague/eip7702_set_code_tx/test_set_code_txs.py:1689`).

---
7. (CN?) SELFDESTRUCT does not apply when triggered via internal CALL/CALLCODE/DELEGATECALL or during init code
    **Note:** The EIP-150 matrix (group B) shows a lot of similar failures on Hedera and GETH

    **Pattern:** `Account.NonceMismatchError: unexpected nonce ...` / `Account.BalanceMismatchError: unexpected balance ...` (including beneficiary addresses labeled by precompile/system-contract name, e.g. `(RIPEMD160)`, `(BLS12_G1ADD)`, `(BEACON_ROOTS_ADDRESS)`; or `want 0x00, got 0x02540be400`, i.e. 1 tinybar left over) / `Account.CodeMismatchError` / `AssertionError: Code of 0x...: is 0x<code>, expected 0x.` / `AssertionError: Balance of 0x...: is 0x<n>, expected 0.` / `Storage.KeyValueMismatchError: ... want 0x1, got 0x0` (cascading from the account not being deleted) / `test_constant_gas[SELFDESTRUCT]`'s own gas measurement reading `0` instead of the expected cold-beneficiary cost (`7600`).

    **Root cause:**Whenever `SELFDESTRUCT` is executed anywhere other than a direct top-level call — via an internal `CALL`/`CALLCODE`/`DELEGATECALL` (at any nesting depth) or directly inside a `CREATE`/`CREATE2`'s init code — Hedera accepts and mines the transaction but silently no-ops the `SELFDESTRUCT`: the victim's nonce/code/balance are left untouched and the beneficiary never receives the transferred balance. The tests expect the account to end up `Account.NONEXISTENT` (or, post-EIP-6780 for a pre-existing account, at least have its balance drained to 0).

    Sub-groups (same cause, different tests):
    - **A. Frontier create/opcode tests.** `test_create_suicide_during_transaction_create` runs `SELFDESTRUCT` directly inside a `CREATE`/`CREATE2`'s init code; `test_create_suicide_store` creates a contract then triggers its `SELFDESTRUCT` via a separate internal `CALL`; `test_constant_gas[SELFDESTRUCT]` reads `0` instead of the cold-beneficiary surcharge, consistent with the operation not being applied.
    - **B. EIP-150 combinatorial matrix.** Every failing test deploys a `victim` contract whose code is `Op.SELFDESTRUCT(beneficiary)` and triggers it via an internal `Op.CALL(gas=inner_call_gas, address=victim)` from a separate `caller` contract (`test_selfdestruct_to_account`, `test_selfdestruct_to_precompile`, `test_selfdestruct_to_system_contract`, `test_selfdestruct_to_self`, and their `_state_access_boundary` variants), or — for `test_initcode_selfdestruct_to_self` — triggers `SELFDESTRUCT(ADDRESS)` directly inside `CREATE`'s init code. Hedera leaves the victim untouched for the "exact_gas" (success) parametrizations across every beneficiary type (EOA, contract, each precompile, each system contract, self).
    - **C. EIP-1052 `EXTCODEHASH` tests.** The target's runtime code ends in `SELFDESTRUCT`, triggered via an internal `CALL` (e.g. `code += Op.CALL(address=target, gas=100_000)` / `trigger(address=target, gas=0x10000)`) — including when nested an extra frame deep (`test_extcodehash_created_and_deleted_recheck_outer`'s outer contract `CALL`s an inner contract that itself `CALL`s the self-destructing target), and when reached via `CALLCODE`/`DELEGATECALL` so `SELFDESTRUCT` executes in the *caller's* own context (`test_extcodehash_subcall_selfdestruct`).
    - **D. EIP-7702 same-transaction deploy.** In `test_set_code_to_self_destructing_account_deployed_in_same_tx`, the transaction's top-level target is `contract_creator_address`, which internally `CREATE`s a new contract and then issues a nested `CALL` into it, and that nested call runs the `SELFDESTRUCT`. A contract both `CREATE`d and `SELFDESTRUCT`ed within the same transaction (fully wiped per EIP-6780) still has its deployed code after the transaction is mined successfully. Confirmed independent of two other candidate explanations by testing all four combinations of `balance` (`0` / `10_000_000_000`) × `external_sendall_recipient` (`False` / `True`):

      | `balance` | `external_sendall_recipient` | beneficiary funded on-chain? | result |
      |---|---|---|---|
      | `0` | `False` (recipient = `auth_signer`) | no | code not wiped |
      | `0` | `True` (recipient = separate EOA) | no | code not wiped |
      | `10000000000` | `True` (recipient = separate EOA) | no | code not wiped |
      | `10000000000` | `False` (recipient = `auth_signer`) | **yes** | code not wiped |

    - **E. Cancun EIP-6780 (`tests/cancun/eip6780_selfdestruct/`).** Same symptoms in the Cancun run: account `Code`/`Balance`/`Nonce` left behind (`AssertionError: Code of 0x...: is 0x<code>, expected 0x.`, `Balance ... expected 0.`, `Nonce ... is 0x01, expected 0.`) and CREATE2 re-creation after SELFDESTRUCT failing because the old contract is still there (`Storage.KeyValueMismatchError: ... want 0x<address>, got 0x0`).
    - **F. Cancun `test_dynamic_create2_selfdestruct_collision*`.** These first failed with `Insufficient funds for transfer` (sender hard-coded to 7 ETH vs. a 150M gas limit × 1070 Gwei = 160.5 ETH). That was a test-funding problem, fixed in the test (`# Run On Hedera: increase funding because of "Insufficient funds for transfer"`, `pre.fund_eoa()`). After the fix the same tests fail with the SELFDESTRUCT symptoms above (`Balance of 0x...: is 0x174876e800, expected 0.`, `NonceMismatchError ... want 0x00, got 0x01`, `want 0x1, got 0x0`).
      Evidence from `test_dynamic_create2_selfdestruct_collision_two_different_transactions[...call_create2_contract_at_the_end_False-create2_dest_already_in_state_False]` (not a scaling/conversion problem): the post-check fails with `BalanceMismatchError ... want 10000000000000, got 0x174876e800`. The expected `1000` wei is scaled by the harness to `10000000000000`; the actual `0x174876e800` is exactly 10 tinybar, i.e. `first_create2_value = 10` from the *first* transaction, not 1000 from the second. On the node the CREATE2 contract still has its code (`0x73<beneficiary>ff`), nonce `1` and balance 10 tinybar, and the beneficiary has balance `0` / nonce `0`. So in transaction 1 the call with value `100` into the freshly created `SELFDESTRUCT` contract did not deliver the value or delete the contract (the #8 symptom, causing the #7 one), and in transaction 2 the CREATE2 to the same address collides, leaving the balance at 10.

    **Total:** 565 (Hedera-only; not yet checked against Geth): A = 9, B = 437 unique test IDs across 7 test functions (`test_selfdestruct_to_precompile` (187), `test_selfdestruct_to_precompile_state_access_boundary` (170), `test_selfdestruct_to_account` (29), `test_selfdestruct_state_access_boundary` (27), `test_selfdestruct_to_system_contract` (20), `test_selfdestruct_to_self` (3), `test_initcode_selfdestruct_to_self` (1)), C = 8, D = 4 confirmed (all combinations of `balance` × `external_sendall_recipient` for `create_opcode_CREATE-call_set_code_first_False`; full-suite count not yet determined). E = 99, F = 8 (Cancun run).

    **Hedera-only — A. Frontier (9 tests)**
    ```
    tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE2-state_test-operation_Operation.SUICIDE-transaction_create_False]
    tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE2-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_False]
    tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE-transaction_create_False]
    tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE-transaction_create_True]
    tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_False]
    tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_True]
    tests/frontier/create/test_create_suicide_store.py::test_create_suicide_store[fork_Prague-create_opcode_CREATE2-state_test]
    tests/frontier/create/test_create_suicide_store.py::test_create_suicide_store[fork_Prague-create_opcode_CREATE-state_test]
    tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SELFDESTRUCT-state_test]
    ```

    **Hedera-only — B. EIP-150 (7 test functions, 437 parametrized tests total)**
    ```
    tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py::test_initcode_selfdestruct_to_self...
    tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py::test_selfdestruct_state_access_boundary...
    tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py::test_selfdestruct_to_account...
    tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py::test_selfdestruct_to_precompile...
    tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py::test_selfdestruct_to_precompile_state_access_boundary...
    tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py::test_selfdestruct_to_self...
    tests/tangerine_whistle/eip150_operation_gas_costs/test_eip150_selfdestruct.py::test_selfdestruct_to_system_contract...
    ```

    **Hedera-only — C. EXTCODEHASH (8 tests)**
    ```
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_after_selfdestruct[fork_Prague-state_test-create]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_after_selfdestruct[fork_Prague-state_test-create2]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_created_and_deleted[fork_Prague-state_test-call]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_created_and_deleted_recheck_outer[fork_Prague-state_test]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-pre_existing-callcode]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-pre_existing-delegatecall]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-dynamic-callcode]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-dynamic-delegatecall]
    ```

    **Hedera-only — D. EIP-7702 (4 tests confirmed)**
    ```
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_destructing_account_deployed_in_same_tx[fork_Prague-state_test-create_opcode_CREATE-call_set_code_first_False-balance_0-external_sendall_recipient_False]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_destructing_account_deployed_in_same_tx[fork_Prague-state_test-create_opcode_CREATE-call_set_code_first_False-balance_0-external_sendall_recipient_True]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_destructing_account_deployed_in_same_tx[fork_Prague-state_test-create_opcode_CREATE-call_set_code_first_False-balance_10000000000-external_sendall_recipient_True]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_destructing_account_deployed_in_same_tx[fork_Prague-state_test-create_opcode_CREATE-call_set_code_first_False-balance_10000000000-external_sendall_recipient_False]
    ```

    **Hedera-only — E. Cancun EIP-6780 (99 tests)**
    ```
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-single_call-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-single_call-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_single_sendall_recipient-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_single_sendall_recipient-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_single_self_recipient-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_single_self_recipient-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_sendall_recipients-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_sendall_recipients-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_repeating_sendall_recipients_including_self-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_repeating_sendall_recipients_including_self-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_repeating_sendall_recipients_including_self_last-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_repeating_sendall_recipients_including_self_last-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-single_call-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-single_call-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_single_sendall_recipient-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_single_sendall_recipient-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_single_self_recipient-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_single_self_recipient-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_sendall_recipients-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_sendall_recipients-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_repeating_sendall_recipients_including_self-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_repeating_sendall_recipients_including_self-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_repeating_sendall_recipients_including_self_last-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_repeating_sendall_recipients_including_self_last-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-call_times_0-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-call_times_0-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-call_times_1-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-call_times_1-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-call_times_2-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-call_times_2-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-call_times_2-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-call_times_2-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode_create_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-tx_value_0]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_self_destructing_initcode_create_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-tx_value_100000]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recreate_self_destructed_contract_different_txs[fork_Prague-blockchain_test-call_times_1-recreate_times_1-selfdestruct_contract_initial_balance_0-selfdestruct_to_self-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recreate_self_destructed_contract_different_txs[fork_Prague-blockchain_test-call_times_1-recreate_times_1-selfdestruct_contract_initial_balance_100000-selfdestruct_to_self-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_calling_from_new_contract_to_pre_existing_contract[fork_Prague-state_test-create_opcode_CREATE-call_opcode_DELEGATECALL-selfdestruct_contract_initial_balance_0-call_times_1]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_calling_from_new_contract_to_pre_existing_contract[fork_Prague-state_test-create_opcode_CREATE-call_opcode_DELEGATECALL-selfdestruct_contract_initial_balance_1-call_times_1]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_calling_from_new_contract_to_pre_existing_contract[fork_Prague-state_test-create_opcode_CREATE-call_opcode_CALLCODE-selfdestruct_contract_initial_balance_0-call_times_1]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_calling_from_new_contract_to_pre_existing_contract[fork_Prague-state_test-create_opcode_CREATE-call_opcode_CALLCODE-selfdestruct_contract_initial_balance_1-call_times_1]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx_increased_nonce[fork_Prague-state_test-single_call-selfdestruct_contract_initial_balance_0-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx_increased_nonce[fork_Prague-state_test-single_call-selfdestruct_contract_initial_balance_0-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx_increased_nonce[fork_Prague-state_test-single_call-selfdestruct_contract_initial_balance_100000-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx_increased_nonce[fork_Prague-state_test-single_call-selfdestruct_contract_initial_balance_100000-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx_increased_nonce[fork_Prague-state_test-multiple_calls_single beneficiary-selfdestruct_contract_initial_balance_0-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx_increased_nonce[fork_Prague-state_test-multiple_calls_single beneficiary-selfdestruct_contract_initial_balance_0-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx_increased_nonce[fork_Prague-state_test-multiple_calls_single beneficiary-selfdestruct_contract_initial_balance_100000-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx_increased_nonce[fork_Prague-state_test-multiple_calls_single beneficiary-selfdestruct_contract_initial_balance_100000-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_and_destroy_multiple_contracts_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-num_contracts_2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_and_destroy_multiple_contracts_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-num_contracts_3]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_and_destroy_multiple_contracts_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-num_contracts_2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_and_destroy_multiple_contracts_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-num_contracts_3]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_multiple_contracts_destroy_one_then_destroy_other_next_tx[fork_Prague-blockchain_test-selfdestruct_contract_initial_balance_0]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_multiple_contracts_destroy_one_then_destroy_other_next_tx[fork_Prague-blockchain_test-selfdestruct_contract_initial_balance_100000]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_parent_creates_child_selfdestruct_one[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-destroy_parent_True]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_parent_creates_child_selfdestruct_one[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-destroy_parent_False]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_parent_creates_child_selfdestruct_one[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-destroy_parent_True]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_parent_creates_child_selfdestruct_one[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-destroy_parent_False]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recursive_contract_creation_and_selfdestruct[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-selfdestruct_on_unwind_True-recursion_depth_2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recursive_contract_creation_and_selfdestruct[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-selfdestruct_on_unwind_True-recursion_depth_3]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recursive_contract_creation_and_selfdestruct[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-selfdestruct_on_unwind_False-recursion_depth_2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recursive_contract_creation_and_selfdestruct[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-selfdestruct_on_unwind_False-recursion_depth_3]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recursive_contract_creation_and_selfdestruct[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-selfdestruct_on_unwind_True-recursion_depth_2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recursive_contract_creation_and_selfdestruct[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-selfdestruct_on_unwind_True-recursion_depth_3]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recursive_contract_creation_and_selfdestruct[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-selfdestruct_on_unwind_False-recursion_depth_2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recursive_contract_creation_and_selfdestruct[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-selfdestruct_on_unwind_False-recursion_depth_3]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case05_other_send-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case05_other_send-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case05_other_send-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case05_other_send-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case06_other_send_send-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case06_other_send_send-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case06_other_send_send-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case06_other_send_send-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case07_other_send_other-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case07_other_send_other-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case07_other_send_other-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case07_other_send_other-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-nonce-zero_balance-other]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-nonce-funded-other]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-storage-zero_balance-other]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-storage-funded-other]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-nonce_and_storage-zero_balance-other]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-nonce_and_storage-funded-other]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_in_delegate_context[fork_Prague-state_test-zero_balance-self-call_opcode_DELEGATECALL]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_in_delegate_context[fork_Prague-state_test-zero_balance-self-call_opcode_CALLCODE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_in_delegate_context[fork_Prague-state_test-zero_balance-other-call_opcode_DELEGATECALL]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_in_delegate_context[fork_Prague-state_test-zero_balance-other-call_opcode_CALLCODE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_in_delegate_context[fork_Prague-state_test-funded-self-call_opcode_DELEGATECALL]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_in_delegate_context[fork_Prague-state_test-funded-self-call_opcode_CALLCODE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_in_delegate_context[fork_Prague-state_test-funded-other-call_opcode_DELEGATECALL]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_in_delegate_context[fork_Prague-state_test-funded-other-call_opcode_CALLCODE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_recreate_in_later_block[fork_Prague-blockchain_test-zero_balance]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_recreate_in_later_block[fork_Prague-blockchain_test-funded]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_to_self_keeps_existing_balance[fork_Prague-state_test-zero_balance]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_to_self_keeps_existing_balance[fork_Prague-state_test-funded]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_revert.py::test_selfdestruct_created_in_same_tx_with_revert[fork_Prague-state_test-outer_selfdestruct_before_inner_call-same_tx]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_revert.py::test_selfdestruct_created_in_same_tx_with_revert[fork_Prague-state_test-outer_selfdestruct_after_inner_call-same_tx]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_revert.py::test_selfdestruct_not_created_in_same_tx_with_revert[fork_Prague-state_test-outer_selfdestruct_after_inner_call-not_same_tx-init_balance_2]
    ```

    **Hedera-only — F. Cancun dynamic CREATE2 collision (8 tests, after the funding fix)**
    ```
    tests/cancun/eip6780_selfdestruct/test_dynamic_create2_selfdestruct_collision.py::test_dynamic_create2_selfdestruct_collision[fork_Prague-state_test-call_create2_contract_in_between_True-call_create2_contract_at_the_end_True-create2_dest_already_in_state_False]
    tests/cancun/eip6780_selfdestruct/test_dynamic_create2_selfdestruct_collision.py::test_dynamic_create2_selfdestruct_collision[fork_Prague-state_test-call_create2_contract_in_between_True-call_create2_contract_at_the_end_False-create2_dest_already_in_state_False]
    tests/cancun/eip6780_selfdestruct/test_dynamic_create2_selfdestruct_collision.py::test_dynamic_create2_selfdestruct_collision[fork_Prague-state_test-call_create2_contract_in_between_False-call_create2_contract_at_the_end_True-create2_dest_already_in_state_False]
    tests/cancun/eip6780_selfdestruct/test_dynamic_create2_selfdestruct_collision.py::test_dynamic_create2_selfdestruct_collision_two_different_transactions[fork_Prague-blockchain_test-call_create2_contract_at_the_end_True-create2_dest_already_in_state_False]
    tests/cancun/eip6780_selfdestruct/test_dynamic_create2_selfdestruct_collision.py::test_dynamic_create2_selfdestruct_collision_two_different_transactions[fork_Prague-blockchain_test-call_create2_contract_at_the_end_False-create2_dest_already_in_state_False]
    tests/cancun/eip6780_selfdestruct/test_dynamic_create2_selfdestruct_collision.py::test_dynamic_create2_selfdestruct_collision_multi_tx[fork_Prague-blockchain_test-selfdestruct_on_first_tx_False-recreate_on_first_tx_False]
    tests/cancun/eip6780_selfdestruct/test_dynamic_create2_selfdestruct_collision.py::test_dynamic_create2_selfdestruct_collision_multi_tx[fork_Prague-blockchain_test-selfdestruct_on_first_tx_True-recreate_on_first_tx_False]
    tests/cancun/eip6780_selfdestruct/test_dynamic_create2_selfdestruct_collision.py::test_dynamic_create2_selfdestruct_collision_multi_tx[fork_Prague-blockchain_test-selfdestruct_on_first_tx_True-recreate_on_first_tx_True]
    ```

---
8. (CN?) CALL/CALLCODE/DELEGATECALL into a SELFDESTRUCT-only contract reports failure
    **Pattern:** `execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x...: want 0x1 (dec:1), got 0x0 (dec:0)` — the call's own success flag, stored via `Op.SSTORE(slot, call_opcode(address=target))`.
    
    **Root cause:** Related to [#7](#7-cn-selfdestruct-does-not-apply-when-triggered-via-internal-callcallcodedelegatecall-or-during-init-code) but a distinct symptom. `target`'s entire body is `Op.SELFDESTRUCT(beneficiary)`; calling into it with `CALL`, `CALLCODE`, or `DELEGATECALL` should trivially succeed per spec (`call_succeeds = call_opcode != Op.STATICCALL`). On Hedera the call itself reports failure (return value `0`) instead of succeeding — unlike #7's cases, where the call succeeds within the transaction and only the *end-of-transaction* account deletion/balance-drain is silently skipped. Here the failure is visible immediately via the call's own return value, for all three non-static call opcodes.
    
    **Cancun run (B):** 76 more failures in `tests/cancun/eip6780_selfdestruct/` have the same `Storage.KeyValueMismatchError: ... want 0x1 (dec:1), got 0x0`. Confirmed for `test_selfdestruct_pre_existing`, which stores the `CALL` result via `Op.SSTORE(slot, Op.CALL(...))` into a SELFDESTRUCT contract and sees `0` instead of `1`. The other tests in this group were grouped by error text only and are **not individually verified** to store a call result. If the call itself fails on Hedera, the SELFDESTRUCT inside it is rolled back, which would also explain #7 — this link is a hypothesis to check.

    **Total:** 79 (Hedera-only; not yet checked against Geth): A = 3, B = 76 (Cancun run).
    
    **Hedera-only — A. EXTCODEHASH (3 tests)**
    ```
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_CALL-state_test]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_CALLCODE-state_test]
    tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_DELEGATECALL-state_test]
    ```

    **Hedera-only — B. Cancun EIP-6780 (76 tests)**
    ```
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_CALL-first_selfdestruct_CALL]
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_CALL-first_selfdestruct_CALLCODE]
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_CALL-first_selfdestruct_DELEGATECALL]
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_CALLCODE-first_selfdestruct_CALL]
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_CALLCODE-first_selfdestruct_CALLCODE]
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_CALLCODE-first_selfdestruct_DELEGATECALL]
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_DELEGATECALL-first_selfdestruct_CALL]
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_DELEGATECALL-first_selfdestruct_CALLCODE]
    tests/cancun/eip6780_selfdestruct/test_reentrancy_selfdestruct_revert.py::test_reentrancy_selfdestruct_revert[fork_Prague-state_test-second_selfdestruct_DELEGATECALL-first_selfdestruct_DELEGATECALL]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-single_call_self-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-single_call_self-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_sendall_recipients_including_self-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_sendall_recipients_including_self-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_sendall_recipients_including_self_last-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_sendall_recipients_including_self_last-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-single_call_self-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-single_call_self-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_sendall_recipients_including_self-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_sendall_recipients_including_self-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_sendall_recipients_including_self_last-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_create_selfdestruct_same_tx[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_sendall_recipients_including_self_last-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-single_call_self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_single_self_recipient]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_sendall_recipients_including_self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_sendall_recipients_including_self_last]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_repeating_sendall_recipients_including_self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_0-multiple_calls_multiple_repeating_sendall_recipients_including_self_last]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-single_call_self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_single_self_recipient]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_sendall_recipients_including_self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_sendall_recipients_including_self_last]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_repeating_sendall_recipients_including_self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_selfdestruct_pre_existing[fork_Prague-state_test-selfdestruct_contract_initial_balance_100000-multiple_calls_multiple_repeating_sendall_recipients_including_self_last]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case01_self-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case01_self-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case01_self-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case01_self-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case02_self_self-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case02_self_self-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case02_self_self-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case02_self_self-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case03_self_other-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case03_self_other-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case03_self_other-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case03_self_other-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case04_other_self-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case04_other_self-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case04_other_self-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case04_other_self-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case08_other_send_self-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case08_other_send_self-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case08_other_send_self-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case08_other_send_self-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case09_self_send-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case09_self_send-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case09_self_send-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case09_self_send-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case10_self_send_send-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case10_self_send_send-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case10_self_send_send-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case10_self_send_send-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case11_self_send_other-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case11_self_send_other-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case11_self_send_other-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case11_self_send_other-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case12_self_send_self-zero_balance-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case12_self_send_self-zero_balance-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case12_self_send_self-funded-create_opcode_CREATE]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_sequences[fork_Prague-state_test-case12_self_send_self-funded-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-nonce-zero_balance-self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-nonce-funded-self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-storage-zero_balance-self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-storage-funded-self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-nonce_and_storage-zero_balance-self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_finalization.py::test_selfdestruct_clears_nonce_and_storage[fork_Prague-state_test-nonce_and_storage-funded-self]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct_revert.py::test_selfdestruct_not_created_in_same_tx_with_revert[fork_Prague-state_test-outer_selfdestruct_before_inner_call-not_same_tx-init_balance_2]
    ```

---
9. (Not supported on Hedera? Skip?) SELFDESTRUCT beneficiary must be an existing account on Hedera
    **Pattern:** `execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32003, message=Transaction rejected: INVALID_SOLIDITY_ADDRESS - receipt for transaction ... contained error status INVALID_SOLIDITY_ADDRESS)`.
    
    **Root cause:** `test_set_code_to_self_destruct`'s `external_sendall_recipient_True` variants set `recipient = pre.fund_eoa(0)` (`test_set_code_txs.py:515`). Because the amount is `0`, `_fund_eoa` (`pre_alloc.py:710-718`) never sends a funding transaction for it, so `recipient` has no footprint on the Hedera ledger. When the delegated contract executes `SELFDESTRUCT(recipient)`, Hedera rejects the transaction outright with `INVALID_SOLIDITY_ADDRESS` instead of crediting the balance — the beneficiary of a `SELFDESTRUCT` must already exist as an account on Hedera. This reproduces identically regardless of `auth_signer`'s own balance (`balance_0` and `balance_10000000000` both fail the same way), confirming `recipient`'s non-existence — not `auth_signer`'s — is the trigger. This is a different mechanism from [#19](#19-call-to-eip-7702-delegated-eoa-rejected-as-invalid_contract_id) (which is about calling directly into an already-delegated EOA, not about a SELFDESTRUCT beneficiary).
    
    **Total:** 2 (Hedera-only; not yet checked against Geth)
    
    **Hedera-only — 2 tests**
    ```
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_destruct[fork_Prague-state_test-balance_0-external_sendall_recipient_True]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_destruct[fork_Prague-state_test-balance_10000000000-external_sendall_recipient_True]
    ```

---
10. (CN?) Warm-access gas cost not honored — repeat accesses (EIP-2929) and coinbase pre-warming (EIP-3651)
    **Pattern:** `Storage.KeyValueMismatchError: ... want 0x64 (100), got 0xa28 (2600)` (numeric cost reads cold instead of warm) — or `want 0x1, got 0x0` for the `CALL`-family opcodes, where the measurement call itself fails/runs out of gas because it was only given the warm-cost gas allowance.

    **Root cause:** Same underlying gap in two forms: Hedera charges the cold access price (`2600`, or ~`2855` for the `CALL`-family once their own overhead is included) where the warm price (`100`) is expected, so access-list warming isn't honored. Related to [hedera_shanghai.md #1](hedera_shanghai.md#1-cn-coinbase-address-is-not-pre-warmed-eip-3651).
    - **A. Repeat access (EIP-2929).** `test_constant_gas` measures generic warm/cold access for `BALANCE`/`EXTCODESIZE`/`EXTCODECOPY`/`EXTCODEHASH`/`CALLCODE`/`DELEGATECALL`/`STATICCALL`, where the test's own `setup_code` already accesses the address once (making it warm for the measured second access). On Hedera the second access still costs the cold price, suggesting warming isn't honored for repeat accesses within a transaction.
    - **B. Coinbase (EIP-3651).** EIP-3651 (Warm Coinbase, active since Shanghai) requires the `COINBASE` address to be added to the access list at the start of transaction execution, so the first `EXTCODESIZE`/`EXTCODECOPY`/`EXTCODEHASH`/`BALANCE`/`CALL`-family access to it costs the warm price. `test_warm_coinbase_gas_usage` measures this cost directly and expects the warm price on Prague (`fork >= Shanghai`), but measures the cold price — Hedera isn't pre-warming the coinbase address. `test_warm_coinbase_call_out_of_gas`'s `sufficient_gas` variants independently confirm this: they provide exactly enough gas for a warm-cost call to succeed, and the call fails (runs OOG) because Hedera charges the cold price instead.

    **Total:** 19 (Hedera-only; not yet checked against Geth): A = 7; B = 12 — all 8 `test_warm_coinbase_gas_usage` opcodes, plus the 4 `test_warm_coinbase_call_out_of_gas` `sufficient_gas` variants. The matching `insufficient_gas` variants pass (both warm and cold accounting equally run out of gas there, so the distinction doesn't surface).

    **Hedera-only — A. Repeat access (7 tests)**
    ```
    tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-BALANCE-state_test]
    tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODESIZE-state_test]
    tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODECOPY-state_test]
    tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODEHASH-state_test]
    tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CALLCODE-state_test]
    tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DELEGATECALL-state_test]
    tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-STATICCALL-state_test]
    
    ```

    **Hedera-only — B. Coinbase (12 tests)**
    ```
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-EXTCODESIZE]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-EXTCODECOPY]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-EXTCODEHASH]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-BALANCE]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-CALL]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-CALLCODE]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-DELEGATECALL]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-STATICCALL]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-CALL-sufficient_gas]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-CALLCODE-sufficient_gas]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-DELEGATECALL-sufficient_gas]
    tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-STATICCALL-sufficient_gas]
    
    ```

---
11. (CN?) BLOCKHASH returns 0 for genesis/recent blocks
    **Pattern:** `Storage.KeyValueMismatchError: ... want 0x0, got 0x1` — storing `ISZERO(BLOCKHASH(n))`, expecting `0` (hash present) but getting `1` (hash absent/zero).
    
    **Root cause:** `test_genesis_hash_available` expects `BLOCKHASH(0)` (genesis) and `BLOCKHASH(1)` to return a real, nonzero hash when queried from a later block. On Hedera both return `0`, across all four setup variants (no blocks, one empty block, one block with a tx, 256 empty blocks) — suggesting Hedera doesn't populate `BLOCKHASH` for genesis or otherwise returns `0` where a real hash is expected.
    
    **Total:** 4 (Hedera-only; not yet checked against Geth)
    
    **Hedera-only — 4 tests**
    ```
    tests/frontier/opcodes/test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-no_blocks]
    tests/frontier/opcodes/test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-one_empty_block]
    tests/frontier/opcodes/test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-one_block_with_tx]
    tests/frontier/opcodes/test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-256_empty_blocks]
    ```

---
12. ⚠️(CN?) CALL with a nonzero value to a precompile address fails
    **Pattern:** `Storage.KeyValueMismatchError: ... want 0x1, got 0x0` — a `CALL`/`CALLCODE` sending value to the identity precompile (`0x04`), expected to succeed, but the call fails.
    
    **Root cause:** Not the sub-tinybar floor — already ruled out. The test's `value` is already exactly 1 tinybar (`0x2540BE400`), and the caller contract's balance is scaled to match exactly (confirmed via the deploy log: `balance=0.000000010000000000 ETH`). Bumping the caller's balance to 2 tinybar (so balance > value with margin) still fails identically; bumping the call's `gas` from `0x30D40` to `1_000_000` also still fails identically. Both "insufficient balance" and "insufficient gas" are ruled out. The only thing distinguishing this from the passing `identity_1`/`identity_2`/etc. variants in the same file is that it sends a *nonzero value* to a *precompile address* — pointing to Hedera not supporting value transfers to precompile addresses via `CALL`/`CALLCODE` at all, independent of amount, balance, or gas. No test-side parameter fix found.
    
    **Total:** 2 (Hedera-only; not yet checked against Geth)
    
    **Hedera-only — 2 tests**
    ```
    tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1_nonzerovalue-call_type_CALL]
    tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1_nonzerovalue-call_type_CALLCODE]
    ```

---
13. (CN?) Gas-accounting precision mismatches in precompile/CALL cost measurement
    **Pattern:** `Storage.KeyValueMismatchError: ... want 0xa (10), got 0x0` (underfunded-call loop never records expected failures) / `want 0x1, got 0x0` (gas-usage-difference check between a precompile and a reference address).
    
    **Root cause:** Not fully traced — both tests rely on exact-to-the-gas-unit accounting (`test_repeated_underfunded_calls` forwards precompile gas minus exactly 1; `test_precompiles`'s `precompile_exists_False` case diffs the gas cost of calling a precompile address vs. a plain address). Given the other confirmed gas-accounting divergences in this doc (#1, #2), this is plausibly part of the same general theme — Hedera's gas metering for calls/precompiles doesn't precisely match EVM-spec expectations in edge cases — but the exact mechanism here isn't confirmed.
    
    **Total:** 4 (Hedera-only; not yet checked against Geth)
    
    **Hedera-only — 4 tests**
    ```
    tests/frontier/precompiles/test_ecrecover.py::test_repeated_underfunded_calls[fork_Prague-call_opcode_CALL-state_test]
    tests/frontier/precompiles/test_ecrecover.py::test_repeated_underfunded_calls[fork_Prague-call_opcode_CALLCODE-state_test]
    tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000012-precompile_exists_False-state_test]
    tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000000-precompile_exists_False-state_test]
    ```

---
14. Miscellaneous singleton failures — not yet root-caused
    
    **Pattern:** varies per test; see each below.
    ```
    - `test_all_opcodes` (the generic "call every opcode's dedicated contract" test): `Storage.KeyValueMismatchError: ... want 0x1, got 0x0` at key `0x00` — the subcall to opcode `0x00`'s (`STOP`-only) contract reports failure, even though a bare `STOP` contract should trivially succeed. Doesn't fit any other pattern in this doc; needs isolated investigation.
    - `test_block_intermediate_state`: `JSONRPCError(code=-32003, message=Transaction rejected: INVALID_ETHEREUM_TRANSACTION)` for a contract-creation (`to: null`) legacy tx with `gas_limit=150_000_000`. Not yet isolated whether the gas limit size, the creation itself, or something else triggers the rejection.
    - `test_valid_reencoded_transaction`: `JSONRPCError(code=-32001, message=Requested resource not found. address '0x...'.)` — the RLP-reencoding baseline test queries an address the relay doesn't know about yet; not yet traced to a specific cause.
    - `test_scenarios` (`program_COINBASE`/`program_NUMBER`/`program_GASLIMIT`, `scenario_STATICCALL_STATICCALL`): expected `COINBASE`/`NUMBER`/`GASLIMIT` values don't match what's read back through a nested `STATICCALL`→`STATICCALL` context — actual values look arbitrary/unrelated (e.g. `98` instead of a real coinbase address), suggesting something specific to nested static calls rather than the opcodes themselves being wrong at top level.
    ```
    
    **Total:** 6 (Hedera-only; not yet checked against Geth)
    
    **Hedera-only — 6 tests**
    ```
    tests/frontier/opcodes/test_all_opcodes.py::test_all_opcodes[fork_Prague-state_test]
    tests/frontier/examples/test_block_intermediate_state.py::test_block_intermediate_state[fork_Prague-blockchain_test]
    tests/frontier/validation/test_transaction_rlp.py::test_valid_reencoded_transaction[fork_Prague-transaction_test]
    tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_COINBASE-debug]
    tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_NUMBER-debug]
    tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_GASLIMIT-debug]
    ```

---
15. (Possible test-infra flake, not a confirmed Hedera bug) `test_tx_gas_limit` ERROR
    **Pattern:** `ERROR ... JSONRPCError(code=-32003, message=Transaction rejected: WRONG_NONCE)`
    
    **Root cause:** Not confirmed as a genuine Hedera limitation. The failing transaction's `to` field is the session's own worker/seed key address, not the test's own `to = pre.fund_eoa()` target — this looks like a background funding/sweep transaction from shared session infrastructure hit a nonce race, misattributed to this test in the summary, rather than something about `test_tx_gas_limit`'s own content (which already carries an unrelated `# Run On Hedera` fix for its `gas_price`). Needs an isolated re-run to confirm before treating as a real issue.
    
    **Total:** 1 (unconfirmed)
    
    **Unconfirmed — 1 test**
    ```
    tests/frontier/validation/test_transaction.py::test_tx_gas_limit[fork_Prague-blockchain_test]
    ```

---
16. (CN?) Out-of-gas transaction does not consume the full declared gas_limit
    **Pattern:** `execution_testing.base_types.composite_types.Account.BalanceMismatchError: unexpected balance for account 0x...: want 0x00, got 0x01ff973cafa80000` — the sender's post-tx balance is expected to be fully drained (the EVM-spec penalty for running out of gas is to consume the entire `gas_limit`, with no refund), but a nonzero balance remains.
    
    **Root cause:** Per the EVM spec, when a transaction runs out of gas, the *entire* declared `gas_limit` is charged to the sender as a penalty — none of it is refunded, regardless of how much gas was actually consumed by opcodes before the OOG point. `test_create_oog_from_eoa_refunds` relies on exactly this to assert `sender` ends with `balance=0` after an OOG scenario (pre-EIP-8037). Tracing a failing case: the sender was funded with precisely `gas_limit(400_000) × gas_price(1070 Gwei) = 0.428 ETH` (confirmed via the harness's own deferred-funding calculation, which matches exactly), yet it ends with `0.144 ETH` left over — meaning only ~265,420 of the 400,000 declared gas units were actually charged. Hedera appears to charge only for gas consumed up to the point of failure (like a `REVERT`), not the full declared `gas_limit` as EVM-spec OOG semantics require. This is independent of transaction funding — any funding strategy (hardcoded amount or deferred) hits the same shortfall, since the gas simply isn't being charged in full.
    
    **Total:** 16 confirmed — every `refund_type` × `oog_scenario in {oog_code_deposit, oog_invalid_opcode}` combination fails identically (same leftover `0x01ff973cafa80000`). All 8 `no_oog` variants pass, since that scenario doesn't assert sender balance.
    
    **Hedera-only — 16 tests**
    ```
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-sstore_direct-oog_code_deposit]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-sstore_direct-oog_invalid_opcode]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-sstore_call-oog_code_deposit]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-sstore_call-oog_invalid_opcode]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-sstore_delegatecall-oog_code_deposit]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-sstore_delegatecall-oog_invalid_opcode]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-sstore_callcode-oog_code_deposit]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-sstore_callcode-oog_invalid_opcode]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-selfdestruct-oog_code_deposit]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-selfdestruct-oog_invalid_opcode]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-log_op-oog_code_deposit]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-log_op-oog_invalid_opcode]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-nested_create-oog_code_deposit]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-nested_create-oog_invalid_opcode]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-nested_create2-oog_code_deposit]
    tests/cancun/create/test_create_oog_from_eoa_refunds.py::test_create_oog_from_eoa_refunds[fork_Prague-blockchain_test-nested_create2-oog_invalid_opcode]
    ```

---
17. (Relay?) RPC rejects transaction — invalid yParity (-32000)
    **Pattern:** `JSONRPCError(code=-32000, message=Invalid arguments: invalid yParity ...)`
    
    **Root cause:** `test_valid_tx_invalid_auth_signature` intentionally sets a garbage `v`/`r`/`s` (e.g. `v=2`, which isn't a valid yParity — must be 0 or 1) on the authorization tuple. Per the EIP-7702 spec, an authorization with an invalid/unrecoverable signature should simply be **skipped** (ignored) without affecting the rest of the transaction — the outer transaction should still execute normally, which is why the test expects `callee_address`'s storage to be set regardless. Hedera's JSON-RPC relay instead validates the authorization list's signature components upfront and rejects the **entire transaction** at submission (`Invalid arguments: invalid yParity (argument="signature", value={..., "yParity": 2}, code=INVALID_ARGUMENT)`), rather than silently discarding the bad authorization and proceeding — stricter validation than the spec requires, fully Hedera-only (8/8).
    
    **Total:** 8 (0 also fail on Geth, 8 Hedera-only)
    
    **Also fails on Geth — 0 tests**
    _(none)_
    
    **Hedera-only — 8 tests**
    ```
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=2**8-1,r=s=2**256-1]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=2**8-1]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=27]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=28]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=29]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=2]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=35]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=36]
    ```

---
18. (Relay?) Zero-value r/s in authorization tuple serialized as empty '0x'
    **Pattern:** `pydantic_core._pydantic_core.ValidationError: N validation error(s) for TransactionByHashResponse` — `authorizationList.0.r` and/or `authorizationList.0.s`, `Value error, invalid literal for int() with base 0: '0x'`
    
    **Root cause:** `test_valid_tx_invalid_auth_signature` sets `r=0` and/or `s=0` on the authorization tuple. When Hedera's JSON-RPC relay serializes the authorization list in its `getTransactionByHash` response, a zero-valued `r`/`s` is encoded as the empty hex string `'0x'` instead of `'0x0'`. The test client's pydantic model calls `int(value, 0)` on that field, which raises on `'0x'`, so the response fails to parse before the test can assert on results. Narrower and more specific than the general schema-mismatch issue in [1](#1-pydantic-validation-error-on-json-rpc-transaction-response) — this is a single, precise zero-value hex-encoding bug.
    
    **Total:** 3 (0 also fail on Geth, 3 Hedera-only)
    
    **Also fails on Geth — 0 tests**
    _(none)_
    
    **Hedera-only — 3 tests**
    ```
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-r=0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-s=0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_valid_tx_invalid_auth_signature[fork_Prague-state_test-v=r=s=0]
    ```

---
19. (CN?) Call to EIP-7702-delegated EOA rejected as INVALID_CONTRACT_ID
    **Pattern:** Transaction included with `status: "0x0"` and `revertReason: 0x494e56414c49445f434f4e54524143545f4944` (`"INVALID_CONTRACT_ID"`), even though the target EOA's delegation was set correctly.
    
    **Root cause:** After an EOA is given EIP-7702 delegated code (`eth_getCode` correctly returns the `0xef0100...` designation pointing at the implementation contract), sending a plain transaction directly `to:` that EOA is rejected by Hedera's relay/consensus layer with `INVALID_CONTRACT_ID`. The delegated code never executes, so any storage writes it should perform never happen — e.g. in `test_pointer_measurements`, `pointer`'s storage slot 0 is expected to hold `ADDRESS()` (the pointer's own address) but reads back `0x0` because the call that should have triggered execution reverted before running. Hedera appears to not recognize a freshly-delegated EOA as a callable "contract" for this call path.
    
    Repro:
    ```bash
    uv run execute remote -rA --verbose --fork=Prague \
        --rpc-endpoint=http://localhost:37546/ \
        --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
        --rpc-chain-id=298 \
        --seed-account-sweep-amount='1_000_000 ether' \
        --default-max-fee-per-blob-gas=710_000_000_000 \
        --tx-wait-timeout=15 \
        --max-tx-per-batch=1 \
        "tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_measurements[fork_Prague-blockchain_test]"
    ```
    
    **Hedera-only — at least 1 test**
    ```
    tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_measurements[fork_Prague-blockchain_test]
    ```
    Possible more failures like this:
    ```
    FAILED tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_to_pointer[fork_Prague-state_test-sender_is_auth_signer_True-sender_delegated_True] - execution_testing.base_types.composite_types.Account.CodeMismatchError: unexpected code for account 0x3c63fc0d6910d373b7817d9170f10717b59f6cf6: want 0xef010035a80db333f9b20f453db41b92ef4b5f3556539f, got...
    FAILED tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_to_pointer[fork_Prague-state_test-sender_is_auth_signer_True-sender_delegated_False] - execution_testing.base_types.composite_types.Account.CodeMismatchError: unexpected code for account 0x53d66c859f8e3e9d1972a8f3db64e57dc0908ebb: want 0xef01000b89eec315c7fb5c07e757b774637dd3f1122999, got 0x
    FAILED tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_to_pointer[fork_Prague-state_test-sender_is_auth_signer_False-sender_delegated_True] - execution_testing.base_types.composite_types.Account.CodeMismatchError: unexpected code for account 0xd3266eecaad948f0d026305d5d3a9b89d8dc0b3c: want 0xef01001919d12e0178afd6a6cba19cb37b2d3731f1c8bb, got 0x
    FAILED tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_to_pointer[fork_Prague-state_test-sender_is_auth_signer_False-sender_delegated_False] - execution_testing.base_types.composite_types.Account.CodeMismatchError: unexpected code for account 0x79fc2d924ee193b64d85242e579e179ed4cd7699: want 0xef0100d74338f4ac44a1fd326648173801a7595db6baf5, got 0x
    FAILED tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_eoa_init_as_pointer[fork_Prague-state_test] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32001, message=[Request ID: ad1ba505-53be-41ce-b4e1-21b1be22af91] Requested resource not found. address '0x9ce0bD393a8920E2eFC...
    ```

---
20. (Relay caching?) EIP-7702 authorization tuple does not bump authority nonce
    **Pattern:** `execution_testing.base_types.composite_types.Account.NonceMismatchError: unexpected nonce for account 0x...: want 0x01, got 0x00` (higher expected nonces for tests that chain/re-authorize).
    
    **Root cause:** Whenever a set-code (type 0x4) transaction's `authorization_list` is processed on Hedera — whether the authorization is sent as part of the pre-alloc setup (e.g. `pre.fund_eoa(0, delegation="Self")`) or as part of the test's own transaction — the outer transaction is accepted and mined, but the authority account's nonce is not incremented. This occurs for both self-delegation and delegation to a separately deployed contract, so it isn't limited to one authorization shape; it points to a broader gap in how Hedera applies EIP-7702 authorization tuples. See also [#21](#21-eip-7702-authorization-tuple-does-not-write-delegation-designation-code) — a related but distinct symptom (delegation code missing instead of nonce not bumped), likely the same underlying gap.
    
    **Total:** 196 (Hedera-only; not yet checked against Geth)
    
    **Hedera-only — 196 tests**
    ```
    tests/prague/eip7702_set_code_tx/test_gas.py::test_self_set_code_cost[fork_Prague-state_test-pre_authorized_False]
    tests/prague/eip7702_set_code_tx/test_gas.py::test_self_set_code_cost[fork_Prague-state_test-pre_authorized_True]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_address_from_set_code[fork_Prague-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_call_into_chain_delegating_set_code[fork_Prague-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_call_into_chain_delegating_set_code[fork_Prague-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_call_into_chain_delegating_set_code[fork_Prague-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_call_into_chain_delegating_set_code[fork_Prague-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_call_into_self_delegating_set_code[fork_Prague-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_call_into_self_delegating_set_code[fork_Prague-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_call_into_self_delegating_set_code[fork_Prague-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_call_into_self_delegating_set_code[fork_Prague-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing[fork_Prague-state_test-delegated_account-not_self_sponsored]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing[fork_Prague-state_test-undelegated_account-not_self_sponsored]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing_and_set[fork_Prague-state_test-delegated_account]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing_and_set[fork_Prague-state_test-undelegated_account]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing_failing_tx[fork_Prague-state_test-invalid_opcode]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing_failing_tx[fork_Prague-state_test-out_of_gas]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing_failing_tx[fork_Prague-state_test-revert]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing_tx_to[fork_Prague-state_test-delegated_account-not_self_sponsored]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing_tx_to[fork_Prague-state_test-undelegated_account-not_self_sponsored]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_chain_delegating_set_code[fork_Prague-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_self_delegating_set_code[fork_Prague-state_test-balance_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_self_delegating_set_code[fork_Prague-state_test-balance_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_set_code[fork_Prague-state_test-CONTRACT-balance_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_set_code[fork_Prague-state_test-CONTRACT-balance_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_set_code[fork_Prague-state_test-EMPTY_ACCOUNT-balance_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_set_code[fork_Prague-state_test-EMPTY_ACCOUNT-balance_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_set_code[fork_Prague-state_test-EOA-balance_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_set_code[fork_Prague-state_test-EOA-balance_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_set_code[fork_Prague-state_test-EOA_WITH_SET_CODE-balance_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_ext_code_on_set_code[fork_Prague-state_test-EOA_WITH_SET_CODE-balance_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_reset_code[fork_Prague-blockchain_test-not_self_sponsored]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_code_on_set_code[fork_Prague-state_test-balance_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_code_on_set_code[fork_Prague-state_test-balance_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state[fork_Prague-state_test-call_authority_first_then_set_code_address]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state[fork_Prague-state_test-call_set_code_address_first_then_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state_call_types[fork_Prague-call_opcode_CALL-state_test-call_authority_first_then_set_code_address]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state_call_types[fork_Prague-call_opcode_CALL-state_test-call_set_code_address_first_then_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state_call_types[fork_Prague-call_opcode_CALLCODE-state_test-call_authority_first_then_set_code_address]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state_call_types[fork_Prague-call_opcode_CALLCODE-state_test-call_set_code_address_first_then_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state_call_types[fork_Prague-call_opcode_DELEGATECALL-state_test-call_authority_first_then_set_code_address]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state_call_types[fork_Prague-call_opcode_DELEGATECALL-state_test-call_set_code_address_first_then_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state_call_types[fork_Prague-call_opcode_STATICCALL-state_test-call_authority_first_then_set_code_address]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_address_and_authority_warm_state_call_types[fork_Prague-call_opcode_STATICCALL-state_test-call_set_code_address_first_then_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_call_set_code[fork_Prague-call_opcode_CALL-state_test-value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_call_set_code[fork_Prague-call_opcode_CALL-state_test-value_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_call_set_code[fork_Prague-call_opcode_CALLCODE-state_test-value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_call_set_code[fork_Prague-call_opcode_CALLCODE-state_test-value_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_call_set_code[fork_Prague-call_opcode_DELEGATECALL-state_test-value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_call_set_code[fork_Prague-call_opcode_STATICCALL-state_test-value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_multiple_first_valid_authorization_tuples_same_signer[fork_Prague-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_multiple_valid_authorization_tuples_first_invalid_same_signer[fork_Prague-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_multiple_valid_authorization_tuples_same_signer_increasing_nonce[fork_Prague-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_account_deployed_in_same_tx[fork_Prague-create_opcode_CREATE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_account_deployed_in_same_tx[fork_Prague-create_opcode_CREATE2-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_contract_creator[fork_Prague-create_opcode_CREATE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_contract_creator[fork_Prague-create_opcode_CREATE2-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000001-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000001-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000001-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000001-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000002-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000002-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000002-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000002-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000003-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000003-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000003-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000003-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000004-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000004-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000004-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000004-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000005-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000005-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000005-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000005-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000006-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000006-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000006-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000006-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000007-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000007-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000007-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000007-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000008-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000008-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000008-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000008-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000009-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000009-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000009-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000009-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000a-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000a-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000a-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000a-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000b-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000b-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000b-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000b-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000c-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000c-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000c-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000c-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000d-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000d-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000d-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000d-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000e-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000e-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000e-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000e-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000f-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000f-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000f-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000f-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000010-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000010-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000010-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000010-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000011-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000011-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000011-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000011-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000001-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000002-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000003-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000004-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000005-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000006-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000007-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000008-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000009-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x000000000000000000000000000000000000000a-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x000000000000000000000000000000000000000b-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x000000000000000000000000000000000000000c-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x000000000000000000000000000000000000000d-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x000000000000000000000000000000000000000e-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x000000000000000000000000000000000000000f-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000010-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_precompile_not_enough_gas_for_precompile_execution[fork_Prague-precompile_0x0000000000000000000000000000000000000011-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_caller[fork_Prague-call_opcode_CALL-state_test-value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_caller[fork_Prague-call_opcode_CALL-state_test-value_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_caller[fork_Prague-call_opcode_CALLCODE-state_test-value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_caller[fork_Prague-call_opcode_CALLCODE-state_test-value_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_caller[fork_Prague-call_opcode_DELEGATECALL-state_test-value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_caller[fork_Prague-call_opcode_STATICCALL-state_test-value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_destruct[fork_Prague-state_test-balance_0-external_sendall_recipient_False]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_self_destruct[fork_Prague-state_test-balance_10000000000-external_sendall_recipient_False]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-invalid-tx_value_0-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-invalid-tx_value_0-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-invalid-tx_value_10000000000-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-invalid-tx_value_10000000000-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-out-of-gas-tx_value_0-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-out-of-gas-tx_value_0-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-out-of-gas-tx_value_10000000000-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-out-of-gas-tx_value_10000000000-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-return-tx_value_0-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-return-tx_value_0-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-return-tx_value_10000000000-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-return-tx_value_10000000000-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-revert-tx_value_0-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-revert-tx_value_0-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-revert-tx_value_10000000000-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-revert-tx_value_10000000000-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-stop-tx_value_0-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-stop-tx_value_0-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-stop-tx_value_10000000000-one_wei_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-stop-tx_value_10000000000-zero_balance_authority]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore_then_sload[fork_Prague-blockchain_test-]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore_then_sload[fork_Prague-blockchain_test-auth_signer_in_access_list]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore_then_sload[fork_Prague-blockchain_test-sender_in_access_list]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_system_contract[fork_Prague-call_opcode_CALL-system_contract_0x00000000219ab540356cbb839cbe05303d7705fa-blockchain_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_system_contract[fork_Prague-call_opcode_CALL-system_contract_0x00000961ef480eb55e80d19ad83579a64c007002-blockchain_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_system_contract[fork_Prague-call_opcode_CALL-system_contract_0x0000bbddc7ce488642fb579f8b00f3a590007251-blockchain_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_system_contract[fork_Prague-call_opcode_CALL-system_contract_0x0000f90827f1c53a10cb7a02335b175320002935-blockchain_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_system_contract[fork_Prague-call_opcode_CALL-system_contract_0x000f3df6d732807ef1319fb7b8bb8522d0beac02-blockchain_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_tstore_reentry[fork_Prague-call_opcode_CALL-state_test-return_opcode_RETURN]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_tstore_reentry[fork_Prague-call_opcode_CALL-state_test-return_opcode_REVERT]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_tstore_reentry[fork_Prague-call_opcode_CALLCODE-state_test-return_opcode_RETURN]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_tstore_reentry[fork_Prague-call_opcode_CALLCODE-state_test-return_opcode_REVERT]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_tstore_reentry[fork_Prague-call_opcode_DELEGATECALL-state_test-return_opcode_RETURN]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_tstore_reentry[fork_Prague-call_opcode_DELEGATECALL-state_test-return_opcode_REVERT]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_tstore_reentry[fork_Prague-call_opcode_STATICCALL-state_test-return_opcode_RETURN]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_tstore_reentry[fork_Prague-call_opcode_STATICCALL-state_test-return_opcode_REVERT]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_using_chain_specific_id[fork_Prague-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_using_valid_synthetic_signatures[fork_Prague-state_test-v=0,r=1,s=1]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_using_valid_synthetic_signatures[fork_Prague-state_test-v=0,r=1,s=SECP256K1N_OVER_2]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_using_valid_synthetic_signatures[fork_Prague-state_test-v=0,r=SECP256K1N-2,s=1]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_using_valid_synthetic_signatures[fork_Prague-state_test-v=1,r=1,s=1]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_using_valid_synthetic_signatures[fork_Prague-state_test-v=1,r=1,s=SECP256K1N_OVER_2]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_using_valid_synthetic_signatures[fork_Prague-state_test-v=1,r=SECP256K1N-2,s=1]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_tx_into_chain_delegating_set_code[fork_Prague-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_tx_into_self_delegating_set_code[fork_Prague-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_resets_an_empty_code_account_with_storage[fork_Prague-blockchain_test]
    ```

---
21. (CN?) EIP-7702 authorization tuple does not write delegation designation code
    **Pattern:** `execution_testing.base_types.composite_types.Account.CodeMismatchError: unexpected code for account 0x...: want 0xef0100..., got 0x` — the authority account's code is left empty instead of holding the expected delegation designation.
    
    **Root cause:** Same underlying gap as [#20](#20-relay-caching-eip-7702-authorization-tuple-does-not-bump-authority-nonce): Hedera accepts and mines the outer set-code transaction but does not apply the authorization tuple. Here the test's `post` check happens to assert `code` (rather than `nonce`), surfacing as a `CodeMismatchError` instead — the authority's code stays empty (`0x`) rather than becoming the `0xef0100<address>` delegation designation.
    
    **Total:** 19 (Hedera-only; not yet checked against Geth)
    
    **Hedera-only — 19 tests**
    ```
    tests/prague/eip7702_set_code_tx/test_gas.py::test_call_to_pre_authorized_oog[fork_Prague-call_opcode_CALL-state_test]
    tests/prague/eip7702_set_code_tx/test_gas.py::test_call_to_pre_authorized_oog[fork_Prague-call_opcode_CALLCODE-state_test]
    tests/prague/eip7702_set_code_tx/test_gas.py::test_call_to_pre_authorized_oog[fork_Prague-call_opcode_DELEGATECALL-state_test]
    tests/prague/eip7702_set_code_tx/test_gas.py::test_call_to_pre_authorized_oog[fork_Prague-call_opcode_STATICCALL-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_sponsored_set_code[fork_Prague-state_test-invalid-tx_value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_sponsored_set_code[fork_Prague-state_test-invalid-tx_value_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_sponsored_set_code[fork_Prague-state_test-out-of-gas-tx_value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_sponsored_set_code[fork_Prague-state_test-out-of-gas-tx_value_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_sponsored_set_code[fork_Prague-state_test-revert-tx_value_0]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_self_sponsored_set_code[fork_Prague-state_test-revert-tx_value_10000000000]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-invalid-tx_value_0-self_sponsored_tx]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-invalid-tx_value_10000000000-self_sponsored_tx]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-out-of-gas-tx_value_0-self_sponsored_tx]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-out-of-gas-tx_value_10000000000-self_sponsored_tx]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-revert-tx_value_0-self_sponsored_tx]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_set_code_to_sstore[fork_Prague-state_test-revert-tx_value_10000000000-self_sponsored_tx]
    tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_to_pointer[fork_Prague-state_test-sender_is_auth_signer_False-sender_delegated_False]
    tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_to_pointer[fork_Prague-state_test-sender_is_auth_signer_False-sender_delegated_True]
    tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_pointer_to_pointer[fork_Prague-state_test-sender_is_auth_signer_True-sender_delegated_False]
    ```

---
22. (CN?) Delegated EOA used as transaction sender is not found as an existing account
    **Pattern:** `execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32001, message=Requested resource not found. address '0x...'.)` — the address reported missing is the transaction's own `sender`.
    
    **Root cause:** `test_creating_tx_to_contract_creator` sets up `auth_signer = pre.fund_eoa(delegation=creator_code_address)` — the same pre-alloc mechanism from [#20](#20-relay-caching-eip-7702-authorization-tuple-does-not-bump-authority-nonce)/[#21](#21-eip-7702-authorization-tuple-does-not-write-delegation-designation-code) that sends a real on-chain "fund_eoa" transaction carrying an `authorization_list` entry before the actual test runs. The test's own transaction is then sent **from** `auth_signer` (`sender=auth_signer`). Submission fails outright because Hedera doesn't recognize `auth_signer` as an existing account at all. This looks like a downstream consequence of the same gap documented in #20/#21: if the pre-alloc delegation-setup transaction doesn't properly register the account on Hedera's ledger (beyond just failing to bump its nonce or write its code), then using that address as a transaction `sender` later fails with "resource not found" instead of just silently missing the delegation.
    
    **Total:** 5 (Hedera-only; not yet checked against Geth)
    
    **Hedera-only — 5 tests**
    ```
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_creating_tx_to_contract_creator[fork_Prague-create_opcode_CREATE-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_creating_tx_to_contract_creator[fork_Prague-create_opcode_CREATE2-state_test]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing[fork_Prague-state_test-delegated_account-self_sponsored]
    tests/prague/eip7702_set_code_tx/test_set_code_txs.py::test_delegation_clearing_tx_to[fork_Prague-state_test-delegated_account-self_sponsored]
    tests/prague/eip7702_set_code_tx/test_set_code_txs_2.py::test_eoa_init_as_pointer[fork_Prague-state_test]
    ```

---
23. (Relay/Mirror Node) Account-state queries for a deleted (self-destructed) contract fail with `-32020` mirror node 500
    **Pattern:** `pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse` — `error.data.str: Input should be a valid string [input_value=500, input_type=int]` / `error.data.dict[any,any]: Input should be a valid dictionary`. The raised error is a client-side parsing failure; the real response is `{"error": {"code": -32020, "message": "[Request ID: ...] Mirror node upstream failure: statusCode=500, message=Internal error", "data": 500}}`.

    **Root cause:** `get_alloc` (`rpc.py`, post-state check) queries every address in `post`. For a contract that the test created and then `SELFDESTRUCT`ed, the relay answers `eth_getBalance`, `eth_getTransactionCount` and `eth_getStorageAt` with `-32020 Mirror node upstream failure: statusCode=500` (reproducible from the relay directly, see below). `eth_getCode` for the same address correctly returns `0x`, and neighboring never-used addresses return `0x0`. A deleted contract should look like an unused address (`0x0` balance/nonce); instead the mirror node errors out. The client then fails to parse the response, because the relay sends `error.data` as the integer `500` while `JSONRPCErrorObject.data` is typed `str | dict | None` (`rpc_types.py:83`), so the actual relay error is hidden behind a `ValidationError`.

    Widening the client type to also accept `int` would surface the real error, but would not make the test pass: the underlying query still fails. Skipping the `Account.NONEXISTENT` post-check for the deleted contract would hide the problem and drop the test's main assertion.

    **Reproducer:** run the test, then query the deleted contract directly (the address varies per run; take it from the failing request):
    ```bash
    uv run execute remote -rA -vv --fork=Prague \
        --rpc-endpoint=http://localhost:37546/ \
        --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
        --rpc-chain-id=298 \
        --seed-account-sweep-amount='1_000_000 ether' \
        --default-max-fee-per-blob-gas=710_000_000_000 \
        --tx-wait-timeout=15 \
        --max-tx-per-batch=1 \
        "tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recreate_self_destructed_contract_different_txs[fork_Prague-blockchain_test-call_times_1-recreate_times_1-selfdestruct_contract_initial_balance_0-selfdestruct_other_address-create_opcode_CREATE2]"
    ```
    ```bash
    curl -s -X POST http://localhost:37546/ -H 'content-type: application/json' \
      -d '{"jsonrpc":"2.0","id":1,"method":"eth_getBalance","params":["<deleted contract address>","latest"]}'
    # {"error":{"code":-32020,"message":"... Mirror node upstream failure: statusCode=500, message=Internal error","data":500}}
    ```

    **Total:** 2 confirmed (Hedera-only; not yet checked against Geth). Other tests whose post-state includes a deleted contract may hit the same failure behind a different message.

    **Hedera-only — 2 tests**
    ```
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recreate_self_destructed_contract_different_txs[fork_Prague-blockchain_test-call_times_1-recreate_times_1-selfdestruct_contract_initial_balance_0-selfdestruct_other_address-create_opcode_CREATE2]
    tests/cancun/eip6780_selfdestruct/test_selfdestruct.py::test_recreate_self_destructed_contract_different_txs[fork_Prague-blockchain_test-call_times_1-recreate_times_1-selfdestruct_contract_initial_balance_100000-selfdestruct_other_address-create_opcode_CREATE2]
    ```
