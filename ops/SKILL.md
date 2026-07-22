---
name: ops
description: Apertum production ops (Chain ID 2786) — RPC writer hardening, observability and canaries, security-at-throughput, anti-patterns, and deploy/feature checklists. Use when hardening backends, debugging timeouts, or shipping mainnet automation safely.
---

# Ops Hardening on Apertum

## What You Probably Got Wrong

**Public RPC will survive your firehose.** Avalanche subnet full paths matter; naive parallel blasts produce `ConnectTimeoutError` / mid-burst failures. Dedicated writer RPC + chunking is not optional for production senders.

**More speed is free.** Throughput multiplies blast radius: admin keys in writers, unbounded automation roles, and secrets in events all get worse as you scale.

**Retries fix bad nonces.** Wrong nonce management, missing `chainId`, underpriced replacements, and contract reverts are not RPC problems. Simulate with `eth_call` before user-facing sends.

---

## RPC survival guide

### Must-have endpoints and env

| Item | Value |
|------|--------|
| Chain ID | `2786` |
| Full default RPC | `https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc` |
| Explorer | https://explorer.apertum.io |
| Explorer API | https://explorer.apertum.io/api |
| Env | `APERTUM_RPC_URL`, `APERTUM_DEPLOYER_PRIVATE_KEY`, `APERTUM_EXPLORER_API_KEY` |

**Full path required** — bare hosts often fail on Avalanche L1 RPCs.

### Symptoms under load

- `ConnectTimeoutError` / `UND_ERR_CONNECT_TIMEOUT` mid-blast  
- `insufficient funds for gas * price + value` with **queued cost** (underfunded multi-send)  
- Empty `eth_call` / decode errors under flaky connections  

### Writer hardening checklist

- [ ] `APERTUM_RPC_URL` full path (subnet RPC path matters)  
- [ ] Dedicated RPC for writers; public OK for light wallet reads  
- [ ] Failover URLs; sticky session per process  
- [ ] HTTP keep-alive / connection pooling  
- [ ] Retries with exponential backoff on **timeout / 429 / 502 / 503** only  
- [ ] Retries on `sendRaw` only if you are sure the tx was not accepted (or resend **same** raw tx idempotently)  
- [ ] Separate read vs write clients  
- [ ] Health metric: `eth_blockNumber` latency p50/p99  
- [ ] Receipt polling in **batches** (e.g. 40 hashes), not unbounded parallel always  
- [ ] Assert `chainId === 2786` before send  

### What RPC will not fix

Wrong nonce management, missing `chainId`, underpriced replacements, or contract reverts. See `write-pipeline/SKILL.md` for nonce + pre-sign.

---

## Observability and canaries

### Per-block watchdog (cron, no LLM required)

Log / alert:

- `block.timestamp` delta (block time)  
- `gasUsed / gasLimit`  
- tx count  
- your contracts' share of gas (optional)  
- tip lag vs wall clock  

Alert examples:

- block time ≥ 5s twice in a row  
- gas util ≥ 80% sustained (congestion)  
- writer balance &lt; threshold  
- RPC p99 latency spike  

### Product canaries

- One mainnet "hello" tx after each deploy  
- Read path smoke: multicall critical views  
- Explorer link in deploy receipt message (Telegram, chat, CI)  

### Metrics worth dashboards

- actions/s or business-ops/s (not only TPS)  
- $/business-op  
- inclusion p50/p95  
- % failed txs  
- RPC error rate  

Calibrated baselines (re-measure after infra changes): ~2s-class blocks, 12M gas limit, mesh suite peaks — see `throughput/SKILL.md`.

---

## Security at throughput

More speed ⇒ more blast radius.

- Separate **admin** and **writer/keeper** keys  
- Role grant/revoke runbooks tested on mainnet once  
- Rate limits and daily APTM budgets per writer  
- No secrets in events, CIDs, or goal/result strings — hash them  
- Simulate user txs before send  
- Pause / revoke switches for automation roles  
- Don't leave ephemeral `WRITER_ROLE` addresses granted after demos  
- Treat public RPC as adversarial for metadata (not for key safety — keys never go there)  
- Browser: never inject admin/writer hot keys  
- Backend writers: env / HSM / separate EOAs; least privilege  
- Hard-check `chainId === 2786` before send  

General Solidity audit depth: `security/SKILL.md` and `audit/SKILL.md`. This section is the **ops multiplier** when you add firehose writers.

---

## Anti-patterns

| Anti-pattern | Why it hurts on Apertum |
|--------------|-------------------------|
| Serial `send`+`wait` as "throughput test" | Measures RTT; chain packs many txs/block |
| Hardhat signer pre-sign | Not implemented |
| Waiting 12 confs for UX | Wastes ~20s+ for no benefit |
| estimateGas × 100 in a burst | Multiplies RPC load |
| One underfunded hot wallet for 200 txs | Mid-queue insufficient funds |
| Full metadata on-chain | Gas + bad UX; use CID/hash |
| Admin key in browser or cron without budget | Catastrophic drain risk |
| Ignoring public RPC timeouts | Flaky prod under load |
| Claiming "max TPS" with empty transfers only | Weak product story; OK as one stress leg |
| Copy-pasting Ethereum gas UI fear | Users over-hesitate on sub-cent fees |

---

## Checklists

### A. New feature (every PR)

- [ ] Can this be **one user signature**?  
- [ ] Can N ops be **one contract call**?  
- [ ] Reads multicall'd + cached ~1 block?  
- [ ] Hot path avoids extra `estimateGas` if limit known?  
- [ ] UI unlocks on **hash**, not only receipt?  
- [ ] `chainId` 2786 asserted?  
- [ ] GasUsed measured on canary if new calldata shape?  
- [ ] Failures: user-readable + explorer link  

### B. Existing platform speed-up sprint

See `optimize/SKILL.md` (profile, collapse txs, multicall, fixed gas, re-measure).

### C. Backend firehose / agent

See `write-pipeline/SKILL.md` (pre-sign, nonce lane, fund math, multi-wallet, private RPC).

### D. Mainnet deploy

- [ ] chainId 2786  
- [ ] compiler settings documented  
- [ ] Standard JSON + constructor args saved  
- [ ] roles granted to intended EOAs only  
- [ ] canary tx + explorer verify attempt  
- [ ] monitors updated with new address  
- [ ] no private keys in repo, CI logs, or chat  

---

## Env template (public shape)

```bash
APERTUM_CHAIN_ID=2786
APERTUM_RPC_URL=https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc
APERTUM_DEPLOYER_PRIVATE_KEY=0x...   # writers/deploy only; never commit
APERTUM_EXPLORER_API_KEY=            # if required
APTM_USD=0.195                       # ops reporting only; update as needed
```

Workspace-local deploy scripts and private keys stay **out of this public pack**. Prefer env / secret managers; document only patterns, not secrets.

---

## One-page ops summary

```
Apertum 2786 | ~2s blocks | 12M gas | APTM 18 dec

RPC:    full path; dedicated writers; failover; retry timeouts/429/5xx only
SEND:   pre-sign + raw + nonce manager; multi-wallet if firehose
WATCH:  block time, gas util, writer balance, RPC p99, canary after deploy
SECURE: admin ≠ writer; budgets; revoke demos; no secrets in events
UX:     1 conf; unlock on hash; explorer links
REALITY: if busy blocks <30% full, fix client not the L1
```

---

## Related skills

- Performance numbers: `throughput/SKILL.md`
- Write pipeline: `write-pipeline/SKILL.md`
- Brownfield optimize: `optimize/SKILL.md`
- Gas fee tables: `gas/SKILL.md`
- Indexing / explorer API: `indexing/SKILL.md`
- Contract security: `security/SKILL.md`
