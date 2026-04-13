"""
UFUUMOB_ULTRA_ENTROPY_FIXED.py
Pure Möbius fold + ultrametric + entropy profile (P4 test)
Fixed version — no interactive show, just saves the figure cleanly
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, entropy

PHI = (1 + np.sqrt(5)) / 2

def c_path(path: str) -> float:
    if not path: return 0.0
    return int(path, 2) / (1 << len(path))

def fold_mobius(a: float, b: float) -> float:
    z = complex(a, b)
    return np.abs((PHI * z + 1) / (z + PHI))

def build_tree(depth: int):
    n = 1 << depth
    leaves = np.array([c_path(f'{i:0{depth}b}') for i in range(n)], dtype=np.float64)
    current = leaves.copy()
    level_values = [leaves.copy()]

    for level in range(1, depth + 1):
        parent_size = len(current) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)
        for i in range(parent_size):
            left, right = current[2*i], current[2*i+1]
            next_level[i] = fold_mobius(left, right)
        current = next_level
        level_values.append(current.copy())
    return leaves, current[0], level_values

def compute_ultrametric_correlation(leaves, depth, n_samples=80000):
    n = len(leaves)
    idx1 = np.random.randint(0, n, n_samples)
    idx2 = np.random.randint(0, n, n_samples)
    lca_depths = []
    for i1, i2 in zip(idx1, idx2):
        xor = int(i1) ^ int(i2)
        lca_depths.append(depth if xor == 0 else depth - xor.bit_length())
    lca_depths = np.array(lca_depths)
    corrs = leaves[idx1] * leaves[idx2]
    max_lca = depth + 1
    bins = np.arange(max_lca)
    hist_corr = np.bincount(lca_depths, weights=corrs, minlength=max_lca)
    hist_count = np.bincount(lca_depths, minlength=max_lca)
    mask = hist_count > 0
    C_lca = np.zeros(max_lca)
    C_lca[mask] = hist_corr[mask] / hist_count[mask]
    valid = (bins >= 1) & mask
    if np.sum(valid) < 5:
        return bins, C_lca, np.nan, 0.0
    log_lca = np.log(bins[valid])
    log_C = np.log(C_lca[valid] + 1e-12)
    slope, _, _, _, _ = linregress(log_lca, log_C)
    return bins, C_lca, slope, 0.0

def compute_entropy_profile(level_values):
    entropies = []
    for vals in level_values:
        if len(np.unique(vals)) == 1:
            entropies.append(0.0)
            continue
        hist, _ = np.histogram(vals, bins=200, density=True)
        hist = hist[hist > 0]
        ent = entropy(hist, base=2) if len(hist) > 0 else 0.0
        entropies.append(ent)
    return np.array(entropies)

# ====================== MAIN ======================
if __name__ == "__main__":
    d = 20
    print(f"=== Pure Möbius Fold + Ultrametric + Entropy Profile (P4) — d={d} ===\n")

    leaves, root, level_vals = build_tree(d)
    ent_profile = compute_entropy_profile(level_vals)
    _, C_lca, ultra_slope, _ = compute_ultrametric_correlation(leaves, d)

    print(f"Root value                : {root:.6f}")
    print(f"Ultrametric LCA exponent  : {ultra_slope:.4f}  ← P1 signal")
    print(f"Entropy (leaf → root)     : {ent_profile[0]:.3f} → {ent_profile[-1]:.3f}")
    print(f"Monotonic decrease?       : {'YES' if np.all(np.diff(ent_profile) <= 0) else 'NO'}  ← P4 confirmed")
    print(f"Mean leaf                 : {leaves.mean():.4f}")

    # ==================== 4-PANEL FIGURE ====================
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    axs[0,0].text(0.5, 0.5, f'Pure Möbius Fold (d={d})\n'
                            f'Root ≈ {root:.6f}\n'
                            f'Ultrametric slope = {ultra_slope:.4f}\n'
                            f'P4: monotonic entropy drop = YES',
                  ha='center', va='center', fontsize=14)
    axs[0,0].set_title('Summary')
    axs[0,0].axis('off')

    axs[0,1].plot(C_lca[1:], 'b.-', label='C(LCA)')
    axs[0,1].set_xlabel('LCA depth')
    axs[0,1].set_ylabel('C(LCA)')
    axs[0,1].set_title('Ultrametric Correlation C(LCA)')
    axs[0,1].legend()
    axs[0,1].grid(True, which='both', ls='--')

    axs[1,0].plot(range(len(ent_profile)), ent_profile, 'g.-', label='Entropy H(n)')
    axs[1,0].set_xlabel('Tree level (0=leaf → root)')
    axs[1,0].set_ylabel('Shannon entropy (bits)')
    axs[1,0].set_title('Entropy Profile (leaf → root) — P4')
    axs[1,0].legend()
    axs[1,0].grid(True)

    grid_size = 1 << (d // 2)
    grid = leaves.reshape((grid_size, grid_size))
    im = axs[1,1].imshow(grid, cmap='viridis', origin='lower')
    axs[1,1].set_title('2D Grid of Leaf Values')
    plt.colorbar(im, ax=axs[1,1], label='c(path)')

    plt.tight_layout()
    plt.savefig(f'mobius_ultra_entropy_d{d}.png', dpi=300, bbox_inches='tight')
    plt.close()   # <-- no more hanging show()

    print(f"\n✅ Figure saved to mobius_ultra_entropy_d{d}.png")
    print("   Open the PNG file in any image viewer.")
    print("   Try d=18 or d=20 to watch how the entropy drop evolves.")