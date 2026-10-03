## ✅Homestead

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
    --env-gas-limit=15000000 \
    "tests/homestead/"
```

### Run Results
```
=========================================================================================== short test summary info ===========================================================================================
PASSED tests/homestead/coverage/test_coverage.py::test_coverage[fork_Prague-state_test]
PASSED tests/homestead/identity_precompile/test_identity.py::test_identity_return_overwrite[fork_Prague-call_opcode_STATICCALL-state_test]
PASSED tests/homestead/identity_precompile/test_identity.py::test_identity_return_overwrite[fork_Prague-call_opcode_DELEGATECALL-state_test]
PASSED tests/homestead/identity_precompile/test_identity.py::test_identity_return_overwrite[fork_Prague-call_opcode_CALL-state_test]
PASSED tests/homestead/identity_precompile/test_identity.py::test_identity_return_overwrite[fork_Prague-call_opcode_CALLCODE-state_test]
PASSED tests/homestead/identity_precompile/test_identity.py::test_identity_return_buffer_modify[fork_Prague-call_opcode_STATICCALL-state_test]
PASSED tests/homestead/identity_precompile/test_identity.py::test_identity_return_buffer_modify[fork_Prague-call_opcode_DELEGATECALL-state_test]
PASSED tests/homestead/identity_precompile/test_identity.py::test_identity_return_buffer_modify[fork_Prague-call_opcode_CALL-state_test]
PASSED tests/homestead/identity_precompile/test_identity.py::test_identity_return_buffer_modify[fork_Prague-call_opcode_CALLCODE-state_test]
=================================================================================== 9 passed, 1 warning in 67.87s (0:01:07) ===================================================================================
```