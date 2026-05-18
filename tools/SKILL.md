---
name: tools
description: Development tools for building on Apertum (Chain ID 2786). Blockscout explorer, Foundry, Hardhat, OpenZeppelin Wizard, RPC providers. Apertum-specific tool discovery for AI agents.
---

# Development Tools for Apertum

## What You Probably Got Wrong

**"I'll use Etherscan."** Apertum uses Blockscout, not Etherscan. The explorer is at `https://explorer.apertum.io/`. No Etherscan API key needed.

**"I'll use Infura/Alchemy."** The standard Ethereum RPC providers don't support Apertum. Use the Apertum RPC endpoint directly or the Blockscout API.

---

## Core Tools

### Blockscout Explorer

The primary block explorer for Apertum.

- **URL:** `https://explorer.apertum.io/`
- **API:** `https://explorer.apertum.io/api/v2`
- **Features:** Contract verification, token tracking, address monitoring, gas tracker

**API Usage:**
```bash
# Get chain stats
curl https://explorer.apertum.io/api/v2/stats

# Get address info
curl "https://explorer.apertum.io/api/v2/addresses/0xAddress"

# Get transaction
curl "https://explorer.apertum.io/api/v2/transactions/0xTxHash"
```

### OpenZeppelin Contract Wizard

Generate ERC-20/ERC-721/ERC-1155 contracts with configurable features.

- **URL:** `https://wizard.apertum.io/`

---

## Development Frameworks

### Foundry (Recommended)

```bash
# Install
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Configure for Apertum
# foundry.toml
[rpc_endpoints]
apertum = "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"

[etherscan]
apertum = { key = "verify", url = "https://explorer.apertum.io/api" }
```

**Key commands:**
```bash
# Build
forge build

# Test
forge test -vvv

# Deploy
forge create --rpc-url apertum --private-key $KEY src/Contract.sol:Contract

# Verify
forge verify-contract --verifier blockscout \
  --verifier-url "https://explorer.apertum.io/api" \
  0xAddress src/Contract.sol:Contract

# Interact
cast call 0xAddress "balanceOf(address)(uint256)" 0xUser --rpc-url apertum
cast send 0xAddress "transfer(address,uint256)" 0xTo 100 --private-key $KEY --rpc-url apertum
```

### Hardhat

```javascript
// hardhat.config.js
module.exports = {
  solidity: "0.8.22",
  networks: {
    apertum: {
      url: "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc",
      chainId: 2786,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

---

## Frontend Libraries

### wagmi + viem

```typescript
import { createConfig, http } from "wagmi";
import { apertum } from "./chains"; // Chain ID 2786

const config = createConfig({
  chains: [apertum],
  transports: { [apertum.id]: http() }
});
```

### web3.py

```python
from web3 import Web3
w3 = Web3(Web3.HTTPProvider(
    "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"
))
assert w3.eth.chain_id == 2786
```

---

## Indexing & Data

### The Graph Subgraph

Query indexed onchain data:

- **DEX Subgraph:** `https://graph.apertum.io/subgraphs/name/dex/dex-subgraph`

### Blockscout API (Etherscan-Compatible)

The Blockscout API is largely compatible with Etherscan's API format:

```bash
# Account balance
curl "https://explorer.apertum.io/api?module=account&action=balance&address=0x..."

# Token balance
curl "https://explorer.apertum.io/api?module=account&action=tokenbalance&contractaddress=0x...&address=0x..."
```

---

## Infrastructure Services

| Service | URL |
|---------|-----|
| RPC Endpoint | `https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc` |
| Explorer | `https://explorer.apertum.io/` |
| Explorer API | `https://explorer.apertum.io/api/v2` |
| DEX | `https://dex.apertum.io/` |
| Bridge | `https://bridge.apertum.io/` |
| Contract Wizard | `https://wizard.apertum.io/` |
| Faucet | `https://faucet.apertum.io/` |
| Testnet Explorer | `https://explorer-testnet.apertum.io/` |
| Whitepaper | `https://apertum.io/apt-whitepaper.pdf` |

---

## Tool Selection Guide

| Task | Best Tool |
|------|-----------|
| Contract development | Foundry (forge + cast) |
| Rapid prototyping | OpenZeppelin Wizard → Remix → deploy |
| Contract verification | `forge verify-contract --verifier blockscout` |
| Onchain reads | Blockscout API or `cast call` |
| Onchain writes | `cast send` or web3.py |
| Frontend reads | wagmi + viem (hooks) or Blockscout API |
| Frontend writes | wagmi + viem (useWriteContract) |
| Event indexing | The Graph subgraph |
| Gas check | `cast gas-price --rpc-url apertum` or explorer |
| Token info | Explorer token page or `cast call` |
