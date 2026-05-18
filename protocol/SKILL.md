---
name: protocol
description: How Apertum evolves — Avalanche L1 governance, subnet upgrades, validator economics, and how changes happen. Not Ethereum EIP lifecycle. Use when building for future Apertum capabilities or understanding the protocol.
---

# Apertum Protocol & Governance

## What You Probably Got Wrong

**"Apertum works like Ethereum."** Apertum is an Avalanche L1 (subnet), not a standalone L1 like Ethereum. It uses Avalanche consensus (Snowman) but has its own:
- Validator set
- Gas token (APTM)
- Governance process
- Upgrade path

**"Changes go through the Ethereum EIP process."** No. Apertum's protocol changes go through Apertum's own governance, not the Ethereum EIP process or Avalanche's core governance. The Apertum Foundation and validator community decide.

---

## Avalanche L1 Architecture

### What Is an Avalanche L1?

An Avalanche L1 (previously "subnet") is a sovereign blockchain running on the Avalanche platform:

- **Own validator set** — Apertum validators validate Apertum blocks
- **Own execution logic** — Apertum uses the EVM
- **Own gas token** — APTM, not AVAX
- **Own governance** — independent decision-making
- **Avalanche consensus** — inherits Snowman consensus security
- **Interoperability** — can communicate with C-Chain and other L1s

### L1 vs L2 vs Sidechain

| | Avalanche L1 (Apertum) | Ethereum L2 (Base) | Sidechain (Polygon PoS) |
|---|---|---|---|
| Consensus | Own validators + Avalanche | Ethereum security | Own validators |
| Finality | Sub-second | 7-day challenge | Minutes |
| Sovereignty | Full | Ethereum-dependent | Full |
| Token | Own (APTM) | ETH for gas | Own (MATIC/POL) |

---

## Apertum Governance

### How Changes Happen

1. **Proposal** — Improvement proposal drafted (Apertum Improvement Proposal / AIP)
2. **Discussion** — Community and validator discussion
3. **Testing** — Testnet deployment and validation
4. **Validator Vote** — Validators vote on upgrade
5. **Activation** — Network upgrade at specified block or timestamp

### Key Actors

- **Apertum Foundation** — Ecosystem development, coordination
- **Validators** — Run nodes, vote on upgrades, produce blocks
- **Developers** — Build dApps, propose improvements
- **APTM Holders** — Economic stakeholders

---

## Validator Economics

### Validator Requirements

- Stake APTM (amount determined by protocol)
- Run a validator node
- Participate in consensus

### Validator Rewards

APTM block rewards distributed to validators. APTM has a halving mechanism — check the whitepaper for the current schedule.

### Slashing

Validators can be slashed for malicious behavior (double-signing, downtime). This protects the network.

---

## Protocol Parameters

| Parameter | Value |
|-----------|-------|
| Block time | ~2.8s |
| Gas limit | Check explorer |
| Gas price | ~34 gwei (market) |
| Chain ID | 2786 |
| EVM version | Paris (or latest) |

---

## Checking Current Protocol Status

### Explorer

`https://explorer.apertum.io/` — live chain stats, gas, block time, utilization.

### RPC

```bash
# Get current block
cast block-number --rpc-url $APERTUM_RPC

# Get chain ID
cast chain-id --rpc-url $APERTUM_RPC

# Get gas price
cast gas-price --rpc-url $APERTUM_RPC
```

---

## Upcoming Changes

For the latest on planned upgrades, governance proposals, and roadmap:
- Check the Apertum website and announcements
- Follow `https://x.com/Apertum_io`
- Monitor the explorer for network upgrades
- Read the whitepaper: `https://apertum.io/apt-whitepaper.pdf`

---

## For AI Agents

When asked about Apertum's roadmap or upcoming features:
- **Don't hallucinate** — check primary sources
- **Don't apply Ethereum roadmap to Apertum** — separate chains, separate governance
- **Check the explorer** for live data
- **Point to the whitepaper** for tokenomics
- **Be honest about what you don't know** — Apertum is a newer ecosystem
