"""
UFUUMOB_MOBIUS_DEEP_FORMAN.py
Pure Möbius + Random baseline
Forman-Ricci DIRECT on native binary tree
Depths 24, 26, 28, 30 — Option 1 only
"""

import numpy as np
from scipy.stats import linregress, entropy

PHI = (1 + np.sqrt(5)) / 2
np.random.seed(42)
print("Random seed: 42 (fixed for reproducible comparison)\n")

def c_path(i: int, depth: int) -> float:
    """Binary fraction for leaf i"""
    frac = 0.0
    for k in range(depth):
        if (i & (1 << k)):
            frac += 0.5 ** (k + 1)
    return frac

def fold_mobius(a: float, b: float) -> float:
    z = complex(a, b)
    return np.abs((PHI * z + 1) / (z + PHI))

def fold_random(a: float, b: float) -> float:
    return np.random.uniform(0, 1)

def compute_forman_residual(depth: int, fold_func, fold_name: str):
    """Memory-efficient level-by-level computation"""
    n_leaves = 1 << depth
    current = np.array([c_path(i, depth) for i in range(n_leaves)], dtype=np.float64)
    
    total_abs_residual = 0.0
    total_edges = 0
    
    for level in range(1, depth + 1):
        parent_size = len(current) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)
        
        for i in range(parent_size):
            left = current[2 * i]
            right = current[2 * i + 1]
            if fold_name == "Random":
                parent = fold_func(left, right)
            else:
                parent = fold_func(left, right)
            next_level[i] = parent
            
            # Two edges per parent: parent-left and parent-right
            delta_l = abs(parent - left)
            delta_r = abs(parent - right)
            
            # Degrees on tree: parent (internal) deg=3 (except root), child deg=1 if leaf else 3
            # Forman-Ricci = 2 - deg(parent) - deg(child)
            # Internal parent to leaf child: 2 - 3 - 1 = -2
            # Internal parent to internal child: 2 - 3 - 3 = -4
            is_leaf_level = (level == depth)
            r_l = -2 if is_leaf_level else -4
            r_r = -2 if is_leaf_level else -4
            
            total_abs_residual += abs(r_l - 8 * np.pi * delta_l)
            total_abs_residual += abs(r_r - 8 * np.pi * delta_r)
            total_edges += 2
        
        current = next_level
    
    mean_residual = total_abs_residual / total_edges
    return mean_residual

# ====================== MAIN ======================
if __name__ == "__main__":
    depths = [24, 26, 28, 30]
    print("=== PURE MÖBIUS + RANDOM — Forman-Ricci on Native Tree (Deep Test) ===\n")
    print("d     | Fold    | Tree GR residual")
    print("-" * 45)
    
    for d in depths:
        print(f"\nRunning d = {d} (2^{d} leaves)...")
        
        mobius_res = compute_forman_residual(d, fold_mobius, "Möbius")
        random_res = compute_forman_residual(d, fold_random, "Random")
        
        print(f"{d:2d}    | Möbius  | {mobius_res:.6f}")
        print(f"{d:2d}    | Random  | {random_res:.6f}")
        
        if mobius_res < random_res:
            print("   → Möbius beats Random (signal?)")
        else:
            print("   → Random still lower (no signal)")

    print("\n✅ Deep Forman-Ricci test complete.")
    print("   Watch the Möbius residual column.")
    print("   If it stays ~19.56 → structural constant.")
    print("   If it drops toward zero → GR signal emerging.")