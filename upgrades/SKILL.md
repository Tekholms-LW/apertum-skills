---
name: upgrades
description: OpenZeppelin-style Solidity upgrades and library integration on Apertum (Chain ID 2786). Use for UUPS/Transparent/Beacon proxies, ERC-7201 namespaced storage, Hardhat/Foundry upgrades plugins, OZ install remappings, contracts-cli pattern discovery, and v4→v5 upgrade restrictions. Solidity only.
---

# Upgrades & OpenZeppelin Integration on Apertum

Solidity-only. Prefer OpenZeppelin Contracts over hand-rolled access control, tokens, pause, and reentrancy guards. Deploy and verify against **chainId `2786`**, full RPC path, and Blockscout at `https://explorer.apertum.io`.

This skill is original Apertum pack content (MIT). It summarizes practices aligned with current OpenZeppelin Contracts v5+ tooling — always confirm against **your installed** package version and [docs.openzeppelin.com/contracts](https://docs.openzeppelin.com/contracts).

---

## What You Probably Got Wrong

**"I'll copy Ownable / pause into the contract."** Import and inherit. Pasted library code does not get security patches.

**"`__gap` is enough forever."** Gaps help legacy layouts. New upgradeables should prefer **ERC-7201 namespaced storage** (OZ v5 default).

**"Upgrade the proxy from OZ v4 impl to v5 impl."** **Not supported.** Storage layout models differ (sequential vs namespaced). Redeploy + migrate users.

**"`forge create` the implementation and ship."** Use upgrades plugins so storage layout and initializer rules are validated before mainnet.

---

## Library-first rules (agents)

1. **Search the installed dependency** before writing custom logic: Hardhat → `node_modules/@openzeppelin/contracts/`; Foundry → `lib/openzeppelin-contracts/` (or the upgradeable submodule tree).
2. **Exact match** → import and use. **Close match** → extend only virtual / hook / documented override points.
3. **Never embed** OZ source into the project. Depend on the package so upgrades flow in via version bumps.
4. **Read NatSpec on the installed version.** Hooks change across majors (e.g. ERC-20 transfer customization differed between v4 and v5). Do not assume from memory.
5. Default Apertum stack: Solidity **0.8.24+**, OZ **5.x**, optimizer 200, `cancun` if your OZ/mcopy needs require it.

Related checklists and vuln patterns: `security/SKILL.md`. Token standards: `standards/SKILL.md`.

---

## Project setup (Solidity + OZ)

### Hardhat

```bash
npm install @openzeppelin/contracts
# only if deploying behind proxies:
npm install @openzeppelin/contracts-upgradeable
npm install --save-dev @openzeppelin/hardhat-upgrades @nomicfoundation/hardhat-ethers ethers
```

Register in `hardhat.config`:

```js
require("@openzeppelin/hardhat-upgrades");
// networks.apertum: chainId 2786, full RPC URL from env
```

### Foundry

```bash
forge install OpenZeppelin/openzeppelin-contracts@v5.2.0   # pin a release tag
# upgradeable projects:
forge install OpenZeppelin/openzeppelin-contracts-upgradeable@v5.2.0
forge install OpenZeppelin/openzeppelin-foundry-upgrades
forge install foundry-rs/forge-std
```

Look up current tags on the OZ releases page — always **pin**. Unpinned `forge install` can track an unstable default branch.

### Remappings (upgradeable projects)

For Blockscout / explorer verification, both import roots should come from the **upgradeable** dependency tree (same release), not two unrelated checkouts:

```text
@openzeppelin/contracts/=lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/
@openzeppelin/contracts-upgradeable/=lib/openzeppelin-contracts-upgradeable/contracts/
```

Non-upgradeable only:

```text
@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/
```

### Import conventions

| Kind | Import |
|------|--------|
| Standard (no proxy) | `@openzeppelin/contracts/token/ERC20/ERC20.sol` |
| Upgradeable base | `@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol` |
| Interfaces / libs | usually `@openzeppelin/contracts/...` even in upgradeable apps |

Use upgradeable variants **only** when the contract is deployed behind a proxy.

---

## Proxy patterns (pick deliberately)

| Pattern | Upgrade logic lives in | Best for on Apertum |
|---------|------------------------|---------------------|
| **UUPS** | Implementation (`_authorizeUpgrade`) | Default for most dApps — lighter proxy, lower deploy gas |
| **Transparent** | Separate `ProxyAdmin` | Strict admin vs user call separation |
| **Beacon** | Shared beacon | Many proxies, one shared implementation upgrade |

All use EIP-1967 slots for implementation / admin / beacon.

**Transparent (OZ v5):** the proxy constructor auto-deploys a `ProxyAdmin`; the admin argument is the **owner of that ProxyAdmin**, not an existing ProxyAdmin address (v4 behavior differed).

**Apertum default:** UUPS + multisig/timelock on upgrade auth when value is material. Gas is cheap, but proxy deploy size and upgrade ops still matter for product clarity.

---

## Writing upgradeable contracts

### Initializers, not constructors (for state)

Proxies `delegatecall` the implementation. Constructor runs only for the implementation deployment.

```solidity
import {Initializable} from "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import {ERC20Upgradeable} from "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";

contract MyToken is Initializable, ERC20Upgradeable, OwnableUpgradeable, UUPSUpgradeable {
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers(); // lock implementation against hostile initialize()
    }

    function initialize(address initialOwner) public initializer {
        __ERC20_init("MyToken", "MTK");
        __Ownable_init(initialOwner);
        __UUPSUpgradeable_init();
    }

    function _authorizeUpgrade(address) internal override onlyOwner {}
}
```

Rules:

- Top-level `initialize` uses `initializer`.
- Call each parent `__X_init` explicitly (no constructor-style auto linearization).
- Always `_disableInitializers()` in the implementation constructor.
- Do **not** assign non-constant state in field initializers (`uint256 x = 42`) — that lives in the constructor and will not run for the proxy. `constant` is fine; `immutable` is shared across proxies and often flagged — only allow intentionally.
- V2+ one-time setup: `reinitializer(2)` (not a second `initializer`).

### Storage layout (legacy append rules)

When not using a full namespace isolation story yet:

- Never reorder / remove / change type of existing variables  
- Never insert before existing slots  
- Only append  
- Never change inheritance order of bases that share sequential storage  

Legacy `__gap` arrays still appear in older templates in this pack (`security/SKILL.md`, `references/secure-upgradable-template.md`). Prefer ERC-7201 for **new** bases.

### ERC-7201 namespaced storage (preferred for new code)

Group state in a struct at a deterministic slot so bases can grow without clobbering children:

```solidity
/// @custom:storage-location erc7201:myproject.token.main
struct MainStorage {
    uint256 totalMinted;
    mapping(address => uint256) nonces;
}

// Formula: keccak256(abi.encode(uint256(keccak256(id)) - 1)) & ~bytes32(uint256(0xff))
// Compute the real constant — never leave 0x... placeholders in production code.
bytes32 private constant MAIN_STORAGE_LOCATION = /* computed */;

function _mainStorage() private pure returns (MainStorage storage $) {
    assembly {
        $.slot := MAIN_STORAGE_LOCATION
    }
}
```

Compute location example (Node + ethers):

```bash
node -e "const{keccak256,toUtf8Bytes,zeroPadValue,toBeHex}=require('ethers');const id=process.argv[1];const h=BigInt(keccak256(toUtf8Bytes(id)))-1n;console.log(toBeHex(BigInt(keccak256(zeroPadValue(toBeHex(h),32)))&~0xffn,32))" "myproject.token.main"
```

Rules:

- Unique namespace id per contract in the inheritance graph (collisions = silent corruption).  
- Do not drop a namespace from inheritance on upgrade (orphaned storage). Keep the base even if unused.  
- Adding fields **inside** the namespaced struct is the safe evolution path.

### Unsafe patterns in upgradeables

- No `selfdestruct` on implementation (bricks proxies on many histories; still flagged post-Dencun).  
- No `delegatecall` to untrusted targets.  
- Prefer injecting addresses over `new` child contracts that themselves need upgrade paths.

---

## Hardhat upgrades workflow

```bash
npm install --save-dev @openzeppelin/hardhat-upgrades
```

Typical flow (API names are stable; check installed plugin README for options):

1. `upgrades.deployProxy(factory, args, { kind: "uups" })` — validates, deploys impl + proxy, runs initializer.  
2. `upgrades.upgradeProxy(proxyAddress, newFactory)` — storage-compatible upgrade.  
3. `upgrades.prepareUpgrade(proxy, newFactory)` — deploy new impl only when a multisig/timelock will call `upgradeTo`.  
4. Beacon: `deployBeacon` / `upgradeBeacon` / `deployBeaconProxy` when many clones share one impl.

Plugin state lives under `.openzeppelin/` per network — **commit non-dev network files** so teammates and CI share validation history.

Apertum network config: `chainId: 2786`, RPC = full path  
`https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc` (or `APERTUM_RPC_URL`).

---

## Foundry upgrades workflow

```bash
forge install OpenZeppelin/openzeppelin-foundry-upgrades
```

`foundry.toml` needs validation outputs:

```toml
[profile.default]
ffi = true
ast = true
build_info = true
extra_output = ["storageLayout"]
```

Node.js required — the library shells out to OZ validation tooling.

```solidity
import {Upgrades} from "openzeppelin-foundry-upgrades/Upgrades.sol";

address proxy = Upgrades.deployUUPSProxy(
    "MyToken.sol:MyToken",
    abi.encodeCall(MyToken.initialize, (initialOwner))
);

// Before upgrading: annotate V2 with
// /// @custom:oz-upgrades-from MyToken
Upgrades.upgradeProxy(proxy, "MyTokenV2.sol:MyTokenV2", "");
```

Notes:

- Contracts referenced by **name string**, not factories.  
- No automatic Hardhat-style network manifest — use `@custom:oz-upgrades-from` or `Options.referenceContract`.  
- `UnsafeUpgrades` skips validation — **never** for production scripts.  
- `forge clean` or `--force` before scripts if build info is stale.

---

## OpenZeppelin Contracts major versions (v4 → v5)

**Do not** point an existing proxy at a v5 implementation if the previous implementation was OZ v4.

| | v4 | v5 |
|--|----|----|
| Storage model | Sequential declaration order | ERC-7201 namespaced structs |
| Cross-major proxy upgrade | — | **Unsupported** |

**Do:** new v5 proxies for new products; upgrade **within** the same major using plugins.  
**Don't:** assume mappings can be bulk-migrated (keys are not enumerable).

Updating source to v5 for **new** deploys is encouraged.

---

## contracts-cli (pattern discovery)

Optional reference generator for correct OZ wiring:

```bash
npx @openzeppelin/contracts-cli --help
npx @openzeppelin/contracts-cli solidity-erc20 --help
```

Generate-compare-apply (keeps large dumps out of chat context):

```bash
npx @openzeppelin/contracts-cli solidity-erc20 --name MyToken --symbol MTK > /tmp/oz-base.sol
npx @openzeppelin/contracts-cli solidity-erc20 --name MyToken --symbol MTK --pausable > /tmp/oz-pausable.sol
diff /tmp/oz-base.sol /tmp/oz-pausable.sol
```

Apply the **diff** (imports, inheritance, inits, modifiers) to the user's existing contract — do not replace their product logic wholesale. If no CLI command exists for a type, fall back to reading installed OZ sources and tests under `test/` / `mocks/`.

Wizard UI also available: https://wizard.apertum.io/ (Apertum-branded) and the official OpenZeppelin Wizard.

---

## Handling plugin validation failures

1. **Fix the root cause** (storage order, missing initializer, unsafe opcode).  
2. **Narrow in-source annotations** only when the pattern is truly safe and documented.  
3. **Scoped allow flags** for third-party bases you cannot edit.  
4. **Broad unsafe skip** only as last resort, with a written reason and manual review — you no longer have automated protection.

---

## Upgrade safety checklist (Apertum)

- [ ] Proxy kind chosen deliberately (default UUPS)  
- [ ] `chainId` 2786 and full RPC path in deploy scripts  
- [ ] Implementation constructor calls `_disableInitializers()`  
- [ ] `initialize` / parent `__X_init` correct; V2+ uses `reinitializer` if needed  
- [ ] Storage: ERC-7201 (preferred) or append-only + gaps; no reordering  
- [ ] Unique ERC-7201 namespace ids  
- [ ] UUPS `_authorizeUpgrade` restricted (owner / role / multisig — not open)  
- [ ] Plugin validation green (Hardhat upgrades or Foundry `Upgrades`)  
- [ ] Upgrade path tested: deploy V1 → write state → upgrade V2 → assert state + new logic  
- [ ] Verify **proxy and implementation** on Blockscout (`--verifier blockscout`)  
- [ ] No OZ v4→v5 implementation swap on an existing proxy  
- [ ] Production upgrade key not a single browser hot wallet (`ops/SKILL.md`, `wallets/SKILL.md`)  

---

## Apertum deploy notes

```bash
export APERTUM_RPC_URL="https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"

# After proxy + impl exist:
forge verify-contract --verifier blockscout \
  --verifier-url "https://explorer.apertum.io/api" \
  <ADDRESS> src/MyToken.sol:MyToken
```

Save Standard JSON + constructor/initializer args under `deployments/`. Run a mainnet canary read/write after upgrade (`ops/SKILL.md`).

---

## Related skills

- Vulnerability patterns & CEI: `security/SKILL.md`  
- Marketplace UUPS template (gap-era example): `references/secure-upgradable-template.md`  
- Token standards: `standards/SKILL.md`  
- Ship pipeline: `ship/SKILL.md`  
- Testing / fork: `testing/SKILL.md`  

## External references (do not vendor AGPL skill text)

- https://docs.openzeppelin.com/contracts  
- https://docs.openzeppelin.com/upgrades-plugins  
- https://github.com/OpenZeppelin/openzeppelin-contracts  
- https://github.com/OpenZeppelin/openzeppelin-foundry-upgrades  
- Official agent skills (install separately if desired): https://github.com/OpenZeppelin/openzeppelin-skills  
