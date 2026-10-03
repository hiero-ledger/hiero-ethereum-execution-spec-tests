## ⚠️Shanghai

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
    "tests/shanghai/"
```

### Run Failures

---
##### 1. (CN?) Coinbase address is not pre-warmed (EIP-3651)
**Pattern:** `execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x...: want 0x64 (dec:100), got 0xa28 (dec:2600)` (gas-cost measurements), or `want 0x1 (dec:1), got 0x0 (dec:0)` (a call given just enough gas for a warm access runs out of gas and fails).

**Root cause:** EIP-3651 (Warm Coinbase, active since Shanghai) requires the `COINBASE` address to be added to the access list at the start of transaction execution, so the first `EXTCODESIZE`/`EXTCODECOPY`/`EXTCODEHASH`/`BALANCE`/`CALL`-family access to it costs the warm price (100 gas) instead of the cold price (2600 gas, or ~2855 for the `CALL`-family opcodes once their own overhead is included). `test_warm_coinbase_gas_usage` measures this cost directly and expects the warm price on Prague (`fork >= Shanghai`), but measures the cold price instead — Hedera isn't pre-warming the coinbase address. `test_warm_coinbase_call_out_of_gas`'s `sufficient_gas` variants independently confirm this: they provide exactly enough gas for a warm-cost call to succeed, and the call fails (runs OOG) because Hedera charges the cold price instead.

**Total:** 12 (Hedera-only; not yet checked against Geth) — all 8 `test_warm_coinbase_gas_usage` opcodes, plus the 4 `test_warm_coinbase_call_out_of_gas` `sufficient_gas` variants. The matching `insufficient_gas` variants pass (both warm and cold accounting equally run out of gas there, so the distinction doesn't surface).

**Hedera-only — 12 tests**
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

### Run Results
```
=========================================================================================== short test summary info ===========================================================================================
PASSED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-CALL-insufficient_gas]
PASSED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-CALLCODE-insufficient_gas]
PASSED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-DELEGATECALL-insufficient_gas]
PASSED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-STATICCALL-insufficient_gas]
PASSED tests/shanghai/eip3855_push0/test_push0.py::test_push0_contracts[fork_Prague-state_test-key_sstore]
PASSED tests/shanghai/eip3855_push0/test_push0.py::test_push0_contracts[fork_Prague-state_test-fill_stack]
PASSED tests/shanghai/eip3855_push0/test_push0.py::test_push0_contracts[fork_Prague-state_test-stack_overflow]
PASSED tests/shanghai/eip3855_push0/test_push0.py::test_push0_contracts[fork_Prague-state_test-storage_overwrite]
PASSED tests/shanghai/eip3855_push0/test_push0.py::test_push0_contracts[fork_Prague-state_test-before_jumpdest]
PASSED tests/shanghai/eip3855_push0/test_push0.py::test_push0_contracts[fork_Prague-state_test-gas_cost]
PASSED tests/shanghai/eip3855_push0/test_push0.py::TestPush0CallContext::test_push0_contract_during_call_contexts[fork_Prague-state_test-call]
PASSED tests/shanghai/eip3855_push0/test_push0.py::TestPush0CallContext::test_push0_contract_during_call_contexts[fork_Prague-state_test-callcode]
PASSED tests/shanghai/eip3855_push0/test_push0.py::TestPush0CallContext::test_push0_contract_during_call_contexts[fork_Prague-state_test-delegatecall]
PASSED tests/shanghai/eip3855_push0/test_push0.py::TestPush0CallContext::test_push0_contract_during_call_contexts[fork_Prague-state_test-staticcall]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::test_contract_creating_tx[fork_Prague-state_test-initcode_name_max_size_zeros]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::test_contract_creating_tx[fork_Prague-state_test-initcode_name_max_size_ones]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::test_contract_creating_tx[fork_Prague-state_test-initcode_name_over_limit_zeros]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::test_contract_creating_tx[fork_Prague-state_test-initcode_name_over_limit_ones]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_zeros-gas_test_case_too_little_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_zeros-gas_test_case_exact_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_zeros-gas_test_case_too_little_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_zeros-gas_test_case_exact_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_ones-gas_test_case_too_little_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_ones-gas_test_case_exact_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_ones-gas_test_case_too_little_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_ones-gas_test_case_exact_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_empty-gas_test_case_too_little_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_single_byte-gas_test_case_too_little_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_single_byte-gas_test_case_exact_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_single_byte-gas_test_case_exact_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_32_bytes-gas_test_case_too_little_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_32_bytes-gas_test_case_exact_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_32_bytes-gas_test_case_too_little_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_32_bytes-gas_test_case_exact_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_33_bytes-gas_test_case_too_little_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_33_bytes-gas_test_case_exact_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_33_bytes-gas_test_case_too_little_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_33_bytes-gas_test_case_exact_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_minus_word-gas_test_case_too_little_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_minus_word-gas_test_case_exact_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_minus_word-gas_test_case_too_little_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_minus_word-gas_test_case_exact_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_minus_word_plus_byte-gas_test_case_too_little_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_minus_word_plus_byte-gas_test_case_exact_intrinsic_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_minus_word_plus_byte-gas_test_case_too_little_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_max_size_minus_word_plus_byte-gas_test_case_exact_execution_gas]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_max_size_zeros]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_max_size_ones]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_over_limit_zeros]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_over_limit_ones]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_empty]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_single_byte]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_32_bytes]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_33_bytes]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_max_size_minus_word]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create-initcode_name_max_size_minus_word_plus_byte]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_max_size_zeros]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_max_size_ones]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_over_limit_zeros]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_over_limit_ones]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_empty]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_single_byte]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_32_bytes]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_33_bytes]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_max_size_minus_word]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::TestCreateInitcode::test_create_opcode_initcode[fork_Prague-state_test-create2-initcode_name_max_size_minus_word_plus_byte]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::test_create2_oversized_initcode_with_insufficient_balance[fork_Prague-state_test-initcode_oversize]
PASSED tests/shanghai/eip3860_initcode/test_initcode.py::test_create2_oversized_initcode_with_insufficient_balance[fork_Prague-state_test-initcode_within_limit]
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-CALL-sufficient_gas] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xa65a7863d2fe107fafa1df1c37370d303edf9222 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x1 (dec:1), got 0x0 (dec:0)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-CALLCODE-sufficient_gas] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x30c758926e856cd6c59ed0cd4d4244b0becb59a9 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x1 (dec:1), got 0x0 (dec:0)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-DELEGATECALL-sufficient_gas] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xddbcc6103cb690700531f38c3c19ddf5ac527dc4 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x1 (dec:1), got 0x0 (dec:0)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_call_out_of_gas[fork_Prague-state_test-STATICCALL-sufficient_gas] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x8c2e27cefdd715143ace4b4a3ea5927f80f93c9d for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x1 (dec:1), got 0x0 (dec:0)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-EXTCODESIZE] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x5df739be4c6e22b8324834af8328b225a120ea22 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x64 (dec:100), got 0xa28 (dec:2600)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-EXTCODECOPY] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x7f1fbe7629217ff71bcb313a922c5a61fa7779c6 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x64 (dec:100), got 0xa28 (dec:2600)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-EXTCODEHASH] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xb224a2d21c12304d7bc173588740d79e522c1d34 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x64 (dec:100), got 0xa28 (dec:2600)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-BALANCE] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xcfb83427da9bb7b68f66b57e198a439987d506fc for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x64 (dec:100), got 0xa28 (dec:2600)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-CALL] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x28f1ba5e5bbbcf7d68e77b5fc66441df74bea470 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x64 (dec:100), got 0xb27 (dec:2855)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-CALLCODE] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xa1f332f01ed017c07bc2af8fbf90fc5d43a1d549 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x64 (dec:100), got 0xb27 (dec:2855)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-DELEGATECALL] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0xa51d0eef9cbbf262fc67b01afe44ad30cebd3024 for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x64 (dec:100), got 0xb27 (dec:2855)
FAILED tests/shanghai/eip3651_warm_coinbase/test_warm_coinbase.py::test_warm_coinbase_gas_usage[fork_Prague-state_test-STATICCALL] - execution_testing.base_types.composite_types.Storage.KeyValueMismatchError: incorrect value in address 0x82ec3106c8ee882997e790a3cb0bc3d0f99d3ced for key 0x0000000000000000000000000000000000000000000000000000000000000000: want 0x64 (dec:100), got 0xb27 (dec:2855)
FAILED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_empty-gas_test_case_exact_intrinsic_gas] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32003, message=[Request ID: 636d2034-2021-40b9-821f-9fd1432cb5ba] Transaction rejected: INVALID_ETHEREUM_TRANSACTION - receipt for transaction 0.0.2@1791044520.997376853 contained error status INVALID_ETHEREUM_TRANSACTION) Transaction={"rlp_override":null,"ty":"0x1","chain_id":"0x12a","nonce":"0x0","gas_price":"0xf920f84c00","max_priority_fee_per_gas":null,"max_fee_per_gas":null,"gas_limit":"0x184868","to":null,"value":"0x0","data":"0x","access_list":[{"rlp_override":null,"address":"0x0000000000000000000000000000000000000001","storage_keys":[]},{"rlp_override":null,"address":"0x0000000000000000000000000000000000000002","storage_keys":[]},{"rlp_override":null,"address":"0x0000000000000000000000000000000000000003","storage_keys":[]},...
FAILED tests/shanghai/eip3860_initcode/test_initcode.py::TestContractCreationGasUsage::test_gas_usage[fork_Prague-state_test-initcode_name_empty-gas_test_case_exact_execution_gas] - execution_testing.rpc.rpc.SendTransactionExceptionError: JSONRPCError(code=-32003, message=[Request ID: 34656b07-2676-4850-87b6-ba8a4d4cc83b] Transaction rejected: INVALID_ETHEREUM_TRANSACTION - receipt for transaction 0.0.2@1791044525.146113600 contained error status INVALID_ETHEREUM_TRANSACTION) Transaction={"rlp_override":null,"ty":"0x1","chain_id":"0x12a","nonce":"0x0","gas_price":"0xf920f84c00","max_priority_fee_per_gas":null,"max_fee_per_gas":null,"gas_limit":"0x184868","to":null,"value":"0x0","data":"0x","access_list":[{"rlp_override":null,"address":"0x0000000000000000000000000000000000000001","storage_keys":[]},{"rlp_override":null,"address":"0x0000000000000000000000000000000000000002","storage_keys":[]},{"rlp_override":null,"address":"0x0000000000000000000000000000000000000003","storage_keys":[]},...
```