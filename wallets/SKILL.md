---
name: wallets
description: How to create, manage, and use wallets on Apertum (Chain ID 2786). Covers EOAs, smart contract wallets, multisig (Safe), and account abstraction. Includes guardrails for safe key handling.
---

# Wallets on Apertum

## What You Probably Got Wrong

**EIP-7702 is live.** Since Ethereum's Pectra upgrade (May 2025), regular EOAs can delegate execution to smart-contract code. This works on any EVM chain including Apertum. This is NOT "coming soon."

**Account abstraction status:** ERC-4337 is available on all EVM chains. EntryPoint v0.7: `0x0000000071727De22E5E9d8BAf0edAc6f37da032` — check if deployed on Apertum before using.

**Most secure storage:** Hardware wallets alone are single points of failure. An audited multisig smart contract (e.g. Safe) is more secure. Multisig does not require multiple people; one user can control multiple keys on separate devices.

---

## Adding Apertum to Your Wallet

### MetaMask / Rainbow / Rabby

| Field | Value |
|-------|-------|
| **Network Name** | Apertum |
| **RPC URL** | `https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc` |
| **Chain ID** | 2786 |
| **Currency Symbol** | APTM |
| **Block Explorer URL** | `https://explorer.apertum.io/` |

---

## Creating Wallets Programmatically

### JavaScript (viem)

```typescript
import { generatePrivateKey, privateKeyToAccount } from "viem/accounts";

// Generate
const privateKey = generatePrivateKey();
const account = privateKeyToAccount(privateKey);
console.log(account.address);

// From existing key
const account = privateKeyToAccount("0xYourPrivateKey");
```

### Python (web3.py)

```python
from web3 import Web3
from eth_account import Account

# Generate
account = Account.create()
print(account.address, account.key.hex())

# From existing key
account = Account.from_key("0xYourPrivateKey")
```

### CLI (cast)

```bash
# Generate a new wallet
cast wallet new

# Import an existing private key
cast wallet import mykey --private-key 0x...
```

---

## Safe (Multisig) on Apertum

Safe contracts are deterministic across EVM chains:

| Contract | Address |
|----------|---------|
| Safe Singleton v1.4.1 | `0x41675C099F32341bf84BFc5382aF534df5C7461a` |
| Safe Proxy Factory | `0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67` |
| MultiSend | `0x38869bf66a61cF6bDB996A6aE40D5853Fd43B526` |

Verify deployment on Apertum explorer before use. If Safe is deployed, these addresses will work.

**Pattern for AI Agents:** 2-of-3 Safe
- Owner 1: Agent's wallet (hot, automated)
- Owner 2: Human's hot wallet (hot, manual)
- Owner 3: Human's cold wallet (offline, recovery)

The agent can execute transactions independently, but the human can veto or recover.

---

## Key Management Rules

### NEVER:
- Commit private keys to git
- Store keys in `.env` files that get committed
- Generate keys from predictable seeds
- Share keys in chat, logs, or screenshots
- Use a single key for development and production

### ALWAYS:
- Use environment variables for keys
- Add `.env` to `.gitignore`
- Use hardware wallets for production funds
- Use separate keys for dev, testnet, and mainnet
- Audit multisig configurations before funding

### .env Setup

```bash
# .env (add to .gitignore!)
PRIVATE_KEY=0xYourPrivateKey
APERTUM_RPC=https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc
```

```solidity
// foundry.toml
[rpc_endpoints]
apertum = "${APERTUM_RPC}"
```

---

## Sending Transactions

### Transfer APTM

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(APERTUM_RPC))

tx = {
    "from": sender_address,
    "to": recipient_address,
    "value": w3.to_wei(0.01, "ether"),
    "gas": 21000,
    "gasPrice": w3.eth.gas_price,
    "nonce": w3.eth.get_transaction_count(sender_address),
    "chainId": 2786
}

signed = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Confirmed in block {receipt.blockNumber}")
```

### Transfer ERC-20 Token

```python
# Minimal ERC-20 ABI
abi = '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]'

contract = w3.eth.contract(address=token_address, abi=abi)
tx = contract.functions.transfer(recipient, amount).build_transaction({
    "from": sender_address,
    "gas": 100000,
    "gasPrice": w3.eth.gas_price,
    "nonce": w3.eth.get_transaction_count(sender_address),
    "chainId": 2786
})

signed = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
```

---

## Checking Balances

### APTM Balance

```python
balance_wei = w3.eth.get_balance(address)
balance_aptm = w3.from_wei(balance_wei, "ether")
print(f"Balance: {balance_aptm} APTM")
```

```bash
# CLI
cast balance 0xAddress --rpc-url $APERTUM_RPC
```

### Token Balance

```python
abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]'

contract = w3.eth.contract(address=token_address, abi=abi)
balance = contract.functions.balanceOf(address).call()
decimals = contract.functions.decimals().call()
print(f"Balance: {balance / 10**decimals}")
```

---

## EIP-7702: Smart EOAs

Since May 2025, EOAs can delegate execution to smart-contract code. This works on Apertum.

**What this enables:**
- Batch multiple token approvals into one transaction
- Gas sponsorship for EOA users
- Session keys with limited permissions
- Eliminates "approval fatigue" (approve + execute → one step)

**Status (May 2026):** Deployed on Ethereum mainnet. Tooling support is early. For Apertum, check if your wallet supports EIP-7702 transactions on custom chains.

---

## Common Pitfalls

1. **Wrong chain ID.** Sending a tx with chain ID 1 (Ethereum) to Apertum will fail. Always set chain ID 2786.

2. **USDC has 6 decimals.** When transferring USDC, use 1e6 for one USDC, not 1e18.

3. **Nonce issues.** If a tx is pending, the next tx needs the next nonce. Use `get_transaction_count("pending")` to include pending txs.

4. **Gas price too low.** Apertum gas is ~34 gwei. Setting 1 gwei will cause the tx to sit pending.

5. **Checking balance on wrong chain.** Your APTM balance on Apertum is different from your ETH balance on Ethereum, even with the same address.

6. **Never share private keys.** In logs, error messages, or chat. Use `0x...` or addresses.
