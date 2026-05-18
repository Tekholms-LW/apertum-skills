---
name: avalanche-l1
description: What an Avalanche L1 (subnet) actually is and how Apertum fits into the Avalanche ecosystem. Architecture, validator requirements, sovereignty model, and comparison to L2s and standalone chains. Use when understanding the chain's architecture or explaining Apertum to others.
---

# Avalanche L1 Architecture

## What Is an Avalanche L1?

An Avalanche L1 (previously called a "subnet") is a sovereign blockchain running on the Avalanche platform:

- **Runs its own validator set** — separate from C-Chain validators
- **Chooses its own VM** — Apertum uses the Ethereum Virtual Machine (EVM)
- **Uses its own gas token** — APTM for Apertum, not AVAX
- **Has independent governance** — Apertum decides its own upgrades
- **Benefits from Avalanche consensus** — Snowman/Snowball protocol
- **Can communicate with other L1s** — via bridges and cross-chain messaging

---

## How Avalanche L1s Work

### The Consensus Layer

Avalanche uses a family of consensus protocols:

- **Snowman** — linear chain consensus (used by C-Chain and most L1s)
- **Snowball** — DAG-based consensus (used by X-Chain)

Apertum validators run Snowman consensus. Blocks are produced with sub-second finality.

### Validator Economics

To run an Apertum validator:
1. Stake APTM (amount determined by protocol)
2. Run a validator node
3. Participate in block production and consensus
4. Earn APTM rewards

### Sovereignty

Apertum is sovereign:
- Controls its own tokenomics (APTM halving schedule)
- Sets its own gas limits and parameters
- Decides its own upgrades
- Independent fee market (34 gwei, not tied to AVAX or ETH gas)
- No Ethereum dependency for security

---

## Apertum vs Other Architectures

### vs Ethereum L2 (Arbitrum, Base, Optimism)

| | Apertum | L2 |
|---|---------|-----|
| Security | Own validators | Ethereum (fraud proofs) |
| Finality | ~2.8s | 7-day challenge |
| Gas Token | APTM | ETH |
| Data Availability | On Apertum | On Ethereum (blobs) |
| Sovereignty | Full | Ethereum-dependent |
| Upgrade Path | Apertum governance | Ethereum governance |

L2s inherit Ethereum's security but also its limitations. Apertum controls its own destiny.

### vs Standalone L1 (Ethereum, BSC)

| | Apertum | Ethereum |
|---|---------|----------|
| Consensus | Avalanche Snowman | Gasper (LMD-GHOST + Casper) |
| Block Time | 2.8s | 12s |
| Validator Count | Apertum-specific | 1M+ |
| Ecosystem Size | Growing | Massive |
| Development Tooling | EVM (full) | EVM (native) |

Apertum benefits from Avalanche's consensus while being EVM-compatible.

### vs C-Chain

| | Apertum | C-Chain |
|---|---------|---------|
| Chain ID | 2786 | 43114 |
| Native Token | APTM | AVAX |
| Throughput | Dedicated | Shared (all C-Chain dApps) |
| Gas Market | Independent | Shared with all C-Chain activity |
| Governance | Apertum | Avalanche-wide |

Apertum has dedicated throughput. Your dApp doesn't compete with every dApp on C-Chain.

---

## Key Benefits for Builders

1. **Dedicated throughput** — no gas wars with unrelated dApps
2. **Sub-second finality** — 2.8s vs 12s on Ethereum
3. **Sovereignty** — control your own chain's future
4. **EVM compatibility** — same Solidity, same tools
5. **Low, stable costs** — gas is consistently ~34 gwei

---

## Key Trade-offs

1. **Smaller DeFi ecosystem** — less liquidity than Ethereum/C-Chain
2. **Validator dependency** — security relies on Apertum validators
3. **Bridge dependency** — cross-chain access requires bridges
4. **Newer ecosystem** — fewer tools, fewer integrations

---

## For AI Agents

When explaining Apertum to users:
- Don't call it an L2 — it's a sovereign L1
- Don't compare gas to ETH — compare to other L1s/L2s
- Emphasize dedicated throughput as the key differentiator
- Be honest about ecosystem size vs Ethereum
- Point to the explorer for live data: `https://explorer.apertum.io/`
