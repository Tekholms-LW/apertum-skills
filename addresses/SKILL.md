---
name: addresses
description: Verified contract addresses for protocols deployed on Apertum (Chain ID 2786). Use this instead of guessing or hallucinating addresses. Includes the native DEX, tokens, bridge contracts, and infrastructure. Always verify addresses against the explorer before sending transactions.
---

# Contract Addresses on Apertum

> **CRITICAL:** Never hallucinate a contract address. Wrong addresses mean lost funds. If an address isn't listed here, look it up on the explorer at `https://explorer.apertum.io/` or check the protocol's official documentation before using it.

**Network:** Apertum Mainnet (Chain ID 2786)
**Last Verified:** May 18, 2026
**Explorer:** https://explorer.apertum.io/

---

## Native Token

| Asset | Symbol | Decimals | Notes |
|-------|--------|----------|-------|
| Apertum | APTM | 18 | Native gas token, no contract address (use zero address `0x0000000000000000000000000000000000000000` for checks) |

---

## Bridge Tokens (Wrapped)

Tokens bridged from other chains to Apertum. These have different addresses on Apertum than on their native chains.

### Wrapped Stablecoins

| Token | Origin Chain | Apertum Address | Decimals | Status |
|-------|--------------|-----------------|----------|--------|
| Apertum Wrapped USDC | Ethereum/Avalanche C-Chain | *Verify on explorer* | 6 | ⚠️ Verify before use |

### Wrapped Tokens

| Token | Origin Chain | Apertum Address | Decimals | Status |
|-------|--------------|-----------------|----------|--------|
| Wrapped G999 | G999 Chain | *Verify on explorer* | *Verify* | ⚠️ Verify before use |

> **How to verify wrapped token addresses:** Go to `https://explorer.apertum.io/` and search for the token name or symbol. Check the token page for verified contract source code. Compare the bytecode with the canonical token implementation.

---

## Native DEX

The Apertum native DEX at `https://dex.apertum.io/`.

| Contract | Address | Status |
|----------|---------|--------|
| DEX Router | *Verify on explorer* | ⚠️ Verify before use |
| DEX Factory | *Verify on explorer* | ⚠️ Verify before use |
| DEX Pair (APTM/USDC) | *Verify on explorer* | ⚠️ Verify before use |

> **How to find DEX addresses:** 
> 1. Go to `https://dex.apertum.io/`
> 2. Inspect the swap/pool contracts being called
> 3. Verify on the explorer that the contracts are verified
> 4. Cross-reference with the DEX subgraph at `https://graph.apertum.io/subgraphs/name/dex/dex-subgraph`

---

## Bridge Contracts

| Contract | Address | Status |
|----------|---------|--------|
| Apertum Bridge (C-Chain ↔ Apertum) | *Verify on explorer* | ⚠️ Verify before use |

> The bridge UI is at `https://bridge.apertum.io/`. Inspect the contract interactions there to find verified bridge addresses.

---

## Infrastructure

| Service | URL |
|---------|-----|
| Blockscout Explorer | `https://explorer.apertum.io/` |
| Explorer API | `https://explorer.apertum.io/api/v2` |
| DEX | `https://dex.apertum.io/` |
| Bridge | `https://bridge.apertum.io/` |
| Contract Wizard | `https://wizard.apertum.io/` |
| Faucet (Testnet) | `https://faucet.apertum.io/` |
| DEX Subgraph | `https://graph.apertum.io/subgraphs/name/dex/dex-subgraph` |
| Testnet Explorer | `https://explorer-testnet.apertum.io/` |

---

## How to Verify an Address

**Step 1: Check the explorer**
```
https://explorer.apertum.io/address/0x...
```
Look for:
- ✅ **Verified** badge — source code is available and verified
- Contract tab shows readable Solidity
- Token tab (if applicable) shows token details

**Step 2: Check bytecode exists**
```bash
cast code 0xAddress --rpc-url $APERTUM_RPC
```
Returns `0x` if no contract at that address. Returns bytecode if deployed.

**Step 3: Call a known function**
```bash
# Check it's an ERC-20 token
cast call 0xAddress "symbol()(string)" --rpc-url $APERTUM_RPC
cast call 0xAddress "decimals()(uint8)" --rpc-url $APERTUM_RPC
```

**Step 4: Cross-reference**
- Check the project's official documentation
- Verify on `https://dex.apertum.io/` if it's a DEX contract
- Check the subgraph for known addresses

---

## Multisig (Safe)

Safe contracts are deterministic across EVM chains. Same addresses as everywhere:

| Contract | Address |
|----------|---------|
| Safe Singleton v1.4.1 | `0x41675C099F32341bf84BFc5382aF534df5C7461a` |
| Safe Proxy Factory | `0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67` |
| MultiSend | `0x38869bf66a61cF6bDB996A6aE40D5853Fd43B526` |

Verify deployment on Apertum explorer before use. These addresses are deterministic — if Safe is deployed on Apertum, they'll be at these addresses.

---

## Common Token Interfaces

When interacting with any token on Apertum, use these standard ABIs:

### ERC-20 (Minimal)
```solidity
function name() external view returns (string)
function symbol() external view returns (string)
function decimals() external view returns (uint8)
function totalSupply() external view returns (uint256)
function balanceOf(address) external view returns (uint256)
function transfer(address, uint256) external returns (bool)
function allowance(address, address) external view returns (uint256)
function approve(address, uint256) external returns (bool)
function transferFrom(address, address, uint256) external returns (bool)
```

### ERC-721 (Minimal)
```solidity
function balanceOf(address) external view returns (uint256)
function ownerOf(uint256) external view returns (address)
function tokenURI(uint256) external view returns (string)
function safeTransferFrom(address, address, uint256) external
```

---

## ⚠️ Address Verification Status

Many Apertum contract addresses are not yet documented in this skill. The ecosystem is growing. Before using any address not explicitly verified here:

1. **Check the explorer** first — `https://explorer.apertum.io/`
2. **Verify the bytecode** with `cast code`
3. **Test with small amounts** before large transfers
4. **Report verified addresses** so this skill can be updated

**To help complete this skill:** Deploy or interact with a contract on Apertum, verify the address, and submit an update. The more verified addresses here, the safer everyone builds.
