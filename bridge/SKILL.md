---
name: bridge
description: How to bridge APTM and other assets to/from Apertum (Chain ID 2786). Bridge contracts, C-Chain paths, third-party bridges, verification. Use when moving assets cross-chain to Apertum.
---

# Bridging to/from Apertum

## Bridge Services

### Apertum Native Bridge

- **URL:** `https://bridge.apertum.io/`
- **Paths:** Avalanche C-Chain ↔ Apertum
- **Assets:** APTM, stablecoins (USDC, USDT), wrapped tokens

### Bridge Flow

```
Source Chain                    Apertum
────────────                    ───────
1. Lock/Deposit tokens
2. Validators attest ───────→   3. Mint wrapped tokens
4. Receive wrapped tokens

Reverse (Apertum → Source):
1. Burn wrapped tokens
2. Validators attest ───────→   3. Unlock/release tokens
4. Receive original tokens
```

---

## How to Bridge

### 1. Using the Bridge UI

1. Go to `https://bridge.apertum.io/`
2. Connect wallet
3. Select source chain (C-Chain)
4. Select destination (Apertum)
5. Choose token and amount
6. Confirm transaction
7. Wait for attestation (~seconds to minutes)
8. Switch to Apertum network
9. Receive wrapped tokens

### 2. Programmatic Bridge

```python
from web3 import Web3

# Bridge contract on C-Chain
c_chain_w3 = Web3(Web3.HTTPProvider("https://api.avax.network/ext/bc/C/rpc"))
bridge_abi = '[...]'  # Bridge contract ABI — verify on explorer
bridge_address = "0x..."  # Verify address

# Deposit USDC on C-Chain to bridge to Apertum
bridge = c_chain_w3.eth.contract(address=bridge_address, abi=bridge_abi)
tx = bridge.functions.deposit(
    usdc_address,  # Token to bridge
    amount,        # Amount
    2786,          # Destination chain ID
    recipient      # Recipient address on Apertum
).build_transaction({
    "from": sender,
    "chainId": 43114  # C-Chain
})
```

### 3. Receiving on Apertum

```python
# On Apertum
apertum_w3 = Web3(Web3.HTTPProvider(APERTUM_RPC))

# Check for received tokens
wrapped_usdc = apertum_w3.eth.contract(address=WRAPPED_USDC_APERTUM, abi=erc20_abi)
balance = wrapped_usdc.functions.balanceOf(recipient).call()
print(f"Received: {balance / 1e6} USDC")
```

---

## Supported Assets (Verify Before Use)

| Asset | C-Chain Address | Apertum Address | Decimals |
|-------|----------------|-----------------|----------|
| APTM | N/A (native) | N/A (native) | 18 |
| USDC | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` | *Verify on explorer* | 6 |
| USDT | `0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7` | *Verify on explorer* | 6 |

> **Always verify addresses** on both explorers before bridging. Wrong addresses = lost funds.

---

## Bridge Security

### Trust Model

The Apertum bridge relies on:
- **Validator attestations** — Apertum validators attest to deposits on the source chain
- **Honest majority** — bridge assumes majority of validators are honest
- **Audit** — bridge contracts should be audited (verify on explorer)

### Risks

- **Validator compromise** — if a supermajority of validators collude
- **Smart contract bugs** — bridge contracts are high-value targets
- **Front-running** — cross-chain messages can be intercepted

### Mitigations

- Bridge only what you need
- Don't hold large amounts in bridge contracts
- Monitor for unusual activity
- Use rate limiting if your protocol bridge large amounts

---

## Common Issues

1. **Wrong destination address.** Bridge tokens go to the wrong address on Apertum. Double-check addresses.

2. **Gas on destination.** You need APTM on Apertum to interact with received tokens.

3. **Decimals.** USDC has 6 decimals on both chains. APTM has 18.

4. **Bridge latency.** Attestation takes time. Plan for minutes, not seconds.

5. **Token not supported.** Not all tokens are bridged. Check the bridge UI for supported assets.

---

## Verification

After bridging, verify:
1. Transaction confirmed on source chain explorer
2. Bridge attestation complete (check bridge UI)
3. Wrapped token balance appears on Apertum explorer
4. Token contract is verified on Apertum explorer
