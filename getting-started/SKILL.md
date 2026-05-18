---
name: getting-started
description: 5-minute Apertum setup — chain config, RPC, faucet, wallet connection, first contract deploy. Fetch this FIRST when building on Apertum. Use when an agent or developer needs to connect to the Apertum blockchain for the first time.
---

# Getting Started on Apertum

## What You Probably Got Wrong

**You tried to connect to Ethereum mainnet.** Apertum is a separate Avalanche L1 (Chain ID 2786). Ethereum RPCs, Etherscan, and Ethereum contract addresses won't work here. Everything has an Apertum equivalent — you just need the right config.

**You used an Ethereum chain config.** Apertum has its own chain ID, RPC endpoint, and block explorer. Update your wallet and your code.

**You didn't know about the faucet.** Apertum has a testnet faucet at `https://faucet.apertum.io/`. Use it for test APT before deploying to mainnet.

---

## Step 1: Add Apertum to Your Wallet

### MetaMask / Rainbow / Rabby

Add a custom network:

| Field | Value |
|-------|-------|
| **Network Name** | Apertum |
| **RPC URL** | `https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc` |
| **Chain ID** | 2786 |
| **Currency Symbol** | APTM |
| **Block Explorer URL** | `https://explorer.apertum.io/` |

---

## Step 2: Get Test APTM (Testnet)

1. Go to `https://faucet.apertum.io/`
2. Connect your wallet (make sure you're on Apertum Testnet)
3. Request test APT

Testnet chain config is the same except chain ID (use the testnet RPC if different).

---

## Step 3: Connect Your Code

### JavaScript / TypeScript (wagmi + viem)

```typescript
import { createPublicClient, createWalletClient, http, custom } from "viem";
import { privateKeyToAccount } from "viem/accounts";

// Apertum chain definition
const apertum = {
  id: 2786,
  name: "Apertum",
  nativeCurrency: { decimals: 18, name: "Apertum", symbol: "APTM" },
  rpcUrls: {
    default: { http: ["https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"] }
  },
  blockExplorers: {
    default: { name: "Apertum Explorer", url: "https://explorer.apertum.io/" }
  }
} as const;

// Public client (reads)
const publicClient = createPublicClient({
  chain: apertum,
  transport: http()
});

// Wallet client (writes)
const account = privateKeyToAccount("0x...");
const walletClient = createWalletClient({
  chain: apertum,
  transport: http(),
  account
});

// Verify connection
const chainId = await publicClient.getChainId();
console.log("Connected to chain:", chainId); // 2786
const block = await publicClient.getBlockNumber();
console.log("Current block:", block);
```

### Python (web3.py)

```python
from web3 import Web3

APERTUM_RPC = "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"
CHAIN_ID = 2786

w3 = Web3(Web3.HTTPProvider(APERTUM_RPC))

# Verify connection
assert w3.is_connected(), "Cannot connect to Apertum RPC"
assert w3.eth.chain_id == CHAIN_ID, f"Wrong chain ID: {w3.eth.chain_id}"

print(f"Connected to Apertum — block {w3.eth.block_number}")

# Check APTM balance
balance = w3.eth.get_balance("0xYourAddress")
print(f"Balance: {w3.from_wei(balance, 'ether')} APTM")
```

### Foundry

```bash
# Set RPC in your shell or .env
export APERTUM_RPC="https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"

# Read from chain
cast block-number --rpc-url $APERTUM_RPC
cast balance 0xYourAddress --rpc-url $APERTUM_RPC

# Deploy
forge create --rpc-url $APERTUM_RPC \
  --private-key $PRIVATE_KEY \
  src/MyContract.sol:MyContract

# Verify on explorer (Blockscout)
forge verify-contract \
  --verifier blockscout \
  --verifier-url "https://explorer.apertum.io/api" \
  0xDeployedAddress \
  src/MyContract.sol:MyContract
```

---

## Step 4: Your First Transaction

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(APERTUM_RPC))

# Send 0.01 APTM
tx = {
    "from": w3.to_checksum_address("0xYourAddress"),
    "to": w3.to_checksum_address("0xRecipientAddress"),
    "value": w3.to_wei(0.01, "ether"),
    "gas": 21000,
    "gasPrice": w3.eth.gas_price,
    "nonce": w3.eth.get_transaction_count("0xYourAddress"),
    "chainId": 2786
}

signed = w3.eth.account.sign_transaction(tx, private_key="0x...")
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"Sent! https://explorer.apertum.io/tx/{tx_hash.hex()}")
```

---

## Step 5: Read a Contract

```python
# USDC on Apertum — always verify address in addresses/SKILL.md
usdc_address = "0x..."  # fetch addresses/SKILL.md for current

abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]'

contract = w3.eth.contract(address=usdc_address, abi=abi)
balance = contract.functions.balanceOf("0xYourAddress").call()
print(f"USDC balance: {w3.from_wei(balance, 'mwei')}")  # USDC uses 6 decimals
```

---

## Common Pitfalls

1. **Wrong chain ID.** If you get `eth_chainId` mismatch errors, check you're using chain ID 2786, not 1 (Ethereum) or 43114 (Avalanche C-Chain).

2. **USDC has 6 decimals, not 18.** USDC, USDT use 6 decimals. APTM uses 18. Always check `decimals()` before doing math.

3. **Blockscout, not Etherscan.** Apertum uses Blockscout. Contract verification uses the Blockscout API. No Etherscan API keys needed.

4. **Gas is ~34 gwei.** Not the sub-gwei gas of post-Fusaka Ethereum mainnet. A transfer costs ~21,000 × 34 gwei = ~0.0007 APTM (< $0.01).

5. **No verified contracts on testnet?** Some testnet contracts may not be verified. Check the testnet explorer.

---

## Next Steps

Now that you're connected:
- **Deploying a dApp?** → `ship/SKILL.md`
- **Need contract addresses?** → `addresses/SKILL.md`
- **Understanding gas costs?** → `gas/SKILL.md`
- **Writing Solidity?** → `security/SKILL.md` + `testing/SKILL.md`
- **Building a frontend?** → `frontend-ux/SKILL.md` + `frontend-playbook/SKILL.md`
