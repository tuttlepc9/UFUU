"""
UFUUMOB_CONTRACTION_FORMAN.py
Möbius-Contraction Fold — Forman-Ricci DIRECT on Native Binary Tree
W. Jason Tuttle, 2026

MOTIVATION:
The pure Möbius fold produces a stable Forman-Ricci residual of
10.375383 across d=24-28, consistently below random (~12.377) but
not converging toward zero. The residual is a structural constant
of the fold, not a depth-dependent signal.

For the residual to converge toward zero, parent-child differences
must converge toward:
   Internal edges: |parent - child| → 1/(2π) ≈ 0.15915
   Leaf edges:     |parent - child| → 1/(4π) ≈ 0.07958

The Möbius-Contraction fold addresses this by adding a contraction
term to the pure Möbius output, using 1/φ as the contraction factor.
This is motivated directly by the SL(2,C) parameterization of the
Möbius fold itself — the same golden ratio that defines the fold
also provides the natural contraction constant.

The fold:
   P = (1/φ) × M(a,b) + (1/φ²) × (a+b)/2

Where M(a,b) = |( φz + 1) / (z + φ)| is the pure Möbius output
and z = a + bi.

The contraction by factor 1/φ < 1 guarantees convergence by the
Banach fixed point theorem. Whether it converges to the GR target
value (1/(2π) for internal edges) is an empirical question that
this script is designed to answer.

CAVEAT:
Mathematical analysis confirms the contraction is real and
convergence is guaranteed. However, the specific value toward
which parent-child differences converge cannot be determined
analytically from first principles without running the numerics.
This script tests whether the contraction lands at the GR target.

WHAT TO WATCH:
   - If Möbius-Contraction residual DECREASES with depth → signal
   - If Möbius-Contraction residual is STABLE (like pure Möbius) → different constant
   - If Möbius-Contraction residual is HIGHER than pure Möbius → contraction fighting fold
   - If Möbius-Contraction beats Random → worth investigating further

Seed: 42 (fixed for reproducibility)
"""

import numpy as np
from scipy.stats import linregress, entropy

PHI = (1 + np.sqrt(5)) / 2
INV_PHI = 1 / PHI        # ≈ 0.61803
INV_PHI2 = 1 / PHI**2   # ≈ 0.38197  (note: 1/φ + 1/φ² = 1, exact)

np.random.seed(42)
print("Random seed: 42 (fixed for reproducible comparison)")
print(f"φ = {PHI:.6f}")
print(f"1/φ = {INV_PHI:.6f}  (contraction factor)")
print(f"1/φ² = {INV_PHI2:.6f}  (mean weight)")
print(f"1/φ + 1/φ² = {INV_PHI + INV_PHI2:.6f}  (should be exactly 1.0)")
print(f"GR target (internal): 1/(2π) = {1/(2*np.pi):.6f}")
print(f"GR target (leaf):     1/(4π) = {1/(4*np.pi):.6f}")
print()

# ====================== FOLD FUNCTIONS ======================

def fold_mobius(a: float, b: float) -> float:
    """Pure Möbius conformal fold — baseline"""
    z = complex(a, b)
    return np.abs((PHI * z + 1) / (z + PHI))

def fold_mobius_contraction(a: float, b: float) -> float:
    """
    Möbius-Contraction fold.
    Mixes pure Möbius output with arithmetic mean,
    weighted by 1/φ and 1/φ² respectively.
    Contraction factor 1/φ < 1 guarantees Banach convergence.
    """
    z = complex(a, b)
    mobius_out = np.abs((PHI * z + 1) / (z + PHI))
    mean_out = (a + b) / 2
    return INV_PHI * mobius_out + INV_PHI2 * mean_out

def fold_random(a: float, b: float) -> float:
    """Pure random fold — baseline (no relationship to inputs)"""
    return np.random.uniform(0, 1)

# ====================== LEAF VALUES ======================

def c_path(i: int, depth: int) -> float:
    """Path-dependent leaf value — binary fraction"""
    frac = 0.0
    for k in range(depth):
        if (i & (1 << k)):
            frac += 0.5 ** (k + 1)
    return frac

# ====================== FORMAN-RICCI ON NATIVE TREE ======================

def compute_forman_residual(depth: int, fold_func, fold_name: str):
    """
    Memory-efficient level-by-level Forman-Ricci computation
    on the native binary tree topology.

    Forman-Ricci curvature on edge (u,v):
       F(u,v) = 2 - deg(u) - deg(v)
    Binary tree degrees:
       Root: deg=2 (two children, no parent)
       Internal: deg=3 (one parent, two children)
       Leaf: deg=1 (one parent only)

    For internal→internal edge: F = 2 - 3 - 3 = -4
    For internal→leaf edge:     F = 2 - 3 - 1 = -2
    For root→internal edge:     F = 2 - 2 - 3 = -3
    For root→leaf edge (d=1):   F = 2 - 2 - 1 = -1

    Energy proxy per edge: |parent_value - child_value|
    GR residual per edge:  |F(edge) - 8π × |parent - child||
    Mean residual over all edges reported.
    """
    n_leaves = 1 << depth
    current = np.array([c_path(i, depth) for i in range(n_leaves)], dtype=np.float64)

    total_abs_residual = 0.0
    total_edges = 0

    for level in range(1, depth + 1):
        parent_size = len(current) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)

        is_leaf_level = (level == depth)
        is_root_level = (level == 1)

        # Track parent-child differences for diagnostics
        diffs = []

        for i in range(parent_size):
            left = current[2 * i]
            right = current[2 * i + 1]
            parent = fold_func(left, right)
            next_level[i] = parent

            delta_l = abs(parent - left)
            delta_r = abs(parent - right)
            diffs.extend([delta_l, delta_r])

            # Forman curvature values
            if is_leaf_level:
                # parent is internal (or root), children are leaves
                if is_root_level:
                    f_l = -1  # root→leaf
                    f_r = -1
                else:
                    f_l = -2  # internal→leaf
                    f_r = -2
            else:
                # parent is internal (or root), children are internal
                if is_root_level:
                    f_l = -3  # root→internal
                    f_r = -3
                else:
                    f_l = -4  # internal→internal
                    f_r = -4

            total_abs_residual += abs(f_l - 8 * np.pi * delta_l)
            total_abs_residual += abs(f_r - 8 * np.pi * delta_r)
            total_edges += 2

        current = next_level

    mean_residual = total_abs_residual / total_edges
    return mean_residual

# ====================== DIAGNOSTIC: MEAN PARENT-CHILD DIFF ======================

def compute_mean_diff(depth: int, fold_func):
    """
    Compute mean |parent - child| across all edges.
    GR target: 1/(2π) ≈ 0.15915 for internal edges.
    Tells us how close the fold gets to the GR target value.
    """
    n_leaves = 1 << depth
    current = np.array([c_path(i, depth) for i in range(n_leaves)], dtype=np.float64)

    all_diffs = []

    for level in range(1, depth + 1):
        parent_size = len(current) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)

        for i in range(parent_size):
            left = current[2 * i]
            right = current[2 * i + 1]
            parent = fold_func(left, right)
            next_level[i] = parent
            all_diffs.append(abs(parent - left))
            all_diffs.append(abs(parent - right))

        current = next_level

    return np.mean(all_diffs), np.std(all_diffs), current[0]

# ====================== MAIN ======================

if __name__ == "__main__":
    depths = [12, 14, 16, 18, 20, 22, 24, 26, 28]

    folds = [
        ("Möbius",      fold_mobius),
        ("Contraction", fold_mobius_contraction),
        ("Random",      fold_random),
    ]

    print("=== MÖBIUS-CONTRACTION FOLD — Forman-Ricci on Native Tree ===\n")

    # ---- TABLE 1: Forman-Ricci residuals ----
    print("TABLE 1: Forman-Ricci GR Residual")
    print(f"{'d':>4} | {'Fold':>12} | {'Root':>10} | {'GR Residual':>14} | {'vs Random':>12}")
    print("-" * 65)

    results = {}
    for d in depths:
        print(f"\n  Running d = {d} (2^{d} = {1<<d:,} leaves)...")
        depth_results = {}
        for name, func in folds:
            res = compute_forman_residual(d, func, name)

            # Get root value
            n = 1 << d
            current = np.array([c_path(i, d) for i in range(n)], dtype=np.float64)
            for _ in range(d):
                ps = len(current) // 2
                nxt = np.zeros(ps)
                for i in range(ps):
                    nxt[i] = func(current[2*i], current[2*i+1])
                current = nxt
            root = current[0]

            depth_results[name] = (res, root)

        random_res = depth_results["Random"][0]
        for name, (res, root) in depth_results.items():
            vs = "BEATS RANDOM ✓" if res < random_res else "above random"
            if name == "Random":
                vs = "(baseline)"
            print(f"{d:>4} | {name:>12} | {root:>10.6f} | {res:>14.6f} | {vs}")

        results[d] = depth_results

    # ---- TABLE 2: Mean parent-child differences ----
    print("\n\nTABLE 2: Mean |parent - child| per fold")
    print(f"GR target (internal edges): {1/(2*np.pi):.6f}")
    print(f"{'d':>4} | {'Fold':>12} | {'Mean diff':>12} | {'Std diff':>12} | {'Distance from GR target':>24}")
    print("-" * 75)

    for d in [16, 20, 24, 28]:
        print(f"\n  d = {d}:")
        for name, func in folds:
            mean_d, std_d, _ = compute_mean_diff(d, func)
            dist = abs(mean_d - 1/(2*np.pi))
            print(f"{d:>4} | {name:>12} | {mean_d:>12.6f} | {std_d:>12.6f} | {dist:>24.6f}")

    print("\n\n✅ Möbius-Contraction Forman-Ricci test complete.")
    print()
    print("INTERPRETATION GUIDE:")
    print("  Residual DECREASING with depth → GR coupling signal emerging")
    print("  Residual STABLE (like pure Möbius) → new structural constant")
    print("  Residual HIGHER than Möbius → contraction fighting the fold")
    print("  Mean diff APPROACHING 0.15915 → parent-child diffs converging to GR target")
    print()
    print("  Pure Möbius baseline residual: ~10.375383 (stable d=24-28)")
    print("  Random baseline residual:       ~12.377    (stable)")
    print("  GR signal would be: residual decreasing below 10.375383 with depth")
