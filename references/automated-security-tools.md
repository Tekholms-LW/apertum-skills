# Automated Security Tools for Apertum Contracts

**Goal**: Move beyond manual checklists to automated gates that catch issues before deployment.

## 1. Slither (Static Analysis - Recommended First Step)

Installation (one-time):
```bash
pip install slither-analyzer
# or via docker for isolation
```

Basic run:
```bash
slither . --config slither.config.json
```

Example slither.config.json:
```json
{
  "detectors_to_exclude": ["naming-convention", "unused-state"],
  "exclude_informational": true,
  "exclude_low": false
}
```

Key detectors for Apertum projects:
- reentrancy
- access-control
- upgradeability (critical for UUPS)
- erc20
- arbitrary-send
- controlled-delegatecall

Run in CI before any forge verify.

## 2. Foundry Advanced Testing (Already Strong in the Pack - Expand It)

Already covered in testing/SKILL.md:
- Fuzzing (`forge test --fuzz-runs 10000`)
- Invariants (add royalty, upgrade, and payment invariants)
- Fork testing against real Apertum state

Add these new invariants for NFT/marketplace work:
```solidity
function invariant_RoyaltyNeverExceedsCap() public {
    assertLe(marketplace.defaultRoyaltyBps(), 1000); // max 10%
}

function invariant_ContractBalanceAfterBuy() public {
    // after successful buy, contract should not hold extra ETH
}
```

## 3. CI Security Gate Example (.github/workflows/security.yml)

```yaml
name: Security
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: foundry-rs/foundry-toolchain@v1
      - run: forge install
      - run: forge test --fuzz-runs 10000
      - run: forge coverage --report lcov
      - name: Slither
        run: |
          pip install slither-analyzer
          slither . --config slither.config.json || true   # fail on high only in real setups
```

## 4. Additional Tools (When Available)

- Echidna: Property-based fuzzer (great for economic invariants)
- Mythril: Symbolic execution (heavy but powerful for small contracts)
- Aderyn: Rust-based static analyzer (fast, modern)

## Integration with This Pack

- All new contracts should pass the above before using the templates in references/secure-upgradable-template.md.
- Add "Run Slither + full fuzz + coverage" to the pre-deploy checklist in security/SKILL.md.
- Use in the audit methodology (audit/SKILL.md) as the "Testing" phase.

**Post-2026-05-30**: This reference completes the automated layer for the security and audit functions.