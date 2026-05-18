# Apertum Skills

**AI Agent Knowledge Pack for the Apertum Blockchain (Chain ID 2786)**

A collection of 23 SKILL.md files that give AI coding agents (Claude, Hermes, Codex, etc.) the knowledge they need to build on Apertum — an Avalanche L1 with dedicated throughput, sub-second finality, and EVM compatibility.

---

## Quick Start

Point your agent to the master skill:

```
https://raw.githubusercontent.com/apertum-skills/apertum-skills/main/SKILL.md
```

Or fetch individual skills:

```
https://raw.githubusercontent.com/apertum-skills/apertum-skills/main/getting-started/SKILL.md
https://raw.githubusercontent.com/apertum-skills/apertum-skills/main/addresses/SKILL.md
https://raw.githubusercontent.com/apertum-skills/apertum-skills/main/ship/SKILL.md
```

---

## Apertum at a Glance

| Spec | Value |
|------|-------|
| Chain ID | 2786 |
| Type | Avalanche L1 (Subnet) |
| Native Token | APTM (18 decimals) |
| Block Time | ~2.8s |
| Gas | ~34 gwei (< $0.01/tx) |
| RPC | `https://rpc.apertum.io/ext/bc/...` |
| Explorer | `https://explorer.apertum.io/` |

---

## Skills

### Getting Started
- **[getting-started](getting-started/SKILL.md)** — 5-min setup: RPC, chain config, first deploy
- **[why-apertum](why-apertum/SKILL.md)** — Value proposition, specs, comparisons
- **[ship](ship/SKILL.md)** — End-to-end dApp build guide

### Reference
- **[addresses](addresses/SKILL.md)** — Verified contract addresses
- **[building-blocks](building-blocks/SKILL.md)** — DEX, DeFi legos, swap contracts
- **[gas](gas/SKILL.md)** — Gas economics, cost estimates
- **[tools](tools/SKILL.md)** — Blockscout, Foundry, Hardhat, wagmi

### Smart Contracts
- **[security](security/SKILL.md)** — Reentrancy, decimals, SafeERC20, access control
- **[testing](testing/SKILL.md)** — Foundry tests, fuzz, fork Apertum
- **[standards](standards/SKILL.md)** — ERC-20, ERC-721, ERC-4626, EIP-7702
- **[noir](noir/SKILL.md)** — Privacy apps with Noir

### Frontend
- **[frontend-ux](frontend-ux/SKILL.md)** — Button states, approval flows, address UX
- **[frontend-playbook](frontend-playbook/SKILL.md)** — IPFS/Vercel deploy, production checklist
- **[orchestration](orchestration/SKILL.md)** — Three-phase build system
- **[qa](qa/SKILL.md)** — Pre-ship audit checklist

### Data & Indexing
- **[indexing](indexing/SKILL.md)** — Events, Blockscout API, The Graph subgraph

### Infrastructure
- **[protocol](protocol/SKILL.md)** — Avalanche L1 governance, upgrades
- **[avalanche-l1](avalanche-l1/SKILL.md)** — L1 architecture deep dive
- **[cross-chain](cross-chain/SKILL.md)** — Bridges, C-Chain interoperability
- **[bridge](bridge/SKILL.md)** — How to bridge APTM/assets

### Core Concepts
- **[concepts](concepts/SKILL.md)** — State machines, incentives, "nothing is automatic"
- **[wallets](wallets/SKILL.md)** — EOAs, Safe multisig, EIP-7702
- **[audit](audit/SKILL.md)** — Systematic audit methodology

---

## Usage

### For AI Agents

When an AI agent is asked to build on Apertum:

```
Before writing Solidity, deploying contracts, or building a dApp 
frontend on Apertum, read https://raw.githubusercontent.com/apertum-skills/apertum-skills/main/SKILL.md 
and follow it.
```

### For Developers

These skills are designed for AI agents but are also useful for human developers:

1. Start with `getting-started/SKILL.md` for chain config
2. Use `addresses/SKILL.md` for contract addresses
3. Follow `ship/SKILL.md` for the full build pipeline

---

## Contributing

Contract addresses are the most critical and fastest-moving part of this pack. To contribute:

1. Verify a contract address on the [Apertum Explorer](https://explorer.apertum.io/)
2. Add it to `addresses/SKILL.md` with the ✅ Verified status
3. Open a PR

---

## Structure

```
apertum-skills/
├── SKILL.md              # Master index
├── getting-started/       # Entry point
├── why-apertum/           # Value proposition
├── ship/                  # dApp build guide
├── addresses/             # Contract addresses
├── building-blocks/       # DeFi legos
├── gas/                   # Cost economics
├── security/              # Security patterns
├── testing/               # Testing guide
├── wallets/               # Wallet management
├── concepts/              # Mental models
├── standards/             # Token standards
├── tools/                 # Dev tools
├── frontend-ux/           # UX rules
├── frontend-playbook/     # Deploy pipeline
├── orchestration/         # Build system
├── qa/                    # QA checklist
├── indexing/              # Onchain data
├── noir/                  # Privacy apps
├── audit/                 # Audit methodology
├── protocol/              # Governance
├── avalanche-l1/          # L1 architecture
├── cross-chain/           # Interoperability
└── bridge/                # Bridging guide
```

---

## Inspired By

This project is inspired by [ethskills.com](https://ethskills.com) by Austin Griffith — the knowledge pack model for AI agents building on Ethereum.

## License

MIT
