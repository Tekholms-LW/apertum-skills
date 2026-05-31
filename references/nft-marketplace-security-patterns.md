# NFT Marketplace Security Patterns (Apertum / OpenPlaza)

**Context**: Specific security rules for building or auditing NFT marketplaces on Apertum (e.g. projects like OpenPlaza). Specific contract addresses and deployment details for any individual marketplace are deliberately kept local-only and are not present in this public repository.

## Core Principles
- Every value-moving function must use Checks-Effects-Interactions + ReentrancyGuard.
- Prefer EIP-712 signed orders over simple on-chain listings to reduce front-running (2.8s blocks still allow MEV).
- Always enforce or at least surface EIP-2981 royalties.
- Treat approvals as high-risk (setApprovalForAll is especially dangerous).
- Combine contract prevention with Hermes runtime monitoring (transfer chains + DID verification).

## Recommended Patterns

### 1. EIP-712 Signed Listings (Anti Front-Running)
```solidity
// Domain separator + struct for listing intent
struct ListingIntent {
    address nftContract;
    uint256 tokenId;
    uint256 price;
    uint256 nonce;
    uint256 deadline;
}

bytes32 public constant LISTING_TYPEHASH = keccak256("ListingIntent(...)");

function listWithSignature(ListingIntent calldata intent, bytes calldata signature) external {
    // verify signature from seller
    // then proceed with listing
}
```

### 2. Royalty Enforcement on Buy
See the full example in references/secure-upgradable-template.md (royaltyInfo + split payment).

### 3. Batch Operations Safety
- Validate every item in the batch first.
- Update state for the entire batch before any external calls.
- Use ReentrancyGuard on the batch entry point.

### 4. DID / Identity Integration
- Optional hook: before allowing a listing, check if seller holds a valid DID from the known distributor.
- This is best done off-chain in the frontend + runtime scanner (see Hermes openplaza-security-scan) rather than on-chain gas cost.

### 5. Emergency Controls
- Admin-role pausable on the whole marketplace.
- Emergency delist + NFT return function (protected by timelock or multisig in production).

## Common Vulnerabilities in NFT Marketplaces
- Reentrancy during royalty or seller payment distribution.
- Price manipulation via self-list / cancel loops.
- Approval theft (attacker lists using stolen approval).
- Royalty bypass on direct transfers or non-compliant collections.
- Upgrade risk if the proxy admin is not properly protected.

## Integration with Apertum Skills
- Use the UUPS template in references/secure-upgradable-template.md.
- Follow contract layout in standards/SKILL.md.
- Pre-deploy checklist in security/SKILL.md (now includes NFT marketplace row).
- Runtime detection: openplaza-security-scan + apertum-nft-forensics (transfer history, rapid list flags, DID cross-check).

## Testing Recommendations
- Property: "After successful buy, seller receives price - royalty and NFT moves to buyer".
- Fuzz royalty percentages and payment amounts.
- Fork test against real Apertum state (specific marketplace data for validation is kept local-only).

This document + the upgradable template bring any new or upgraded marketplace up to current 2026 standards.