---
name: frontend-playbook
description: Build-to-production pipeline for Apertum dApps. Setup, IPFS deployment, Vercel config, and the full production checklist. Use when deploying any Apertum dApp to production.
---

# Frontend Playbook for Apertum

## What You Probably Got Wrong

**"I'll use Infinity/Infura RPC."** Those don't support Apertum. Configure the Apertum RPC directly.

**"I'll deploy to IPFS and it'll just work."** Did the CID change? Without `trailingSlash`, routes except `/` return 404.

**"Default Chain ID is fine."** Your deployment must target Chain ID 2786. Not 1 (Ethereum), not 43114 (C-Chain).

---

## Setup

```bash
npm create vite@latest my-apertum-dapp -- --template react-ts
cd my-apertum-dapp
npm install wagmi viem @tanstack/react-query
```

### Apertum Chain Config

```typescript
// src/chains/apertum.ts
import { defineChain } from "viem";

export const apertum = defineChain({
  id: 2786,
  name: "Apertum",
  nativeCurrency: { decimals: 18, name: "Apertum", symbol: "APTM" },
  rpcUrls: {
    default: {
      http: ["https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"]
    }
  },
  blockExplorers: {
    default: { name: "Explorer", url: "https://explorer.apertum.io/" }
  }
});
```

### Wagmi Config

```typescript
// src/wagmi.ts
import { createConfig, http } from "wagmi";
import { apertum } from "./chains/apertum";

export const config = createConfig({
  chains: [apertum],
  transports: {
    [apertum.id]: http()
  }
});
```

---

## Development

```bash
npm run dev
```

Test with MetaMask/RainbowWallet connected to Apertum.

---

## Building for Production

### Environment Variables

```bash
# .env.production
VITE_APERTUM_RPC=https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc
VITE_CHAIN_ID=2786
VITE_PRODUCTION_URL=https://your-app.com
```

### Build

```bash
npm run build
```

---

## Deploying to IPFS

```bash
npm run build
# Upload dist/ (Vite) or out/ (Next.js) to IPFS via:
# - Pinata
# - web3.storage
# - IPFS CLI: ipfs add -r dist/
```

### Critical: SPA Routing on IPFS

IPFS serves static files. For a SPA, all routes must resolve to `index.html`.

**Vite:** Already handles this with hash routing. Use `HashRouter` instead of `BrowserRouter`.

```typescript
import { HashRouter } from "react-router-dom";
// NOT BrowserRouter!
```

**Next.js:** Use `trailingSlash: true` in `next.config.js` for static export.

---

## Deploying to Vercel

```bash
vercel --prod
```

Set environment variables in Vercel dashboard:
- `VITE_APERTUM_RPC`
- `VITE_CHAIN_ID=2786`

---

## Pre-Flight Production Checklist

- [ ] Chain ID set to 2786 (not testnet, not Ethereum)
- [ ] RPC URL is production endpoint
- [ ] Contract addresses are mainnet addresses (not testnet)
- [ ] `VITE_PRODUCTION_URL` set correctly
- [ ] OG image URL uses production URL, not localhost
- [ ] Favicon set (not Vite default)
- [ ] Title and meta description set
- [ ] No console.error on page load
- [ ] Connect Wallet button renders (not text saying "connect")
- [ ] Wrong network → switch button (not silent failure)
- [ ] All external contract addresses verified
- [ ] Build succeeds with no errors
- [ ] SPA routing works (all paths load, not 404)

---

## Post-Deploy Verification

1. Open in an incognito window
2. Connect wallet on Apertum network
3. Go through the full user flow
4. Check the explorer for contract interactions
5. Verify OG metadata renders on social previews

---

## Common Apertum-Specific Pitfalls

1. **Wrong chain ID in build.** Local dev might use Ethereum defaults. Production MUST use 2786.
2. **Testnet addresses in production.** Verify ALL contract addresses are mainnet before deploying.
3. **Missing fallback RPC.** If the Apertum RPC goes down, users can't interact. Configure a fallback.
4. **IPFS routing.** Without hash routing, IPFS pages return 404 on refresh.
5. **APTM vs token labels.** Label native currency as APTM, not ETH, in all UI.
