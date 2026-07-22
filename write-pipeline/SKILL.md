---
name: write-pipeline
description: High-throughput write patterns on Apertum (Chain ID 2786) — nonce lanes, pre-sign + sendRaw, batch ABI, multi-writer packing. Use for agents, keepers, indexers, mesh/receipt writers, or any multi-tx backend firehose.
---

# Write Pipeline on Apertum

## What You Probably Got Wrong

**Serial `send` + `wait` is not a throughput test.** It measures RTT. On Apertum the chain packs many txs per ~2s block; your laptop loop does not.

**Hardhat signer pre-sign works.** `HardhatEthersSigner.signTransaction` is **not implemented**. Use a real `ethers.Wallet` / viem account from the private key for pre-sign legs.

**One underfunded hot wallet for 200 txs.** Mid-queue `insufficient funds for gas * price + value` looks like random RPC failures. Fund from math, not vibes.

---

## The three speeds

| Mode | Pattern | Ballpark (mainnet mesh suite, 2026-07-22) | Use |
|------|---------|-------------------------------------------|-----|
| Slow | `send → wait → send → wait` | ~1 tx/s | interactive single-user tx OK |
| Medium | parallel nonce send, wait end | ~ few–10 tx/s / wallet | bursts from one key |
| Fast | pre-sign all + `sendRaw` chunks + multi-wallet | ~10+ tx/s aggregate; **80–100 txs/block** packing | agents, indexers, liquidations, mesh |

Chain constants: **chainId `2786`**, full RPC path required, explorer `https://explorer.apertum.io`. See `throughput/SKILL.md` for measured ceilings (~161 mesh TPS theory vs ~10.5 wall observed).

---

## Nonce manager (required for >1 in-flight tx / address)

Rules:

- Track `nextNonce` per address in process memory (and durable store if multi-process).  
- Seed from `getTransactionCount(addr, "pending")` on startup and after errors.  
- **Never** two processes same key without a distributed lock.  
- On `nonce too low` / `already known`: resync pending count.  
- On stuck tx: **same nonce**, higher fee (replace-by-fee).  
- On gap (nonce n+1 sent before n lands): you created a stall — fix ordering.

Sketch:

```ts
// one process owns one address
class NonceLane {
  private next: number | null = null;
  constructor(private provider: Provider, private address: string) {}

  async seed() {
    this.next = await this.provider.getTransactionCount(this.address, "pending");
  }

  take(): number {
    if (this.next == null) throw new Error("call seed() first");
    return this.next++;
  }

  async resync() {
    this.next = await this.provider.getTransactionCount(this.address, "pending");
  }
}
```

---

## Pre-sign + raw blast (backend)

```text
for each op:
  encode calldata
  build tx { to, data, nonce, gasLimit, gasPrice|maxFee, chainId: 2786, type }
  raw = wallet.signTransaction(tx)     # real Wallet/account — NOT HardhatEthersSigner
chunk raw[] and provider.broadcastTransaction / sendRawTransaction
wait receipts in bulk (poll / subscribe) with RPC retry
```

**Funding pitfall (multi-wallet):** fund ≥ `gasLimit * gasPrice * txs * 1.35 + dust`, not a guess like "0.05 APTM". Underfund looks like random RPC errors mid-blast.

**Hardhat pitfall:** use `ethers.Wallet` from `APERTUM_DEPLOYER_PRIVATE_KEY` (or per-writer keys) for pre-sign; never assume the Hardhat network signer can sign raw payloads.

Env keys (writers / deploy — never commit):

```bash
APERTUM_CHAIN_ID=2786
APERTUM_RPC_URL=https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc
APERTUM_DEPLOYER_PRIVATE_KEY=0x...
```

---

## Contract batching

If you control the ABI:

```solidity
function doMany(Item[] calldata items) external returns (uint256 firstId, uint256 lastId);
// bounds: require(items.length > 0 && items.length <= MAX);
```

Guidelines:

- Cap batch size (mesh uses **max 100**).  
- Emit one event per logical item + optional summary event.  
- Prefer `calldata` arrays.  
- Define failure policy: all-or-nothing vs best-effort — do not leave fragile shared state undefined.  
- Measured density example: ~37.2k gas/action alone vs ~9.1k/action inside a batch of 100 (~4× denser).

---

## Multi-writer / multi-lane

When one wallet still leaves busy blocks under ~30% gas full:

1. Confirm RPC and nonce path are solid (not serial waits).  
2. Split work across **N EOAs**, each with its own nonce lane and pre-signed queue.  
3. Use a **dedicated writer RPC** (public OK for light wallet reads only).  
4. Grant least-privilege roles (`WRITER_ROLE` / keeper) — not admin keys.  
5. Revoke ephemeral writers after demos.

Observed packing improvement (mesh suite): 1 writer peak **80 txs/block** → 4 writers peak **100 txs/block** (still well under theoretical ~322 mesh txs/block).

---

## Relayer / session keys

Use when:

- High-freq game or agent actions  
- Users should not pop a wallet 50 times  
- You can budget gas and revoke sessions  

Still: rate limit, per-user budgets, and kill switches. Prefer Permit/Permit2 to collapse approve+action when ERC-20 allowance is in the path.

---

## Gas limits and fees on the write path

| Approach | Pros | Cons |
|----------|------|------|
| `estimateGas` every time | safe for varying calldata | extra RTT; fails open on node load |
| Fixed limit from measured gasUsed × 1.15–1.25 | fast hot path; better packing | must refresh when bytecode/args change |

**Hot path recipe:** measure `gasUsed` on mainnet canary → set `gasLimit = gasUsed * 1.2` → re-canary after upgrades.

Fee policy during bursts:

```text
fee = getFeeData() cached 1–2s during bursts
send with small buffer (e.g. * 1.1)
if not mined in ~2–3 blocks: replace same nonce with higher tip
```

Prefer EIP-1559 fields if the network returns `baseFeePerGas`; else legacy `gasPrice`. Assert `chainId === 2786` before every send.

Calldata: long CIDs/URLs raise gas and shrink txs/block. Prefer `bytes32` hashes on-chain; short refs off-chain; clip CID length in hot paths.

---

## Backend firehose checklist

- [ ] Real Wallet / viem account pre-sign path  
- [ ] Nonce manager + single owner process per key  
- [ ] Fund math: `gasLimit * price * n * 1.35`  
- [ ] Chunked raw send + bulk receipts + retries  
- [ ] Multi-wallet if still under ~30% block util  
- [ ] Batch contract API if logical fan-in  
- [ ] Revoke/disable switch  
- [ ] Private / dedicated RPC for writers  
- [ ] `chainId` 2786 asserted  

---

## Related skills

- Baselines and ceilings: `throughput/SKILL.md`
- Brownfield ladder / KPIs: `optimize/SKILL.md`
- RPC hardening + canaries + security at speed: `ops/SKILL.md`
- UX confirmations (1 conf, optimistic hash): `frontend-ux/SKILL.md`
