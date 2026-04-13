"""
UFUUMOB_ULTRA.py
Pure Möbius fold + ultrametric correlation (paper's natural metric)
Optimized full-tree version based on test11.py
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
    """Paper's natural ultrametric LCA distance"""
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
    slope, intercept, _, _, _ = linregress(log_lca, log_C)
    return bins, C_lca, slope, intercept

def compute_spatial_correlation(leaves, depth, n_samples=80000):  # Manhattan for comparison
    # (same as test11.py - kept for completeness)
    # ... omitted for brevity; uses 2D coords as before
    pass  # full implementation is in test11.py if you want it

# ====================== MAIN ======================
if __name__ == "__main__":
    d = 16   # Change to 18/20 as desired
    print(f"=== Pure Möbius Fold + Ultrametric Correlation (d={d}) ===\n")

    leaves, root, level_vals = build_tree(d)

    # Ultrametric (the key metric)
    _, C_lca, ultra_slope, ultra_intercept = compute_ultrametric_correlation(leaves, d)
    print(f"Root value                : {root:.6f}")
    print(f"Ultrametric LCA exponent  : {ultra_slope:.4f} (R² will be high if signal strong)")
    print(f"Mean leaf                 : {leaves.mean():.4f}")
    print(f"Entropy (leaf → root)     : {entropy(np.histogram(leaves, bins=50, density=True)[0], base=2):.3f} → {entropy(np.histogram(level_vals[-1], bins=50, density=True)[0], base=2):.3f}")

    # Optional 4-panel figure (same style as UFUUGR1)
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs[0,0].text(0.5, 0.5, f'Pure Möbius Fold (d={d})\nRoot ≈ {root:.6f}\nUltrametric slope = {ultra_slope:.4f}', 
                  ha='center', va='center', fontsize=14)
    axs[0,0].set_title('Summary')
    axs[0,0].axis('off')

    axs[0,1].plot(C_lca[1:], 'b.-', label='C(LCA)')
    axs[0,1].set_xlabel('LCA depth')
    axs[0,1].set_ylabel('C(LCA)')
    axs[0,1].set_title('Ultrametric Correlation (paper metric)')
    axs[0,1].legend()
    axs[0,1].grid(True)

    # Bottom-left can show entropy profile or curvature if you add it later
    axs[1,0].text(0.5, 0.5, 'Add GR proxy or entropy plot here', ha='center', va='center')
    axs[1,0].axis('off')

    im = axs[1,1].imshow(leaves.reshape((1 << (d//2), 1 << (d//2))), cmap='viridis', origin='lower')  # rough grid
    axs[1,1].set_title('Leaf Values (2D map)')
    plt.colorbar(im, ax=axs[1,1])

    plt.tight_layout()
    plt.savefig(f'mobius_ultra_d{d}.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("\n✅ Graphics saved to mobius_ultra_d{d}.png")
    print("   Run at higher depth (18–20) to watch the ultrametric exponent trend.")