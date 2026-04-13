"""
m6_universality_v2.py
=====================
M6 Universality Test — Corrected Edition

Tests whether the level-2 |parent-child| ≈ 1/(2π) coincidence survives
four different c(path) leaf initializations.

What we're measuring:
  - Mean |parent - child| at EVERY level (not std of values)
  - Corrected Forman-Ricci residual per level
  - Fixed-point convergence (z and gauge channels separately)
  - Which levels hit the GR internal target 1/(2π) ≈ 0.159155

What we're testing:
  - Does the level-2 coincidence survive all four c(path) variants?
  - If yes → the fold produces emergent GR-scale edge weights universally
  - If no  → the leaf initialization is doing physical work (Section 8.4)

Four c(path) variants (per Section 7.1 Step 2):
  1. Original binary fraction
  2. Reversed bit ordering
  3. Gray code
  4. Random permutation (seeded)

Plus two additional variants for robustness:
  5. Random permutation (different seed)
  6. Uniform random (no index structure at all)

W. Jason Tuttle — Recursive Fold Architectures (2026)
"""

import math
import numpy as np
import pandas as pd
from typing import List, Tuple

phi = (1 + math.sqrt(5)) / 2
p = 17
TARGET = 1.0 / (2 * np.pi)  # ≈ 0.159155 — GR internal edge target

# =============================================================================
# FOLDS (exact from paper)
# =============================================================================
def mobius_fold(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Vectorized Möbius conformal fold — Section 4.4"""
    z = left + 1j * right
    return np.abs((phi * z + 1) / (z + phi))

def modular_fold(left_g: np.ndarray, right_g: np.ndarray) -> np.ndarray:
    """Vectorized modular fold — Section 4.2"""
    return (left_g * right_g + left_g + 1) % p

# =============================================================================
# LEAF VARIANTS
# =============================================================================
def leaves_original(d: int) -> Tuple[np.ndarray, np.ndarray]:
    """Original: linear fraction ∈ [0,1) + index mod p"""
    n = 1 << d
    indices = np.arange(n)
    frac = indices / max(n - 1, 1)
    g = indices % p
    return frac.astype(np.float64), g.astype(np.int64)

def leaves_binary_fraction(d: int) -> Tuple[np.ndarray, np.ndarray]:
    """Paper Section 2.2: actual binary fraction c(path) = 0.path"""
    n = 1 << d
    indices = np.arange(n, dtype=np.int64)
    frac = np.zeros(n, dtype=np.float64)
    for k in range(d):
        frac += ((indices >> k) & 1).astype(np.float64) * (0.5 ** (k + 1))
    g = indices % p
    return frac, g

def leaves_reversed_bits(d: int) -> Tuple[np.ndarray, np.ndarray]:
    """Reversed bit ordering of index"""
    n = 1 << d
    indices = np.arange(n)
    rev = np.zeros(n, dtype=np.int64)
    for i in range(n):
        rev[i] = int(bin(i)[2:].zfill(d)[::-1], 2)
    frac = rev / max(n - 1, 1)
    g = rev % p
    return frac.astype(np.float64), g.astype(np.int64)

def leaves_gray_code(d: int) -> Tuple[np.ndarray, np.ndarray]:
    """Gray code ordering"""
    n = 1 << d
    indices = np.arange(n)
    gray = indices ^ (indices >> 1)
    frac = gray / max(n - 1, 1)
    g = gray % p
    return frac.astype(np.float64), g.astype(np.int64)

def leaves_random_perm(d: int, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """Random permutation of indices"""
    n = 1 << d
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    frac = perm / max(n - 1, 1)
    g = perm % p
    return frac.astype(np.float64), g.astype(np.int64)

def leaves_random_perm_alt(d: int) -> Tuple[np.ndarray, np.ndarray]:
    """Random permutation with different seed"""
    return leaves_random_perm(d, seed=137)

def leaves_uniform_random(d: int, seed: int = 99) -> Tuple[np.ndarray, np.ndarray]:
    """Pure uniform random — no index structure at all"""
    n = 1 << d
    rng = np.random.default_rng(seed)
    frac = rng.uniform(0, 1, n)
    g = rng.integers(0, p, n)
    return frac.astype(np.float64), g.astype(np.int64)

# =============================================================================
# FULL LEVEL-BY-LEVEL DIAGNOSTIC
# =============================================================================
def run_diagnostic(depth: int, leaf_func, name: str) -> dict:
    """
    Fold the tree level by level. At each level, record:
      - mean |parent - child| (the actual GR-relevant quantity)
      - corrected Forman-Ricci residual
      - Forman-Ricci target at that level
    """
    z_vals, g_vals = leaf_func(depth)
    
    level_data = []
    
    for level in range(1, depth + 1):
        left_z = z_vals[0::2]
        right_z = z_vals[1::2]
        left_g = g_vals[0::2]
        right_g = g_vals[1::2]
        
        # Apply folds
        parent_z = mobius_fold(left_z, right_z)
        parent_g = modular_fold(left_g, right_g)
        
        # Edge weights: |parent - child| for both children
        delta_left = np.abs(parent_z - left_z)
        delta_right = np.abs(parent_z - right_z)
        all_deltas = np.concatenate([delta_left, delta_right])
        mean_delta = np.mean(all_deltas)
        std_delta = np.std(all_deltas)
        
        # Sibling spread
        lr_diff = np.mean(np.abs(left_z - right_z))
        
        # Corrected Forman-Ricci
        if level == 1:       # children are leaves (degree 1)
            R_forman = -2.0
        elif level == depth:  # parent is root (degree 2)
            R_forman = -3.0
        else:                 # both internal (degree 3)
            R_forman = -4.0
        
        target_delta = abs(R_forman) / (8 * np.pi)
        residual = np.mean(np.abs(R_forman - 8 * np.pi * all_deltas))
        
        # How close is mean_delta to the internal GR target 1/(2π)?
        ratio_to_target = mean_delta / TARGET
        
        level_data.append({
            'level': level,
            'mean_delta': mean_delta,
            'std_delta': std_delta,
            'lr_diff': lr_diff,
            'R_forman': R_forman,
            'target_delta': target_delta,
            'residual': residual,
            'ratio_to_target': ratio_to_target,
            'n_edges': 2 * len(parent_z),
        })
        
        z_vals = parent_z
        g_vals = parent_g
    
    # Fixed-point check
    root_z = float(z_vals[0])
    root_g = int(g_vals[0])
    
    fp_z_test = float(mobius_fold(np.array([root_z]), np.array([root_z]))[0])
    fp_g_test = int(modular_fold(np.array([root_g]), np.array([root_g]))[0])
    fp_err_z = abs(fp_z_test - root_z)
    fp_err_g = abs(fp_g_test - root_g)
    
    return {
        'name': name,
        'root_z': root_z,
        'root_g': root_g,
        'fp_err_z': fp_err_z,
        'fp_err_g': fp_err_g,
        'level_data': level_data,
    }

# =============================================================================
# MAIN
# =============================================================================
def main():
    depth = 16
    
    variants = [
        ("Original (linear fraction)", leaves_original),
        ("Binary fraction (paper 2.2)", leaves_binary_fraction),
        ("Reversed bits",              leaves_reversed_bits),
        ("Gray code",                  leaves_gray_code),
        ("Random perm (seed=42)",      lambda d: leaves_random_perm(d, 42)),
        ("Random perm (seed=137)",     leaves_random_perm_alt),
        ("Uniform random (no index)",  leaves_uniform_random),
    ]
    
    print("=" * 80)
    print("  M6 UNIVERSALITY TEST v2 — |parent-child| Edge Weight Analysis")
    print("  Tuttle 2026 Recursive Fold Architectures")
    print("=" * 80)
    print(f"\n  Depth: {depth}  ({1<<depth:,} leaves)")
    print(f"  GR internal target: 1/(2π) = {TARGET:.6f}")
    print(f"  GR leaf target:     1/(4π) = {1/(4*np.pi):.6f}")
    print(f"  Variants: {len(variants)}\n")
    
    all_results = []
    
    for name, leaf_func in variants:
        print(f"  Running: {name}...", end=" ", flush=True)
        result = run_diagnostic(depth, leaf_func, name)
        all_results.append(result)
        print(f"root_z={result['root_z']:.8f}, g={result['root_g']}, "
              f"fp_err_z={result['fp_err_z']:.2e}")
    
    # ===== LEVEL-BY-LEVEL COMPARISON =====
    print(f"\n{'='*80}")
    print(f"  LEVEL-BY-LEVEL mean |parent-child| — ALL VARIANTS")
    print(f"  (★ marks levels within 5% of GR target {TARGET:.6f})")
    print(f"{'='*80}\n")
    
    # Header
    header = f"{'Level':>5} {'R':>4} {'Target':>8}"
    for r in all_results:
        short = r['name'][:12]
        header += f" | {short:>12}"
    print(header)
    print("-" * len(header))
    
    # Data rows
    for lvl_idx in range(depth):
        level = lvl_idx + 1
        ld0 = all_results[0]['level_data'][lvl_idx]
        row = f"{level:5d} {ld0['R_forman']:4.0f} {ld0['target_delta']:8.6f}"
        
        for r in all_results:
            ld = r['level_data'][lvl_idx]
            md = ld['mean_delta']
            ratio = md / TARGET
            star = "★" if 0.95 <= ratio <= 1.05 else " "
            row += f" | {md:11.6f}{star}"
        
        print(row)
    
    # ===== LEVEL-2 FOCUS =====
    print(f"\n{'='*80}")
    print(f"  LEVEL-2 GR COINCIDENCE — DETAIL")
    print(f"  Target: 1/(2π) = {TARGET:.6f}")
    print(f"{'='*80}\n")
    
    print(f"  {'Variant':<30} {'mean|p-c|':>10} {'ratio':>8} {'within 5%':>10} "
          f"{'within 10%':>11} {'|L-R| at L1':>12}")
    print(f"  {'-'*85}")
    
    l2_ratios = []
    for r in all_results:
        ld2 = r['level_data'][1]  # level 2 (0-indexed)
        ld1 = r['level_data'][0]  # level 1
        md = ld2['mean_delta']
        ratio = md / TARGET
        w5 = "YES" if 0.95 <= ratio <= 1.05 else "no"
        w10 = "YES" if 0.90 <= ratio <= 1.10 else "no"
        l2_ratios.append(ratio)
        
        print(f"  {r['name']:<30} {md:10.6f} {ratio:8.4f} {w5:>10} {w10:>11} "
              f"{ld1['lr_diff']:12.6f}")
    
    # ===== LEVEL-1 (LEAF FOLD) DETAIL =====
    print(f"\n{'='*80}")
    print(f"  LEVEL-1 (LEAF FOLD) — DETAIL")
    print(f"  Target: 1/(4π) = {1/(4*np.pi):.6f}")
    print(f"{'='*80}\n")
    
    print(f"  {'Variant':<30} {'mean|p-c|':>10} {'ratio':>8} {'leaf target':>12}")
    print(f"  {'-'*65}")
    
    leaf_target = 1 / (4 * np.pi)
    for r in all_results:
        ld1 = r['level_data'][0]
        md = ld1['mean_delta']
        ratio = md / leaf_target
        print(f"  {r['name']:<30} {md:10.6f} {ratio:8.4f} {leaf_target:12.6f}")
    
    # ===== FORMAN-RICCI RESIDUAL COMPARISON =====
    print(f"\n{'='*80}")
    print(f"  MEAN FORMAN-RICCI RESIDUAL (lower = closer to R = 8πT)")
    print(f"{'='*80}\n")
    
    print(f"  {'Variant':<30} {'All levels':>10} {'Level 2 only':>12} "
          f"{'Levels 2-5':>10}")
    print(f"  {'-'*65}")
    
    for r in all_results:
        all_resid = np.mean([ld['residual'] for ld in r['level_data']])
        l2_resid = r['level_data'][1]['residual']
        l25_resid = np.mean([r['level_data'][i]['residual'] for i in range(1, min(5, depth))])
        print(f"  {r['name']:<30} {all_resid:10.4f} {l2_resid:12.4f} {l25_resid:10.4f}")
    
    # ===== FIXED-POINT SUMMARY =====
    print(f"\n{'='*80}")
    print(f"  FIXED-POINT CONVERGENCE")
    print(f"{'='*80}\n")
    
    print(f"  {'Variant':<30} {'root_z':>12} {'root_g':>7} {'fp_err_z':>10} "
          f"{'fp_err_g':>10} {'z converged':>12} {'g converged':>12}")
    print(f"  {'-'*95}")
    
    for r in all_results:
        z_conv = "YES" if r['fp_err_z'] < 1e-6 else "no"
        g_conv = "YES" if r['fp_err_g'] == 0 else "no"
        print(f"  {r['name']:<30} {r['root_z']:12.8f} {r['root_g']:7d} "
              f"{r['fp_err_z']:10.2e} {r['fp_err_g']:10d} {z_conv:>12} {g_conv:>12}")
    
    # ===== VERDICT =====
    print(f"\n{'='*80}")
    print(f"  VERDICT")
    print(f"{'='*80}\n")
    
    # Check z convergence universality
    z_values = [r['root_z'] for r in all_results]
    z_spread = max(z_values) - min(z_values)
    z_universal = z_spread < 1e-5
    
    # Check gauge convergence
    g_values = [r['root_g'] for r in all_results]
    g_unique = len(set(g_values))
    g_universal = g_unique == 1
    
    # Check level-2 GR coincidence
    l2_within_5 = sum(1 for ratio in l2_ratios if 0.95 <= ratio <= 1.05)
    l2_within_10 = sum(1 for ratio in l2_ratios if 0.90 <= ratio <= 1.10)
    l2_universal_5 = l2_within_5 == len(l2_ratios)
    l2_universal_10 = l2_within_10 == len(l2_ratios)
    
    print(f"  z-channel fixed point:  {'UNIVERSAL' if z_universal else 'NOT UNIVERSAL'} "
          f"(spread: {z_spread:.2e})")
    print(f"  g-channel attractor:    {'UNIVERSAL' if g_universal else 'NOT UNIVERSAL'} "
          f"({g_unique} distinct values: {sorted(set(g_values))})")
    print(f"  Level-2 |p-c| ≈ 1/(2π): {l2_within_5}/{len(l2_ratios)} within 5%, "
          f"{l2_within_10}/{len(l2_ratios)} within 10%")
    print(f"  Level-2 GR coincidence: {'UNIVERSAL (5%)' if l2_universal_5 else 'UNIVERSAL (10%)' if l2_universal_10 else 'NOT UNIVERSAL'}")
    
    # What IS universal vs what ISN'T
    print(f"\n  UNIVERSAL (invariant under c(path) change):")
    if z_universal:
        print(f"    ✓ z* ≈ {np.mean(z_values):.8f} — Möbius fixed point")
    
    print(f"\n  NOT UNIVERSAL (depends on c(path)):")
    if not g_universal:
        print(f"    ✗ Gauge attractor — landed on {sorted(set(g_values))}")
    if not l2_universal_5:
        print(f"    ? Level-2 GR coincidence — ratios: "
              f"{', '.join(f'{r:.3f}' for r in l2_ratios)}")
    
    print()

if __name__ == "__main__":
    main()
