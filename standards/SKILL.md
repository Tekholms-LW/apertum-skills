---
name: standards
description: Token and protocol standards on Apertum (Chain ID 2786). ERC-20, ERC-721, ERC-1155, ERC-4626, EIP-7702. When to use each, how they work, key interfaces. Apertum is fully EVM-compatible — all Ethereum standards apply.
---

# Token & Protocol Standards on Apertum

Apertum is fully EVM-compatible. All Ethereum token standards work identically.

---

## ERC-20 — Fungible Tokens

The standard for currencies, governance tokens, LP tokens, and any fungible asset.

### Minimal Interface

```solidity
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
```

### Usage

```solidity
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("MyToken", "MTK") {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }
}
```

### Apertum Note

APTM is the native token — it's not an ERC-20. To use APTM in DeFi, it's typically wrapped as WAPTM. Check `addresses/SKILL.md` for the WAPTM address.

---

## ERC-721 — Non-Fungible Tokens (NFTs)

The standard for unique assets — art, collectibles, identities, real-world assets.

### Usage

```solidity
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721URIStorage} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract MyNFT is ERC721URIStorage {
    uint256 private _nextTokenId;

    constructor() ERC721("MyNFT", "NFT") {}

    function mint(address to, string memory uri) external returns (uint256) {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }
}
```

---

## ERC-1155 — Multi-Token

One contract for both fungible and non-fungible tokens. Useful for games, membership tiers, and multi-asset platforms.

```solidity
import {ERC1155} from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract MyItems is ERC1155 {
    constructor() ERC1155("https://metadata.example.com/{id}.json") {}
    
    function mint(address to, uint256 id, uint256 amount) external {
        _mint(to, id, amount, "");
    }
}
```

---

## ERC-4626 — Tokenized Vaults

Standard for vaults that take deposits and mint shares. Used for yield-bearing tokens, lending pools, and staking derivatives.

```solidity
import {ERC4626} from "@openzeppelin/contracts/token/ERC20/extensions/ERC4626.sol";

contract MyVault is ERC4626 {
    constructor(IERC20 asset) ERC4626(asset) ERC20("Vault Token", "vTKN") {}
    
    function totalAssets() public view override returns (uint256) {
        return asset.balanceOf(address(this));
    }
}
```

---

## ERC-4337 — Account Abstraction

Standard for smart contract wallets and meta-transactions. EntryPoint v0.7: `0x0000000071727De22E5E9d8BAf0edAc6f37da032`.

Check Apertum deployment before using — not all chains have the canonical EntryPoint deployed.

---

## EIP-7702 — Smart EOAs

Since Ethereum's Pectra upgrade (May 2025), EOAs can delegate execution to smart-contract code. This works on Apertum.

**What it enables:**
- Batch transactions from EOA
- Gas sponsorship
- Session keys
- Eliminate approve + execute pattern

---

## ERC-2612 — Permit (Gasless Approvals)

Allows gasless token approvals via signatures:

```solidity
import {ERC20Permit} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract MyToken is ERC20, ERC20Permit {
    constructor() ERC20("MyToken", "MTK") ERC20Permit("MyToken") {}
}
```

**Why it matters on Apertum:** Even though gas is cheap, permit eliminates an extra transaction for approve + action, improving UX.

---

## EIP-2981 — NFT Royalties (Critical for Marketplaces like OpenPlaza)
```solidity
import {IERC2981} from "@openzeppelin/contracts/interfaces/IERC2981.sol";

contract MyNFT is ERC721, IERC2981 {
    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        external
        view
        override
        returns (address receiver, uint256 royaltyAmount)
    {
        royaltyAmount = (salePrice * 500) / 10_000; // 5%
        receiver = royaltyRecipient; // or ownerOf(tokenId)
    }
}
```
Enforce this in any marketplace buy/fulfill logic. Pitfall: royalties can be bypassed on direct transfers — document clearly and consider hooks.

## Secure ERC-721 & ERC-1155 Extensions
- Recommended secure base: ERC721 + URIStorage + Burnable + Pausable + AccessControl (roles for mint).
- Enumerable: Only for small collections (high gas cost on large sets).
- High-volume minting: Consider ERC721A for batch efficiency — audit the batch mint logic carefully.
- Non-transferable / soulbound (especially for DID/identity tokens): Implement ERC-5192.
- ERC-1155: Add supply tracking, batch burn, pausable, and role-restricted minting.

## Upgradable Token & Protocol Bases
Use the upgradeable equivalents from @openzeppelin/contracts-upgradeable together with the UUPS pattern documented in security/SKILL.md (storage gaps, initializer, _authorizeUpgrade).

## Other Relevant Standards
- ERC-1363: Payable tokens with transfer hooks.
- ERC-777: Token hooks (high reentrancy risk — use only with extreme caution and full guards).
- Permissioned/RWA tokens: Patterns similar to ERC-3643 (transfer restrictions + compliance attestations).

## Recommended Contract Layout & Ordering (2026 Standard)

Follow this exact ordering in every contract for consistency, readability, and easier audits:

1. SPDX + pragma
2. Imports (OZ first, local interfaces, then others)
3. Custom Errors (preferred — gas + better UX than require strings)
4. Events
5. State variables (constants/immutables first, then mappings/storage; always include uint256[50] __gap for upgradeables)
6. Modifiers
7. Constructor or initialize()
8. receive() / fallback()
9. External functions (Admin group → Core writes → Views)
10. Public functions
11. Internal / private helpers last

Example (see security/SKILL.md for the full skeleton with errors/events/state/modifiers).

**Enforcement**: `forge fmt`, solhint (ordering plugin), prettier-plugin-solidity, CI gate.

---

## Quick Reference

| Standard | Purpose | When to Use |
|----------|---------|-------------|
| ERC-20 | Fungible tokens | Currencies, governance, LP tokens |
| ERC-721 | NFTs | Unique assets, identities |
| ERC-1155 | Multi-token | Games, multi-asset platforms |
| ERC-4626 | Tokenized vaults | Yield-bearing, staking |
| ERC-4337 | Account abstraction | Smart wallets, gasless UX |
| EIP-7702 | Smart EOAs | Batching, sponsorship from EOA |
| ERC-2612 | Permit | Gasless approvals |

## Pitfalls

1. **Decimals vary.** USDC = 6, APTM = 18, WBTC = 8. Always call `.decimals()`.
2. **Not all tokens return bool.** Use SafeERC20 (`safeTransfer`, `safeApprove`) for all token interactions.
3. **Infinite approvals are dangerous.** Approve exact amounts or 3-5x, never `type(uint256).max`.
4. **WAPTM ≠ APTM.** APTM is the native currency. WAPTM is an ERC-20 wrapper. They're different for DeFi interactions.

**Post-2026-05-30 update**: This file now includes EIP-2981 (mandatory for NFT marketplaces), full secure extensions for ERC-721/1155, upgradable token bases, and the official contract layout standard used across the entire pack. Cross-reference security/SKILL.md for the matching upgradable + industry patterns and enforcement checklist.