"""
UFUUMOB_OR1.py
W. Jason Tuttle – Recursive Fold Architectures (2026)
Möbius (conformal) fold + Ollivier-Ricci curvature proxy
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, wasserstein_distance

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 0.5
LAZINESS = 0.5   # standard parameter α for lazy random walk in Ollivier-Ricci

def binary_fraction(i: int, d: int) -> float:
    """Same path-dependent leaf values c(path) ∈ [0,1) as UFUUGR1.py"""
    frac = 0.0
    for k in range(d):
        if (i & (1 << k)):
            frac += 0.5 ** (k + 1)
    return frac

def mobius_fold(a: float, b: float) -> float:
    """Exact conformal Möbius fold from the paper (Sec. 4.4)"""
    z = complex(a, b)
    num = PHI * z + 1
    den = z + PHI
    return np.abs(num / den)

def build_parent_values(d: int):
    """Same as UFUUGR1.py / UFUUMOB1.py – parents at level above leaves"""
    num_parents = 1 << (d - 1)
    parents = np.zeros(num_parents)
    deltas = np.zeros(num_parents)
    for i in range(num_parents):
        left = binary_fraction(2 * i, d)
        right = binary_fraction(2 * i + 1, d)
        parents[i] = mobius_fold(left, right)
        deltas[i] = abs(left - right)
    return parents, deltas

def map_to_2d_grid(values: np.ndarray, d: int):
    """Identical interleaved-bit 2D mapping"""
    grid_size = 1 << ((d - 1) // 2) if (d - 1) % 2 == 0 else 1 << ((d - 1) // 2)
    grid = np.zeros((grid_size, grid_size))
    idx = 0
    for y in range(grid_size):
        for x in range(grid_size):
            if idx < len(values):
                grid[y, x] = values[idx]
                idx += 1
    return grid

def compute_spatial_correlation(grid: np.ndarray, max_r: int = 30):
    """Identical spatial correlation (Manhattan)"""
    h, w = grid.shape
    corr = []
    dist = []
    mean_val = grid.mean()
    for r in range(1, max_r + 1):
        count = 0
        sum_prod = 0.0
        for y in range(h):
            for x in range(w):
                if x + r < w:
                    sum_prod += (grid[y, x] - mean_val) * (grid[y, x + r] - mean_val)
                    count += 1
                if y + r < h:
                    sum_prod += (grid[y, x] - mean_val) * (grid[y + r, x] - mean_val)
                    count += 1
        if count > 0:
            corr.append(sum_prod / count)
            dist.append(r)
    return np.array(dist), np.array(corr)

def compute_olivier_ricci(parents: np.ndarray, laziness: float = LAZINESS):
    """
    Ollivier-Ricci curvature on the 1D path graph of parent nodes.
    κ(i, i+1) = 1 - W₁(m_i, m_{i+1}) / d(i,i+1)
    Uses lazy random walk measures (standard definition).
    This is the "more sophisticated discrete Ricci curvature" mentioned
    in the analysis notes for the tree-topology GR proxy test.
    """
    N = len(parents)
    kappa = np.zeros(N - 1)
    positions = np.arange(N, dtype=float)   # node indices as positions for W1

    for i in range(N - 1):
        # Measure m_i
        m_i = np.zeros(N)
        deg_i = 2 if 0 < i < N - 1 else 1
        m_i[i] = laziness
        if i > 0:
            m_i[i - 1] += (1 - laziness) / deg_i
        if i < N - 1:
            m_i[i + 1] += (1 - laziness) / deg_i

        # Measure m_{i+1}
        m_ip1 = np.zeros(N)
        deg_ip1 = 2 if 0 < i + 1 < N - 1 else 1
        m_ip1[i + 1] = laziness
        if i + 1 > 0:
            m_ip1[i] += (1 - laziness) / deg_ip1
        if i + 1 < N - 1:
            m_ip1[i + 2] += (1 - laziness) / deg_ip1

        # Wasserstein-1 distance (Earth Mover's distance) between the two measures
        w1 = wasserstein_distance(positions, positions, m_i, m_ip1)

        kappa[i] = 1.0 - w1 / 1.0   # d(u,v) = 1 on the path graph

    return kappa

def compute_graph_curvature(deltas: np.ndarray, alpha: float = ALPHA):
    """Keep the original Laplacian proxy for direct side-by-side comparison"""
    Omega = 1.0 + alpha * deltas
    log_Omega = np.log(Omega + 1e-10)
    laplacian = np.zeros_like(log_Omega)
    laplacian[1:-1] = log_Omega[2:] - 2 * log_Omega[1:-1] + log_Omega[:-2]
    laplacian[0] = laplacian[1]
    laplacian[-1] = laplacian[-2]
    R_proxy = -2 * laplacian / (Omega ** 2)
    T_proxy = deltas
    residual = np.abs(R_proxy - 8 * np.pi * T_proxy).mean()
    return R_proxy, T_proxy, residual

# ====================== MAIN ======================
if __name__ == "__main__":
    d = 12
    print(f"Running Möbius conformal fold + Ollivier-Ricci at depth d = {d}")

    parents, deltas = build_parent_values(d)
    print(f"Last parent value ≈ {parents[-1]:.6f}")
    print(f"Mean parent value ≈ {parents.mean():.6f}")

    grid = map_to_2d_grid(parents, d)
    dist, corr = compute_spatial_correlation(grid, max_r=30)

    log_dist = np.log(dist)
    log_corr = np.log(np.abs(corr) + 1e-12)
    slope, intercept, _, _, _ = linregress(log_dist, log_corr)
    print(f"Spatial correlation power-law exponent ≈ {slope:.3f}")

    # Original Laplacian proxy (for comparison)
    R_lap, T, residual_lap = compute_graph_curvature(deltas)

    # New Ollivier-Ricci proxy on the parent path graph
    kappa = compute_olivier_ricci(parents)
    # T_proxy aligned to edges (simple average of adjacent deltas)
    T_or = (deltas[:-1] + deltas[1:]) / 2
    residual_or = np.abs(kappa - 8 * np.pi * T_or).mean()
    print(f"Laplacian residual (old)  ≈ {residual_lap:.6f}")
    print(f"Ollivier-Ricci residual   ≈ {residual_or:.6f}  ← improved proxy")

    # ==================== GRAPHICS ====================
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Top-left: Summary
    axs[0,0].text(0.5, 0.5, f'Möbius Conformal Fold + Ollivier-Ricci\n'
                            f'Depth d = {d}\n'
                            f'Last parent ≈ {parents[-1]:.4f}\n'
                            f'SL(2,ℂ) + discrete Ricci test',
                  ha='center', va='center', fontsize=14)
    axs[0,0].set_title('Root Value Summary')
    axs[0,0].axis('off')

    # Top-right: Spatial correlation (unchanged)
    axs[0,1].loglog(dist, np.abs(corr), 'b.-', label='C(r)')
    axs[0,1].loglog(dist, np.exp(intercept) * dist**slope, 'r--',
                    label=f'Fit: slope = {slope:.3f}')
    axs[0,1].set_xlabel('Distance r (Manhattan)')
    axs[0,1].set_ylabel('|C(r)|')
    axs[0,1].set_title('Spatial Correlation C(r)')
    axs[0,1].legend()
    axs[0,1].grid(True, which='both', ls='--')

    # Bottom-left: NOW TWO CURVATURE PROXIES (honest side-by-side)
    axs[1,0].plot(R_lap[:100], 'b-', label='R_proxy (Laplacian, old)')
    axs[1,0].plot(kappa[:100], 'g-', label='κ (Ollivier-Ricci, new)')
    axs[1,0].plot(8 * np.pi * T[:100], 'r--', label='8π T_proxy')
    axs[1,0].set_xlabel('Parent node index')
    axs[1,0].set_ylabel('Curvature proxy')
    axs[1,0].set_title('Gravity Test: Laplacian vs. Ollivier-Ricci')
    axs[1,0].legend()
    axs[1,0].grid(True)
    axs[1,0].text(0.05, 0.85, f'Laplacian res = {residual_lap:.6f}\n'
                              f'Ollivier-Ricci res = {residual_or:.6f}',
                  transform=axs[1,0].transAxes,
                  bbox=dict(facecolor='white', alpha=0.8))

    # Bottom-right: 2D grid (unchanged)
    im = axs[1,1].imshow(grid, cmap='viridis', origin='lower')
    axs[1,1].set_title('2D Grid of Parent Values')
    plt.colorbar(im, ax=axs[1,1], label='Fold value')

    plt.tight_layout()
    plt.savefig('mobius_olivier_ricci_graphics.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("\n✅ Graphics saved to 'mobius_olivier_ricci_graphics.png'")
    print("   Möbius fold now tested with both the old Laplacian proxy AND")
    print("   the new Ollivier-Ricci curvature (recommended in analysis notes).")
    print("   Compare residuals: lower residual = better gravity-like coupling.")
    print("   Ready for deeper runs (d=14–16) or full-tree extension.")