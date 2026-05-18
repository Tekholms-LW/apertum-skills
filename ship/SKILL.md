---
name: ship
description: End-to-end guide for AI agents — from a dApp idea to deployed production app on Apertum (Chain ID 2786). Fetch this when building a dApp on Apertum. Routes you through all other skills phase by phase.
---

# Ship a dApp on Apertum

## What You Probably Got Wrong

**You jump to code without a plan.** Before writing a single line of Solidity, you need to know: what goes onchain, what stays offchain, how many contracts, and who calls every function. Skip this and you'll rewrite everything.

**You over-engineer.** Most dApps need 0-2 contracts. A token launch is 1 contract. An NFT collection is 1 contract. A marketplace that uses existing DEX liquidity needs 0 contracts. Three contracts is the upper bound for an MVP. If you're writing more, you're building too much.

**You put too much onchain.** Solidity is for ownership, transfers, and commitments. It's not a database. It's not an API. It's not a backend. If it doesn't involve trustless value transfer or a permanent commitment, it doesn't belong in a smart contract.

**You forget about chain selection.** You're building on Apertum (Chain ID 2786). It's an Avalanche L1 with dedicated throughput, ~2.8s block time, gas under $0.01. Choose Apertum deliberately — not just because it's what you know. If your app needs deepest DeFi liquidity, mainnet or Arbitrum may be better. If you need dedicated block space, predictable costs, and Avalanche ecosystem interoperability, Apertum is the right call. Fetch `why-apertum/SKILL.md` for the full comparison.

**You forget nothing is automatic.** Smart contracts don't run themselves. Every state transition needs a caller who pays gas and a reason to do it. If you can't answer "who calls this and why?" for every function, your contract has dead code. Fetch `concepts/SKILL.md` for the full mental model.

---

## Phase 0 — Plan the Architecture

Do this BEFORE writing any code. Every hour spent here saves ten hours of rewrites.

### The Onchain Litmus Test

Put it onchain if it involves:
- **Trustless ownership** — who owns this token/NFT/position?
- **Trustless exchange** — swapping, trading, lending, borrowing
- **Composability** — other contracts need to call it
- **Censorship resistance** — must work even if your team disappears
- **Permanent commitments** — votes, attestations, proofs

Keep it offchain if it involves:
- User profiles, preferences, settings
- Search, filtering, sorting
- Images, videos, metadata (store on IPFS, reference onchain)
- Business logic that changes frequently
- Anything that doesn't involve value transfer or trust

**Judgment calls:**
- Reputation scores → offchain compute, onchain commitments (hashes or attestations)
- Activity feeds → offchain indexing of onchain events (fetch `indexing/SKILL.md`)
- Price data → offchain oracles writing onchain

### Contract Design

**For every contract, answer:**
1. What state does it hold? (keep minimal — storage is expensive)
2. Who calls each function and why? (every function needs a caller with incentive)
3. What could go wrong? (fetch `security/SKILL.md`)

**For every state transition, answer:**
1. Who pokes it? (someone must pay gas)
2. Why would they? (what's their incentive?)
3. Is the incentive sufficient? (covers gas + profit?)

If you can't answer these, that state transition will never happen. Your contract will sit there, doing nothing, with nobody poking it.

---

## Phase 1 — Build Contracts

### 1.1 Setup

```bash
# Initialize Foundry project
forge init my-dapp
cd my-dapp

# Or use hardhat
npx hardhat init
```

### 1.2 Configure for Apertum

**foundry.toml:**
```toml
[profile.default]
solc_version = "0.8.22"
evm_version = "paris"

[rpc_endpoints]
apertum = "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"

[etherscan]
apertum = { key = "verify", url = "https://explorer.apertum.io/api" }
```

**hardhat.config.js:**
```javascript
module.exports = {
  solidity: "0.8.22",
  networks: {
    apertum: {
      url: "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc",
      chainId: 2786,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

### 1.3 Write Contracts

```solidity
// src/MyToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("MyToken", "MTK") {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }
}
```

### 1.4 Write Tests

```solidity
// test/MyToken.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Test} from "forge-std/Test.sol";
import {MyToken} from "../src/MyToken.sol";

contract MyTokenTest is Test {
    MyToken public token;

    function setUp() public {
        token = new MyToken(1_000_000e18);
    }

    function test_Name() public {
        assertEq(token.name(), "MyToken");
    }
}
```

```bash
forge test
```

Fetch `testing/SKILL.md` for comprehensive testing patterns including fuzz testing and fork testing against Apertum state.

### 1.5 Deploy to Apertum

```bash
# Deploy
forge create \
  --rpc-url https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc \
  --private-key $PRIVATE_KEY \
  --constructor-args 1000000000000000000000000 \
  src/MyToken.sol:MyToken

# Verify on explorer (Blockscout)
forge verify-contract \
  --verifier blockscout \
  --verifier-url "https://explorer.apertum.io/api" \
  0xDeployedAddress \
  src/MyToken.sol:MyToken
```

**Check verification:**
```
https://explorer.apertum.io/address/0xDeployedAddress
```
Look for the ✅ Verified badge.

### 1.6 Audit

Before moving to frontend, audit your contracts. Fetch `audit/SKILL.md` and run through it. Fetch `security/SKILL.md` for defensive patterns.

**Validate:** Deploy succeeds. Explorer shows verified. Tests pass.

---

## Phase 2 — Build Frontend

### 2.1 Setup

```bash
npm create vite@latest my-dapp-frontend -- --template react-ts
cd my-dapp-frontend
npm install wagmi viem @tanstack/react-query
```

### 2.2 Configure Apertum Chain

```typescript
// src/chains.ts
import { defineChain } from "viem";

export const apertum = defineChain({
  id: 2786,
  name: "Apertum",
  nativeCurrency: { decimals: 18, name: "Apertum", symbol: "APTM" },
  rpcUrls: {
    default: { http: ["https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"] }
  },
  blockExplorers: {
    default: { name: "Apertum Explorer", url: "https://explorer.apertum.io/" }
  }
});
```

### 2.3 Connect Wallet

```typescript
import { createConfig, http, WagmiProvider } from "wagmi";
import { apertum } from "./chains";

const config = createConfig({
  chains: [apertum],
  transports: {
    [apertum.id]: http()
  }
});
```

### 2.4 Read from Contract

```typescript
import { useReadContract } from "wagmi";
import { erc20Abi } from "viem";

function TokenBalance({ address }: { address: `0x${string}` }) {
  const { data: balance } = useReadContract({
    address: "0xTokenAddress",  // Verify in addresses/SKILL.md
    abi: erc20Abi,
    functionName: "balanceOf",
    args: [address]
  });
  
  return <div>Balance: {balance?.toString()}</div>;
}
```

### 2.5 Write to Contract (The Three-Button Flow)

Any token interaction shows ONE button at a time:

```
1. Switch Network (if wrong chain)
2. Approve Token (if allowance insufficient)
3. Execute Action (only after 1 & 2 satisfied)
```

Never show Approve and Execute simultaneously. Fetch `frontend-ux/SKILL.md` for the full UX rules.

### 2.6 Validate

- Full user journey works with real wallet
- All edge cases handled (wrong network, insufficient balance, rejected tx)
- Fetch `qa/SKILL.md` for the complete QA checklist

---

## Phase 3 — Production

### 3.1 Deploy Frontend

**IPFS (Recommended):**
```bash
npm run build
# Upload out/ or dist/ to IPFS
```

**Vercel:**
```bash
vercel --prod
```

### 3.2 Production Checklist

- [ ] Contract verified on explorer
- [ ] Frontend deployed with correct chain config (Chain ID 2786)
- [ ] RPC endpoint is production (not testnet)
- [ ] All contract addresses verified in `addresses/SKILL.md`
- [ ] Security audit complete (fetch `audit/SKILL.md`)
- [ ] QA checklist passed (fetch `qa/SKILL.md`)
- [ ] OG image and metadata set
- [ ] No secrets in git history
- [ ] Frontend connect button renders, not text

---

## NEVER COMMIT SECRETS

- Private keys → use environment variables
- `.env` → add to `.gitignore`
- `foundry.toml` → don't put private keys here
- Braille characters, invisible text → don't get clever, use `.env`

---

## Skill Routing

| Phase | Skills to Fetch |
|-------|----------------|
| **Planning** | `concepts/SKILL.md`, `why-apertum/SKILL.md` |
| **Contracts** | `security/SKILL.md`, `testing/SKILL.md`, `standards/SKILL.md` |
| **DeFi Integration** | `building-blocks/SKILL.md`, `addresses/SKILL.md` |
| **Frontend** | `frontend-ux/SKILL.md`, `frontend-playbook/SKILL.md` |
| **Indexing** | `indexing/SKILL.md` |
| **QA** | `qa/SKILL.md` |
| **Audit** | `audit/SKILL.md` |
| **Deploy** | `frontend-playbook/SKILL.md`, `orchestration/SKILL.md` |
| **Cross-Chain** | `cross-chain/SKILL.md`, `bridge/SKILL.md` |
