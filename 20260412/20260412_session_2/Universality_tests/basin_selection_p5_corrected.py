"""
basin_selection_p5_corrected.py
================================
Corrected P5 basin selection test.

Fixes:
  1. Integer cast bug in get_final_attractor (was producing spurious CYCLE3)
  2. Degenerate variant collapse — 7 of 11 original variants had identical
     g-seeds (all = i % 17). Only variants with genuinely distinct g-seed
     distributions are included.
  3. Adds explicit deduplication check.

W. Jason Tuttle — Recursive Fold Architectures (2026)
"""

import math
import numpy as np
import pandas as pd
from collections import Counter

phi = (1 + math.sqrt(5)) / 2
p = 17

# =============================================================================
# MODULAR FOLD
# =============================================================================
def modular_fold(left_g: int, right_g: int) -> int:
    return int((int(left_g) * int(right_g) + int(left_g) + 1) % p)

# =============================================================================
# ATTRACTOR TRACER — bug-fixed with explicit int casting
# =============================================================================
def get_final_attractor(g_start: int) -> dict:
    x = int(g_start)
    orbit = [x]
    seen = {x: 0}
    for step in range(200):
        x = modular_fold(x, x)   # self-application: g → g²+g+1 mod 17
        if x in seen:
            cycle_start = seen[x]
            cycle = orbit[cycle_start:]
            if len(cycle) == 1:
                return {"label": f"FP{cycle[0]}", "type": "fixed_point", "value": cycle[0]}
            else:
                return {"label": f"CYCLE{len(cycle)}", "type": "cycle", "value": tuple(cycle)}
        seen[x] = len(orbit)
        orbit.append(x)
    return {"label": "UNKNOWN", "type": "unknown", "value": None}

# Sanity check — print full attractor map for verification
print("=== GF(17) Attractor Map Sanity Check ===")
ATTRACTOR_MAP = {}
for g in range(p):
    att = get_final_attractor(g)
    ATTRACTOR_MAP[g] = att
    print(f"  g={g:2d} → {att['label']}")

# Verify no CYCLE3 exists (it cannot under this map)
all_labels = set(v['label'] for v in ATTRACTOR_MAP.values())
print(f"\nDistinct attractor labels found: {sorted(all_labels)}")
assert 'CYCLE3' not in all_labels, "BUG: CYCLE3 should not exist under g→g²+g+1 mod 17"
print("✓ No spurious cycles detected\n")

# =============================================================================
# LEAF VARIANTS — only those with genuinely distinct g-seed distributions
# =============================================================================
def leaves_original(d):
    """g = i mod 17  (linear index)"""
    n = 1 << d
    return np.arange(n, dtype=np.int64) % p

def leaves_reversed_bits(d):
    """g = bit-reverse(i) mod 17  — distinct permutation"""
    n = 1 << d
    rev = np.zeros(n, dtype=np.int64)
    for i in range(n):
        rev[i] = int(bin(i)[2:].zfill(d)[::-1], 2)
    return rev % p

def leaves_gray_code(d):
    """g = gray(i) mod 17  — distinct permutation"""
    n = 1 << d
    idx = np.arange(n, dtype=np.int64)
    gray = idx ^ (idx >> 1)
    return gray % p

def leaves_random_perm(d, seed=42):
    """g = random_perm(i) mod 17  — seed-controlled permutation"""
    n = 1 << d
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    return (perm % p).astype(np.int64)

def leaves_uniform_random(d, seed=99):
    """g = uniform random in [0,16]  — not derived from index permutation"""
    n = 1 << d
    rng = np.random.default_rng(seed)
    return rng.integers(0, p, n, dtype=np.int64)

def leaves_uniform_random_2(d, seed=777):
    """g = uniform random, different seed"""
    n = 1 << d
    rng = np.random.default_rng(seed)
    return rng.integers(0, p, n, dtype=np.int64)

def leaves_constant_g(d, g_val=0):
    """All leaves same g-value — extreme test"""
    n = 1 << d
    return np.full(n, g_val, dtype=np.int64)

def leaves_alternating_fg(d):
    """Alternating FP-basin seeds: 4, 13, 4, 13, ..."""
    n = 1 << d
    vals = np.zeros(n, dtype=np.int64)
    vals[0::2] = 4
    vals[1::2] = 13
    return vals

def leaves_cycle_seeded(d):
    """Seeds from the {6,9} cycle basin only: alternating 6,9"""
    n = 1 << d
    vals = np.zeros(n, dtype=np.int64)
    vals[0::2] = 6
    vals[1::2] = 9
    return vals

# =============================================================================
# DEDUPLICATION CHECK
# =============================================================================
def fingerprint(leaf_func, d=8):
    """First 17 g-values as tuple — fast identity check"""
    return tuple(leaf_func(d)[:17].tolist())

variants = [
    ("Original (i mod 17)",          leaves_original),
    ("Reversed bits",                 leaves_reversed_bits),
    ("Gray code",                     leaves_gray_code),
    ("Random perm (seed=42)",         lambda d: leaves_random_perm(d, 42)),
    ("Random perm (seed=137)",        lambda d: leaves_random_perm(d, 137)),
    ("Uniform random (seed=99)",      leaves_uniform_random),
    ("Uniform random (seed=777)",     leaves_uniform_random_2),
    ("Constant g=0",                  lambda d: leaves_constant_g(d, 0)),
    ("Alternating FP seeds (4,13)",   leaves_alternating_fg),
    ("Cycle seeds (6,9)",             leaves_cycle_seeded),
]

print("=== Deduplication Check ===")
seen_fps = {}
deduped = []
for name, func in variants:
    fp = fingerprint(func)
    if fp in seen_fps:
        print(f"  SKIP (duplicate of '{seen_fps[fp]}'): {name}")
    else:
        seen_fps[fp] = name
        deduped.append((name, func))
        print(f"  KEEP: {name}")

print(f"\n{len(deduped)} distinct variants proceeding to test.\n")

# =============================================================================
# TREE FOLD — gauge channel only
# =============================================================================
def fold_gauge_root(depth: int, leaf_func) -> int:
    g_vals = leaf_func(depth).astype(np.int64)
    for _ in range(depth):
        left = g_vals[0::2]
        right = g_vals[1::2]
        g_vals = np.array([modular_fold(int(l), int(r)) for l, r in zip(left, right)],
                          dtype=np.int64)
    return int(g_vals[0])

# =============================================================================
# MAIN P5 TEST
# =============================================================================
def run_p5_test(depth: int = 18):
    print(f"=== Tuttle 2026 — Basin Selection Map P5 (depth={depth}) ===\n")
    
    results = []
    attractor_counts = Counter()
    
    for name, leaf_func in deduped:
        g_root = fold_gauge_root(depth, leaf_func)
        attractor = ATTRACTOR_MAP[g_root]
        
        results.append({
            "Leaf Variant":        name,
            "Root_g":              g_root,
            "Attractor":           attractor['label'],
            "Type":                attractor['type'],
        })
        attractor_counts[attractor['label']] += 1
        print(f"  {name:<35} root_g={g_root:>2}  →  {attractor['label']}")
    
    df = pd.DataFrame(results)
    
    print(f"\n{'='*70}")
    print("BASIN-SELECTION SUMMARY (P5)")
    print(f"{'='*70}")
    for att, count in sorted(attractor_counts.items()):
        pct = 100 * count / len(deduped)
        print(f"  {att:>12} : {count:2d} / {len(deduped)} variants  ({pct:.0f}%)")
    
    print(f"\nNote: P5 claim requires showing that distinct c(path) distributions")
    print(f"produce distinct vacuum selections — not just that diversity exists.")
    
    fp_total = sum(v for k, v in attractor_counts.items() if k.startswith('FP'))
    cycle_total = sum(v for k, v in attractor_counts.items() if k.startswith('CYCLE'))
    
    if fp_total > 0 and cycle_total > 0:
        print(f"\n✓ Both fixed-point and cycle attractors observed — vacuum landscape is non-trivial.")
    if 'FP4' in attractor_counts and 'FP13' in attractor_counts:
        print(f"✓ Both fixed points selected by distinct inputs — binary vacuum confirmed.")
    
    return df

if __name__ == "__main__":
    df = run_p5_test(depth=18)
    print(f"\n{df.to_string(index=False)}")
