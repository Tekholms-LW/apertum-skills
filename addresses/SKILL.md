---
name: addresses
description: Verified contract addresses for protocols deployed on Apertum (Chain ID 2786). Use this instead of guessing or hallucinating addresses. Includes the native DEX, wrapped tokens, bridge contracts, and infrastructure. Always verify addresses against the explorer before sending transactions.
---

# Contract Addresses on Apertum

> **CRITICAL:** Never hallucinate a contract address. Wrong addresses mean lost funds. If an address isn't listed here, look it up on the explorer at `https://explorer.apertum.io/` or check the protocol's official documentation before using it.

**Network:** Apertum Mainnet (Chain ID 2786)
**Last Verified:** May 18, 2026 (all addresses verified via explorer API)
**Explorer:** https://explorer.apertum.io/

---

## Native Token

| Asset | Symbol | Decimals | Notes |
|-------|--------|----------|-------|
| Apertum | APTM | 18 | Native gas token, no contract address. Use zero address `0x0000000000000000000000000000000000000000` for pair/swap references |

---

## Wrapped Tokens (Bridged Assets)

Tokens bridged from other chains to Apertum. All wrapped tokens are normalized to **18 decimals** on Apertum.

> **Note:** Even USDC/USDT (6 decimals on native chains) use 18 decimals in their Apertum wrapped versions. Always call `.decimals()` to confirm, but these have been verified as 18.

### Core Wrapped Assets

| Token | Symbol | Apertum Address | Origin Chain | Status |
|-------|--------|-----------------|--------------|--------|
| Wrapped Apertum | wAPTM | `0x110Ac02Ba3384Bc055c13A87766049a74517BedA` | Native wrapper | ✅ Verified |
| Apertum wrapped USDC | wUSDC | `0xd979F41E12A69Aa82f04866444Ea91e8e8FaeFd9` | Ethereum/C-Chain | ✅ Verified |
| Apertum wrapped USDT | wUSDT | `0x1487Db421F6B58e77bfefc905fDc1EDE5Fb85C7F` | Ethereum/C-Chain | ✅ Verified |
| Apertum wrapped WETH | wETH | `0x01882C43AA0bEe891b54857c15CC19A3dF946f01` | Ethereum | ✅ Verified |
| Apertum wrapped WBTC | wBTC | `0x75598B9f54Df1472bB2bDC3b5dc791bDb109A52b` | Ethereum | ✅ Verified |
| Apertum wrapped AVAX | wAVAX | `0xf75dD43F59cBa81329F2fA3d98d0C0908CFFeBb8` | Avalanche C-Chain | ✅ Verified |
| Apertum wrapped BNB | wBNB | `0xF3074054737B9E83D73c3c17a007939E12698d5C` | BSC | ✅ Verified |
| Apertum wrapped SOL | wSOL | `0xf081DAa36f367F4A5f93AC68C14FB39b50a58Ef8` | Solana (bridged) | ✅ Verified |
| Wrapped G999 | wG999 | `0x47400a37EB73C786FC92Bac7F9bf046925F4797e` | G999 Chain | ✅ Verified |

---

## Native DEX (Apertum Dex V2)

The Apertum native DEX is a Uniswap V2-style AMM. All core contracts are verified on the explorer.

**DEX UI:** `https://dex.apertum.io/`

### Core Contracts

| Contract | Address | Status |
|----------|---------|--------|
| **DexRouter** | `0x73cf8b5c2F4920967Bd8e9dECDb18F9F1e12A29f` | ✅ Verified |
| **DexFactory** | `0x8bb8aA56642042A8c4dE698E801f2e54Ed5417dc` | ✅ Verified |

### Key LP Pairs (IDEX-V2 LP Tokens)

| Pair | LP Token Address | Status |
|------|-----------------|--------|
| DexPair (generic) | `0x38AcBfA5108D3c76d6cEa4D380182E832A289b57` | ✅ Verified |
| DexPair | `0x40DBAf6C2E9E0a721CF5f01aFb4FdAeacCDcd593` | ✅ Verified |
| DexPair | `0x724843c32F36813C382F7480BC8DB16c4546207e` | ✅ Verified |
| DexPair | `0x51268c6C7Ec5c025e9c2dC87F096C2142f9a5D17` | ✅ Verified |
| DexPair | `0x0c720666d124A28ceA215C197A3aD963F735A7a0` | ✅ Verified |
| DexPair | `0x374b57cbb890847956cC6C4391556Ef00cee9D46` | ✅ Verified |

> **To find a specific pair address:** Call `DexFactory.getPair(tokenA, tokenB)` or use the DEX subgraph at `https://graph.apertum.io/subgraphs/name/dex/dex-subgraph`.

### Standard Uniswap V2 Interface

The DexRouter supports the standard Uniswap V2 interface:

```solidity
// Router
function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts);
function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline) external payable returns (uint[] memory amounts);
function addLiquidity(address tokenA, address tokenB, uint amountADesired, uint amountBDesired, uint amountAMin, uint amountBMin, address to, uint deadline) external returns (uint amountA, uint amountB, uint liquidity);
function removeLiquidity(address tokenA, address tokenB, uint liquidity, uint amountAMin, uint amountBMin, address to, uint deadline) external returns (uint amountA, uint amountB);
function getAmountsOut(uint amountIn, address[] calldata path) external view returns (uint[] memory amounts);
function factory() external view returns (address);
```

```solidity
// Factory
function getPair(address tokenA, address tokenB) external view returns (address pair);
function createPair(address tokenA, address tokenB) external returns (address pair);
```

```solidity
// Pair
function token0() external view returns (address);
function token1() external view returns (address);
function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
```

### Swap Example

```python
from web3 import Web3

ROUTER = "0x73cf8b5c2F4920967Bd8e9dECDb18F9F1e12A29f"
wAPTM = "0x110Ac02Ba3384Bc055c13A87766049a74517BedA"
wUSDC = "0xd979F41E12A69Aa82f04866444Ea91e8e8FaeFd9"

# Get quote: 1 APTM → USDC
router = w3.eth.contract(address=ROUTER, abi=router_abi)
path = [wAPTM, wUSDC]
amounts = router.functions.getAmountsOut(Web3.to_wei(1, "ether"), path).call()
print(f"1 APTM → {amounts[1] / 1e18:.2f} USDC")
```

---

## Other Notable Tokens

Community and ecosystem tokens verified on the explorer:

| Token | Symbol | Address | Status |
|-------|--------|---------|--------|
| ANOUBIS | ANOUBIS | `0x8d38aFbD54020C15F02F7f1F848ec66E17c1004C` | ✅ Verified |
| Sky | SKY | `0x54687168079dd179CEa93C42aFe88650E1D4967c` | ✅ Verified |
| SportsFuture | SFUT | `0xA8532d029320AD0176EfD0959e044aA610A751Ed` | ✅ Verified |
| NoSleepToken | SLEEP | `0xC90C7e7ed44A17258532E1BAcCeE0Ad2468Ea8b5` | ✅ Verified |
| BigPicture | BIG | `0xE6de1535D3E6152c82b065e5Fe734002899CcB4d` | ✅ Verified |
| BabyAnoubis | BabyAnoubis | `0x59E7Af5eA3a7c95B2d3f2dd7bEF7fCB4E0ddD996` | ✅ Verified |
| PUGLORD | PUG | `0xC84B40231E270B827cEb0A27b78AA3fBa443Cf46` | ✅ Verified |
| EROCOIN | ERO | `0x37adB066ac584fE0eb8e1A3b9465935f248C1c3f` | ✅ Verified |
| VITALIUM | VTLM | `0x52071d0fd6DDf9BFDbBC577e693b1AaD9b125914` | ✅ Verified |
| ZOV | ZOV | `0x2836Ef32D7D3AA5723eb76aa6287c26891796038` | ✅ Verified |
| HYPE | HYPE | `0x38b5Bdf80f88cFf43E3Cf0a5902490dc7b35028b` | ✅ Verified |
| AMONRA | AMRA | `0xD08931CFdAeE18847c985Ea3279A85280FA17fEE` | ✅ Verified |
| NEBULA | NEBULA | `0x5D55CcEd452b0090b976789d943Ff0F72f952FE4` | ✅ Verified |
| KINGofMEMES | KINGofMEMES | `0x8C9429093b513da97f5D01CBdDB4F04B913Dc9dE` | ✅ Verified |
| BabyAMONRA | BabyRA | `0x434DBf8A87D37655741138da2431a02e8c1DdBDc` | ✅ Verified |

> **For the complete live token list:** Query `https://explorer.apertum.io/api/v2/tokens?type=ERC-20`

---

## Apertum Bridge — Wallet Addresses

The Apertum bridge at `https://bridge.apertum.io/` uses cross-chain hot/cold wallets to hold and manage bridged assets. These are verified via the [Proof of Assets](https://bridge.apertum.io/en/proof-of-assets) page. All addresses below are EOAs (wallets), not contracts — confirmed on the Apertum explorer.

### Apertum Chain Bridge Wallets

| Role | Address | Status |
|------|---------|--------|
| Bridge Wallet 1 | `0x2dE2D985Ac56e444F79D851aeE1d79b60C49c522` | ✅ EOA, active (928 txns) |
| Bridge Wallet 2 | `0x3EF999E19B44E4c8e9E339B813008C86E514f68c` | ✅ EOA, active (16K+ txns) |
| Bridge Wallet 3 | `0xc6913f979bd2ab0a0eDA33f2271AFc80B765e7d5` | ✅ EOA, active |
| Shared Cold Wallet | `0x9A5e0DAEFed1F88faC890a3bf12d61CCd165114E` | ✅ EOA, cross-chain cold |

### Ethereum Side (ERC-20 Bridge Paths)

| Asset | Hot Wallet | Cold Wallet |
|-------|-----------|-------------|
| USDT (via Apertum Bridge) | `0x25dAa3520c664F2018e8040798A0D6bD34C77969` | `0x9A5e0DAEFed1F88faC890a3bf12d61CCd165114E` |
| USDT (via separate route) | `0x6f2E09A58A9961eD3609578591ED4210fa444f76` | `0x9A5e0DAEFed1F88faC890a3bf12d61CCd165114E` |
| USDT (via separate route) | `0xb0902C722809234B369dA0d7896E07614412f261` | `0x9A5e0DAEFed1F88faC890a3bf12d61CCd165114E` |

### BSC Side

| Asset | Hot Wallet | Cold Wallet |
|-------|-----------|-------------|
| BNB | `0x23aAf7A6933f11252217363FbDebd04c430b8C19` | `0x9A5e0DAEFed1F88faC890a3bf12d61CCd165114E` |
| USDT | `0x7EbaB49a8B7e3eF5d98d9CBA694C3b15C6E57182` | `0x9A5e0DAEFed1F88faC890a3bf12d61CCd165114E` |

### Avalanche C-Chain Side

| Asset | Hot Wallet | Cold Wallet |
|-------|-----------|-------------|
| Core | `0x23aAf7A6933f11252217363FbDebd04c430b8C19` | `0x9A5e0DAEFed1F88faC890a3bf12d61CCd165114E` |
| Alt | `0x3EF999E19B44E4c8e9E339B813008C86E514f68c` | `0x9A5e0DAEFed1F88faC890a3bf12d61CCd165114E` |

### Bridge Paths Supported

| Source Chain → Apertum | Assets |
|------------------------|--------|
| BSC | BNB, USDT |
| Ethereum | USDT |
| Avalanche C-Chain | Core, USDT |
| Solana | SOL (verified) |
| G999 | G999 (verified) |

> **Note:** Bridge addresses are EOAs (wallets), not smart contracts. The actual bridge logic runs offchain through the bridge infrastructure. Verify against `https://bridge.apertum.io/en/proof-of-assets` before transacting.

---

## Multisig (Safe)

Safe contracts are deterministic across EVM chains. Same addresses as everywhere:

| Contract | Address |
|----------|---------|
| Safe Singleton v1.4.1 | `0x41675C099F32341bf84BFc5382aF534df5C7461a` |
| Safe Proxy Factory | `0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67` |
| MultiSend | `0x38869bf66a61cF6bDB996A6aE40D5853Fd43B526` |

Verify deployment on Apertum explorer before use.

---

## Infrastructure

| Service | URL |
|---------|-----|
| Blockscout Explorer | `https://explorer.apertum.io/` |
| Explorer API | `https://explorer.apertum.io/api/v2` |
| DEX | `https://dex.apertum.io/` |
| Bridge | `https://bridge.apertum.io/` |
| Contract Wizard | `https://wizard.apertum.io/` |
| Faucet (Testnet) | `https://faucet.apertum.io/` |
| DEX Subgraph | *Check explorer for subgraph URL* |
| Testnet Explorer | `https://explorer-testnet.apertum.io/` |

---

## How to Verify an Address

**Step 1: Check the explorer**
```
https://explorer.apertum.io/address/0x...
```
Look for:
- ✅ **Verified** badge — source code is available and verified
- Contract tab shows readable Solidity
- Token tab (if applicable) shows token details

**Step 2: Check bytecode exists**
```bash
cast code 0xAddress --rpc-url $APERTUM_RPC
```

**Step 3: Call a known function**
```bash
cast call 0xAddress "symbol()(string)" --rpc-url $APERTUM_RPC
cast call 0xAddress "decimals()(uint8)" --rpc-url $APERTUM_RPC
```

**Step 4: Cross-reference**
- Check the project's official documentation
- Search the explorer for verified contracts
- Check the subgraph for known addresses

---

## Common Token Interfaces

### ERC-20 (Minimal)
```solidity
function name() external view returns (string)
function symbol() external view returns (string)
function decimals() external view returns (uint8)
function totalSupply() external view returns (uint256)
function balanceOf(address) external view returns (uint256)
function transfer(address, uint256) external returns (bool)
function allowance(address, address) external view returns (uint256)
function approve(address, uint256) external returns (bool)
function transferFrom(address, address, uint256) external returns (bool)
```

### ERC-721 (Minimal)
```solidity
function balanceOf(address) external view returns (uint256)
function ownerOf(uint256) external view returns (address)
function tokenURI(uint256) external view returns (string)
function safeTransferFrom(address, address, uint256) external
```

---

## Decimal Reference

| Token | Decimals on Apertum |
|-------|---------------------|
| APTM (native) | 18 |
| wAPTM | 18 |
| wUSDC | 18 |
| wUSDT | 18 |
| wETH | 18 |
| wBTC | 18 |
| wAVAX | 18 |
| wBNB | 18 |
| wSOL | 18 |
| wG999 | 18 |
| All IDEX-V2 LP tokens | 18 |

**Key insight:** All wrapped tokens on Apertum use 18 decimals, regardless of their native chain decimals. This simplifies DeFi math but must be confirmed per token with `.decimals()`.

---

*Addresses verified via `https://explorer.apertum.io/api/v2/tokens?type=ERC-20` and smart contract search on May 18, 2026.*
