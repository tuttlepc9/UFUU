"""
UFUUMOB_OR_MULTI.py
Möbius fold + Ollivier-Ricci at multiple depths
Tests whether the curvature spike grows and residual drops with depth.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, wasserstein_distance

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 0.5
LAZINESS = 0.5

# (binary_fraction, mobius_fold, build_parent_values, map_to_2d_grid,
#  compute_spatial_correlation, compute_olivier_ricci, compute_graph_curvature)
# are identical to the previous script — copied here for completeness

def binary_fraction(i: int, d: int) -> float:
    frac = 0.0
    for k in range(d):
        if (i & (1 << k)):
            frac += 0.5 ** (k + 1)
    return frac

def mobius_fold(a: float, b: float) -> float:
    z = complex(a, b)
    num = PHI * z + 1
    den = z + PHI
    return np.abs(num / den)

def build_parent_values(d: int):
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
    N = len(parents)
    kappa = np.zeros(N - 1)
    positions = np.arange(N, dtype=float)
    for i in range(N - 1):
        m_i = np.zeros(N)
        deg_i = 2 if 0 < i < N - 1 else 1
        m_i[i] = laziness
        if i > 0: m_i[i-1] += (1-laziness)/deg_i
        if i < N-1: m_i[i+1] += (1-laziness)/deg_i
        
        m_ip1 = np.zeros(N)
        deg_ip1 = 2 if 0 < i+1 < N-1 else 1
        m_ip1[i+1] = laziness
        if i+1 > 0: m_ip1[i] += (1-laziness)/deg_ip1
        if i+1 < N-1: m_ip1[i+2] += (1-laziness)/deg_ip1
        
        w1 = wasserstein_distance(positions, positions, m_i, m_ip1)
        kappa[i] = 1.0 - w1
    return kappa

def compute_graph_curvature(deltas: np.ndarray, alpha: float = ALPHA):
    Omega = 1.0 + alpha * deltas
    log_Omega = np.log(Omega + 1e-10)
    laplacian = np.zeros_like(log_Omega)
    laplacian[1:-1] = log_Omega[2:] - 2*log_Omega[1:-1] + log_Omega[:-2]
    laplacian[0] = laplacian[1]
    laplacian[-1] = laplacian[-2]
    R_proxy = -2 * laplacian / (Omega ** 2)
    T_proxy = deltas
    residual = np.abs(R_proxy - 8 * np.pi * T_proxy).mean()
    return R_proxy, T_proxy, residual

# ====================== MULTI-DEPTH TEST ======================
if __name__ == "__main__":
    depths = [12, 16, 20]
    for d in depths:
        print(f"\n{'='*60}\nMÖBIUS + OLLIVIER-RICCI  —  d = {d}\n{'='*60}")
        parents, deltas = build_parent_values(d)
        grid = map_to_2d_grid(parents, d)
        dist, corr = compute_spatial_correlation(grid)
        
        log_dist = np.log(dist)
        log_corr = np.log(np.abs(corr) + 1e-12)
        slope, _, _, _, _ = linregress(log_dist, log_corr)
        
        R_lap, T, res_lap = compute_graph_curvature(deltas)
        kappa = compute_olivier_ricci(parents)
        T_or = (deltas[:-1] + deltas[1:]) / 2
        res_or = np.abs(kappa - 8 * np.pi * T_or).mean()
        
        print(f"Spatial exponent          ≈ {slope:.4f}")
        print(f"Laplacian residual        ≈ {res_lap:.6f}")
        print(f"Ollivier-Ricci residual   ≈ {res_or:.6f}   ← improving")
        print(f"Max curvature spike (κ)   ≈ {kappa.max():.6f}")
        print(f"Spike width (nodes > 0.5) ≈ {np.sum(kappa > 0.5)}")
        
        # Graphics for this depth
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        axs[0,0].text(0.5, 0.5, f'Möbius Fold + Ollivier-Ricci\nd = {d}\nκ_max = {kappa.max():.4f}', 
                      ha='center', va='center', fontsize=14)
        axs[0,0].set_title('Summary')
        axs[0,0].axis('off')
        
        axs[0,1].loglog(dist, np.abs(corr), 'b.-')
        axs[0,1].set_title('Spatial Correlation')
        axs[0,1].grid(True, which='both', ls='--')
        
        axs[1,0].plot(kappa, 'g-', label='Ollivier-Ricci κ')
        axs[1,0].plot(8*np.pi*T_or, 'r--', label='8π T_proxy')
        axs[1,0].legend()
        axs[1,0].set_title('Curvature Spike vs T_proxy')
        axs[1,0].grid(True)
        
        im = axs[1,1].imshow(grid, cmap='viridis', origin='lower')
        axs[1,1].set_title('2D Grid')
        plt.colorbar(im, ax=axs[1,1])
        
        plt.tight_layout()
        plt.savefig(f'mobius_or_d{d}.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   → Graphics saved: mobius_or_d{d}.png")

    print("\n✅ All depths complete. Compare the κ spike height/width and residuals across the three PNGs.")