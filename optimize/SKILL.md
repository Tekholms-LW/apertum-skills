---
name: optimize
description: Brownfield optimization for Apertum dApps (Chain ID 2786) — measure first, optimization ladder L0–L8, KPIs, "is it the chain?" decision tree, product-type patterns (marketplace, agents, DeFi keepers, indexers), and contract design for a fast L1.
---

# Optimize Existing Platforms on Apertum

## What You Probably Got Wrong

**You redesign contracts first.** On Apertum most "slowness" is client/RPC/nonce/batch. Peak blocks under a real flood often stay **&lt;30–50% gas full** — fix the feed before the protocol.

**You wait 5–10 confirmations for UX.** ~2s-class blocks mean 1 conf is usually enough; extra confs burn wall clock for little reorg benefit.

**You blame the L1 without gas util data.** If blocks are ~2s and your busy blocks are not &gt;60% full, it is almost always **you**.

---

## Measure before changing product code

Capture one week of:

| Signal | How | Red flag |
|--------|-----|----------|
| Time from click → hash | client timing | &gt; 1–2s |
| Time from hash → 1 conf | receipt wait | &gt; 6–8s sustained |
| Tx count per user action | product analytics | ≥3 when 1 is possible |
| `estimateGas` calls per action | RPC logs | &gt;1 on hot path |
| Serial `await tx.wait()` chains | code search | any multi-step flow |
| Block gas util when *you* are busy | watch-blocks during peak | your peak blocks &lt;30% full |
| RPC errors | 429/timeout/tx underpriced | any during normal load |
| Duplicate nonce / replacement storms | wallet logs | stuck queues |

Chain facts for interpretation: **chainId `2786`**, APTM **18 decimals**, full default RPC  
`https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc`,  
explorer `https://explorer.apertum.io`, ~2s-class blocks, **12M** block gas (calibrated 2026-07-22). Details: `throughput/SKILL.md`.

---

## Optimization ladder (stop when KPIs hit target)

```
L0  Fix RPC + timeouts + retries (idempotent)
L1  Optimistic UI; wait(1); don't block on receipt for navigation
L2  Multicall reads; cache ~1–2s (≈1 block)
L3  Collapse multi-tx flows (Permit/Permit2, multicall write, batch ABI)
L4  Fixed gas limits on hot paths after measuring gasUsed
L5  Nonce manager + parallel send for any multi-tx session
L6  Backend writer pool / relayer for high-freq automation
L7  Off-chain index for history; chain as settlement + events
L8  Only then: protocol redesign / new contracts
```

Write-path details for L5–L6: `write-pipeline/SKILL.md`. RPC hardening: `ops/SKILL.md`.

---

## "Is it the chain?" decision tree

```
blocks ~2s and stable?
  no  → check RPC skew / explorer lag / real block production (chain ops)
  yes →
    are your peak blocks >60% gas full?
      no  → client/RPC/nonce/batch problem (you) ← most teams stop here
      yes → competing traffic or need higher gas limit / fee market (chain ops)
```

---

## Refactors that usually pay off

1. **Approve + action → Permit/Permit2 + action** (one less tx).  
2. **N cancels / N claims → one batch function**.  
3. **Page load with 20 `eth_call`s → one Multicall3**.  
4. **History via RPC logs every visit → indexed DB**.  
5. **Admin scripts on Hardhat `run` for bursts → thin ethers/viem script with raw send**.  
6. **Hardcoded public RPC only → env RPC list + failover**.  
7. **Wait 5–10 confs → wait 1 conf + background reorg handler** (reorg depth usually shallow for UX).  

---

## KPI targets (practical)

| KPI | Good on Apertum | Stretch |
|-----|-----------------|---------|
| Click → hash | &lt; 500ms | &lt; 200ms |
| Hash → 1 conf | &lt; 4s p50 | &lt; 3s |
| Txs per checkout | 1 (2 max) | 1 |
| Read waterfall on home | 1 multicall | cached |
| Writer throughput (backend) | &gt; 20 tx/s | &gt; 100 tx/s |
| Your busy-block gas util | &gt; 50% | &gt; 70% |

---

## Speed-up sprint checklist

- [ ] Profile click→hash and hash→conf  
- [ ] Code search: `await.*wait(`, sequential sends  
- [ ] Count txs per top user journeys  
- [ ] RPC latency p99 + error rate  
- [ ] Add multicall on heaviest page  
- [ ] Collapse approve+action if present  
- [ ] Fixed gas limits on top 3 write paths  
- [ ] Indexer for history if still RPC-scraping UI  
- [ ] Re-measure KPIs  

---

## Contract design for a fast L1

### Prefer

- Events as the index bus; minimal storage  
- Batch / multicall entrypoints from v1  
- `calldata` + custom errors  
- Pull-over-push for N-user payouts  
- Explicit status enums (e.g. 0 started / 1 ok / 2 error / 3 skipped)  
- Role separation: `DEFAULT_ADMIN_ROLE` vs hot `WRITER_ROLE` / minters / keepers  
- Bounds on loops (`n > 0 && n <= MAX`)  

### Avoid

- Unbounded arrays iterated on every call  
- Multi-tx protocols without Permit when ERC-20 allowance is needed  
- Huge string returns on view methods used every render  
- Admin and hot writer as the same key forever  

### Upgrade / verify

- Save Standard JSON + constructor args at deploy  
- Blockscout verify may need UI upload if solc CDN is flaky  
- Document implementation address if proxy  

**Example pattern:** event-heavy receipts with single + batch entrypoints (cap batch size, AccessControl writers) — good template for **telemetry / audit / agent** workloads, not for storing full transcripts on-chain.

Typical compile defaults that work: Solidity **0.8.24**, optimizer **200**, `evmVersion: cancun` if using OZ ≥5.2; `metadata.bytecodeHash = "none"` helps Blockscout verify stability.

---

## Patterns by product type

### NFT marketplace

- Batch cancel / batch update price  
- Index Transfer + sale events for history UI  
- Don't resolve tokenURI on every row in a list (cache)  
- Buyer-pays flows; clear fee math in UI  
- Watch for DID / provenance false positives in security scans — accuracy &gt; noise  

### Tokenized apps / web2.5 migrations

- Wallet sign-in over email/password when moving on-chain  
- On-chain only for settlements and critical commitments  
- Signed forms → IPFS → CID on-chain later if needed  
- Privacy toggles: mask address if desired; **don't** fake balances  

### Agents / automation

- Buffer work receipts → **batch flush** every 1–2s or N items  
- Dedicated fast-path node writers for single receipts; suite scripts for bursts  
- Auto-record only with min interval / min size filters  
- Cron/monitors: prefer deterministic scripts over LLM loops for health checks  

### DeFi

- Multicall quotes; deadlines; slippage  
- Don't assume private mempool  
- Keeper bots: multi-lane + private/dedicated RPC (see `write-pipeline/SKILL.md`)  

### Indexers / bots / scanners

- Poll 1–2s or WS heads  
- Checkpoint blocks; idempotent handlers  
- Rate-limit explorer API; correct headers  
- Alert on block time &gt; 4–5s or util spikes  
- Source of truth for UX lists: your DB; for settlement: chain  

### Reads: multicall, cache, index

| Data | Suggested staleTime |
|------|---------------------|
| Block number / tip | 1s |
| Balances / listings that change often | 1–2s |
| Rarely changing config / roles | 30–300s |
| Token metadata / tokenURI | minutes–hours (immutable if IPFS CID) |

Refetch-on-new-block often beats fixed 10s polling for "live" feel without thrash. Explorer API base: `https://explorer.apertum.io/api` (Blockscout-style); prefer server-side proxy for keys and rate limits. Deeper indexing: `indexing/SKILL.md`.

---

## Related skills

- Measured baselines: `throughput/SKILL.md`
- Write firehose: `write-pipeline/SKILL.md`
- Ops / canaries / anti-patterns: `ops/SKILL.md`
- Frontend optimistic UX: `frontend-ux/SKILL.md`
- Security deep-dive: `security/SKILL.md`
