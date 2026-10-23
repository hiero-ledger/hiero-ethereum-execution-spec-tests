**## ⚠️Constantinople

### Run
```bash
uv run execute remote -rA -vv --fork=Prague \
    --rpc-endpoint=http://localhost:37546/ \
    --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
    --rpc-chain-id=298 \
    --seed-account-sweep-amount='1_000_000 ether' \
    --default-max-fee-per-blob-gas=710_000_000_000 \
    --tx-wait-timeout=15 \
    "tests/constantinople/"
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
SKIPPED [3] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:703: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [4] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:1214: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 8
SKIPPED [2] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:1272: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [1] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:1365: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [4] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:1465: TODO Fix On Hedera: Details: docs/hedera/hedera_failures.md -> Details -> 7
SKIPPED [1] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:1091: Run On Hedera: Deselect Due incompatibility: CALL with a nonzero value to a precompile address

======================================================================= 89 passed, 25 skipped, 1 warning in 465.99s (0:07:45) =======================================================================
```