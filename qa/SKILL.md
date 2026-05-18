---
name: qa
description: Pre-ship audit checklist for Apertum dApps. Wallet flow, four-state buttons, mobile, metadata, trust signals. Give this to a separate reviewer agent (or fresh context) AFTER the build is complete. Use when finalizing an Apertum dApp.
---

# dApp QA — Pre-Ship Audit for Apertum dApps

## 🚨 Critical: Wallet Flow — Button Not Text

Open the app with NO wallet connected.

- ❌ **FAIL:** Text saying "Connect your wallet" as a paragraph
- ✅ **PASS:** A big, obvious Connect Wallet button

---

## 🚨 Critical: Four-State Button Flow

The app must show exactly ONE primary button at a time:

```
1. Not connected  → Connect Wallet button
2. Wrong network  → Switch to Apertum button
3. Needs approval → Approve button
4. Ready          → Action button
```

Check specifically:
- ❌ **FAIL:** Approve and Action buttons both visible
- ❌ **FAIL:** No network check — app fails silently on wrong network
- ❌ **FAIL:** Main action renders instead of "Switch to Apertum" on wrong chain
- ❌ **FAIL:** User can click Approve, sign, then click Approve again while tx pending
- ✅ **PASS:** One button at a time. Each button has spinner + disabled state.

---

## 🚨 Critical: Chain ID

- ❌ **FAIL:** Chain config shows any ID other than 2786
- ❌ **FAIL:** Testnet RPC or addresses in production build
- ✅ **PASS:** Chain ID 2786. Production RPC. Mainnet contract addresses.

---

## Critical: Pending States

Every onchain button must:
1. Disable immediately on click
2. Show spinner + action text
3. Stay disabled until onchain confirmation
4. Show success/error when done

- ❌ **FAIL:** Button re-enables before block confirmation
- ❌ **FAIL:** No visual change after clicking
- ✅ **PASS:** Spinner + disabled + `...ing` text on all onchain buttons

---

## Critical: Error Messages

- ❌ **FAIL:** Raw Solidity errors (`execution reverted: ERC20: transfer amount exceeds balance`)
- ✅ **PASS:** Human-readable errors ("Insufficient balance")

---

## UI & UX

- [ ] Token amounts show decimals correctly (6 for USDC, 18 for APTM)
- [ ] Addresses are truncated with copy + explorer link
- [ ] Explorer links go to `explorer.apertum.io`, not Etherscan
- [ ] Currency shown as APTM, not ETH
- [ ] APTM/USD prices shown where relevant

---

## Metadata

- [ ] `<title>` is custom (not "Vite + React" or template default)
- [ ] Meta description is set
- [ ] Favicon is custom (not Vite default)
- [ ] OG image renders on social preview
- [ ] OG image uses production URL, not localhost

---

## Network & RPC

- [ ] RPC endpoint is production: `https://rpc.apertum.io/ext/bc/.../rpc`
- [ ] Not using default public RPCs (Infura, Alchemy) that don't support Apertum
- [ ] Fallback RPC configured

---

## Responsive & Mobile

- [ ] Layout works at 375px width
- [ ] Buttons are tappable (min 44px height)
- [ ] Text is readable without zooming
- [ ] WalletConnect modal works on mobile

---

## Security

- [ ] No private keys or secrets in source
- [ ] `.env` in `.gitignore`
- [ ] No `console.log` of sensitive data
- [ ] All external contract addresses verified on explorer

---

## Build

- [ ] `npm run build` succeeds with no errors
- [ ] No TypeScript errors
- [ ] No console errors on page load
- [ ] SPA routing works (no 404 on refresh if applicable)

---

## Pass/Fail Summary

| Category | Items | Pass | Fail |
|----------|-------|------|------|
| Wallet Flow | Button vs Text | | |
| Four-State Buttons | One at a time | | |
| Pending States | Spinner + disabled | | |
| Error Messages | Human-readable | | |
| Chain ID | 2786 | | |
| UI/UX | Amounts, addresses, links | | |
| Metadata | Title, OG, favicon | | |
| RPC | Production + fallback | | |
| Security | No secrets | | |
| Build | No errors | | |

**All Critical items must PASS before shipping.**
