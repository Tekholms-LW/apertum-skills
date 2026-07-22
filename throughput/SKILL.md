---
name: throughput
description: Calibrated Apertum chain performance (Chain ID 2786) — block time, 12M block gas limit, measured baselines and theoretical ceilings. Use when sizing throughput, interpreting TPS claims, designing batch density, or deciding whether slowness is the L1 or your client.
---

# Throughput & Performance Baselines on Apertum

## What You Probably Got Wrong

**"The chain is slow."** On Apertum, serial `send → wait → send` usually measures **your RPC RTT and client**, not the L1. Busy blocks in real floods still had **~70% free gas**.

**You cite marketing block time as capacity.** Capacity is **sustained gas utilization + apps that feed the chain without serializing on RPC**. ~2s blocks exist; they do not auto-fill.

**You treat empty-transfer TPS as the product story.** Useful as one stress leg. Product capacity is **actions/s**, **$/logical op**, and **txs packed per block** under real calldata.

---

## Chain constants (copy-paste)

Calibrated **2026-07-22** from live mainnet (Agent Action Mesh throughput suite + block samples). Re-run canaries after RPC, gas limit, or fee-market changes.

```ts
// chains/apertum.ts — single source of truth for every repo
export const APERTUM = {
  chainId: 2786,
  name: "Apertum",
  nativeCurrency: { name: "APTM", symbol: "APTM", decimals: 18 },
  // Full path required — bare hosts often fail on Avalanche subnet RPCs
  rpcUrls: {
    default: {
      http: [
        process.env.APERTUM_RPC_URL ||
          "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc",
      ],
    },
  },
  blockExplorers: {
    default: {
      name: "Apertum Explorer",
      url: "https://explorer.apertum.io",
      apiUrl: "https://explorer.apertum.io/api",
    },
  },
  // Calibrated 2026-07-22 — re-verify with a watch-blocks canary
  targetBlockTimeMs: 2000,
  blockGasLimit: 12_000_000,
} as const;
```

| Item | Value |
|------|--------|
| Chain ID | `2786` |
| Native token | APTM (**18 decimals**) |
| RPC (default) | `https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc` |
| Explorer | https://explorer.apertum.io |
| Explorer API | https://explorer.apertum.io/api |
| Env keys | `APERTUM_RPC_URL`, `APERTUM_DEPLOYER_PRIVATE_KEY`, `APERTUM_EXPLORER_API_KEY` |
| Target block time | **~2s-class** (measured 2.0s flat under flood; idle avg ~2.4s) |
| Block gas limit | **12,000,000** (tip sample 2026-07-22) |

> Older pack summaries sometimes said **~2.8s**. Prefer the **2026-07-22** calibration above for capacity math; re-measure live if your RPC or network epoch differs.

---

## Mental model: what "fast" means here

Apertum is a **dedicated Avalanche L1** with:

- **~2s block times** (measured 2.0s flat under floods; recent idle avg ~2.4s, occasional 5s)
- **12M block gas limit**
- **Low fees** relative to L1 Ethereum
- Public RPC that **will** timeout under a naive firehose

| Ethereum-mainnet habit | Apertum habit |
|------------------------|---------------|
| Wait 12+ confirmations | **1 confirmation** is usually enough for UX |
| Gas optimization above all | **Batch + RPC + nonce** dominate wall time |
| One tx per user action is fine | Prefer **1 signature / 1 tx per mental action** |
| Serial `await send; await wait` | **Pipeline**: pre-sign, blast raw, bulk receipts |
| "The chain is slow" | Usually **your client/RPC** is slow |

**Prime is not "2s blocks exist."**  
Prime is **high sustained gas utilization + apps that feed the chain without serializing on RPC RTT.**

---

## Measured performance baselines (2026-07-22)

From live mainnet Agent Action Mesh suite. Example mesh-style workload; adapt numbers to your ABI.

### Block production

| Metric | Value |
|--------|--------|
| Burst span block time | **2.0s** (min=max=med) |
| Recent ~40 blocks | avg **~2.41s**, med **2s**, max **5s** |
| Block gas limit | **12,000,000** |
| Idle avg gas util | often **&lt;5%** |
| Peak util during flood | **~25–31%** on busiest blocks |
| Tip sample max util (other traffic) | ~**49%** |

### Application path (mesh receipts)

| Path | Result |
|------|--------|
| Batch `recordActionBatch` 5×100 | **500 actions / 11.71s → 42.7 actions/s**, ~$0.0275 total |
| Pre-sign + raw, 1 writer, 100 txs | **8.65 tx/s** wall, peak **80 our txs/block** |
| Pre-sign + raw, 4 writers × 50 | **10.51 tx/s** wall, peak **100 our txs/block** |
| Serial individual (older test) | ~**1.27 tx/s** — client-bound |
| Gas / single `recordAction` | **~37,200** |
| Gas / action inside batch of 100 | **~9,100** (~4× denser) |
| Inclusion latency (approx) | p50 **~2.4s**, p95 **~4.1s** |

### Cost order of magnitude

At APTM ≈ $0.195 (ops reporting only — update for your reports):

| Work | APTM (approx) | USD |
|------|----------------|-----|
| 25 actions / 1 batch tx | ~0.008 | ~$0.0015 |
| 500 actions / 5 batch txs | ~0.14 | ~$0.028 |
| 100 individual record txs | ~0.12 | ~$0.023 |
| 200 multi-writer individuals | ~0.23 | ~$0.045 |

**Takeaway:** batching wins on **$/logical op** and **actions/s**. Multi-writer + raw send wins on **txs/block packing**. Serial wait loops measure your laptop, not Apertum.

---

## Theoretical ceilings (gas-bound)

Assumptions: `gasLimit = 12_000_000`, `blockTime = 2.0s`, measured mesh gas.

```
max_per_block = floor(gasLimit / gas_per_tx)
max_per_sec   = max_per_block / block_time
```

| Workload | Gas/tx (approx) | Max / block | Max / sec @ 2s |
|----------|-----------------|-------------|----------------|
| Mesh-like `recordAction` | 37.2k | **~322 txs** | **~161 TPS** |
| Simple transfer | 21k | **~571 txs** | **~286 TPS** |
| Batch of 100 actions | 911k | **~13 batch txs** | **~6.5 batch-tx/s** |
| Actions via full batch packing | 9.1k / action | **~1,300 actions** | **~650 actions/s** |

Observed vs ceiling (mesh flood):

| | Peak observed | Theory | % of theory |
|--|---------------|--------|-------------|
| Mesh txs/block | 100 | ~322 | ~31% |
| Wall mesh TPS | ~10.5 | ~161 | ~7% |

So **the chain still had ~70% free gas** on "busy" blocks. Optimization order for most teams:

1. Client / RPC / nonce lanes  
2. Batching logical work  
3. Only then "is the L1 gas limit too low?"

At **2.4s** average blocks, scale TPS by `2/2.4` (~17% lower).

**Caveats:** gas math ignores mempool policy, validator CPU, bandwidth, competing traffic, and long calldata (longer CIDs → fewer txs/block).

---

## Greenfield day-0 (performance-shaped layout)

```
my-apertum-app/
  src/chain/apertum.ts          # chain constants (above)
  src/lib/nonceManager.ts       # per-address queue
  src/lib/sendRaw.ts            # sign + chunked broadcast + bulk wait
  src/lib/multicall.ts          # batched eth_call
  src/lib/fees.ts               # fee cache + bump
  scripts/canary-gas.ts         # one mainnet call → gasUsed
  scripts/watch-blocks.ts       # block gap + gas util
  contracts/
  .env.example                  # APERTUM_RPC_URL, keys never committed
```

Day-0 decisions:

1. **Who sends txs?** User wallet only vs backend writers vs hybrid.  
2. **What must be on-chain?** Commitments, receipts, settlements — not bulky JSON.  
3. **Batch entrypoints** in v1 ABI (even if UI starts with `n=1`).  
4. **Event schema** for indexers on day 1.  
5. **One RPC strategy:** public for light wallet reads; **dedicated for writers**.  
6. **Verify path** (Standard JSON) ready before marketing mainnet.

Minimal mainnet canary before building UI: `eth_blockNumber` latency, one tiny known call or self-transfer, print blockTime / gasUsed / effective fee / explorer URL. If `getBlockNumber` p99 &gt; ~300ms, fix RPC before optimizing contracts.

Ship order: read-only multicall UI → single write + optimistic UI → indexer/cache → batch/permit/multi-lane when a real hotspot appears.

---

## Related skills

- High-throughput **writes**: `write-pipeline/SKILL.md`
- Brownfield speed-up ladder: `optimize/SKILL.md`
- RPC hardening, canaries, anti-patterns: `ops/SKILL.md`
- Fee tables (gwei / USD): `gas/SKILL.md`
- Chain setup: `getting-started/SKILL.md`
