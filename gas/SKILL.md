---
name: gas
description: Current Apertum gas prices, transaction costs, and the real economics of building on Apertum (Chain ID 2786). Use when estimating costs, deploying contracts, or comparing Apertum to other chains.
---

# Gas & Costs on Apertum

## What You Probably Got Wrong

**Your gas estimate is wrong.** Apertum is not Ethereum. Gas is ~34 gwei, not 0.1-1 gwei like post-Fusaka Ethereum, and not 10-30 gwei like old Ethereum. It's consistently ~34 gwei.

**"APTM costs what ETH costs."** APTM is priced around $0.195 (May 2026), not $2,000. A transaction that costs the same in gas units is 10,000x cheaper in USD terms.

---

## Current Gas (May 2026)

From the Apertum Blockscout explorer (`https://explorer.apertum.io/`):

| Gas Tier | Gwei | 
|----------|------|
| Slow | 33.97 |
| Average | 34.1 |
| Fast | 34.1 |

Gas is remarkably stable at ~34 gwei. There's virtually no spread between slow and fast — a sign of low network congestion (~1.3% utilization).

**Check live:**
```bash
cast gas-price --rpc-url https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc
```
Or visit `https://explorer.apertum.io/` and check the gas tracker.

---

## What Things Actually Cost

> Costs calculated at APTM ~$0.195, gas ~34 gwei. Gas fluctuates — use `cast gas-price` for current. These are order-of-magnitude guides, not exact quotes.

| Action | Gas Used | APTM Cost | USD Cost |
|--------|----------|-----------|----------|
| APTM transfer | 21,000 | 0.000714 | **$0.00014** |
| ERC-20 transfer | ~65,000 | 0.002210 | **$0.00043** |
| ERC-20 approve | ~46,000 | 0.001564 | **$0.00031** |
| DEX swap | ~180,000 | 0.006120 | **$0.00119** |
| NFT mint (ERC-721) | ~150,000 | 0.005100 | **$0.00099** |
| Simple contract deploy | ~500,000 | 0.017000 | **$0.00332** |
| ERC-20 deploy | ~1,200,000 | 0.040800 | **$0.00796** |
| Complex DeFi contract | ~3,000,000 | 0.102000 | **$0.01989** |

**Key insight:** Apertum is extremely cheap. A swap costs ~$0.001. A transfer costs ~$0.00014. You can deploy a full ERC-20 token for under $0.01.

---

## Gas Cost Formula

```
total_cost_usd = gas_used × gas_price_gwei × 1e-9 × aptm_price_usd
```

Example — DEX swap:
```
180,000 × 34 × 1e-9 × 0.195 = $0.00119
```

**In Python:**
```python
gas_used = 180_000
gas_price_gwei = 34
aptm_price_usd = 0.195

cost_aptm = gas_used * gas_price_gwei * 1e-9
cost_usd = cost_aptm * aptm_price_usd
print(f"Cost: {cost_aptm:.6f} APTM (${cost_usd:.6f})")
```

**In Solidity (estimating):**
```solidity
// Gas cost for a user action
// tx.gasprice is in wei, not gwei
uint256 gasCost = gasUsed * tx.gasprice; // in wei (1e-18 APTM)
```

---

## Why Apertum Gas is Stable

1. **Dedicated throughput.** Apertum doesn't compete with other applications for block space. Your DeFi app doesn't get priced out by an NFT mint on another protocol.

2. **Low utilization.** ~1.3% network utilization means blocks are rarely full. Gas stays at the minimum.

3. **PoS with gossip protocol.** Validators produce blocks predictably without the bidding wars of Ethereum's gas market.

4. **No MEV spikes.** With low utilization and dedicated block space, there are no gas spikes from MEV bots competing for inclusion.

---

## Storage Costs

Smart contract storage is persistent and expensive. Apertum uses the same EVM storage pricing as Ethereum:

| Operation | Gas Cost |
|-----------|----------|
| SSTORE (new slot) | 20,000 |
| SSTORE (update) | 5,000 |
| SLOAD (read) | 2,100 (warm) / 2,600 (cold) |

**Storage cost example — new mapping entry:**
```
20,000 gas × 34 gwei × $0.195 = $0.00013
```

Cheap per write, but it adds up. Keep storage minimal.

---

## Contract Deployment Costs

Deployment gas scales with contract bytecode size:

| Contract Size | Gas | APTM Cost | USD Cost |
|---------------|-----|-----------|----------|
| Simple ERC-20 | ~1.2M | 0.041 | $0.008 |
| ERC-721 | ~1.5M | 0.051 | $0.010 |
| Vault | ~3.5M | 0.119 | $0.023 |
| Complex protocol | ~7M | 0.238 | $0.046 |

---

## Estimating Gas for Your Contract

```bash
# Get the gas estimate from Foundry
forge test --gas-report

# Or estimate a specific function
cast estimate 0xContractAddress "transfer(address,uint256)" \
  0xRecipient 1000000000000000000 \
  --rpc-url https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc
```

---

## Comparison: Apertum vs Other Chains

| Action | Apertum | Ethereum Mainnet | Arbitrum | Base |
|--------|---------|-----------------|----------|------|
| Transfer | < $0.01 | < $0.01 | < $0.01 | < $0.01 |
| ERC-20 transfer | < $0.01 | < $0.01 | < $0.01 | < $0.01 |
| Swap | < $0.01 | < $0.05 | < $0.01 | < $0.01 |
| NFT mint | < $0.01 | < $0.05 | < $0.01 | < $0.01 |
| ERC-20 deploy | < $0.01 | < $0.30 | < $0.05 | < $0.05 |

At current prices, Apertum is cost-competitive with all major chains. The difference is dedicated throughput — your costs don't spike because of someone else's activity.

---

## APTM Tokenomics

APTM has a halving mechanism that reduces block rewards over time. This affects validator revenue, not user gas costs. Gas prices are set by the market (users bidding for inclusion), not by the protocol.

- **Current supply:** Check the explorer
- **Halving schedule:** See the whitepaper at `https://apertum.io/apt-whitepaper.pdf`
- **Gas is burned/paid to validators:** Check protocol docs

---

## Optimization Tips

1. **Batch transactions** — If you need approve + transfer, use a router that batches them
2. **Use exact approvals** — Don't approve `type(uint256).max`, approve the amount you need
3. **Pack storage variables** — Solidity packs uint128s, uint64s, etc. into single slots
4. **Use events** — Events cost ~375 gas. Storage costs 20,000. Index offchain, store onchain.
5. **Cache storage reads** — SLOAD costs 2,100 gas. Cache values in memory during function execution.
