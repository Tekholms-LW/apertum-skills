#!/usr/bin/env python3
"""Structural verification of playbook-derived Apertum skills.

Reads shipped SKILL.md files from the repo root (not hardcoded expected
bodies). Fails if new skills are missing, lack frontmatter, or omit
must-have playbook facts / catalog links.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_SKILLS = ("throughput", "write-pipeline", "optimize", "ops")

MUST_FACTS = {
    "chainId_2786": re.compile(r"\b2786\b"),
    "aptm_18_decimals": re.compile(r"18\s*decimals|decimals:\s*18|decimals:\s*\{\s*[^}]*18", re.I),
    "full_rpc_path": re.compile(
        r"https://rpc\.apertum\.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"
    ),
    "explorer": re.compile(r"https://explorer\.apertum\.io"),
    "block_gas_12m": re.compile(r"12[_,]?000[_,]?000|12M\b"),
    "block_time_2s": re.compile(r"~?2(\.0)?\s*s|2s-class|targetBlockTimeMs:\s*2000", re.I),
}

# At least one skill must document write pipeline pieces
WRITE_MARKERS = {
    "nonce": re.compile(r"nonce\s+(manager|lane)", re.I),
    "presign_raw": re.compile(r"pre-?sign|sendRaw|sendRawTransaction|broadcastTransaction", re.I),
    "batch_abi": re.compile(r"batch|doMany|recordActionBatch", re.I),
    "multi_writer": re.compile(r"multi-?writer|multi-?wallet|multi-?lane", re.I),
}

# Coverage cores mapped across the four skills
COVERAGE = {
    "sec1_constants": ("throughput", re.compile(r"chainId:\s*2786|Chain ID \| `2786`")),
    "sec2_mental_model": ("throughput", re.compile(r"Mental model|what \"fast\" means", re.I)),
    "sec3_baselines": ("throughput", re.compile(r"Measured performance baselines", re.I)),
    "sec4_ceilings": ("throughput", re.compile(r"Theoretical ceilings", re.I)),
    "sec5_greenfield": ("throughput", re.compile(r"Greenfield day-0", re.I)),
    "sec6_brownfield": ("optimize", re.compile(r"Optimization ladder|Brownfield|Is it the chain", re.I)),
    "sec7_writes": ("write-pipeline", re.compile(r"Pre-sign|Nonce manager|three speeds", re.I)),
    "sec9_gas_limits": ("write-pipeline", re.compile(r"gasLimit|Fixed limit|estimateGas", re.I)),
    "sec10_rpc": ("ops", re.compile(r"RPC survival|Writer hardening", re.I)),
    "sec12_contract_design": ("optimize", re.compile(r"Contract design for a fast L1", re.I)),
    "sec14_product_types": ("optimize", re.compile(r"Patterns by product type|NFT marketplace|Agents", re.I)),
    "sec16_canaries": ("ops", re.compile(r"Observability and canaries|watchdog", re.I)),
    "sec17_security_throughput": ("ops", re.compile(r"Security at throughput", re.I)),
    "sec18_checklists": ("ops", re.compile(r"Checklists|New feature \(every PR\)", re.I)),
    "sec19_antipatterns": ("ops", re.compile(r"Anti-patterns", re.I)),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter_ok(text: str) -> tuple[bool, str]:
    if not text.startswith("---"):
        return False, "missing YAML frontmatter start"
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return False, "invalid frontmatter block"
    fm = m.group(1)
    if not re.search(r"^name:\s*\S+", fm, re.M):
        return False, "missing name"
    if not re.search(r"^description:\s*\S+", fm, re.M):
        return False, "missing description"
    return True, "ok"


def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}

    for name in NEW_SKILLS:
        p = ROOT / name / "SKILL.md"
        if not p.is_file() or p.stat().st_size == 0:
            errors.append(f"missing or empty skill: {name}/SKILL.md")
            continue
        text = read(p)
        texts[name] = text
        ok, msg = frontmatter_ok(text)
        if not ok:
            errors.append(f"{name}: frontmatter {msg}")
        # machine-local absolute paths must not appear as required setup
        if re.search(r"/home/sky_ai/", text):
            errors.append(f"{name}: leaked /home/sky_ai/ path")

    # Must-have facts appear across the union of new skills
    corpus = "\n".join(texts.values())
    for key, pat in MUST_FACTS.items():
        if not pat.search(corpus):
            errors.append(f"missing must-have fact in new skills: {key}")

    for key, pat in WRITE_MARKERS.items():
        if not pat.search(texts.get("write-pipeline", "")):
            errors.append(f"write-pipeline missing marker: {key}")

    for key, (skill, pat) in COVERAGE.items():
        body = texts.get(skill, "")
        if not pat.search(body):
            errors.append(f"coverage fail {key}: expected in {skill}/SKILL.md")

    # Catalog links
    for catalog_name in ("SKILL.md", "README.md"):
        cat = read(ROOT / catalog_name)
        for name in NEW_SKILLS:
            if name not in cat and f"{name}/" not in cat:
                errors.append(f"{catalog_name}: does not list skill {name}")
        if "2s-class" not in cat and "2.0" not in cat and "~2s" not in cat:
            # allow calibrated language
            if "2s-class" not in cat:
                errors.append(f"{catalog_name}: expected block-time calibration note (~2s-class)")
        if "upgrades" not in cat:
            errors.append(f"{catalog_name}: does not list skill upgrades")

    # OZ-derived upgrades skill (Solidity-only helpful subset)
    up_path = ROOT / "upgrades" / "SKILL.md"
    if not up_path.is_file() or up_path.stat().st_size == 0:
        errors.append("missing or empty skill: upgrades/SKILL.md")
    else:
        up = read(up_path)
        ok, msg = frontmatter_ok(up)
        if not ok:
            errors.append(f"upgrades: frontmatter {msg}")
        if re.search(r"/home/sky_ai/", up):
            errors.append("upgrades: leaked /home/sky_ai/ path")
        for key, pat in {
            "uups": re.compile(r"\bUUPS\b"),
            "erc7201": re.compile(r"ERC-7201|namespaced storage", re.I),
            "hardhat_plugin": re.compile(r"hardhat-upgrades", re.I),
            "foundry_plugin": re.compile(r"foundry-upgrades|openzeppelin-foundry-upgrades", re.I),
            "v4_v5": re.compile(r"v4.*v5|v4→v5|v4↛v5", re.I),
            "remappings": re.compile(r"remappings", re.I),
            "chain_2786": re.compile(r"\b2786\b"),
        }.items():
            if not pat.search(up):
                errors.append(f"upgrades missing marker: {key}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("PASS")
    print(f"  skills verified: {', '.join(NEW_SKILLS)}")
    print(f"  must-have facts: {', '.join(MUST_FACTS)}")
    print(f"  coverage cores: {len(COVERAGE)}")
    print(f"  catalogs: SKILL.md, README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
