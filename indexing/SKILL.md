---
name: indexing
description: How to read and query onchain data on Apertum. Events, Blockscout API (v1/v2), The Graph subgraph (graph.apertum.io), RPC access, and indexing patterns. Includes verified endpoints and test cases using the DEX Router contract.
---

# Onchain Data & Indexing on Apertum

## What You Probably Got Wrong

**You try to query historical state via RPC calls.** You can't cheaply read past state. `eth_call` reads current state. For historical data, you need an indexer.

**You loop through blocks looking for events.** Scanning millions of blocks is O(n) — it will timeout or get rate-limited. Use an indexer that has already processed every block.

**You store query results onchain.** Leaderboards, activity feeds, analytics — compute offchain. If you need an onchain commitment, store a hash.

---

## Events Are Your API

Every state change should emit an event. Events are cheap (~375 gas) and free to read offchain.

```solidity
contract Marketplace {
    event Listed(uint256 indexed listingId, address indexed seller, uint256 price);
    event Sold(uint256 indexed listingId, address indexed buyer, uint256 price);

    function list(uint256 price) external returns (uint256) {
        uint256 id = nextListingId++;
        emit Listed(id, msg.sender, price);
    }
}
```

## Reading Events

### Via RPC (Small Scale)

```typescript
import { createPublicClient, http, parseAbiItem } from "viem";
import { apertum } from "./chains";

const client = createPublicClient({ chain: apertum, transport: http() });

const logs = await client.getLogs({
  address: "0xContractAddress",
  event: parseAbiItem("event Transfer(address indexed from, address indexed to, uint256 value)"),
  fromBlock: 0n,
  toBlock: "latest"
});
```

### Via Blockscout API (Recommended for most AI/agent use)

See the full verified catalog below.

## The Graph Subgraph

The primary indexing solution for Apertum:

- **DEX Subgraph:** `https://graph.apertum.io/subgraphs/name/dex/dex-subgraph`

### GraphQL Query Example

```graphql
{
  swaps(first: 10, orderBy: timestamp, orderDirection: desc) {
    id
    pair { token0 { symbol } token1 { symbol } }
    amount0In
    amount1Out
    timestamp
  }
}
```

```typescript
const response = await fetch(
  "https://graph.apertum.io/subgraphs/name/dex/dex-subgraph",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  }
);
const { data } = await response.json();
```

---

## Indexing Patterns

### 1. Event-Driven

Index every event as it happens. Standard approach used by The Graph.

### 2. Polling

Regularly fetch the latest block and process new events. Good for simple use cases.

```python
import time
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(APERTUM_RPC))
last_block = w3.eth.block_number

while True:
    current_block = w3.eth.block_number
    if current_block > last_block:
        for block_num in range(last_block + 1, current_block + 1):
            process_block(block_num)
        last_block = current_block
    time.sleep(2.8)  # Apertum block time
```

### 3. Hybrid

Use The Graph for historical + polling for the latest few blocks (before the subgraph indexes them).

---

## Blockscout API — Verified Endpoints (2026-05-30)

Apertum uses Blockscout. There are two API surfaces:

**Base**: `https://explorer.apertum.io`

- **v1** (Etherscan-compatible query params): `https://explorer.apertum.io/api`
- **v2** (modern REST): `https://explorer.apertum.io/api/v2`

### Working v1 Endpoints (reliable)
- `?module=contract&action=getsourcecode&address=...`
- `?module=contract&action=getabi&address=...`
- Account: balance, txlist, tokentx, tokenbalance, etc.

### Working v2 Endpoints (preferred for new work)
- `/api/v2/stats` — coin price, gas, utilization
- `/api/v2/addresses/{addr}/logs`
- `/api/v2/addresses/{addr}/transactions?filter=to`
- `/api/v2/tokens/{contract}/instances/{id}/transfers`
- `/api/v2/addresses/{addr}/tokens?type=ERC-721`
- `/api/v2/tokens?type=ERC-721` (or ERC-20)

**Pagination**: v2 responses include `next_page_params`. URL-encode the JSON object when following.

**Timestamps**: ISO 8601 strings (e.g. `2026-05-30T20:18:39.000000Z`). Use `datetime.fromisoformat()`.

**Log topics**: 32-byte zero-padded. Strip `0x000000000000000000000000` prefix for addresses.

**Null addresses**: Filter `0x000...000` before certain calls (can cause 422).

**Tested working** with proper User-Agent header in Python urllib/requests.

### Non-working (as of 2026-05-30)
- Most v2 smart-contract POST read/query endpoints return 404/403.
- v1 `contract.call` often returns "Something went wrong".

Full practical patterns (including OpenPlaza NFT forensics use cases) are also maintained in the Hermes Agent skills (`apertum-nft-forensics` and `nft-marketplace-dev`).

---

## RPC Access (Verified 2026-05-30)

**Correct full RPC URL** (from https://chainlist.org/chain/2786):

```
https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc
```

**Tested with Verified DEX Router contract**:
- Address: `0x73cf8b5c2F4920967Bd8e9dECDb18F9F1e12A29f`
- ABI: Available on explorer (`?tab=contract_abi`)
- Example: `eth_call` to `factory()` selector `0xc45a0155` returns `0x8bb8aa56642042a8c4de698e801f2e54ed5417dc` (correct).

**For AI agents**:
- Explorer v1/v2 REST API → Works reliably inside sandboxes and agent loops.
- Direct RPC (`eth_call`, etc.) → Works from terminal tool, host Python (requests + json or web3.py), and external scripts. Some sandboxes (e.g. execute_code) return 403 — use Explorer API as primary path in those environments.

Example curl test:
```bash
RPC="https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"
curl -s -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x73cf8b5c2F4920967Bd8e9dECDb18F9F1e12A29f","data":"0xc45a0155"},"latest"],"id":1}' \
  $RPC
```

The Python client at https://github.com/Tekholms-LW (or local /home/sky_ai/apertum/apertum.py) already uses this RPC.

---

## Common Patterns

### Get All Holders of a Token

Query `Transfer` events and aggregate balances (or use v2 `/tokens/.../holders` where available).

### Track Daily Volume

Sum transfer amounts grouped by date from Transfer events (cross-reference timestamps via transactions endpoint).

### Monitor Specific Activity

Filter events by address and topic, process incrementally using the logs endpoint.

---

## Pitfalls

1. **Don't scan blocks linearly** for large ranges. Use The Graph or Blockscout API.
2. **Events are in transaction receipts**, not contract storage. You can't read past events from a contract call.
3. **Index by the fields you filter on.** You get 3 indexed topics per event. Use them for addresses and IDs.
4. **Subgraph may lag behind** the latest blocks. Use polling for the trailing edge.
5. **APTM transfers don't emit ERC-20 events.** Native transfers are tracked in transaction traces, not logs.
6. **Sandbox RPC restrictions**: Some agent environments block or rate-limit direct RPC — prefer Explorer API for agent-internal logic.

---

*Last major verification: 2026-05-30 (RPC + full explorer v1/v2 catalog using DEX Router 0x73cf8b5c2F4920967Bd8e9dECDb18F9F1e12A29f as test case).*