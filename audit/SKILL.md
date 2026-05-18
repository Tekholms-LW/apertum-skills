---
name: audit
description: Deep EVM smart contract audit system for Apertum (Chain ID 2786). Use when asked to audit a contract, find vulnerabilities, or review code for security issues. Systematic audit methodology with parallel specialist agents.
---

# Smart Contract Audit on Apertum

## Audit Methodology

1. **Recon** — Read the contract(s), understand the architecture
2. **Checklists** — Walk through domain-specific vulnerability checklists
3. **Testing** — Write exploit tests, fuzz, fork-test
4. **Findings** — Document vulnerabilities with severity, impact, PoC
5. **Issues** — File GitHub issues for Medium+

---

## Domain Checklists

| Domain | When to Check |
|--------|---------------|
| General | Always — reentrancy, access control, overflow, SafeERC20 |
| ERC-20 | Token contracts — decimals, permit, approve race |
| DeFi | AMM, DEX, lending — oracle manipulation, TWAP, slippage |
| Staking | Staking, vaults — share calculation, rounding errors |
| Proxies | Upgradeable — storage collisions, initialize vs constructor |
| Signatures | EIP-712, permits — replay protection, signature malleability |
| Bridges | Cross-chain — validation, replay, access control |
| DOS | Unbounded loops, gas griefing, block filling |
| Access Control | Ownership, roles, centralization risks |
| Assembly | Inline Yul, CREATE2, low-level calls |
| Chain-Specific | Apertum-specific considerations |

---

## Severity Definitions

| Severity | Definition |
|----------|------------|
| **Critical** | Direct loss of funds, no conditions, zero cost to attacker |
| **High** | Loss of funds, specific conditions, low attacker cost |
| **Medium** | Loss of funds, complex conditions, or indirect damage |
| **Low** | No direct loss, best practice violations, info leaks |
| **Info** | Observations, gas optimizations, style suggestions |

---

## Finding Format

```
## [SEVERITY] Vulnerability Name

**Contract:** 0x...
**Function:** `foo()` at line 42
**Category:** Reentrancy

### Description
Brief explanation of the vulnerability.

### Impact
What an attacker can do, how much they could steal.

### Proof of Concept
```solidity
// Minimal reproduction
```

### Remediation
How to fix it, with specific code.
```

---

## Apertum-Specific Audit Notes

1. **Verify contracts on Blockscout** — not Etherscan. Use `forge verify-contract --verifier blockscout --verifier-url "https://explorer.apertum.io/api"`

2. **Check DEX interaction safety** — verify DEX addresses against `addresses/SKILL.md` and the explorer

3. **Bridge contracts are high-value targets** — audit cross-chain message validation especially thoroughly

4. **Gas is cheap (~34 gwei)** — don't dismiss attacks thinking "gas is too expensive." It's not.

5. **Fork test against Apertum mainnet** — use the Apertum RPC to fork the real chain state for testing

6. **Check for correct Chain ID** — contracts that hardcode chain ID 1 (Ethereum) will fail on Apertum or have replay issues

7. **Verify token decimals** — USDC is 6, APTM is 18. Many exploits start with decimal mismatches

---

## After the Audit

- File findings as GitHub issues (Medium+)
- Fix Critical and High findings before deploy
- Re-audit after significant changes
- Verify fixes don't introduce new issues
