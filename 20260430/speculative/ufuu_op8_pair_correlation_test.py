import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from itertools import product   # ← Fixed: import at top level

print("UFUU OP8 Pair-Correlation Test (D=12 vs SDSS-like web)...")

# === Generate FULL D=12 UFUU map (4096 states) ===
def generate_full_address_to_position_map(depth=12, dim=3):
    r0 = np.zeros(dim)
    phi = (1 + np.sqrt(5)) / 2
    basis = []
    for i in range(6):
        theta1 = 2 * np.pi * (i / phi)
        theta2 = 2 * np.pi * (i / phi**2)
        vec = np.array([np.cos(theta1), np.sin(theta1)*np.cos(theta2), np.sin(theta1)*np.sin(theta2)])
        basis.append(vec / np.linalg.norm(vec))
    
    positions = []
    for bits in product([0, 1], repeat=depth):
        pos = r0.copy()
        scale = 1.0
        for m in range(depth):
            scale *= 1.06
            b = basis[m % len(basis)]
            pos += bits[m] * scale * b
        positions.append(pos)
    return np.array(positions)

ufuu = generate_full_address_to_position_map()
print(f"UFUU D=12 positions: {len(ufuu):,}")

# === Realistic SDSS-like galaxy web (same as D=12 overlay) ===
np.random.seed(42)
n_gal = 3500
galaxies = np.random.normal(0, 80, (n_gal, 3))
for i in range(12):
    t = np.linspace(-120, 120, 180)
    angle = i * np.pi / 6
    filament = np.column_stack((t * np.cos(angle) + np.random.normal(0, 4, len(t)),
                                t * np.sin(angle) + np.random.normal(0, 4, len(t)),
                                t * 0.3 + np.random.normal(0, 12, len(t))))
    galaxies = np.vstack((galaxies, filament))
for _ in range(6):
    cluster_center = np.random.normal(0, 60, 3)
    cluster = cluster_center + np.random.normal(0, 8, (120, 3))
    galaxies = np.vstack((galaxies, cluster))
for _ in range(5):
    void_center = np.random.normal(0, 70, 3)
    dists = np.linalg.norm(galaxies - void_center, axis=1)
    galaxies = galaxies[dists > 18]

# === Pair-correlation function ===
def pair_correlation(pos, bins=80, r_max=300):
    tree = KDTree(pos)
    dists, _ = tree.query(pos, k=len(pos)//10 + 2)  # limit for speed
    dists = dists[:, 1:].flatten()
    dists = dists[dists < r_max]
    hist, bin_edges = np.histogram(dists, bins=bins, density=True)
    r = (bin_edges[:-1] + bin_edges[1:]) / 2
    return r, hist

r_ufuu, c_ufuu = pair_correlation(ufuu)
r_gal, c_gal = pair_correlation(galaxies)

# === Plot ===
plt.figure(figsize=(10, 6))
plt.loglog(r_ufuu, c_ufuu, 'cyan', label='UFUU D=12 Fold Map', linewidth=2)
plt.loglog(r_gal, c_gal, 'coral', label='SDSS-like Galaxies', linewidth=2, alpha=0.8)
plt.xlabel('r (Mpc)')
plt.ylabel('C(r) (pair correlation)')
plt.title('UFUU OP8 Pair-Correlation Test\nQuasicrystalline Order in Fold vs. Cosmic Web?')
plt.legend()
plt.grid(True, which='both', ls='--')
plt.savefig('op8_pair_correlation_d12.png', dpi=300)
plt.show()

print("\nPair-correlation plot saved to 'op8_pair_correlation_d12.png'")
print("Check for power-law ~ r^{-0.141} + quasi-periodic oscillations in both curves.")