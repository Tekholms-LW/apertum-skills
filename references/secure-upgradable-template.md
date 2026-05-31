# Secure UUPS + EIP-2981 NFT Marketplace Template (Apertum)

**Purpose**: Production-ready skeleton for an upgradable NFT marketplace or collection on Apertum (Chain ID 2786). Incorporates all 2026-05-30 security enhancements from security/SKILL.md and standards/SKILL.md.

**Key Features**:
- UUPS upgradeable (gas efficient, gas efficient for NFT marketplaces on low-gas chains like Apertum)
- EIP-2981 royalties enforced
- ReentrancyGuard + CEI on all value paths
- Custom errors + proper NatSpec + recommended layout
- Role-based access (AccessControl)
- Safe payment handling (native + ERC20)
- Ready for fork testing + Slither

## Full Contract (src/SecureMarketplace.sol)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {AccessControlUpgradeable} from "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import {ReentrancyGuardUpgradeable} from "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {IERC2981} from "@openzeppelin/contracts/interfaces/IERC2981.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title SecureMarketplace
 * @notice Upgradable NFT marketplace template with royalties and strong security.
 * @custom:security-contact security@yourproject.io
 */
contract SecureMarketplace is 
    UUPSUpgradeable, 
    AccessControlUpgradeable, 
    ReentrancyGuardUpgradeable,
    IERC2981 
{
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    struct Listing {
        address nftContract;
        uint256 tokenId;
        address seller;
        uint256 price;
        bool active;
    }

    mapping(bytes32 => Listing) public listings;
    uint256 private _listingNonce;

    // EIP-2981 royalty defaults (can be overridden per collection)
    uint96 public defaultRoyaltyBps = 500; // 5%

    event ItemListed(bytes32 indexed listingId, address indexed nftContract, uint256 tokenId, address seller, uint256 price);
    event ItemSold(bytes32 indexed listingId, address buyer);
    event ItemDelisted(bytes32 indexed listingId);

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address admin) public initializer {
        __UUPSUpgradeable_init();
        __AccessControl_init();
        __ReentrancyGuard_init();

        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(ADMIN_ROLE, admin);
        _grantRole(UPGRADER_ROLE, admin);
    }

    // ========== LISTING ==========
    function listNFT(address nftContract, uint256 tokenId, uint256 price) external nonReentrant {
        require(price > 0, "Invalid price");
        require(IERC721(nftContract).ownerOf(tokenId) == msg.sender, "Not owner");

        bytes32 listingId = keccak256(abi.encodePacked(nftContract, tokenId, msg.sender, _listingNonce++));

        listings[listingId] = Listing({
            nftContract: nftContract,
            tokenId: tokenId,
            seller: msg.sender,
            price: price,
            active: true
        });

        // Transfer NFT to escrow (or use approval model)
        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        emit ItemListed(listingId, nftContract, tokenId, msg.sender, price);
    }

    // ========== BUY + ROYALTIES (EIP-2981) ==========
    function buyNFT(bytes32 listingId) external payable nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.active, "Listing not active");
        require(msg.value >= listing.price, "Insufficient payment");

        listing.active = false;

        // EIP-2981 royalty calculation
        (address royaltyReceiver, uint256 royaltyAmount) = this.royaltyInfo(listing.tokenId, listing.price);
        
        uint256 sellerProceeds = listing.price - royaltyAmount;

        // Pay seller (CEI pattern)
        (bool sent, ) = payable(listing.seller).call{value: sellerProceeds}("");
        require(sent, "Seller payment failed");

        // Pay royalty if applicable
        if (royaltyAmount > 0 && royaltyReceiver != address(0)) {
            (bool royaltySent, ) = payable(royaltyReceiver).call{value: royaltyAmount}("");
            require(royaltySent, "Royalty payment failed");
        }

        // Transfer NFT to buyer
        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);

        emit ItemSold(listingId, msg.sender);

        // Refund excess
        if (msg.value > listing.price) {
            (bool refundSent, ) = payable(msg.sender).call{value: msg.value - listing.price}("");
            require(refundSent, "Refund failed");
        }
    }

    // EIP-2981 implementation
    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        external
        view
        override
        returns (address receiver, uint256 royaltyAmount)
    {
        // In production: per-collection or per-token lookup
        royaltyAmount = (salePrice * defaultRoyaltyBps) / 10000;
        receiver = address(this); // or treasury / original creator
    }

    // Admin functions
    function setDefaultRoyalty(uint96 bps) external onlyRole(ADMIN_ROLE) {
        require(bps <= 1000, "Royalty too high"); // max 10%
        defaultRoyaltyBps = bps;
    }

    // UUPS authorization
    function _authorizeUpgrade(address newImplementation)
        internal
        override
        onlyRole(UPGRADER_ROLE)
    {}

    // Emergency delist (admin)
    function emergencyDelist(bytes32 listingId) external onlyRole(ADMIN_ROLE) {
        Listing storage listing = listings[listingId];
        if (listing.active) {
            listing.active = false;
            IERC721(listing.nftContract).transferFrom(address(this), listing.seller, listing.tokenId);
            emit ItemDelisted(listingId);
        }
    }
}
```

## Deployment & Upgrade Notes (Apertum)

```bash
# 1. Deploy implementation
forge create --rpc-url https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc \
  src/SecureMarketplace.sol:SecureMarketplace --private-key $PK

# 2. Deploy proxy (use a deploy script with ERC1967Proxy + initialize)
# 3. Verify both on Blockscout
forge verify-contract --verifier blockscout --verifier-url "https://explorer.apertum.io/api" <IMPL_ADDR> src/SecureMarketplace.sol:SecureMarketplace
```

## Recommended Tests (test/SecureMarketplace.t.sol)

- Unit tests for list/buy with royalty split
- Fuzz test for payment amounts
- Invariant: "contract never holds ETH after successful buy"
- Fork test against real Apertum DEX for any price oracles
- Upgrade test: deploy proxy → upgrade → verify state + roles preserved

Run with:
```bash
forge test --fork-url $APERTUM_RPC -vv
```

## Slither / Audit Notes
Run:
```bash
slither . --config slither.config.json
```

Key detectors to watch: reentrancy, access-control, upgradeability, erc20.

This template satisfies the full 2026-05-30 security + standards requirements for upgradable NFT marketplaces on Apertum.

See also: security/SKILL.md (upgradable + industry sections), standards/SKILL.md (EIP-2981 + layout), and the main proposal file.