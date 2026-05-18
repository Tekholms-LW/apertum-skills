---
name: cross-chain
description: How Apertum (Chain ID 2786) interacts with other chains. Bridging assets, cross-chain messaging, and interoperability with Avalanche C-Chain and other L1s. Not an L2 landscape — Apertum is sovereign.
---

# Cross-Chain & Interoperability on Apertum

## What You Probably Got Wrong

**"Apertum is an L2 that posts data to Ethereum."** No. Apertum is a sovereign Avalanche L1 with its own validators. It does NOT post data to Ethereum.

**"I can just use any bridge."** Bridges are protocol-specific. The Apertum bridge at `https://bridge.apertum.io/` handles C-Chain ↔ Apertum transfers. Other bridges may or may not support Apertum.

**"Assets from Ethereum have the same address on Apertum."** No. Bridged tokens have different addresses. USDC on Ethereum (`0xA0b86991...`) is NOT the same as Apertum Wrapped USDC.

---

## Apertum Bridge

### Primary Bridge

- **URL:** `https://bridge.apertum.io/`
- **Routes:** Avalanche C-Chain ↔ Apertum
- **Assets:** APTM, stablecoins, wrapped tokens

### How It Works

1. Lock tokens on source chain
2. Validators attest the lock
3. Mint wrapped tokens on destination chain
4. Reverse: burn on destination, unlock on source

### Bridge Security

The bridge is secured by Apertum validators. Trust assumptions:
- Honest majority of validators
- Bridge contracts are audited
- No single point of failure in the attestation process

---

## Avalanche C-Chain ↔ Apertum

The C-Chain is the primary interoperability hub for Avalanche L1s:

```
Ethereum ←→ C-Chain ←→ Apertum
               ↓
          Other L1s (DFK, Dexalot, etc.)
```

### C-Chain Details

| Property | Value |
|----------|-------|
| Chain ID | 43114 |
| Native Token | AVAX |
| Explorer | snowtrace.io (Etherscan) |

### Bridging Flow

1. Send USDC from Ethereum to C-Chain (via C-Chain bridge or third-party)
2. Send USDC from C-Chain to Apertum (via Apertum bridge)
3. Receive Apertum Wrapped USDC

---

## Third-Party Bridges

Other cross-chain protocols may support Apertum:

| Bridge | Status | Notes |
|--------|--------|-------|
| Apertum Native Bridge | ✅ Live | `bridge.apertum.io` |
| LayerZero | ⚠️ Check | May integrate Apertum |
| Wormhole | ⚠️ Check | May integrate Apertum |
| CCIP (Chainlink) | ⚠️ Check | Requires Chainlink on Apertum |

Check the Apertum bridge page for the current list of supported bridges and assets.

---

## Cross-Chain Messaging

### For dApps

If your dApp needs to send messages cross-chain:

1. **Use the native bridge** for simple asset transfers
2. **Design defensively** — bridges are complex, assume delays and possible failures
3. **Validate everything** — check origin chain, sender, and payload integrity

### Pattern: Cross-Chain Token

```solidity
contract CrossChainToken {
    // Token total supply is locked on source chain
    // Wrapped version exists on each destination chain
    // Bridge contracts handle mint/burn
    
    function bridge(uint256 amount, uint256 destinationChainId) external {
        _burn(msg.sender, amount);
        emit BridgeInitiated(msg.sender, amount, destinationChainId);
    }
    
    function mint(address to, uint256 amount) external onlyBridge {
        _mint(to, amount);
    }
}
```

---

## Common Cross-Chain Pitfalls

1. **Wrong chain ID.** Sending to chain ID 1 (Ethereum) instead of 43114 (C-Chain) or 2786 (Apertum).

2. **Bridged token addresses differ.** USDC on Apertum has a different address than USDC on C-Chain or Ethereum.

3. **Bridge delays.** Attestation takes time. Don't design protocols that require instant cross-chain settlement.

4. **Replay attacks.** Cross-chain messages can be replayed if not properly guarded. Use unique nonces and chain IDs.

5. **Bridge risk.** Bridge hacks are the largest source of crypto losses. Understand the trust model of any bridge you use.

---

## For AI Agents

When building cross-chain functionality on Apertum:
- Use `bridge/SKILL.md` for technical bridge details
- Verify all token addresses on BOTH chains
- Test with small amounts first
- Account for bridge latency in UX
- Never hardcode bridge addresses — check `addresses/SKILL.md`
