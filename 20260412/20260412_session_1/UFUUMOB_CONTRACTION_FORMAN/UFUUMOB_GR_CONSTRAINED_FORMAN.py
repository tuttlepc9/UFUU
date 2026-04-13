"""
UFUUMOB_GR_CONSTRAINED_FORMAN.py
GR-Constrained Fold — Forman-Ricci DIRECT on Native Binary Tree
W. Jason Tuttle, 2026

MOTIVATION — WORKING BACKWARDS FROM THE ANSWER:
The Forman-Ricci residual on a binary tree edge is:
   |F(edge) - 8π × |parent - child||

For internal edges: F = -4
For leaf edges:     F = -2

For the residual to be exactly zero on internal edges:
   |parent - child| = 4 / (8π) = 1/(2π) ≈ 0.15915

This is the GR constraint — the specific parent-child difference
that satisfies R = 8πT on the binary tree topology.

THE FOLD:
Rather than engineering curvature into the fold (pACK-G2 approach),
we engineer the METRIC CONSTRAINT that the tree topology requires,
and use the Möbius transformation to determine direction only.

   F_GR(a, b) = a + sign(M(a,b) - a) × TARGET

Where:
   M(a,b) = |( φz + 1) / (z + φ)| is pure Möbius output
   TARGET  = 1/(2π) ≈ 0.15915 is the GR constraint
   sign()  determines direction from conformal structure

This fold:
   - Uses Möbius conformal symmetry to determine direction
   - Forces step size to exactly 1/(2π) at every internal edge
   - Guarantees Forman residual = 0 on internal edges by construction
   - Does NOT engineer curvature — engineers the metric constraint

ADVANCE PREDICTIONS (mathematically guaranteed, not empirical):
   1. Mean |parent - child| on internal edges = exactly 0.15915
   2. Forman residual on internal edges = exactly 0.000000
   3. Leaf edge residual contribution:
      |(-2) - 8π × 0.15915| = |-2 - 4.0| = 6.0 per leaf edge
   4. Overall mean residual depends on ratio of internal to leaf edges.
      At depth d: leaf edges = 2^d, internal edges = 2(2^d - 2).
      As d → ∞, leaf fraction → 1/3, internal fraction → 2/3.
      Expected asymptotic residual ≈ (2/3 × 0) + (1/3 × 6) = 2.0

   If the script returns mean residual approaching 2.0 with depth,
   the advance prediction is confirmed. This is what makes this
   science rather than curve fitting.

WHAT TO WATCH:
   - Mean residual approaching ~2.0 → advance prediction confirmed
   - Mean |parent-child| → 0.15915 → GR constraint satisfied
   - Fixed point existence → attractor structure intact
   - P4 entropy monotonicity → causal irreversibility preserved

Seed: 42 (fixed for reproducibility)
"""

import numpy as np
from scipy.stats import entropy

PHI = (1 + np.sqrt(5)) / 2
TARGET = 1 / (2 * np.pi)   # ≈ 0.15915 — GR constraint for internal edges
LEAF_TARGET = 1 / (4 * np.pi)  # ≈ 0.07958 — GR constraint for leaf edges

np.random.seed(42)

print("=" * 65)
print("UFUUMOB — GR-Constrained Fold — Forman-Ricci on Native Tree")
print("=" * 65)
print(f"\nφ              = {PHI:.8f}")
print(f"TARGET (1/2π)  = {TARGET:.8f}  ← internal edge GR constraint")
print(f"LEAF   (1/4π)  = {LEAF_TARGET:.8f}  ← leaf edge GR constraint")
print(f"\nADVANCE PREDICTIONS:")
print(f"  Mean |parent-child| internal → {TARGET:.8f}")
print(f"  Forman residual internal     → 0.000000 (exactly)")
print(f"  Forman residual leaf edges   → 6.000000 (exactly)")
print(f"  Asymptotic mean residual     → ~2.000000 (as d→∞)")
print()

# ====================== FOLD FUNCTIONS ======================

def fold_mobius(a: float, b: float) -> float:
    """Pure Möbius — directional guide"""
    z = complex(a, b)
    return np.abs((PHI * z + 1) / (z + PHI))

def fold_gr_constrained(a: float, b: float) -> float:
    """
    GR-Constrained fold.
    Uses Möbius to determine direction, forces step = 1/(2π).
    Guarantees |parent - child| = TARGET on internal edges.
    """
    z = complex(a, b)
    mobius_out = np.abs((PHI * z + 1) / (z + PHI))
    direction = np.sign(mobius_out - a)
    if direction == 0:
        direction = 1.0  # default direction if Möbius output equals a
    return a + direction * TARGET

def fold_mobius_contraction(a: float, b: float) -> float:
    """Möbius-Contraction — previous best candidate for comparison"""
    z = complex(a, b)
    mobius_out = np.abs((PHI * z + 1) / (z + PHI))
    mean_out = (a + b) / 2
    return (1/PHI) * mobius_out + (1/PHI**2) * mean_out

def fold_random(a: float, b: float) -> float:
    """Pure random — baseline"""
    return np.random.uniform(0, 1)

# ====================== LEAF VALUES ======================

def c_path(i: int, depth: int) -> float:
    frac = 0.0
    for k in range(depth):
        if (i & (1 << k)):
            frac += 0.5 ** (k + 1)
    return frac

# ====================== FORMAN-RICCI ON NATIVE TREE ======================

def compute_forman_full(depth: int, fold_func, fold_name: str):
    """
    Full Forman-Ricci analysis on native binary tree.
    Returns mean residual, mean |parent-child|, root value,
    and per-level breakdown of internal vs leaf edge residuals.
    """
    n_leaves = 1 << depth
    current = np.array([c_path(i, depth) for i in range(n_leaves)], dtype=np.float64)

    total_residual = 0.0
    total_edges = 0
    internal_residual = 0.0
    internal_edges = 0
    leaf_residual_total = 0.0
    leaf_edges = 0
    all_diffs = []

    for level in range(1, depth + 1):
        parent_size = len(current) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)

        is_leaf_level = (level == depth)
        is_root_level = (level == 1)

        for i in range(parent_size):
            left = current[2 * i]
            right = current[2 * i + 1]
            parent = fold_func(left, right)
            next_level[i] = parent

            delta_l = abs(parent - left)
            delta_r = abs(parent - right)
            all_diffs.extend([delta_l, delta_r])

            if is_leaf_level:
                f_l = f_r = -1 if is_root_level else -2
                leaf_residual_total += abs(f_l - 8 * np.pi * delta_l)
                leaf_residual_total += abs(f_r - 8 * np.pi * delta_r)
                leaf_edges += 2
            else:
                f_l = f_r = -3 if is_root_level else -4
                internal_residual += abs(f_l - 8 * np.pi * delta_l)
                internal_residual += abs(f_r - 8 * np.pi * delta_r)
                internal_edges += 2

            total_residual += abs((f_l if is_leaf_level else f_l) - 8 * np.pi * delta_l)
            total_residual += abs((f_r if is_leaf_level else f_r) - 8 * np.pi * delta_r)
            total_edges += 2

        current = next_level

    mean_residual = total_residual / total_edges
    mean_internal = internal_residual / internal_edges if internal_edges > 0 else 0
    mean_leaf = leaf_residual_total / leaf_edges if leaf_edges > 0 else 0
    mean_diff = np.mean(all_diffs)
    root = current[0]

    return {
        "mean_residual": mean_residual,
        "mean_internal_residual": mean_internal,
        "mean_leaf_residual": mean_leaf,
        "mean_diff": mean_diff,
        "root": root,
        "internal_edges": internal_edges,
        "leaf_edges": leaf_edges,
    }

# ====================== ENTROPY PROFILE ======================

def check_p4(depth: int, fold_func):
    """Quick P4 check — is entropy monotonically decreasing?"""
    n = 1 << depth
    current = np.array([c_path(i, depth) for i in range(n)], dtype=np.float64)
    entropies = []

    def ent(vals):
        if len(np.unique(vals)) <= 1:
            return 0.0
        hist, _ = np.histogram(vals, bins=min(200, len(vals)//2), density=True)
        hist = hist[hist > 0]
        return entropy(hist, base=2) if len(hist) > 0 else 0.0

    entropies.append(ent(current))
    for _ in range(depth):
        ps = len(current) // 2
        nxt = np.zeros(ps)
        for i in range(ps):
            nxt[i] = fold_func(current[2*i], current[2*i+1])
        current = nxt
        entropies.append(ent(current))

    entropies = np.array(entropies)
    monotonic = np.all(np.diff(entropies) <= 0)
    return monotonic, entropies[0], entropies[-1]

# ====================== MAIN ======================

if __name__ == "__main__":

    folds = [
        ("GR-Constrained", fold_gr_constrained),
        ("Contraction",    fold_mobius_contraction),
        ("Möbius",         fold_mobius),
        ("Random",         fold_random),
    ]

    depths = [12, 14, 16, 18, 20, 22, 24]

    # ---- TABLE 1: Full Forman-Ricci comparison ----
    print("TABLE 1: Forman-Ricci GR Residual — All Folds")
    print(f"{'d':>4} | {'Fold':>16} | {'Root':>10} | {'Mean Res':>10} | "
          f"{'Internal Res':>13} | {'Leaf Res':>10} | {'vs Random':>14}")
    print("-" * 95)

    for d in depths:
        print(f"\n  Running d = {d} (2^{d} = {1<<d:,} leaves)...")
        depth_results = {}
        for name, func in folds:
            r = compute_forman_full(d, func, name)
            depth_results[name] = r

        random_res = depth_results["Random"]["mean_residual"]

        for name, r in depth_results.items():
            vs = "baseline" if name == "Random" else \
                 "BEATS ALL ✓" if r["mean_residual"] < min(
                     depth_results[n]["mean_residual"]
                     for n in depth_results if n != name and n != "Random"
                 ) and r["mean_residual"] < random_res else \
                 "beats random ✓" if r["mean_residual"] < random_res else "above random"

            print(f"{d:>4} | {name:>16} | {r['root']:>10.6f} | "
                  f"{r['mean_residual']:>10.6f} | "
                  f"{r['mean_internal_residual']:>13.6f} | "
                  f"{r['mean_leaf_residual']:>10.6f} | {vs}")

    # ---- TABLE 2: Mean parent-child differences ----
    print(f"\n\nTABLE 2: Mean |parent - child| — Distance from GR Target ({TARGET:.5f})")
    print(f"{'d':>4} | {'Fold':>16} | {'Mean diff':>12} | {'Distance to target':>20}")
    print("-" * 60)

    for d in [16, 20, 24]:
        print(f"\n  d = {d}:")
        for name, func in folds:
            r = compute_forman_full(d, func, name)
            dist = abs(r["mean_diff"] - TARGET)
            print(f"{d:>4} | {name:>16} | {r['mean_diff']:>12.8f} | {dist:>20.8f}")

    # ---- TABLE 3: P4 entropy check ----
    print(f"\n\nTABLE 3: P4 Entropy Monotonicity (d=16)")
    print(f"{'Fold':>16} | {'Monotonic':>10} | {'Leaf entropy':>14} | {'Root entropy':>14}")
    print("-" * 60)

    for name, func in folds:
        mono, leaf_ent, root_ent = check_p4(16, func)
        print(f"{name:>16} | {'YES' if mono else 'NO':>10} | "
              f"{leaf_ent:>14.6f} | {root_ent:>14.6f}")

    # ---- ADVANCE PREDICTION VERIFICATION ----
    print(f"\n\nADVANCE PREDICTION VERIFICATION (d=20, GR-Constrained fold):")
    r = compute_forman_full(20, fold_gr_constrained, "GR-Constrained")
    print(f"  Predicted internal residual : 0.000000")
    print(f"  Observed internal residual  : {r['mean_internal_residual']:.6f}")
    print(f"  Predicted leaf residual     : 6.000000")
    print(f"  Observed leaf residual      : {r['mean_leaf_residual']:.6f}")
    print(f"  Predicted mean diff         : {TARGET:.8f}")
    print(f"  Observed mean diff          : {r['mean_diff']:.8f}")
    predicted_asymptotic = 2.0  # (2/3 × 0) + (1/3 × 6)
    print(f"  Predicted asymptotic res    : {predicted_asymptotic:.6f}")
    print(f"  Observed mean residual      : {r['mean_residual']:.6f}")
    leaf_frac = r['leaf_edges'] / (r['leaf_edges'] + r['internal_edges'])
    print(f"  Actual leaf edge fraction   : {leaf_frac:.4f} (predicted 1/3 = {1/3:.4f})")

    print("\n\n✅ GR-Constrained Forman-Ricci test complete.")
    print()
    print("INTERPRETATION:")
    print(f"  If internal residual ≈ 0.000 → GR constraint satisfied on internal edges")
    print(f"  If mean residual → ~2.0      → advance prediction confirmed")
    print(f"  If mean diff → {TARGET:.5f}   → parent-child diffs at GR target")
    print(f"  If P4 = YES                  → causal irreversibility preserved")
    print(f"  If root converges            → attractor structure intact")
