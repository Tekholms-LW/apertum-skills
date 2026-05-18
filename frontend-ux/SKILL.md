---
name: frontend-ux
description: Frontend UX rules for Apertum dApps that prevent the most common AI agent UI bugs. Mandatory patterns for onchain buttons, approval flows, address UX, RPC reliability, and pre-publish metadata. Use whenever building a frontend for an Apertum dApp.
---

# Frontend UX Rules for Apertum dApps

## What You Probably Got Wrong

**"The button works."** A clickable button is not enough. It must disable immediately, show a clear pending state, and stay locked until onchain confirmation.

**"Addresses are just strings."** Address UX needs validation, safe formatting, copy support, explorer linking, and name handling.

**"Apertum is fast so I can skip pending states."** Even at 2.8s block times, users need feedback. A button that stays enabled after clicking invites double-submission.

---

## Rule 1: Every Onchain Button Needs Its Own Pending State

Any button that triggers an onchain transaction must:
1. Disable immediately on click
2. Show spinner + action text (`Approving...`, `Staking...`)
3. Stay disabled until chain state confirms completion
4. Show success/error feedback when done

```typescript
const [isApproving, setIsApproving] = useState(false);
const [isStaking, setIsStaking] = useState(false);

<button
  disabled={isApproving}
  onClick={async () => {
    setIsApproving(true);
    try {
      await sendApproveTx();
    } catch (e) {
      notifyError("Approval failed");
    } finally {
      setIsApproving(false); // always release — even on rejection
    }
  }}
>
  {isApproving ? "Approving..." : "Approve"}
</button>
```

Never use one shared `isLoading` for multiple buttons. It causes wrong labels, wrong disabled states.

---

## Rule 2: Four-State Action Flow

Show exactly ONE primary button at a time:

```
1. Not connected  → Connect Wallet
2. Wrong network  → Switch to Apertum
3. Needs approval → Approve
4. Ready          → Execute action
```

Critical details:
- Wrong-network check must happen before approval/action checks
- Never show Approve and Execute simultaneously
- Approval status must come from fresh onchain state
- Connection state must render a clickable button, not passive text

---

## Rule 3: Address UX

```typescript
function formatAddress(address: string): string {
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

function explorerLink(address: string): string {
  return `https://explorer.apertum.io/address/${address}`;
}
```

For addresses, always provide: copy button, explorer link, and truncated display.

---

## Rule 4: USD Context

Show USD values alongside token amounts:

```typescript
function TokenAmount({ amount, token }: { amount: bigint; token: Token }) {
  const usdValue = Number(amount) / 10 ** token.decimals * token.price;
  
  return (
    <span>
      {formatUnits(amount, token.decimals)} {token.symbol}
      <span className="text-gray-400">
        (${usdValue.toFixed(2)})
      </span>
    </span>
  );
}
```

---

## Rule 5: RPC Reliability

Apertum RPC at `https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc`.

Always configure fallbacks:

```typescript
const transports = {
  [apertum.id]: fallback([
    http("https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"),
    http("https://alternative-apertum-rpc.example.com")
  ])
};
```

---

## Rule 6: Error Messages

Parse blockchain errors into human-readable messages:

| Raw Error | User-Friendly |
|-----------|---------------|
| `insufficient funds for gas` | "You need more APTM for gas" |
| `user rejected transaction` | "Transaction cancelled" |
| `execution reverted: ERC20: transfer amount exceeds balance` | "Insufficient balance" |

```typescript
function parseError(error: Error): string {
  const msg = error.message.toLowerCase();
  if (msg.includes("insufficient funds")) return "You need more APTM for gas";
  if (msg.includes("user rejected")) return "Transaction cancelled";
  if (msg.includes("transfer amount exceeds")) return "Insufficient balance";
  return "Transaction failed";
}
```

---

## Rule 7: Chain Switch UX

When user is on wrong network:

```typescript
import { useSwitchChain } from "wagmi";

function SwitchToApertumButton() {
  const { switchChain } = useSwitchChain();
  
  return (
    <button onClick={() => switchChain({ chainId: 2786 })}>
      Switch to Apertum
    </button>
  );
}
```

Never render the main action button when on the wrong network. The button must become the switch CTA.

---

## Checklist

- [ ] Every onchain button has independent pending state
- [ ] Four-state flow (connect → switch → approve → action)
- [ ] Approve and Execute never visible simultaneously
- [ ] Addresses have copy + explorer link
- [ ] Token amounts show USD context
- [ ] RPC has fallback transports
- [ ] Errors are human-readable
- [ ] Wrong network = switch button, not action button
