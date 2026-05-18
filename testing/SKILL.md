---
name: testing
description: Smart contract testing with Foundry on Apertum. Unit tests, fuzz testing, fork testing against Apertum mainnet state. Use when writing or reviewing tests for Apertum smart contracts.
---

# Smart Contract Testing on Apertum

## What You Probably Got Wrong

**You test getters and trivial functions.** Testing that `name()` returns the name is worthless. Test edge cases, failure modes, and economic invariants — the things that lose money when they break.

**You don't fuzz.** `forge test` finds the bugs you thought of. Fuzzing finds the ones you didn't. If your contract does math, fuzz it. If it handles user input, fuzz it. If it moves value, definitely fuzz it.

**You don't fork-test.** If your contract calls the Apertum DEX or any external protocol (verified addresses: `addresses/SKILL.md`), test against their real deployed contracts on a fork of Apertum. Mocking hides integration bugs.

**You write tests that mirror the implementation.** Testing that `deposit(100)` sets `balance[user] = 100` is tautological — you're testing that Solidity assignments work. Test properties: "after deposit and withdraw, user gets their tokens back." Test invariants: "total deposits always equals contract balance."

---

## Unit Testing with Foundry

### Setup

```bash
forge init my-project
cd my-project
forge install OpenZeppelin/openzeppelin-contracts
```

### Test File Structure

```solidity
// test/MyToken.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Test, console} from "forge-std/Test.sol";
import {MyToken} from "../src/MyToken.sol";

contract MyTokenTest is Test {
    MyToken public token;
    address public alice = makeAddr("alice");
    address public bob = makeAddr("bob");

    function setUp() public {
        token = new MyToken("Test", "TST", 1_000_000e18);
        token.transfer(alice, 10_000e18);
    }

    function test_TransferUpdatesBalances() public {
        vm.prank(alice);
        token.transfer(bob, 1_000e18);

        assertEq(token.balanceOf(alice), 9_000e18);
        assertEq(token.balanceOf(bob), 1_000e18);
    }

    function test_RevertWhen_TransferExceedsBalance() public {
        vm.prank(alice);
        vm.expectRevert();
        token.transfer(bob, 999_999e18);
    }

    function test_RevertWhen_TransferToZeroAddress() public {
        vm.prank(alice);
        vm.expectRevert();
        token.transfer(address(0), 100e18);
    }
}
```

### Run Tests

```bash
forge test                    # All tests
forge test -vvv               # Verbose (show traces on failure)
forge test --match-test test_Transfer  # Specific tests
forge test --gas-report       # Gas usage report
```

---

## Fuzz Testing

Fuzzing throws random inputs at your contract. It finds the edge cases you didn't think of.

```solidity
// test/MyToken.fuzz.t.sol
contract MyTokenFuzzTest is Test {
    MyToken public token;

    function setUp() public {
        token = new MyToken("Test", "TST", 1_000_000e18);
    }

    // Foundry will call this with hundreds of random amounts
    function testFuzz_TransferToSelf(uint256 amount) public {
        // Bound amount to total supply to avoid overflow reverts
        amount = bound(amount, 0, token.totalSupply());
        
        uint256 balanceBefore = token.balanceOf(address(this));
        token.transfer(address(this), amount);
        assertEq(token.balanceOf(address(this)), balanceBefore);
    }

    function testFuzz_DepositWithdraw(uint256 amount) public {
        amount = bound(amount, 1, 1_000_000e18);
        
        // Mint to alice
        address alice = makeAddr("alice");
        token.transfer(alice, amount);
        
        // Alice can always transfer her full balance
        vm.prank(alice);
        token.transfer(address(0xdead), amount);
        assertEq(token.balanceOf(alice), 0);
    }
}
```

```bash
# Fuzz tests with 10,000 runs
forge test --fuzz-runs 10000
```

---

## Fork Testing Against Apertum

Test your contracts against the REAL Apertum state — real DEX, real tokens, real liquidity.

```solidity
// test/MyDapp.fork.t.sol
contract MyDappForkTest is Test {
    using SafeERC20 for IERC20;

    // Apertum token addresses — verify in addresses/SKILL.md
    address constant USDC = 0x...;   // Apertum wrapped USDC
    address constant DEX_ROUTER = 0x...; // Apertum DEX Router

    function setUp() public {
        // Create a fork of Apertum mainnet
        string memory APERTUM_RPC = vm.envString("APERTUM_RPC");
        vm.createSelectFork(APERTUM_RPC);
        
        // Fund our test account with APTM from a whale
        // (find a whale address on the explorer)
        vm.deal(address(this), 100 ether);
    }

    function testFork_SwapOnApertumDEX() public {
        // This runs against the REAL Apertum DEX
        uint256 amountIn = 1 ether; // 1 APTM
        
        address[] memory path = new address[](2);
        path[0] = 0x0000000000000000000000000000000000000000; // APTM
        path[1] = USDC;

        uint256[] memory amounts = IDexRouter(DEX_ROUTER).getAmountsOut(amountIn, path);
        assertGt(amounts[1], 0, "Should get positive USDC for APTM");
    }
}
```

```bash
# Run fork tests against Apertum
APERTUM_RPC="https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc" \
  forge test --match-test testFork_ -vvv
```

---

## Invariant Testing

For stateful protocols with multiple interacting functions:

```solidity
contract VaultInvariantTest is Test {
    Vault public vault;
    
    function setUp() public {
        vault = new Vault();
    }

    // This property must ALWAYS hold, no matter what sequence of calls happens
    function invariant_TotalDepositsMatchesBalance() public {
        assertEq(vault.totalDeposits(), address(vault).balance);
    }
}
```

---

## Assertion Patterns

```solidity
// Equality
assertEq(actual, expected);
assertEq(actual, expected, "description");

// True/False
assertTrue(condition);
assertFalse(condition);

// Greater/Less
assertGt(a, b);
assertGe(a, b);
assertLt(a, b);
assertLe(a, b);

// Revert
vm.expectRevert();              // Any revert
vm.expectRevert("message");     // Specific message
vm.expectRevert(bytes4 error);  // Custom error

// Events
vm.expectEmit(true, true, false, true);
emit Transfer(from, to, amount);
```

---

## Coverage

```bash
forge coverage
forge coverage --report lcov
```

Aim for >90% coverage. The 10% you skip is the 10% attackers exploit.

---

## Apertum-Specific Testing Notes

1. **Fork Apertum, not Ethereum.** When fork-testing, use the Apertum RPC, not an Ethereum RPC. The contracts and state are different.

2. **Gas is ~34 gwei.** Adjust any gas-dependent tests accordingly. Tests that hardcode gas expectations from Ethereum will fail.

3. **Apertum block time is ~2.8s.** Time-dependent tests should account for this. `vm.warp()` and `vm.roll()` work identically.

4. **Test with real Apertum tokens.** Use verified addresses from `addresses/SKILL.md` for integration tests.

5. **Foundry verification uses Blockscout.** Test that your verification command works:
```bash
forge verify-contract --verifier blockscout \
  --verifier-url "https://explorer.apertum.io/api" \
  0xAddress src/Contract.sol:Contract
```
