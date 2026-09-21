## ⚠️ Frontier

### Issues

1. ✅ Local Hedera node's JSON-RPC relay doesn't handle multiple same-sender transactions submitted in one JSON-RPC batch call reliably — it races on nonce sequencing when 2+ txs from the same
   account arrive together, causing "nonce too low"/"nonce too high" depending on timing. Sending them one-at-a-time (waiting for each to land in a block before sending the next) sidesteps the race entirely,
- Fix: Used existed `--max-tx-per-batch=1` flag for tet runs
2. ✅ Head block returning `"gasLimit":"0x8f0d180"` = 150_000_000 gas
```bash
curl -s -X POST http://localhost:37546/ \          
   -H "Content-Type: application/json" \
   -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}'
{"jsonrpc":"2.0","result":{"timestamp":"0x6ab11f16","difficulty":"0x0","extraData":"0x","gasLimit":"0x8f0d180","baseFeePerGas":"0xa54f4c3c00","gasUsed":"0x0","logsBloom":"0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000","miner":"0x0000000000000000000000000000000000000000","mixHash":"0x0000000000000000000000000000000000000000000000000000000000000000","nonce":"0x0000000000000000","receiptsRoot":"0x0000000000000000000000000000000000000000000000000000000000000000","sha3Uncles":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","size":"0x251","stateRoot":"0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421","totalDifficulty":"0x0","transactions":[],"transactionsRoot":"0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421","uncles":[],"withdrawals":[],"withdrawalsRoot":"0x0000000000000000000000000000000000000000000000000000000000000000","number":"0x268d","hash":"0xc4f9131e5f230b182bde83dbd5199a263cb20252e1d1d46387064d5a81dc78f9","parentHash":"0x5885d271d77e19ffd3d00a18239a8980b58328f3f49f98d6700f642b793fc37f"},"id":1}
```
- Fix: added `--env-gas-limit` flag. Override the environment gas limit used


### Run
```bash
uv run execute remote -rA -vv --fork=Prague \
    --rpc-endpoint=http://localhost:37546/ \
    --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
    --rpc-chain-id=298 \
    --seed-account-sweep-amount='1_000_000 ether' \
    --default-max-fee-per-blob-gas=710 \
    --tx-wait-timeout=15 \
    --max-tx-per-batch=1 \
    --env-gas-limit=15000000 \
    "tests/frontier/"
```

### Run Failures

##### ✅ 1. "Value can't be non-zero and less than 10,000,000,000 wei" (53 failures)

The remote client enforces a minimum nonzero transfer amount (10 Gwei), which breaks any test using small nonzero `value` fields (a common construct in these opcode/scenario tests).

###### Affected tests

✅ **Identity precompile (2)**
- `test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1_nonzerovalue-call_type_CALL]`
- `test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1_nonzerovalue-call_type_CALLCODE]`

✅ **All opcodes (1)**
- `test_all_opcodes.py::test_all_opcodes[fork_Prague-state_test]`

✅ **Call/callcode gas calculation (8)**
- `test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_0-callee_opcode_CALL]`
- `test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_0-callee_opcode_CALLCODE]`
- `test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_0-callee_opcode_DELEGATECALL]`
- `test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_0-callee_opcode_STATICCALL]`
- `test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_1-callee_opcode_CALL]`
- `test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_1-callee_opcode_CALLCODE]`
- `test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_1-callee_opcode_DELEGATECALL]`
- `test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_1-callee_opcode_STATICCALL]`

✅ **Calldatacopy (8)**
- `test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 1 2]`
- `test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 1 1]`
- `test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 1 0]`
- `test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 0 0]`
- `test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 neg6 ff]`
- `test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 neg6 9]`
- `test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-underflow]`
- `test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-sec]`

✅ **Scenarios (34)** — `test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_<NAME>-debug]` for:
```
SSTORE_SLOAD, TSTORE_TLOAD, LOGS, SUICIDE, INVALID, ADDRESS, BALANCE, ORIGIN,
CALLER, CALLVALUE, CALLDATALOAD, CALLDATASIZE, CALLDATACOPY, CODECOPY_CODESIZE,
GASPRICE, EXTCODECOPY_EXTCODESIZE, RETURNDATASIZE, RETURNDATACOPY, EXTCODEHASH,
BLOCKHASH, COINBASE, TIMESTAMP, NUMBER, DIFFICULTY, GASLIMIT, CHAINID,
SELFBALANCE, BASEFEE, BLOBHASH, BLOBBASEFEE, TLOAD, MCOPY, PUSH0,
ALL_FRONTIER_OPCODES
```

###### Likely fix
Either adjust the client/RPC config to allow small nonzero transfers in this test environment, or the test harness needs a flag/workaround for the minimum-value restriction.

---

##### ⚠️ 2. Storage/state mismatch — `Storage.KeyValueMismatchError` (21 failures)

Actual on-chain storage differs from the expected value — points to real behavioral divergence in opcode/precompile/CREATE semantics.

###### Affected tests

**CREATE one-byte (2)**
- `test_create_one_byte.py::test_create_one_byte[fork_Prague-create_opcode_CREATE2-state_test]`
- `test_create_one_byte.py::test_create_one_byte[fork_Prague-create_opcode_CREATE-state_test]`

**CREATE + SUICIDE during init, SUICIDE_TO_ITSELF variant (3)**
- `test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE2-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_False]`
- `test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_False]`
- `test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_True]`

**Identity precompile, large params (2)**
- `test_identity.py::test_call_identity_precompile_large_params[fork_Prague-state_test-identity_5-call_type_CALL]`
- `test_identity.py::test_call_identity_precompile_large_params[fork_Prague-state_test-identity_5-call_type_CALLCODE]`

**All opcodes constant gas (8)**
- `test_all_opcodes.py::test_constant_gas[fork_Prague-BALANCE-state_test]`
- `test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODESIZE-state_test]`
- `test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODECOPY-state_test]`
- `test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODEHASH-state_test]`
- `test_all_opcodes.py::test_constant_gas[fork_Prague-CALLCODE-state_test]`
- `test_all_opcodes.py::test_constant_gas[fork_Prague-DELEGATECALL-state_test]`
- `test_all_opcodes.py::test_constant_gas[fork_Prague-STATICCALL-state_test]`
- `test_all_opcodes.py::test_constant_gas[fork_Prague-SELFDESTRUCT-state_test]`

**Genesis blockhash availability (4)**
- `test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-no_blocks]`
- `test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-one_empty_block]`
- `test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-one_block_with_tx]`
- `test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-256_empty_blocks]`

**Precompile absence (2)**
- `test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000012-precompile_exists_False-state_test]`
- `test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000000-precompile_exists_False-state_test]`

###### Likely fix
Investigate CREATE/SUICIDE interaction handling, `EXT*`/`*CALL` cost and return-value semantics, genesis blockhash lookup, and precompile-absence behavior at the addresses in question — these may reflect real client bugs rather than test framework issues.

---

##### ⚠️ 3. Nonce/Code mismatch on SUICIDE + CREATE (3 failures)

- `test_test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE2-state_test-operation_Operation.SUICIDE-transaction_create_False]create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE2-state_test-operation_Operation.SUICIDE-transaction_create_False]`
  → `AssertionError: Nonce of 0x6afa8bc124cf2bd6cb2b41b6245ccadaccffb1d6 is 0x01, expected 0.`
- `test_create_suicide_store.py::test_create_suicide_store[fork_Prague-create_opcode_CREATE2-state_test]`
  → `AssertionError: Code of 0x839aea5d1ea566d8926f68d72583bd1aefccaab3 is <non-empty>` (expected different code)
- `test_create_suicide_store.py::test_create_suicide_store[fork_Prague-create_opcode_CREATE-state_test]`
  → same issue, different address (`0x8b7f4cd2181dc1e68c45aced9af7ac6bb91932e5`)

###### Likely fix
Review nonce increment and code-persistence rules when a contract self-destructs during its own initcode execution.

---

##### ✅ 4. (Same fail with GETH) "initcode prefix too long" (3 failures)

- `test_precompile_absence.py::test_precompile_absence[fork_Prague-state_test-empty_calldata]`
- `test_precompile_absence.py::test_precompile_absence[fork_Prague-state_test-31_bytes]`
- `test_precompile_absence.py::test_precompile_absence[fork_Prague-state_test-32_bytes]`

###### Likely fix
Test setup/framework issue generating an oversized initcode prefix — review how `test_precompile_absence` constructs its deployment code; possibly a bumped precompile address range triggering different initcode-length assumptions.

---

##### ✅ 5. (Same fail with GETH) "Sender balance must be set before sending" (4 failures)

- `test_transaction.py::test_tx_gas_limit[fork_Prague-blockchain_test]`
- `test_transaction.py::test_sender_balance[fork_Prague-blockchain_test-balance_diff_-1-expected_exception_TransactionException.INSUFFICIENT_ACCOUNT_FUNDS]`
- `test_transaction.py::test_sender_balance[fork_Prague-blockchain_test-balance_diff_0-expected_exception_None]`
- `test_transaction.py::test_sender_balance[fork_Prague-blockchain_test-balance_diff_1-expected_exception_None]`

###### Likely fix
Pre-alloc/test setup ordering issue — sender balance isn't populated before the transaction-send step in the `blockchain_test` path. This aligns with the 3 tests already **skipped** for "Pre-alloc modification not supported" in `test_transaction.py`.

---

##### ✅ 6. (failing on GETH with 'only replay-protected (EIP-155) transactions allowed over RPC') Unexpected transaction rejection (1 failure)

- `test_block_intermediate_state.py::test_block_intermediate_state[fork_Prague-blockchain_test]`
  → `SendTransactionExceptionError: INVALID_ETHEREUM_TRANSACTION`

###### Likely fix
Investigate whether this is also value/nonce related (per category 1), or a genuinely invalid transaction construction in the intermediate-state test.

---

##### 7. RPC response validation error — pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse (34 failures)

The client's JSON-RPC response no longer matches the expected JSONRPCResponse schema on 2 fields, causing the harness to fail parsing before the test can even evaluate results. This is a new failure mode versus the previous run and affects a broad swath of test_scenarios.py, plus a couple of other tests that share the same RPC call path.

###### Affected tests

Create (2)
- `test_create_one_byte.py::test_create_one_byte[fork_Prague-create_opcode_CREATE2-state_test]`
- `test_create_one_byte.py::test_create_one_byte[fork_Prague-create_opcode_CREATE-state_test]`

All opcodes (1)
- `test_all_opcodes.py::test_all_opcodes[fork_Prague-state_test]`

Scenarios (31) 
- `test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_<NAME>-debug]` for:
```
SSTORE_SLOAD, TSTORE_TLOAD, LOGS, SUICIDE, INVALID, ADDRESS, ORIGIN, CALLER,
CALLVALUE, CALLDATALOAD, CALLDATASIZE, CALLDATACOPY, CODECOPY_CODESIZE,
GASPRICE, RETURNDATASIZE, RETURNDATACOPY, BLOCKHASH, COINBASE, TIMESTAMP,
NUMBER, DIFFICULTY, GASLIMIT, CHAINID, SELFBALANCE, BASEFEE, BLOBHASH,
BLOBBASEFEE, TLOAD, MCOPY, PUSH0, ALL_FRONTIER_OPCODES
```

###### Likely fix

Investigate whether the remote client changed its JSON-RPC response shape (field renamed/removed/retyped) or whether the test harness's JSONRPCResponse pydantic model is out of sync with the client version under test. Since this spans many unrelated opcodes/scenarios, it points to a harness/client protocol mismatch rather than a per-opcode bug — check a raw response payload against the pydantic schema to find the two mismatched fields.

#### Run Results
```
=========================================================================================== short test summary info ===========================================================================================
PASSED tests/frontier/create/test_create_deposit_oog.py::test_create_deposit_oog[fork_Prague-create_opcode_CREATE2-state_test-enough_gas_True]
PASSED tests/frontier/create/test_create_deposit_oog.py::test_create_deposit_oog[fork_Prague-create_opcode_CREATE2-state_test-enough_gas_False]
PASSED tests/frontier/create/test_create_deposit_oog.py::test_create_deposit_oog[fork_Prague-create_opcode_CREATE-state_test-enough_gas_True]
PASSED tests/frontier/create/test_create_deposit_oog.py::test_create_deposit_oog[fork_Prague-create_opcode_CREATE-state_test-enough_gas_False]
PASSED tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE-transaction_create_False]
PASSED tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE-transaction_create_True]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_0-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_0-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1_nonzerovalue_insufficient_balance-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1_nonzerovalue_insufficient_balance-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_2-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_2-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_3-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_3-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_4-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_4-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_4_insufficient_gas-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_4_insufficient_gas-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_4_exact_gas-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_4_exact_gas-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile_large_params[fork_Prague-state_test-identity_6-call_type_CALL]
PASSED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile_large_params[fork_Prague-state_test-identity_6-call_type_CALLCODE]
PASSED tests/frontier/identity_precompile/test_identity_returndatasize.py::test_identity_precompile_returndata[fork_Prague-state_test-output_size_greater_than_input]
PASSED tests/frontier/identity_precompile/test_identity_returndatasize.py::test_identity_precompile_returndata[fork_Prague-state_test-output_size_less_than_input]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_cover_revert[fork_Prague-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_BLOBBASEFEE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_BLOBBASEFEE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH0-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH0-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_BASEFEE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_BASEFEE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_SELFBALANCE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_SELFBALANCE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CHAINID-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CHAINID-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_RETURNDATASIZE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_RETURNDATASIZE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_ADDRESS-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_ADDRESS-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_ORIGIN-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_ORIGIN-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CALLER-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CALLER-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CALLVALUE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CALLVALUE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CALLDATASIZE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CALLDATASIZE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CODESIZE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_CODESIZE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_GASPRICE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_GASPRICE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_COINBASE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_COINBASE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_TIMESTAMP-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_TIMESTAMP-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_NUMBER-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_NUMBER-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PREVRANDAO-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PREVRANDAO-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_GASLIMIT-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_GASLIMIT-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PC-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PC-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_MSIZE-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_MSIZE-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_GAS-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_GAS-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH1-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH1-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH2-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH2-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH3-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH3-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH4-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH4-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH5-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH5-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH6-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH6-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH7-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH7-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH8-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH8-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH9-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH9-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH10-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH10-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH11-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH11-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH12-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH12-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH13-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH13-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH14-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH14-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH15-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH15-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH16-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH16-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH17-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH17-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH18-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH18-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH19-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH19-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH20-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH20-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH21-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH21-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH22-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH22-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH23-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH23-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH24-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH24-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH25-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH25-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH26-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH26-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH27-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH27-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH28-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH28-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH29-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH29-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH30-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH30-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH31-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH31-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH32-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_PUSH32-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP1-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP1-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP2-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP2-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP3-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP3-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP4-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP4-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP5-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP5-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP6-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP6-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP7-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP7-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP8-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP8-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP9-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP9-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP10-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP10-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP11-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP11-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP12-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP12-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP13-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP13-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP14-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP14-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP15-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP15-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP16-state_test-fails_True]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_stack_overflow[fork_Prague-opcode_DUP16-state_test-fails_False]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_MCOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_TLOAD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_TSTORE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_BLOBHASH-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_EXTCODEHASH-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_CREATE2-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SHL-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SHR-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SAR-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_STATICCALL-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_RETURNDATACOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_DELEGATECALL-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_STOP-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_ADD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_MUL-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SUB-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_DIV-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SDIV-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_MOD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SMOD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_ADDMOD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_MULMOD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_EXP-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SIGNEXTEND-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_LT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_GT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SLT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SGT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_EQ-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_ISZERO-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_AND-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_OR-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_XOR-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_NOT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_BYTE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SHA3-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_BALANCE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_CALLDATALOAD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_CALLDATACOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_CODECOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_EXTCODESIZE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_EXTCODECOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_POP-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_MLOAD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_MSTORE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_MSTORE8-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SLOAD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SSTORE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_JUMPI-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_JUMPDEST-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP1-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP2-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP3-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP4-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP5-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP6-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP7-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP8-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP9-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP10-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP11-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP12-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP13-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP14-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP15-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_SWAP16-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_LOG0-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_LOG1-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_LOG2-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_LOG3-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_LOG4-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_CREATE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_CALL-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_CALLCODE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_max_stack[fork_Prague-opcode_RETURN-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-STOP-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-ADD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-MUL-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SUB-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DIV-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SDIV-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-MOD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SMOD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-ADDMOD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-MULMOD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-EXP-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SIGNEXTEND-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-LT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-GT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SLT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SGT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-EQ-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-ISZERO-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-AND-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-OR-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-XOR-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-NOT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-BYTE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SHL-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SHR-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SAR-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SHA3-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-ADDRESS-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-ORIGIN-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CALLER-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CALLVALUE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CALLDATALOAD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CALLDATASIZE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CALLDATACOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CODESIZE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CODECOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-GASPRICE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-RETURNDATASIZE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-RETURNDATACOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-BLOCKHASH-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-COINBASE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-TIMESTAMP-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-NUMBER-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PREVRANDAO-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-GASLIMIT-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CHAINID-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SELFBALANCE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-BASEFEE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-BLOBHASH-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-BLOBBASEFEE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-POP-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-MLOAD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-MSTORE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-MSTORE8-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SLOAD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-JUMP-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-JUMPI-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PC-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-MSIZE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-GAS-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-JUMPDEST-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-TLOAD-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-TSTORE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-MCOPY-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH0-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH1-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH2-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH3-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH4-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH5-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH6-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH7-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH8-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH9-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH10-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH11-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH12-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH13-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH14-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH15-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH16-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH17-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH18-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH19-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH20-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH21-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH22-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH23-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH24-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH25-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH26-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH27-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH28-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH29-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH30-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH31-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-PUSH32-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP1-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP2-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP3-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP4-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP5-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP6-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP7-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP8-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP9-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP10-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP11-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP12-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP13-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP14-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP15-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DUP16-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP1-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP2-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP3-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP4-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP5-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP6-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP7-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP8-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP9-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP10-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP11-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP12-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP13-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP14-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP15-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SWAP16-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-LOG0-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-LOG1-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-LOG2-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-LOG3-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-LOG4-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CREATE-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CALL-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-RETURN-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CREATE2-state_test]
PASSED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-REVERT-state_test]
PASSED tests/frontier/opcodes/test_blockhash_state_test_recency.py::test_blockhash_zero_out_of_window[fork_Prague-state_test-just_past_256_window]
PASSED tests/frontier/opcodes/test_blockhash_state_test_recency.py::test_blockhash_zero_out_of_window[fork_Prague-state_test-just_past_8191_window]
PASSED tests/frontier/opcodes/test_blockhash_state_test_recency.py::test_blockhash_zero_out_of_window[fork_Prague-state_test-far_out_of_window]
PASSED tests/frontier/opcodes/test_blockhash_state_test_recency.py::test_blockhash_zero_out_of_window[fork_Prague-state_test-fuzzer_discovered_number]
PASSED tests/frontier/opcodes/test_call.py::test_call_large_offset_mstore[fork_Prague-state_test]
PASSED tests/frontier/opcodes/test_call.py::test_call_memory_expands_on_early_revert[fork_Prague-state_test]
PASSED tests/frontier/opcodes/test_call.py::test_call_large_args_offset_size_zero[fork_Prague-call_opcode_STATICCALL-state_test]
PASSED tests/frontier/opcodes/test_call.py::test_call_large_args_offset_size_zero[fork_Prague-call_opcode_DELEGATECALL-state_test]
PASSED tests/frontier/opcodes/test_call.py::test_call_large_args_offset_size_zero[fork_Prague-call_opcode_CALL-state_test]
PASSED tests/frontier/opcodes/test_call.py::test_call_large_args_offset_size_zero[fork_Prague-call_opcode_CALLCODE-state_test]
PASSED tests/frontier/opcodes/test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_0-callee_opcode_CALL]
PASSED tests/frontier/opcodes/test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_0-callee_opcode_CALLCODE]
PASSED tests/frontier/opcodes/test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_0-callee_opcode_DELEGATECALL]
PASSED tests/frontier/opcodes/test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_0-callee_opcode_STATICCALL]
PASSED tests/frontier/opcodes/test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_1-callee_opcode_CALL]
PASSED tests/frontier/opcodes/test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_1-callee_opcode_CALLCODE]
PASSED tests/frontier/opcodes/test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_1-callee_opcode_DELEGATECALL]
PASSED tests/frontier/opcodes/test_call_and_callcode_gas_calculation.py::test_value_transfer_gas_calculation[fork_Prague-state_test-gas_shortage_1-callee_opcode_STATICCALL]
PASSED tests/frontier/opcodes/test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 1 2]
PASSED tests/frontier/opcodes/test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 1 1]
PASSED tests/frontier/opcodes/test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 1 0]
PASSED tests/frontier/opcodes/test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 0 0]
PASSED tests/frontier/opcodes/test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 neg6 ff]
PASSED tests/frontier/opcodes/test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-cdc 0 neg6 9]
PASSED tests/frontier/opcodes/test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-underflow]
PASSED tests/frontier/opcodes/test_calldatacopy.py::test_calldatacopy[fork_Prague-state_test-sec]
PASSED tests/frontier/opcodes/test_calldataload.py::test_calldataload[fork_Prague-state_test-calldata_source_contract-two_bytes]
PASSED tests/frontier/opcodes/test_calldataload.py::test_calldataload[fork_Prague-state_test-calldata_source_contract-word_n_byte]
PASSED tests/frontier/opcodes/test_calldataload.py::test_calldataload[fork_Prague-state_test-calldata_source_contract-34_bytes]
PASSED tests/frontier/opcodes/test_calldataload.py::test_calldataload[fork_Prague-state_test-calldata_source_tx-two_bytes]
PASSED tests/frontier/opcodes/test_calldataload.py::test_calldataload[fork_Prague-state_test-calldata_source_tx-word_n_byte]
PASSED tests/frontier/opcodes/test_calldataload.py::test_calldataload[fork_Prague-state_test-calldata_source_tx-34_bytes]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_contract-args_size_0]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_contract-args_size_2]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_contract-args_size_16]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_contract-args_size_33]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_contract-args_size_257]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_tx-args_size_0]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_tx-args_size_2]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_tx-args_size_16]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_tx-args_size_33]
PASSED tests/frontier/opcodes/test_calldatasize.py::test_calldatasize[fork_Prague-state_test-calldata_source_tx-args_size_257]
PASSED tests/frontier/opcodes/test_data_copy_oog.py::test_calldatacopy_word_copy_oog[fork_Prague-state_test-sufficient_gas]
PASSED tests/frontier/opcodes/test_data_copy_oog.py::test_calldatacopy_word_copy_oog[fork_Prague-state_test-insufficient_gas_for_word_copy_cost]
PASSED tests/frontier/opcodes/test_data_copy_oog.py::test_codecopy_word_copy_oog[fork_Prague-state_test-sufficient_gas]
PASSED tests/frontier/opcodes/test_data_copy_oog.py::test_codecopy_word_copy_oog[fork_Prague-state_test-insufficient_gas_for_word_copy_cost]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP1]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP2]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP3]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP4]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP5]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP6]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP7]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP8]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP9]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP10]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP11]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP12]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP13]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP14]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP15]
PASSED tests/frontier/opcodes/test_dup.py::test_dup[fork_Prague-state_test-DUP16]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_0-a_0]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_0-a_1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_0-a2to256minus1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1-a_0]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1-a_1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1-a2to256minus1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_2-a_0]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_2-a_1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_2-a2to256minus1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1023-a_0]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1023-a_1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1023-a2to256minus1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1024-a_0]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1024-a_1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent_1024-a2to256minus1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent2to255-a_0]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent2to255-a_1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent2to255-a2to256minus1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent2to256minus1-a_0]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent2to256minus1-a_1]
PASSED tests/frontier/opcodes/test_exp.py::test_gas[fork_Prague-state_test-exponent2to256minus1-a2to256minus1]
PASSED tests/frontier/opcodes/test_extcodecopy.py::test_extcodecopy_bounds[fork_Prague-state_test]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_0-opcode_LOG0-topics_0]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_0-opcode_LOG1-topics_1]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_0-opcode_LOG2-topics_2]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_0-opcode_LOG3-topics_3]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_0-opcode_LOG4-topics_4]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1-opcode_LOG0-topics_0]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1-opcode_LOG1-topics_1]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1-opcode_LOG2-topics_2]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1-opcode_LOG3-topics_3]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1-opcode_LOG4-topics_4]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_2-opcode_LOG0-topics_0]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_2-opcode_LOG1-topics_1]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_2-opcode_LOG2-topics_2]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_2-opcode_LOG3-topics_3]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_2-opcode_LOG4-topics_4]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1023-opcode_LOG0-topics_0]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1023-opcode_LOG1-topics_1]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1023-opcode_LOG2-topics_2]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1023-opcode_LOG3-topics_3]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1023-opcode_LOG4-topics_4]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1024-opcode_LOG0-topics_0]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1024-opcode_LOG1-topics_1]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1024-opcode_LOG2-topics_2]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1024-opcode_LOG3-topics_3]
PASSED tests/frontier/opcodes/test_log.py::test_gas[fork_Prague-state_test-data_size_1024-opcode_LOG4-topics_4]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH1]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH2]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH3]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH4]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH5]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH6]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH7]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH8]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH9]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH10]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH11]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH12]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH13]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH14]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH15]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH16]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH17]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH18]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH19]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH20]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH21]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH22]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH23]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH24]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH25]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH26]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH27]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH28]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH29]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH30]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH31]
PASSED tests/frontier/opcodes/test_push.py::test_push[fork_Prague-state_test-PUSH32]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH1]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH2]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH3]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH4]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH5]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH6]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH7]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH8]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH9]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH10]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH11]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH12]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH13]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH14]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH15]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH16]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH17]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH18]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH19]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH20]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH21]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH22]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH23]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH24]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH25]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH26]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH27]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH28]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH29]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH30]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH31]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1024-PUSH32]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH1]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH2]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH3]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH4]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH5]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH6]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH7]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH8]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH9]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH10]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH11]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH12]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH13]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH14]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH15]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH16]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH17]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH18]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH19]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH20]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH21]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH22]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH23]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH24]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH25]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH26]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH27]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH28]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH29]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH30]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH31]
PASSED tests/frontier/opcodes/test_push.py::test_stack_overflow[fork_Prague-state_test-stack_height_1025-PUSH32]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP1]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP2]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP3]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP4]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP5]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP6]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP7]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP8]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP9]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP10]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP11]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP12]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP13]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP14]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP15]
PASSED tests/frontier/opcodes/test_swap.py::test_swap[fork_Prague-state_test-SWAP16]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP1]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP2]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP3]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP4]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP5]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP6]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP7]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP8]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP9]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP10]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP11]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP12]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP13]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP14]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP15]
PASSED tests/frontier/opcodes/test_swap.py::test_stack_underflow[fork_Prague-state_test-SWAP16]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-valid_signature_1]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-valid_signature_2]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-z_eq_N]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-invalid_signature_1]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-invalid_signature_2]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-invalid_signature_3]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-r_eq_N]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-s_eq_N]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-r_zero_and_s_eq_N]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-r_eq_N_and_s_zero]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-r_eq_N_and_s_eq_N]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-u1_eq_u2_R_eq_G]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-u1_eq_neg_u2_R_eq_neg_G]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-13u1_eq_u2_R_eq_neg_13G]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-13u1_eq_u2_R_eq_13G]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-R_eq_2G_low_s]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-R_eq_2G_high_s]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-R_eq_3G_low_s]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-R_eq_3G_high_s]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-R_eq_4G_low_s]
PASSED tests/frontier/precompiles/test_ecrecover.py::test_precompiles[fork_Prague-state_test-R_eq_4G_high_s]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x000000000000000000000000000000000000000b-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x000000000000000000000000000000000000000c-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x000000000000000000000000000000000000000d-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x000000000000000000000000000000000000000e-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x000000000000000000000000000000000000000f-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000010-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000011-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x000000000000000000000000000000000000000a-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000009-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000005-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000006-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000007-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000008-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000001-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000002-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000003-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000004-precompile_exists_True-state_test]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_abc]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_message_digest]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_alphabet]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_long]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_alnum]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_numeric]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_quick_brown_fox]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_0]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_1]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_54]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-length fits into the first block]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_56]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_57]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_63]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-full block]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_65]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_119]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_120]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_121]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_127]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-two blocks]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_129]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_True-ripemd_a_10000]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_abc]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_message_digest]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_alphabet]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_long]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_alnum]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_numeric]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_quick_brown_fox]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_0]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_1]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_54]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-length fits into the first block]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_56]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_57]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_63]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-full block]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_65]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_119]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_120]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_121]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_127]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-two blocks]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_129]
PASSED tests/frontier/precompiles/test_ripemd.py::test_precompiles[fork_Prague-state_test-oog_False-ripemd_a_10000]
PASSED tests/frontier/validation/test_header.py::test_block_gas_limit_below_minimum[fork_Prague-zero-blockchain_test]
PASSED tests/frontier/validation/test_header.py::test_block_gas_limit_below_minimum[fork_Prague-one-blockchain_test]
PASSED tests/frontier/validation/test_header.py::test_block_gas_limit_below_minimum[fork_Prague-minimum_minus_one-blockchain_test]
PASSED tests/frontier/validation/test_header.py::test_block_gas_limit_below_minimum[fork_Prague-minimum-blockchain_test]
PASSED tests/frontier/validation/test_transaction.py::test_sender_balance_insufficient_state_test[fork_Prague-state_test]
SKIPPED [1] tests/frontier/examples/test_block_intermediate_state.py:12: Run On Hedera: Same failure on Hedera and GETH
SKIPPED [3] tests/frontier/precompiles/test_precompile_absence.py:20: Run On Hedera: Same failure on Hedera and GETH
SKIPPED [1] tests/frontier/validation/test_transaction.py:23: Run On Hedera: Same failure on Hedera and GETH
SKIPPED [3] tests/frontier/validation/test_transaction.py:59: Pre-alloc modification not supported
SKIPPED [3] tests/frontier/validation/test_transaction.py:106: Run On Hedera: Same failure on Hedera and GETH
FAILED tests/frontier/create/test_create_one_byte.py::test_create_one_byte[fork_Prague-create_opcode_CREATE2-state_test] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/create/test_create_one_byte.py::test_create_one_byte[fork_Prague-create_opcode_CREATE-state_test] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE2-state_test-operation_Operation.SUICIDE-transaction_create_False] - AssertionError: Nonce of 0xe79c6a318d729f2c5916bf7f4cc3432969ca4e6e is 0x01, expected 0.
FAILED tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE2-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_False] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xa89982a7c750fba1adedce34b260c18b8ac28b5b for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_False] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x4b8eac3973633afd4211735d8494f1a4ba745f0b for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/create/test_create_suicide_during_init.py::test_create_suicide_during_transaction_create[fork_Prague-create_opcode_CREATE-state_test-operation_Operation.SUICIDE_TO_ITSELF-transaction_create_True] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x82b622552cb03d78a0702e214e14cbae2bd12c8d for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/create/test_create_suicide_store.py::test_create_suicide_store[fork_Prague-create_opcode_CREATE2-state_test] - AssertionError: Code of 0x2f3393fd95bc0a51cca3ccb33e8b4604f75ac65b is 0x600160003514604b58015760026000351460285801576003600035146008580157604c5801565b60015c6001540160005260206000f360375801565b6012600154...
FAILED tests/frontier/create/test_create_suicide_store.py::test_create_suicide_store[fork_Prague-create_opcode_CREATE-state_test] - AssertionError: Code of 0x8515f02356c9ead7ae50e092ad637670930bab2f is 0x600160003514604b58015760026000351460285801576003600035146008580157604c5801565b60015c6001540160005260206000f360375801565b6012600154...
FAILED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1_nonzerovalue-call_type_CALL] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x69b8a28f987a29d38756f88e51c14f68335d5e91 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile[fork_Prague-state_test-identity_1_nonzerovalue-call_type_CALLCODE] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x5b6db121f7ef461851f0834976e7016f6eed5143 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile_large_params[fork_Prague-state_test-identity_5-call_type_CALL] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x99c0d873bc946910acb5b07b6dafd79cf924676b for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/identity_precompile/test_identity.py::test_call_identity_precompile_large_params[fork_Prague-state_test-identity_5-call_type_CALLCODE] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x4a1d9221b2819b48dca18ac6bb24d9091461732c for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_all_opcodes[fork_Prague-state_test] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-BALANCE-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x715a76611504aaffc24a2146028acd4056879743 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODESIZE-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xdc62f773e076d5a4ab3f3d96e94a865bbad4cb4b for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODECOPY-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xb6296ce69d61eb0129f28baa8c8374ccc16bacba for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-EXTCODEHASH-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xbaaee55d0c736e8a70a3d3a96e43d7f8959c85b7 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-CALLCODE-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xb67ca7aab159731675a2dcb8c36ada8179773f48 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-DELEGATECALL-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x725b6ce973e11a08271e3bde34f858a304f1d99c for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-STATICCALL-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x859589fafdc5f29879132f92ceb00ad099d34bd9 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_all_opcodes.py::test_constant_gas[fork_Prague-SELFDESTRUCT-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x8dab480377b3e635f04faa6cb8dcc1f1f849b989 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-no_blocks] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xc4ae2ca635dd66b5498794731e26196668dc1e6d for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-one_empty_block] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x09b0c3aac8c384460996bfc571e6f3846ec05a51 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-one_block_with_tx] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xd0c41a636814ab576c6a9edc7b8f59d3fedc8986 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/opcodes/test_blockhash.py::test_genesis_hash_available[fork_Prague-blockchain_test-256_empty_blocks] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x2e6a0269ec8eae24f034bba5115fe84b93f6c18c for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000012-precompile_exists_False-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xe543ce70cb251fef0405df7bb4ca1fe52c956350 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/precompiles/test_precompiles.py::test_precompiles[fork_Prague-address_0x0000000000000000000000000000000000000000-precompile_exists_False-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x215ae6c084b7b92391968529aa0d63837c0cee9c for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_SSTORE_SLOAD-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_TSTORE_TLOAD-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_LOGS-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_SUICIDE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_INVALID-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_ADDRESS-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_BALANCE-debug] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32602, message=[Request ID: fe28c230-ab83-4ad8-9d05-bd18b27bb12a] Value can't be non-zero and less than 10_000_000_000 wei whi...
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_ORIGIN-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_CALLER-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_CALLVALUE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_CALLDATALOAD-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_CALLDATASIZE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_CALLDATACOPY-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_CODECOPY_CODESIZE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_GASPRICE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_EXTCODECOPY_EXTCODESIZE-debug] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32602, message=[Request ID: 2c970056-03c1-4c11-83c6-af2f68a436df] Value can't be non-zero and less than 10_000_000_000 wei whi...
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_RETURNDATASIZE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_RETURNDATACOPY-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_EXTCODEHASH-debug] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32602, message=[Request ID: 6127b686-8312-40cc-a968-26e1d51df1d1] Value can't be non-zero and less than 10_000_000_000 wei whi...
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_BLOCKHASH-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_COINBASE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_TIMESTAMP-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_NUMBER-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_DIFFICULTY-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_GASLIMIT-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_CHAINID-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_SELFBALANCE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_BASEFEE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_BLOBHASH-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_BLOBBASEFEE-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_TLOAD-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_MCOPY-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_PUSH0-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
FAILED tests/frontier/scenarios/test_scenarios.py::test_scenarios[fork_Prague-blockchain_test-test_program_program_ALL_FRONTIER_OPCODES-debug] - pydantic_core._pydantic_core.ValidationError: 2 validation errors for JSONRPCResponse
============================================================== 61 failed, 705 passed, 11 skipped, 2 deselected, 1 warning in 15244.12s (4:14:04) ==============================================================
```