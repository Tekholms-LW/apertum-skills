---
name: security
description: Solidity security patterns, common vulnerabilities, and pre-deploy audit checklist for Apertum (Chain ID 2786). The specific code patterns that prevent real losses. Use before deploying any contract on Apertum, when reviewing code, or when building anything that holds or moves value.
---

# Smart Contract Security on Apertum

## What You Probably Got Wrong

**"Solidity 0.8+ prevents overflows, so I'm safe."** Overflow is one of dozens of attack vectors. The big ones today: reentrancy, oracle manipulation, approval exploits, and decimal mishandling.

**"I tested it and it works."** Working correctly is not the same as being secure. Most exploits call functions in orders or with values the developer never considered.

**"It's a small contract, it doesn't need an audit."** The DAO hack was a simple reentrancy bug. The Euler exploit was a single missing check. Size doesn't correlate with safety.

**"Apertum is a smaller chain, so it's not a target."** Attackers scan all EVM chains. If there's value, there's a target. Apertum's low gas costs make it cheap for attackers too.

---

## Critical Vulnerabilities (With Defensive Code)

### 1. Token Decimals Vary

**Not all tokens use 18 decimals.** USDC has 6. This is the #1 source of "where did my money go?" bugs.

```solidity
// ❌ WRONG — assumes 18 decimals. Transfers 1 TRILLION USDC.
uint256 oneToken = 1e18;

// ✅ CORRECT — check decimals
uint256 oneToken = 10 ** IERC20Metadata(token).decimals();
```

Common decimals:
| Token | Decimals |
|-------|----------|
| APTM | 18 |
| USDC, USDT | 6 |
| WBTC | 8 |
| DAI, most tokens | 18 |

**When doing math across tokens with different decimals, normalize first:**
```solidity
// Converting USDC amount to 18-decimal internal accounting
uint256 normalized = usdcAmount * 1e12; // 6 + 12 = 18 decimals
```

### 2. No Floating Point in Solidity

Solidity has no `float` or `double`. Division truncates to zero.

```solidity
// ❌ WRONG — this equals 0
uint256 fivePercent = 5 / 100;

// ✅ CORRECT — basis points (1 bp = 0.01%)
uint256 FEE_BPS = 500; // 5% = 500 basis points
uint256 fee = (amount * FEE_BPS) / 10_000;
```

**Always multiply before dividing.** Division first = precision loss.

```solidity
// ❌ WRONG — loses precision
uint256 result = a / b * c;

// ✅ CORRECT — multiply first
uint256 result = (a * c) / b;
```

### 3. Reentrancy

An external call can call back into your contract before the first call finishes. If you update state AFTER the external call, the attacker re-enters with stale state.

```solidity
// ❌ VULNERABLE — state updated after external call
function withdraw() external {
    uint256 bal = balances[msg.sender];
    (bool success,) = msg.sender.call{value: bal}(""); // ← attacker re-enters here
    require(success);
    balances[msg.sender] = 0; // Too late — attacker already withdrew again
}

// ✅ SAFE — Checks-Effects-Interactions pattern + reentrancy guard
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

function withdraw() external nonReentrant {
    uint256 bal = balances[msg.sender];
    require(bal > 0, "Nothing to withdraw");
    
    balances[msg.sender] = 0;  // Effect BEFORE interaction
    
    (bool success,) = msg.sender.call{value: bal}("");
    require(success, "Transfer failed");
}
```

**The pattern: Checks → Effects → Interactions (CEI)**
1. **Checks** — validate inputs and conditions
2. **Effects** — update all state
3. **Interactions** — external calls last

Always use OpenZeppelin's `ReentrancyGuard` as a safety net on top of CEI.

### 4. SafeERC20

Some tokens (notably USDT) don't return `bool` on `transfer()` and `approve()`. Standard calls will revert even on success.

```solidity
// ❌ WRONG — breaks with USDT and other non-standard tokens
token.transfer(to, amount);
token.approve(spender, amount);

// ✅ CORRECT — handles all token implementations
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;

token.safeTransfer(to, amount);
token.safeApprove(spender, amount);
```

### 5. Access Control

```solidity
// ❌ WEAK — single point of failure
address public owner;

modifier onlyOwner() {
    require(msg.sender == owner, "Not owner");
    _;
}

// ✅ BETTER — Ownable with two-step transfer
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";

// ✅ BEST — role-based for complex systems
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";
```

### 6. Front-Running

On Apertum with ~2.8s block times, front-running is possible (though less severe than Ethereum's 12s public mempool).

```solidity
// ✅ Use commit-reveal for sensitive operations
function commit(bytes32 commitHash) external {
    commitments[msg.sender] = Commit(commitHash, block.number);
}

function reveal(uint256 value, bytes32 salt) external {
    Commit memory c = commitments[msg.sender];
    require(c.block + 10 < block.number, "Too early");
    require(keccak256(abi.encodePacked(value, salt)) == c.hash, "Bad reveal");
    // Use value safely now
}
```

### 7. tx.origin Usage

```solidity
// ❌ NEVER use tx.origin for auth
require(tx.origin == owner, "Not owner"); // Phishing vector!

// ✅ ALWAYS use msg.sender
require(msg.sender == owner, "Not owner");
```

---

## Pre-Deploy Checklist

Before deploying ANY contract on Apertum:

- [ ] Reentrancy guard on all value-transferring functions
- [ ] SafeERC20 for all token interactions
- [ ] Checks-Effects-Interactions pattern
- [ ] Access control (Ownable2Step or AccessControl)
- [ ] Decimals handled correctly (USDC is 6, not 18)
- [ ] No floating point — use basis points
- [ ] Multiply before divide
- [ ] No `tx.origin` for auth
- [ ] Events emitted for all state changes
- [ ] No infinite approvals (approve exact or 3-5x)
- [ ] Contract verified on explorer
- [ ] Tests pass with >90% coverage

---

## Apertum-Specific Considerations

1. **Contract verification uses Blockscout**, not Etherscan. Use `--verifier blockscout` in Foundry.
2. **Low gas costs** mean exploit transactions are cheap for attackers. Don't rely on "gas is expensive" as a security measure.
3. **Apertum is EVM-compatible** — all Ethereum security patterns apply. Same vulnerabilities, same defenses.
4. **Cross-chain bridges** add attack surface. If your contract receives bridged assets, consider the bridge's security model. Fetch `bridge/SKILL.md` and `cross-chain/SKILL.md`.

---

## When to Get a Real Audit

For contracts holding >$10K in value, get a professional audit. Fetch `audit/SKILL.md` for the systematic audit methodology using parallel specialist agents.
