---
name: orchestration
description: How an AI agent plans, builds, and deploys a complete dApp on Apertum (Chain ID 2786). The three-phase build system. Use when building a full application — from contracts to frontend to production deployment.
---

# dApp Orchestration on Apertum

## The Three-Phase Build System

| Phase | Scope | What Happens |
|-------|-------|-------------|
| **Phase 1** | Contracts | Write, test, audit Solidity. Deploy to Apertum. |
| **Phase 2** | Frontend | Build UI, integrate contracts, test with real wallet. |
| **Phase 3** | Production | Deploy frontend to IPFS/Vercel. Final QA. |

---

## Phase 1: Contracts

### 1.1 Setup

```bash
forge init my-dapp
cd my-dapp
forge install OpenZeppelin/openzeppelin-contracts
```

Configure `foundry.toml` for Apertum:

```toml
[profile.default]
solc_version = "0.8.22"

[rpc_endpoints]
apertum = "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"

[etherscan]
apertum = { key = "verify", url = "https://explorer.apertum.io/api" }
```

### 1.2 Write Contracts

Write contracts in `src/`. Use `addresses/SKILL.md` for external protocol addresses.

### 1.3 Write Tests (≥90% Coverage)

```bash
forge test -vvv
forge coverage
```

Fetch `testing/SKILL.md` and `security/SKILL.md`.

### 1.4 Deploy to Apertum

```bash
forge create \
  --rpc-url apertum \
  --private-key $PRIVATE_KEY \
  src/MyContract.sol:MyContract

# Verify
forge verify-contract \
  --verifier blockscout \
  --verifier-url "https://explorer.apertum.io/api" \
  0xDeployedAddress \
  src/MyContract.sol:MyContract
```

### 1.5 Audit

Fetch `audit/SKILL.md` and run through it.

**Validate:** Deploy succeeds. Explorer shows ✅ Verified. Tests pass. Audit checklist cleared.

---

## Phase 2: Frontend

### 2.1 Setup

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install wagmi viem @tanstack/react-query
```

### 2.2 Configure Apertum Chain

```typescript
import { defineChain } from "viem";

export const apertum = defineChain({
  id: 2786,
  name: "Apertum",
  nativeCurrency: { decimals: 18, name: "Apertum", symbol: "APTM" },
  rpcUrls: {
    default: { http: ["https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"] }
  },
  blockExplorers: {
    default: { name: "Explorer", url: "https://explorer.apertum.io/" }
  }
});
```

### 2.3 Build UI

Fetch `frontend-ux/SKILL.md` for mandatory UX rules:
- Four-state button flow
- Independent pending states per button
- Address UX (copy + explorer link)
- USD context
- Human-readable errors

### 2.4 Integrate Contracts

```typescript
import { useReadContract, useWriteContract } from "wagmi";

// Read
const { data: balance } = useReadContract({
  address: CONTRACT_ADDRESS,
  abi: contractAbi,
  functionName: "balanceOf",
  args: [userAddress]
});

// Write
const { writeContractAsync, isPending } = useWriteContract();
await writeContractAsync({
  address: CONTRACT_ADDRESS,
  abi: contractAbi,
  functionName: "deposit",
  args: [amount]
});
```

**Validate:** Full user journey works with real wallet on Apertum.

---

## Phase 3: Production

### 3.1 Deploy Frontend

```bash
npm run build

# IPFS
# Upload dist/ or out/ directory

# Vercel
vercel --prod
```

### 3.2 Production Checklist

- [ ] Contract verified on Apertum explorer
- [ ] Frontend uses chain ID 2786 (not testnet!)
- [ ] RPC endpoint is production (not testnet)
- [ ] All contract addresses verified
- [ ] OG image and metadata set
- [ ] No private keys in repo
- [ ] `frontend-ux/SKILL.md` rules followed
- [ ] `qa/SKILL.md` checklist passed

---

## 🚨 NEVER COMMIT SECRETS

- Private keys → environment variables
- `.env` → `.gitignore`
- No keys in foundry.toml or hardhat.config.js
