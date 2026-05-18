---
name: indexing
description: How to read and query onchain data on Apertum. Events, Blockscout API, The Graph subgraph (graph.apertum.io), and indexing patterns. Why you cannot just loop through blocks, and what to use instead.
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

---

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

### Via Blockscout API

```bash
curl "https://explorer.apertum.io/api?module=logs&action=getLogs&address=0x...&fromBlock=0&toBlock=latest"
```

---

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

## Blockscout API (Etherscan-Compatible)

The Blockscout API on Apertum is largely compatible with the Etherscan API:

```bash
# Account balance
curl "https://explorer.apertum.io/api?module=account&action=balance&address=0x...&tag=latest"

# Transaction list
curl "https://explorer.apertum.io/api?module=account&action=txlist&address=0x...&startblock=0&endblock=latest"

# Token transfers
curl "https://explorer.apertum.io/api?module=account&action=tokentx&address=0x..."

# Contract ABI (if verified)
curl "https://explorer.apertum.io/api?module=contract&action=getabi&address=0x..."
```

---

## Common Patterns

### Get All Holders of a Token

Query `Transfer` events and aggregate balances:

```python
# Process Transfer events to build holder map
holders = {}
for event in transfer_events:
    sender = event["from"]
    receiver = event["to"]
    amount = event["value"]
    
    holders[sender] = holders.get(sender, 0) - amount
    holders[receiver] = holders.get(receiver, 0) + amount

# Filter zero balances
active_holders = {addr: bal for addr, bal in holders.items() if bal > 0}
```

### Track Daily Volume

Sum transfer amounts grouped by date from Transfer events.

### Monitor Specific Activity

Filter events by address and topic, process incrementally.

---

## Pitfalls

1. **Don't scan blocks linearly** for large ranges. Use The Graph or Blockscout API.
2. **Events are in transaction receipts**, not contract storage. You can't read past events from a contract call.
3. **Index by the fields you filter on.** You get 3 indexed topics per event. Use them for addresses and IDs.
4. **Subgraph may lag behind** the latest blocks. Use polling for the trailing edge.
5. **APTM transfers don't emit ERC-20 events.** Native transfers are tracked in transaction traces, not logs.
