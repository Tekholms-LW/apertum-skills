---
name: concepts
description: Essential mental models for building on Apertum (Chain ID 2786). "Nothing is automatic" and "incentives are everything" are the core messages. Use when designing a system — the state machine + incentive framework catches design mistakes before they become dead code.
---

# Core Concepts for Apertum

## What You Probably Got Wrong

**"Smart contracts run automatically."** No. Smart contracts cannot execute themselves. There is no cron job, no scheduler, no background process. Every function needs a caller who pays gas. This single misconception is the root cause of most broken onchain designs.

**"Just add a timer."** There are no timers. If something needs to happen at a certain time, you need someone to call the function at that time — and give them a reason to do it.

**"The protocol team will handle that."** The whole point of decentralization is that no single team operates the system. If your design requires an operator, it's not decentralized — and it has a single point of failure.

---

## Nothing Is Automatic — Incentive Design

**This is the most important concept in all of blockchain. If you internalize nothing else, internalize this.**

### Smart Contracts Are State Machines

A smart contract is a state machine. It sits in one state, and it moves to another state when someone **pokes it** — calls a function, pays gas, triggers a transition. Between pokes, it does absolutely nothing.

```
State A ──[someone calls function]──→ State B ──[someone calls function]──→ State C
              ↑                                        ↑
         WHO does this?                           WHO does this?
         WHY would they?                          WHY would they?
```

There is no cron job. No scheduler. No background process. The blockchain doesn't call your contract — people call your contract. And people don't do things for free.

**For EVERY state transition in your system, you must answer:**

1. **Who pokes it?** (someone must pay gas)
2. **Why would they?** (what's their incentive?)
3. **Is the incentive sufficient?** (covers gas + profit?)

If you can't answer these questions, that state transition will never happen. Your contract will sit in State A forever.

---

### Incentives Are Everything

The people who deployed Uniswap didn't deploy the liquidity. They didn't market-make. They didn't run the exchange. They wrote a set of rules — a state machine — and aligned incentives.

- LPs deposit tokens because they earn fees
- Traders swap because they want different assets
- Arbitrageurs keep prices accurate because they profit from the spread

Nobody operates Uniswap. The incentives are the operator.

### The Incentive Checklist

| What | Who | Why | Sufficient? |
|------|-----|-----|-------------|
| Deposit liquidity | LP | Earn fees | Yes (fees > gas + opportunity cost) |
| Execute swap | Trader | Get desired asset | Yes (utility > gas) |
| Arbitrage prices | Bot | Profit from spread | Yes (when spread > gas) |
| Trigger liquidation | Keeper | Earn liquidation bonus | Yes (bonus > gas) |
| Call your function | ??? | ??? | ??? |

If the last row is empty, your function is dead code.

---

## What Goes Onchain

### The Litmus Test

Put it onchain if:
- **Trustless ownership** — who owns this?
- **Trustless exchange** — swapping, trading, lending
- **Composability** — other contracts need to call it
- **Censorship resistance** — must work if your team disappears
- **Permanent commitments** — votes, attestations, proofs

Keep it offchain if:
- User profiles, preferences, settings
- Search, filtering, sorting
- Images, videos, metadata (IPFS, reference onchain)
- Business logic that changes frequently
- Anything not involving value transfer or trust

---

## Gas Economics

On Apertum, gas is ~34 gwei, APTM is ~$0.195. Every transaction costs ~$0.00014 per 21K gas.

This is cheap enough that you CAN:
- Do daily check-ins onchain
- Run keeper bots profitably
- Deploy many contracts for composability

But it's not free enough to:
- Store every user action as a separate transaction
- Skip gas optimization entirely
- Use storage like a database

**Design for gas efficiency — not because it's expensive, but because it's good architecture.**

---

## Apertum-Specific Concepts

### Avalanche L1 Sovereignty

Apertum is its own chain with its own validators. It's not an L2 dependent on Ethereum security. This means:
- Apertum validators are the security model
- No fraud proofs or challenge periods
- Finality is instant (~2.8s)
- Upgrades happen through Apertum governance, not Ethereum governance

### Dedicated Throughput

Unlike Ethereum where your dApp competes with every NFT mint and MEV bot, Apertum has dedicated block space. Your gas price doesn't spike because someone else launched a token. Network utilization is ~1.3% — massive headroom.

### EVM Compatibility

Apertum runs the Ethereum Virtual Machine. Same bytecode, same opcodes, same Solidity. Everything you know about writing smart contracts applies. The only difference is the chain ID (2786), RPC endpoint, and deployed contract addresses.

---

## Summary

1. **Nothing is automatic** — every state transition needs a caller with incentive
2. **Incentives are the operator** — get them right, the system runs itself
3. **Solidity is for ownership, transfers, and commitments** — not a database or backend
4. **Apertum is cheap but not free** — gas is ~34 gwei, optimize but don't over-optimize
5. **Sovereignty matters** — Apertum controls its own destiny, not dependent on Ethereum
