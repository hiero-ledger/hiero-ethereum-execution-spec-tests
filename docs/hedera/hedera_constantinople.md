## Constantinople

### Run
```bash
uv run execute remote -rA -v --fork=Prague \
    --rpc-endpoint=http://localhost:37546/ \
    --rpc-seed-key=0xde78ff4e5e77ec2bf28ef7b446d4bec66e06d39b6e6967864b2bf3d6153f3e68 \
    --rpc-chain-id=298 \
    --seed-account-sweep-amount='1_000_000 ether' \
    --default-max-fee-per-blob-gas=710_000_000_000 \
    --tx-wait-timeout=15 \
    --max-tx-per-batch=1 \
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
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_of_empty[fork_Prague-state_test-target_exists_False]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_empty_send_value[fork_Prague-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_empty_contract_creation[fork_Prague-state_test-opcode_CREATE]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_empty_contract_creation[fork_Prague-state_test-opcode_CREATE2]
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
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_after_selfdestruct[fork_Prague-state_test-pre_existing]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_changed_account[fork_Prague-state_test]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_self_in_init[fork_Prague-state_test-create_tx]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_self_in_init[fork_Prague-state_test-create_opcode_CREATE]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_self_in_init[fork_Prague-state_test-create_opcode_CREATE2]
PASSED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_argument[fork_Prague-state_test-target_type_precompile]
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
SKIPPED [1] packages/testing/src/execution_testing/cli/pytest_commands/plugins/execute/pre_alloc.py:1042: deterministic deployment proxy is not available on this network; skipping test that requires a deterministic contract deployment
SKIPPED [5] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:161: Pre-alloc modification not supported
SKIPPED [3] tests/constantinople/eip1052_extcodehash/test_extcodehash.py:340: Pre-alloc modification not supported
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_of_empty[fork_Prague-state_test-target_exists_True] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32602, message=[Request ID: dbf2c41f-bbbe-4627-95b2-816fd85577a9] Value can't be non-zero and less than 10_000_000_000 wei which is 1 tinybar) Transaction={"rlp_override":null,"ty":"0x0","chain_id":"0x12a","nonce":"0x27a6","gas_price":"0xf920f84c00","max_priority_fee_per_gas":null,"max_fee_per_gas":null,"gas_limit":"0x5208","to":"0xb0585e291383a53427be468d267051eb097ea101","value":"0x1","data":"0x","access_list":null,"max_fee_per_blob_gas":null,"blob_versioned_hashes":null,"v":"0x277","r":"0xcff21c272e81c57703c7f1c373d31e9165c93404e2211b7a90fb156738cdc160","s":"0x4ed4a86f906b026309d3653f08a1f98121df9b4589aa6b2b031606c3800ace6c","sender":"0xf70febf7420398c3892ce79fdc393c1a5487ad27","authorization_list":null,"initcodes":null,"secret_key":null}
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_account_overwrite[fork_Prague-state_test-target_exists_True] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32602, message=[Request ID: 4d1b182a-151b-4539-b1db-da413a9f72cc] Value can't be non-zero and less than 10_000_000_000 wei which is 1 tinybar) Transaction={"rlp_override":null,"ty":"0x0","chain_id":"0x12a","nonce":"0x27b0","gas_price":"0xf920f84c00","max_priority_fee_per_gas":null,"max_fee_per_gas":null,"gas_limit":"0x5208","to":"0x000ce179cdb31b67fc6ef452471200e8c050ff87","value":"0x1","data":"0x","access_list":null,"max_fee_per_blob_gas":null,"blob_versioned_hashes":null,"v":"0x278","r":"0x5fb03c1237a1dd94e5e772b186aab16b868666222ac368a47b84dc4d55af85cc","s":"0x6d9a181c2c201f550f0e2ecc2751f09d8699a08187be2b05cb89cfd397a5648","sender":"0xf70febf7420398c3892ce79fdc393c1a5487ad27","authorization_list":null,"initcodes":null,"secret_key":null}
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_via_call[fork_Prague-state_test-opcode_CALL] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_via_call[fork_Prague-state_test-opcode_CALLCODE] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_via_call[fork_Prague-state_test-opcode_DELEGATECALL] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_via_call[fork_Prague-state_test-opcode_STATICCALL] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_after_selfdestruct[fork_Prague-state_test-create] - AssertionError: Code of 0x4650da91080d675e59d3c03689e300b7fea257e7 is 0x32ff, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_after_selfdestruct[fork_Prague-state_test-create2] - AssertionError: Code of 0x5d00f6c3dba629da7d9ffa3adc177f64c5f06c59 is 0x32ff, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_max_code_size[fork_Prague-state_test-max-stop] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_max_code_size[fork_Prague-state_test-max-invalid] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_max_code_size[fork_Prague-state_test-max_minus_1-stop] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_max_code_size[fork_Prague-state_test-max_minus_1-invalid] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_in_init_code[fork_Prague-state_test-create_tx] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_in_init_code[fork_Prague-state_test-create_opcode_CREATE] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_in_init_code[fork_Prague-state_test-create_opcode_CREATE2] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_argument[fork_Prague-state_test-target_type_precompile_with_balance] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32602, message=[Request ID: b2080fae-b508-4388-806a-6a826f077d17] Value can't be non-zero and less than 10_000_000_000 wei which is 1 tinybar) Transaction={"rlp_override":null,"ty":"0x0","chain_id":"0x12a","nonce":"0x27ef","gas_price":"0xf920f84c00","max_priority_fee_per_gas":null,"max_fee_per_gas":null,"gas_limit":"0x5208","to":"0x0000000000000000000000000000000000000002","value":"0x1","data":"0x","access_list":null,"max_fee_per_blob_gas":null,"blob_versioned_hashes":null,"v":"0x277","r":"0x9eb6e526e72c644e1ff38deb84c942cb3692b0f0aed330e00da69680022d58b","s":"0xbb33d693a649178860f8f20577e8a3bc7f637c420e65092007e9966ef6c9726","sender":"0xf70febf7420398c3892ce79fdc393c1a5487ad27","authorization_list":null,"initcodes":null,"secret_key":null}
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_dynamic_argument[fork_Prague-state_test-target_type_contract] - AssertionError: incompatible code type: <class 'bytes'>
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_DELEGATECALL-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x74685fa7c6a02630f8b1f6a7d451aebc22cfe287 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x1 (dec:1), got 0x0 (dec:0)
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_CALL-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xe370fe002d32073b95ea74a75e54d780d1992e86 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x1 (dec:1), got 0x0 (dec:0)
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_call_to_selfdestruct[fork_Prague-call_opcode_CALLCODE-state_test] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xb78f20374ce62cce156ef6b7863d06b3e19ad2e8 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x1 (dec:1), got 0x0 (dec:0)
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_created_and_deleted[fork_Prague-state_test-call] - AssertionError: Code of 0xd96d923cd4e5f6388b6ee2df3ea3123c6b040bac is 0x6000ff, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_created_and_deleted_recheck_outer[fork_Prague-state_test] - AssertionError: Code of 0xd0c6c7324682f034c70576f3ccd61be160e56aaa is 0x6000ff, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-pre_existing-callcode] - execution_testing.base_types.composite_types.Account.BalanceMismatchError: unexpected balance for account 0x5f3360f42fd353bd69ea3fc2e55164351dd2cb5a: want 0x00, got 0x02540be400
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-pre_existing-delegatecall] - execution_testing.base_types.composite_types.Account.BalanceMismatchError: unexpected balance for account 0x61ac7ba762f401f093b1012422eabda850539cf4: want 0x00, got 0x02540be400
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-dynamic-callcode] - AssertionError: Code of 0x4e9f07ee427545c5c688e782683e16f06c5264dd is 0x60206000600060006000736c3f2e21e90d38553c2127c958e9a3dceb2fc0b55af2, expected 0x.
FAILED tests/constantinople/eip1052_extcodehash/test_extcodehash.py::test_extcodehash_subcall_selfdestruct[fork_Prague-state_test-dynamic-delegatecall] - AssertionError: Code of 0xda3fb93373ef4d497cbd5b49f2af2439c914048c is 0x6020600060006000732739a4be692ac20c485695345cbd0fcb4485a0e55af4, expected 0x.
====================================================================== 26 failed, 78 passed, 10 skipped, 1 warning in 800.25s (0:13:20) =======================================================================
```