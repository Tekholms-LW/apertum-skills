---
name: noir
description: Building privacy-preserving EVM apps on Apertum with Noir. Toolchain, pattern selection, commitment-nullifier flows, Solidity verifiers, and NoirJS. Apertum is fully EVM-compatible — Noir works identically.
---

# Privacy Apps with Noir on Apertum

## What You Probably Got Wrong

**"Use `nargo prove` and `nargo verify`."** Those commands were removed. Nargo only compiles and executes. Proving and verification use `bb` (Barretenberg CLI) directly.

**"I can use SHA256 for hashing in my circuit."** SHA256 costs ~30,000 gates. Poseidon costs ~600. Use `poseidon::poseidon::bn254::hash_2` after adding the dependency.

**"`pub` goes before the parameter name."** Noir 1.0 changed syntax: `merkle_root: pub Field` (NOT `pub merkle_root: Field`).

**"I built a commitment-nullifier circuit so my app is private."** The ZK proof hides the link between commitment and nullifier, but `msg.sender` is public. Use a fresh burner wallet + paymaster.

---

## Toolchain (March 2026)

```bash
# Check if installed
nargo --version && bb --version

# Install nargo
curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash
noirup

# Install bb
curl -L https://raw.githubusercontent.com/AztecProtocol/aztec-packages/master/barretenberg/bbup/install | bash
bbup
```

---

## Quick Reference

- **Solidity verifier = separate deploy** — deploy generated `HonkVerifier.sol`, pass its address to your app contract
- **Input order must match** — circuit `pub` params, `proof.publicInputs`, Solidity `verify()` call
- **Poseidon ≠ Poseidon2** — different algorithms, don't mix them

---

## Apertum Notes

Apertum is fully EVM-compatible. The generated Solidity verifier deploys and works exactly as on Ethereum.

```bash
# Deploy verifier on Apertum
forge create HonkVerifier \
  --rpc-url apertum \
  --private-key $KEY

# Deploy app contract with verifier address
forge create MyPrivacyApp \
  --constructor-args 0xVerifierAddress \
  --rpc-url apertum \
  --private-key $KEY
```

Gas costs on Apertum are minimal — proof verification costs the same gas as Ethereum (~300K-500K gas ≈ $0.003-0.005).
