# Apertum Skills

**AI Agent Knowledge Pack for the Apertum Blockchain (Chain ID 2786)**

A collection of SKILL.md files that give AI coding agents (Claude, Hermes, Codex, etc.) the knowledge they need to build on Apertum — an Avalanche L1 with dedicated throughput, sub-second finality, and EVM compatibility.

---

## Quick Start

Point your agent to the master skill:

```
https://raw.githubusercontent.com/Tekholms-LW/apertum-skills/main/SKILL.md
```

Or fetch individual skills:

```
https://raw.githubusercontent.com/Tekholms-LW/apertum-skills/main/getting-started/SKILL.md
https://raw.githubusercontent.com/Tekholms-LW/apertum-skills/main/addresses/SKILL.md
https://raw.githubusercontent.com/Tekholms-LW/apertum-skills/main/ship/SKILL.md
https://raw.githubusercontent.com/Tekholms-LW/apertum-skills/main/security/SKILL.md
https://raw.githubusercontent.com/Tekholms-LW/apertum-skills/main/standards/SKILL.md
```

---

## Apertum at a Glance

| Spec          | Value |
|---------------|-------|
| Chain ID      | 2786 |
| Type          | Avalanche L1 (Subnet) |
| Native Token  | APTM (18 decimals) |
| Block Time    | ~2.8s |
| Gas           | ~34 gwei (< $0.01/tx) |
| RPC           | `https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc` (full URL verified 2026-05-30) |
| Explorer      | `https://explorer.apertum.io/` |

---

## Recent Verification (2026-05-30)

**RPC and Explorer API audit completed:**

- Correct RPC URL confirmed against https://chainlist.org/chain/2786.
- All major Blockscout v1 (Etherscan-compatible) and v2 REST endpoints verified live and functional (stats, logs, token transfers, addresses, contracts, getabi, etc.).
- **Test vector**: Verified DEX Router contract `0x73cf8b5c2F4920967Bd8e9dECDb18F9F1e12A29f` (and its ABI at the explorer `?tab=contract_abi`).
  - Successful `eth_call` to `factory()` via JSON-RPC returns the expected factory address.
  - Full details, curl examples, and AI usage guidance (Explorer API preferred in agent sandboxes; RPC via terminal tool or host scripts) documented in `indexing/SKILL.md`.

**AI Access Note**: 
- Explorer REST API (v1/v2): Fully reliable from inside AI agent environments and scripts.
- RPC: Functional for `eth_call`, state reads, etc., from terminal, dedicated Python (e.g., web3.py), or external tools. Direct calls from some sandboxes may return 403 (provider protection) — fall back to Explorer API in those cases.

See `indexing/SKILL.md` for the complete catalog and patterns.

---

## 2026-05-30 Security & Audit Enhancements

Major improvements were added to bring the pack up to current smart contract security standards:

- **Upgradable Contracts**: Full UUPS patterns (recommended on low-gas chains like Apertum), including storage gaps, initializers, `_authorizeUpgrade`, and deployment checklists.
- **Royalties & Token Standards**: Complete EIP-2981 implementation guidance + secure extensions for ERC-721/1155 (including ERC-5192 soulbound, roles, pausable).
- **Consistent Coding Standards**: Recommended 11-step contract layout and function ordering (enforceable with `forge fmt` + solhint).
- **Industry Patterns**: Guidance for NFT marketplaces, gaming (ERC-1155/ERC-5192), RWA/compliance tokens, and agent economies.
- **Automated Security Tooling**: Slither configuration, Foundry invariants/fuzzing recommendations, and CI integration.
- **New Reference Materials** (in `references/`):
  - `secure-upgradable-template.md` — Full production UUPS + EIP-2981 marketplace skeleton
  - `nft-marketplace-security-patterns.md` — EIP-712, royalties, batch safety, and common pitfalls
  - `automated-security-tools.md` — Slither + testing automation
  - `security-audit-enhancement-proposal-2026-05-30.md` — Full findings and implementation notes

**Important**: Project-specific contract addresses and deployment details (for example, individual NFT marketplace contracts) are intentionally **not** included in this public repository. They are maintained locally only for security and operational reasons. Public infrastructure such as the Apertum DEX, Bridge, wrapped tokens, and oracles **are** fully documented in `addresses/SKILL.md`.

---

## Skills

### Getting Started
- **[getting-started](getting-started/SKILL.md)** — 5-min setup: RPC, chain config, first deploy
- **[why-apertum](why-apertum/SKILL.md)** — Value proposition, specs, comparisons
- **[ship](ship/SKILL.md)** — End-to-end dApp build guide

### Reference
- **[addresses](addresses/SKILL.md)** — Verified contract addresses (DEX, Bridge, wrapped tokens, oracles)
- **[building-blocks](building-blocks/SKILL.md)** — DEX, DeFi legos, swap contracts
- **[gas](gas/SKILL.md)** — Gas economics, cost estimates
- **[tools](tools/SKILL.md)** — Blockscout, Foundry, Hardhat, wagmi

### Smart Contracts & Security (2026 Enhanced)
- **[security](security/SKILL.md)** — Reentrancy, decimals, SafeERC20, access control, **UUPS upgradability**, industry patterns
- **[standards](standards/SKILL.md)** — ERC-20/721/1155, EIP-2981 royalties, **consistent layout & ordering**, upgradable bases
- **[audit](audit/SKILL.md)** — Systematic audit methodology + **automated tooling (Slither, Foundry)**
- **[testing](testing/SKILL.md)** — Foundry tests, fuzz, fork Apertum
- **[references/](references/)** — Templates and detailed security patterns (UUPS, NFT marketplace, automation)

### Frontend
- **[frontend-ux](frontend-ux/SKILL.md)** — Button states, approval flows, address UX
- **[frontend-playbook](frontend-playbook/SKILL.md)** — IPFS/Vercel deploy, production checklist
- **[orchestration](orchestration/SKILL.md)** — Three-phase build system
- **[qa](qa/SKILL.md)** — Pre-ship audit checklist

### Data & Indexing
- **[indexing](indexing/SKILL.md)** — Events, Blockscout API (detailed v1/v2 catalog + RPC test), The Graph subgraph

### Infrastructure
- **[protocol](protocol/SKILL.md)** — Avalanche L1 governance, upgrades
- **[avalanche-l1](avalanche-l1/SKILL.md)** — L1 architecture deep dive
- **[cross-chain](cross-chain/SKILL.md)** — Bridges, C-Chain interoperability
- **[bridge](bridge/SKILL.md)** — How to bridge APTM/assets

### Core Concepts
- **[concepts](concepts/SKILL.md)** — State machines, incentives, "nothing is automatic"
- **[wallets](wallets/SKILL.md)** — EOAs, Safe multisig, EIP-7702
- **[noir](noir/SKILL.md)** — Privacy apps with Noir

---

## Usage

### For AI Agents

When an AI agent is asked to build on Apertum:

```
Before writing Solidity, deploying contracts, or building a dApp 
frontend on Apertum, read https://raw.githubusercontent.com/Tekholms-LW/apertum-skills/main/SKILL.md 
and follow it.
```

### For Developers

These skills are designed for AI agents but are also useful for human developers:

1. Start with `getting-started/SKILL.md` for chain config
2. Use `addresses/SKILL.md` for contract addresses (public infrastructure)
3. Follow `ship/SKILL.md` for the full build pipeline
4. Use `security/SKILL.md` + `references/` for modern secure development

---

## Contributing

Contract addresses are the most critical and fastest-moving part of this pack. To contribute:

1. Verify a contract address on the [Apertum Explorer](https://explorer.apertum.io/)
2. Add it to `addresses/SKILL.md` with the ✅ Verified status (public infrastructure only)
3. Open a PR

For API/RPC patterns: Update `indexing/SKILL.md` with new verified endpoints or test cases.

**Project-specific data policy**: Individual project contract addresses (e.g. specific NFT marketplace deployments) are intentionally excluded from this public repo and maintained locally. Please do not submit PRs containing them.

---

## Structure

```
apertum-skills/
├── SKILL.md
├── getting-started/
├── why-apertum/
├── ship/
├── addresses/             # Public: DEX, Bridge, tokens, oracles
├── building-blocks/
├── gas/
├── security/              # Enhanced 2026 (UUPS, patterns)
├── standards/             # Enhanced 2026 (EIP-2981, layout)
├── audit/                 # Enhanced 2026 (tooling)
├── testing/
├── references/            # New templates & patterns (public)
├── tools/
├── frontend-ux/
├── frontend-playbook/
├── orchestration/
├── qa/
├── indexing/
├── noir/
├── protocol/
├── avalanche-l1/
├── cross-chain/
├── bridge/
├── concepts/
├── wallets/
└── ...
```

---

## License

MIT
