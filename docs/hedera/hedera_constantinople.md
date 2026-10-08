## ⚠️Constantinople

### Run
```bash
uv run execute remote -rA -vv --fork=Prague \
    --rpc-endpoint=http://localhost:37546/ \
    --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
    --rpc-chain-id=298 \
    --seed-account-sweep-amount='1_000_000 ether' \
    --default-max-fee-per-blob-gas=710_000_000_000 \
    --tx-wait-timeout=15 \
    --max-tx-per-batch=1 \
    "tests/constantinople/"
```

### Run Failures

---
##### 1. (CN?) SELFDESTRUCT via internal CALL/CALLCODE/DELEGATECALL does not apply on Hedera
**Pattern:** `Account.CodeMismatchError: Code of 0x...: is 0x32ff (or 0x6000ff, or the caller's own CALLCODE/DELEGATECALL bytecode), expected 0x.` — or `Account.BalanceMismatchError: ... want 0x00, got 0x02540be400` (1 tinybar left over) when only the balance-drain half of SELFDESTRUCT is being checked.

**Root cause:** Same underlying gap as [hedera_prague.md #18](hedera_prague.md#18-cn-selfdestruct-via-internal-call-does-not-delete-the-account-on-hedera). In each case the target's runtime code ends in `SELFDESTRUCT`, triggered via an internal `CALL` (e.g. `code += Op.CALL(address=target, gas=100_000)` / `trigger(address=target, gas=0x10000)`) rather than a direct top-level call — including when nested an extra frame deep (`test_extcodehash_created_and_deleted_recheck_outer`'s outer contract `CALL`s an inner contract that itself `CALL`s the self-destructing target), and when reached via `CALLCODE`/`DELEGATECALL` so SELFDESTRUCT executes in the *caller's* own context (`test_extcodehash_subcall_selfdestruct`). The tests expect the account to be deleted (or, post-EIP-6780 for a pre-existing account, at least have its balance drained to 0), but neither the code deletion nor the balance transfer happens — Hedera silently no-ops SELFDESTRUCT whenever it's reached via an internal call opcode, regardless of which one or how deep.

**Total:** 8 (Hedera-only; not yet checked against Geth)

**Hedera-only — 8 tests**
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

---
##### 2. (CN?) CALL/CALLCODE/DELEGATECALL into a SELFDESTRUCT-only contract reports failure
**Pattern:** `execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x...: want 0x1 (dec:1), got 0x0 (dec:0)` — the call's own success flag, stored via `Op.SSTORE(slot, call_opcode(address=target))`.

**Root cause:** Related to [#1](#1-cn-selfdestruct-via-internal-callcallcodedelegatecall-does-not-apply-on-hedera) but a distinct symptom. `target`'s entire body is `Op.SELFDESTRUCT(beneficiary)`; calling into it with `CALL`, `CALLCODE`, or `DELEGATECALL` should trivially succeed per spec (`call_succeeds = call_opcode != Op.STATICCALL`). On Hedera the call itself reports failure (return value `0`) instead of succeeding — unlike #1's cases, where the call succeeds within the transaction and only the *end-of-transaction* account deletion/balance-drain is silently skipped. Here the failure is visible immediately via the call's own return value, for all three non-static call opcodes.

**Total:** 3 (Hedera-only; not yet checked against Geth)

**Hedera-only — 3 tests**
```
tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_CALL-state_test]
tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_CALLCODE-state_test]
tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_DELEGATECALL-state_test]
```

### Run Results
```
=========================================================================================== short test summary info ===========================================================================================
PASSED tests/constantinople/eip1014_create2/test_create2_revert.py::test_create2_succeeds_after_reverted_create2[fork_Prague-state_test]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_RETURN-create_type_CREATE-call_return_size_35]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_RETURN-create_type_CREATE-call_return_size_32]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_RETURN-create_type_CREATE-call_return_size_0]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_RETURN-create_type_CREATE2-call_return_size_35]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_RETURN-create_type_CREATE2-call_return_size_32]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_RETURN-create_type_CREATE2-call_return_size_0]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_REVERT-create_type_CREATE-call_return_size_35]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_REVERT-create_type_CREATE-call_return_size_32]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_REVERT-create_type_CREATE-call_return_size_0]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_REVERT-create_type_CREATE2-call_return_size_35]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_REVERT-create_type_CREATE2-call_return_size_32]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_RETURN-return_type_REVERT-create_type_CREATE2-call_return_size_0]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_RETURN-create_type_CREATE-call_return_size_35]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_RETURN-create_type_CREATE-call_return_size_32]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_RETURN-create_type_CREATE-call_return_size_0]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_RETURN-create_type_CREATE2-call_return_size_35]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_RETURN-create_type_CREATE2-call_return_size_32]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_RETURN-create_type_CREATE2-call_return_size_0]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_REVERT-create_type_CREATE-call_return_size_35]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_REVERT-create_type_CREATE-call_return_size_32]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_REVERT-create_type_CREATE-call_return_size_0]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_REVERT-create_type_CREATE2-call_return_size_35]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_REVERT-create_type_CREATE2-call_return_size_32]
PASSED tests/constantinople/eip1014_create2/test_create_returndata.py::test_create2_return_data[fork_Prague-state_test-return_type_in_create_REVERT-return_type_REVERT-create_type_CREATE2-call_return_size_0]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_self[fork_Prague-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_of_empty[fork_Prague-state_test-target_exists_True]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_of_empty[fork_Prague-state_test-target_exists_False]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_empty_send_value[fork_Prague-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_empty_contract_creation[fork_Prague-state_test-opcode_CREATE]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_empty_contract_creation[fork_Prague-state_test-opcode_CREATE2]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_account_overwrite[fork_Prague-state_test-target_exists_True]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_account_overwrite[fork_Prague-state_test-target_exists_False]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000b-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000c-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000d-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000e-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000f-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000010-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000011-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x000000000000000000000000000000000000000a-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000009-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000005-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000006-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000007-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000008-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000001-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000002-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000003-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_precompile[fork_Prague-precompile_0x0000000000000000000000000000000000000004-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_new_account[fork_Prague-state_test-non-empty-opcode_CREATE]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_new_account[fork_Prague-state_test-non-empty-opcode_CREATE2]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_new_account[fork_Prague-state_test-empty-opcode_CREATE]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_new_account[fork_Prague-state_test-empty-opcode_CREATE2]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_via_call[fork_Prague-state_test-opcode_CALL]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_via_call[fork_Prague-state_test-opcode_CALLCODE]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_via_call[fork_Prague-state_test-opcode_DELEGATECALL]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_via_call[fork_Prague-state_test-opcode_STATICCALL]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_after_selfdestruct[fork_Prague-state_test-pre_existing]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_changed_account[fork_Prague-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_max_code_size[fork_Prague-state_test-max-stop]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_max_code_size[fork_Prague-state_test-max-invalid]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_max_code_size[fork_Prague-state_test-max_minus_1-stop]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_max_code_size[fork_Prague-state_test-max_minus_1-invalid]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_in_init_code[fork_Prague-state_test-create_tx]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_in_init_code[fork_Prague-state_test-create_opcode_CREATE]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_in_init_code[fork_Prague-state_test-create_opcode_CREATE2]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_self_in_init[fork_Prague-state_test-create_tx]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_self_in_init[fork_Prague-state_test-create_opcode_CREATE]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_self_in_init[fork_Prague-state_test-create_opcode_CREATE2]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_argument[fork_Prague-state_test-target_type_precompile]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_argument[fork_Prague-state_test-target_type_contract]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_argument[fork_Prague-state_test-target_type_eoa]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_argument[fork_Prague-state_test-target_type_nonexistent]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_nonexistent[fork_Prague-call_opcode_STATICCALL-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_nonexistent[fork_Prague-call_opcode_DELEGATECALL-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_nonexistent[fork_Prague-call_opcode_CALL-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_nonexistent[fork_Prague-call_opcode_CALLCODE-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_STATICCALL-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_created_and_deleted[fork_Prague-state_test-staticcall]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_create2_oog[fork_Prague-state_test-success-call]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_create2_oog[fork_Prague-state_test-success-callcode]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_create2_oog[fork_Prague-state_test-success-delegatecall]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_create2_oog[fork_Prague-state_test-oog-call]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_create2_oog[fork_Prague-state_test-oog-callcode]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_create2_oog[fork_Prague-state_test-oog-delegatecall]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodecopy_zero_code[fork_Prague-state_test-target_type_nonexistent]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodecopy_zero_code[fork_Prague-state_test-target_type_existing]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_codecopy_zero_in_create2[fork_Prague-state_test]
PASSED tests/constantinople/eip145_bitwise_shift/test_shift_combinations.py::test_combinations[fork_Prague-state_test-sar]
PASSED tests/constantinople/eip145_bitwise_shift/test_shift_combinations.py::test_combinations[fork_Prague-state_test-shl]
PASSED tests/constantinople/eip145_bitwise_shift/test_shift_combinations.py::test_combinations[fork_Prague-state_test-shr]
SKIPPED [1] tests/constantinople/eip1014_create2/test_create2_revert.py:24: Pre-alloc modification not supported
SKIPPED [1] packages/testing/src/execution_testing/cli/pytest_commands/plugins/execute/pre_alloc.py:1046: deterministic deployment proxy is not available on this network; skipping test that requires a deterministic contract deployment
SKIPPED [5] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:161: Pre-alloc modification not supported
SKIPPED [3] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:340: Pre-alloc modification not supported
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_after_selfdestruct[fork_Prague-state_test-create] - AssertionError: Code of 0x162f418adf4c8a2aa44108813d2586d13fefc679 is 0x32ff, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_after_selfdestruct[fork_Prague-state_test-create2] - AssertionError: Code of 0xaa216c6cea9f17669002810072e0034848c20c3e is 0x32ff, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_argument[fork_Prague-state_test-target_type_precompile_with_balance] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x185ccf0245ed932e9487f44cd614e355f13c05f1 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_DELEGATECALL-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x10685af20d151c68aa17518c88847faf639b9ab7 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_CALL-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xd05ab2939971a0bd93055db763c93a2c60de06d7 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_CALLCODE-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x0859074bf423bc985df1a0d5e562b6c6ceb7e298 for key 0x0000000000000000000000000000000000000000000000...
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_created_and_deleted[fork_Prague-state_test-call] - AssertionError: Code of 0x100d84e72c20632957f282d1fd4ce34cb9ff5a21 is 0x6000ff, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_created_and_deleted_recheck_outer[fork_Prague-state_test] - AssertionError: Code of 0x2dcf96085a565fd8e46ee2ba7464495e543f60fb is 0x6000ff, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-pre_existing-callcode] - execution_testing.base_types.composite_types.Account.BalanceMismatchError: unexpected balance for account 0x8b4b72e11c346a06f193e34a250c50812462ce9e: want 0x00, got 0x02540be400
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-pre_existing-delegatecall] - execution_testing.base_types.composite_types.Account.BalanceMismatchError: unexpected balance for account 0xcdcfb3914a9452ec70c1d93cec9aee685b07cf51: want 0x00, got 0x02540be400
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-dynamic-callcode] - AssertionError: Code of 0xe05a9a73dae047d81d9f7d5b57daa8c5d2e0477e is 0x6020600060006000600073a8b58fa09118052b46fd944e3e5ff50e381145395af2, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-dynamic-delegatecall] - AssertionError: Code of 0x6426b10b15c7596c0a112c873ac3a2ac5405c1a2 is 0x6020600060006000737ce19ed18e6b9b8df8a13c4b4a5aee2672bfe0355af4, expected 0x.
====================================================================== 12 failed, 92 passed, 10 skipped, 1 warning in 913.74s (0:15:13) =======================================================================
```