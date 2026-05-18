---
name: building-blocks
description: DeFi legos and protocol composability on Apertum (Chain ID 2786). The native DEX, token contracts, and how to compose them into new applications. Use when building DeFi integrations or composing existing protocols.
---

# Building Blocks on Apertum

## What You Probably Got Wrong

**"I'll use Uniswap addresses from Ethereum mainnet."** Apertum has its own DEX at `https://dex.apertum.io/`. Ethereum Uniswap addresses won't work. Check `addresses/SKILL.md` for verified Apertum contract addresses.

**"I'll import Uniswap interfaces."** The Apertum DEX may be a fork of Uniswap V2 or PancakeSwap. Same interfaces, different addresses. Always verify.

---

## The Apertum Native DEX

Apertum's native DEX provides:

- **Swap:** Exchange tokens without an orderbook
- **Pool:** Provide liquidity and earn fees
- **LP Tokens:** ERC-20 tokens representing liquidity positions

### DEX Architecture (Likely Uniswap V2 Fork)

Most Avalanche L1 DEXs are Uniswap V2 forks:

```
Factory → Creates trading pairs (token0 + token1 → Pair contract)
Router → Entry point for swaps, add/remove liquidity
Pair → Holds reserves, executes trades, tracks LP tokens
```

### Standard Uniswap V2 Interface

```solidity
// Router interface (verify on Apertum explorer)
interface IApertumRouter {
    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);
    
    function addLiquidity(
        address tokenA,
        address tokenB,
        uint amountADesired,
        uint amountBDesired,
        uint amountAMin,
        uint amountBMin,
        address to,
        uint deadline
    ) external returns (uint amountA, uint amountB, uint liquidity);
    
    function getAmountsOut(
        uint amountIn,
        address[] calldata path
    ) external view returns (uint[] memory amounts);
}

// Pair interface
interface IApertumPair {
    function token0() external view returns (address);
    function token1() external view returns (address);
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
}
```

### Getting A Quote (Offchain)

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(APERTUM_RPC))

router_abi = '[{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"}]'

router = w3.eth.contract(address=ROUTER_ADDRESS, abi=router_abi)

# Get quote for 1 APTM → USDC (verify addresses!)
path = [
    "0x0000000000000000000000000000000000000000",  # APTM (native)
    "0xUSDC_ADDRESS"  # Apertum USDC — verify!
]
amount_in = w3.to_wei(1, "ether")
amounts = router.functions.getAmountsOut(amount_in, path).call()
print(f"1 APTM → {amounts[1] / 1e6:.2f} USDC")
```

---

## Building on the DEX

### Swap Contract

```solidity
contract MySwapper {
    using SafeERC20 for IERC20;
    
    address public constant ROUTER = 0x...; // Verify in addresses/SKILL.md
    
    function swapAPTMforToken(address tokenOut, uint256 amountOutMin) external payable {
        address[] memory path = new address[](2);
        path[0] = 0x0000000000000000000000000000000000000000; // APTM
        path[1] = tokenOut;
        
        IApertumRouter(ROUTER).swapExactETHForTokens{value: msg.value}(
            amountOutMin,
            path,
            msg.sender,
            block.timestamp + 300
        );
    }
    
    function swapTokenForAPTM(address tokenIn, uint256 amountIn, uint256 amountOutMin) external {
        IERC20(tokenIn).safeTransferFrom(msg.sender, address(this), amountIn);
        IERC20(tokenIn).safeApprove(ROUTER, amountIn);
        
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = 0x0000000000000000000000000000000000000000; // APTM
        
        IApertumRouter(ROUTER).swapExactTokensForETH(
            amountIn,
            amountOutMin,
            path,
            msg.sender,
            block.timestamp + 300
        );
    }
}
```

---

## Composability Patterns

### 1. Flash Swap

Borrow tokens from the DEX, use them, repay + fee in the same transaction. No collateral needed.

```solidity
function uniswapV2Call(address sender, uint amount0, uint amount1, bytes calldata data) external {
    // Execute arb/liquidation/refinance here
    // Must repay amount borrowed + 0.3% fee
    uint256 fee = (amount0 * 3) / 997 + 1;
    uint256 amountToRepay = amount0 + fee;
    
    // Return borrowed tokens to pair
    IERC20(token0).safeTransfer(msg.sender, amountToRepay);
}
```

### 2. LP Token as Collateral

LP tokens are ERC-20s. Use them as collateral in lending protocols, stake them for yield, or use them as governance weight.

### 3. TWAP Oracle

The DEX pair tracks cumulative prices, enabling TWAP (Time-Weighted Average Price) oracles:

```solidity
function getTWAP(address pair, uint256 secondsAgo) external view returns (uint256) {
    (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast) = IApertumPair(pair).getReserves();
    // Compute TWAP from reserve snapshots
}
```

---

## Available Tokens (Verify ALL on Explorer)

| Token | Type | Decimals | Status |
|-------|------|----------|--------|
| APTM | Native gas token | 18 | ✅ |
| Apertum Wrapped USDC | Bridged stablecoin | 6 | ⚠️ Verify address |
| Wrapped G999 | Bridged token | * | ⚠️ Verify address |

> **Always verify addresses** at `https://explorer.apertum.io/` before interacting. Token addresses here may change.

---

## Integration Checklist

- [ ] DEX router address verified on explorer
- [ ] Token addresses verified on explorer
- [ ] SafeERC20 used for all token interactions
- [ ] Slippage protection (amountOutMin) on all swaps
- [ ] Deadline set (block.timestamp + 300) on all swaps
- [ ] Reentrancy guard on all swap functions
- [ ] Test first with small amounts
