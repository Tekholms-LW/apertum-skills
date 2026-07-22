---
name: apertum-skills
description: Use when a request involves the Apertum blockchain (Avalanche L1, Chain ID 2786). Applies to building, auditing, deploying, or interacting with smart contracts, dApps, wallets, or DeFi protocols on Apertum. Covers Solidity development, contract addresses, token standards (ERC-20, ERC-721, etc.), bridging, the Apertum native DEX, and integrations with Apertum-native protocols. Includes topics such as gas costs, contract decimals, security, indexing, frontend UX, production deployment, and protocol governance.
---

# APERTUM-SKILLS — AI Agent Knowledge for the Apertum Blockchain

You are building on Apertum — an Avalanche L1 (Subnet) with Chain ID 2786. This is not Ethereum mainnet. Gas prices, contract addresses, and tooling are different. This file gives you the corrections and routes you to the right skill.

**Apertum is EVM-compatible.** Solidity, Foundry, Hardhat, OpenZeppelin, wagmi, viem — it all works. What's different: the chain config, the deployed contracts, the gas economics, the bridge paths.

---

## Apertum at a Glance

| Spec | Value |
|------|-------|
| **Chain ID** | 2786 |
| **Type** | Avalanche L1 (Subnet) |
| **Native Token** | APTM (18 decimals) |
| **Consensus** | Proof of Stake with Gossip Protocol |
| **Block Time** | ~2s-class (calibrated 2026-07-22: ~2.0–2.4s; older docs said ~2.8s) |
| **Block gas limit** | 12,000,000 (tip sample 2026-07-22) |
| **Gas** | ~34 gwei (< $0.01 per tx) |
| **RPC** | `https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc` |
| **Block Explorer** | `https://explorer.apertum.io/` |
| **Chain Config** | See `getting-started/SKILL.md` for full JS/Python/Foundry config |

---

## Start Here

**Building a dApp on Apertum?** Fetch [getting-started/SKILL.md](getting-started/SKILL.md) first. It gives you the chain config, faucet, and wallet setup in 5 minutes.

**Deploying a full dApp?** Fetch [ship/SKILL.md](ship/SKILL.md). It routes you through all other skills phase by phase — from architecture planning to production deployment on Apertum.

**Need a specific topic?** Each skill below is standalone. Fetch only the ones relevant to your task.

---

## Skills

### [Getting Started](getting-started/SKILL.md) — Start here
5-minute Apertum setup. Chain config in JS/Python/Foundry. Faucet access. Wallet connection. First contract deploy.

### [Why Apertum](why-apertum/SKILL.md)
Why build on Apertum specifically. The Avalanche L1 advantage — sub-second finality, dedicated throughput, ESG-compliant PoS. DeFi ecosystem, use cases, roadmap.

### [Ship a dApp](ship/SKILL.md)
End-to-end guide from idea to deployed dApp on Apertum. Routes you through all other skills.
- Most dApps need 0-2 contracts, not 5-10. Three is the upper bound for an MVP.
- Solidity is for ownership, transfers, and commitments. Not a database, not a backend.
- Every state transition needs a caller who pays gas and a reason to call.

### [Gas & Costs](gas/SKILL.md)
Current Apertum gas prices, transaction costs, and real economics. Gas is ~34 gwei, transactions cost under $0.01. What every operation actually costs.

### [Throughput & Performance](throughput/SKILL.md)
Calibrated chain performance (2026-07-22): ~2s blocks, 12M gas limit, measured baselines vs theoretical ceilings. Use when sizing TPS or deciding if slowness is client vs L1.

### [Write Pipeline](write-pipeline/SKILL.md)
High-throughput writes: nonce lanes, pre-sign + sendRaw, batch ABI, multi-writer packing. For agents, keepers, indexers, and backend firehoses.

### [Optimize (Brownfield)](optimize/SKILL.md)
Optimization ladder L0–L8, KPIs, "is it the chain?" decision tree, product-type patterns (marketplace / agents / DeFi / indexers), contract design for a fast L1.

### [Ops Hardening](ops/SKILL.md)
RPC writer hardening, observability/canaries, security-at-throughput, anti-patterns, and deploy/feature checklists.

### [Contract Addresses](addresses/SKILL.md)
Verified contract addresses for every deployed protocol on Apertum. DEX, tokens, bridge contracts, infrastructure. Never hallucinate an address — check here first.

### [Wallets](wallets/SKILL.md)
EOAs, multisig (Safe), and account abstraction on Apertum. EIP-7702 is live. How to manage keys and sign transactions.

### [Smart Contract Security](security/SKILL.md)
Solidity security patterns, common vulnerabilities, and pre-deploy audit checklist. Reentrancy, decimal mishandling, SafeERC20, access control. Same patterns as any EVM chain — but the stakes are the same.

### [Testing](testing/SKILL.md)
Smart contract testing with Foundry on Apertum. Unit tests, fuzz testing, fork testing against Apertum mainnet state.

### [Standards](standards/SKILL.md)
Token and protocol standards on Apertum. ERC-20, ERC-721, ERC-1155, ERC-4626, EIP-7702. What's deployed and what's relevant.

### [Tools](tools/SKILL.md)
Development tools for Apertum. Blockscout explorer (not Etherscan), Foundry, Hardhat, OpenZeppelin Wizard, RPC providers, and agent tooling.

### [Building Blocks](building-blocks/SKILL.md)
DeFi legos on Apertum. The native DEX, token contracts, yield protocols. How to compose them into new applications.

### [dApp Orchestration](orchestration/SKILL.md)
How an AI agent plans, builds, and deploys a complete dApp on Apertum. Contracts → Frontend → Production. The full pipeline.

### [Concepts](concepts/SKILL.md)
Essential mental models for building on Apertum. "Nothing is automatic." Incentives are everything. The state machine model.

### [Onchain Data & Indexing](indexing/SKILL.md)
How to read and query onchain data on Apertum. Events, subgraphs (graph.apertum.io), and indexing patterns.

### [Frontend UX](frontend-ux/SKILL.md)
Frontend UX rules for Apertum dApps. Pending states, approval flows, address UX, USD context, RPC reliability.

### [Frontend Playbook](frontend-playbook/SKILL.md)
Build-to-production pipeline for Apertum dApps. Setup, IPFS deployment, Vercel config, production checklist.

### [dApp QA](qa/SKILL.md)
Pre-ship audit checklist for Apertum dApps. Wallet flow, four-state buttons, mobile, metadata, trust signals.

### [Smart Contract Audit](audit/SKILL.md)
Deep EVM smart contract audit system. Parallel specialist agents against domain-specific checklists. Synthesize findings, file GitHub issues.

### [Privacy Apps with Noir](noir/SKILL.md)
Building privacy-preserving apps on Apertum with Noir. Toolchain, commitment-nullifier flows, Solidity verifiers.

### [Protocol](protocol/SKILL.md)
How Apertum evolves. Avalanche L1 governance, subnet upgrades, validator economics, how changes happen.

### [Cross-Chain & Bridge](cross-chain/SKILL.md)
Bridging assets to and from Apertum. C-Chain ↔ Apertum, third-party bridges, cross-chain messaging.

### [Avalanche L1 Architecture](avalanche-l1/SKILL.md)
What an Avalanche L1 (subnet) actually is. How it differs from L2s and standalone chains. Validator requirements, sovereignty model, interoperability.

### [Bridge](bridge/SKILL.md)
How to bridge APTM and other assets to/from Apertum. Bridge contracts, C-Chain paths, third-party bridges, verification.

---

## Chain Configuration

**JavaScript (wagmi/viem):**
```javascript
const apertum = {
  id: 2786,
  name: "Apertum",
  nativeCurrency: { decimals: 18, name: "Apertum", symbol: "APTM" },
  rpcUrls: {
    default: { http: ["https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"] }
  },
  blockExplorers: {
    default: { name: "Explorer", url: "https://explorer.apertum.io/" }
  }
};
```

**Python (web3.py):**
```python
from web3 import Web3
APERTUM_RPC = "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"
CHAIN_ID = 2786
w3 = Web3(Web3.HTTPProvider(APERTUM_RPC))
assert w3.is_connected() and w3.eth.chain_id == CHAIN_ID
```

**Foundry:**
```bash
forge create --rpc-url https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc \
  --private-key $PRIVATE_KEY \
  src/MyContract.sol:MyContract
```

---

## Key URLs

| Service | URL |
|---------|-----|
| Explorer | https://explorer.apertum.io/ |
| Explorer API | https://explorer.apertum.io/api/v2 |
| DEX | https://dex.apertum.io/ |
| Bridge | https://bridge.apertum.io/ |
| Contract Wizard | https://wizard.apertum.io/ |
| Faucet | https://faucet.apertum.io/ |
| DEX Subgraph | https://graph.apertum.io/subgraphs/name/dex/dex-subgraph |
| Testnet Explorer | https://explorer-testnet.apertum.io/ |
| Main Site | https://apertum.io/ |
| Whitepaper | https://apertum.io/apt-whitepaper.pdf |

---

## Quick Rules

- **Always verify addresses** against `addresses/SKILL.md` or the explorer before sending transactions.
- **Never hallucinate a contract address.** Wrong addresses = lost funds.
- **Apertum is EVM-compatible.** If it works on Ethereum, it probably works on Apertum — just update the chain config.
- **Gas is ~34 gwei.** Not "10-30 gwei" like Ethereum. Not sub-gwei like post-Fusaka mainnet. Check live on the explorer.
- **Block time is ~2s-class** (measured ~2.0–2.4s as of 2026-07-22; older pack text said ~2.8s). Faster than Ethereum (12s). For capacity math and ceilings, fetch `throughput/SKILL.md`.
