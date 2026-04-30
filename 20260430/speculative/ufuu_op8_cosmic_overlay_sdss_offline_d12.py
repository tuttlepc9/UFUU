import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import KDTree
from itertools import product

print("UFUU OP8 D=12 SDSS Overlay (offline)...")

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
    
    addresses = []
    positions = []
    for bits in product([0, 1], repeat=depth):
        addr = tuple(bits)
        pos = r0.copy()
        scale = 1.0
        for m in range(depth):
            scale *= 1.06
            b = basis[m % len(basis)]
            pos += bits[m] * scale * b
        addresses.append(addr)
        positions.append(pos)
    return np.array(positions)

positions_ufuu = generate_full_address_to_position_map(depth=12)
print(f"Generated full D=12 UFUU map: {len(positions_ufuu):,} positions")

# === Realistic SDSS-like galaxy web (same as last script) ===
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

# === Möbius + scaling + Higgs (same as before) ===
def apply_mobius_fold(pos, scale=1.0):
    r = np.linalg.norm(pos, axis=1, keepdims=True)
    r = np.where(r == 0, 1e-8, r)
    return pos / (r ** 2 + 1e-6) * scale

positions_mobius = apply_mobius_fold(positions_ufuu, scale=1.06)

tree_ufuu = KDTree(positions_mobius)
dists_ufuu, _ = tree_ufuu.query(positions_mobius, k=2)
mean_nn_ufuu = dists_ufuu[:, 1].mean()

tree_gal = KDTree(galaxies)
dists_gal, _ = tree_gal.query(galaxies, k=2)
mean_nn_gal = dists_gal[:, 1].mean()

scale_factor = mean_nn_gal / mean_nn_ufuu * 1.06
positions_scaled = positions_mobius * scale_factor

higgs_mask = np.linalg.norm(positions_scaled, axis=1) < 0.3 * np.max(np.linalg.norm(positions_scaled, axis=1))
higgs_positions = positions_scaled[higgs_mask]

print(f"Higgs VEV attractors: {len(higgs_positions)}")

# === Plot ===
fig = plt.figure(figsize=(14, 11))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(galaxies[:, 0], galaxies[:, 1], galaxies[:, 2],
           c='coral', s=3, alpha=0.3, label='Realistic SDSS-like Galaxies')

ax.scatter(positions_scaled[:, 0], positions_scaled[:, 1], positions_scaled[:, 2],
           c='cyan', s=8, alpha=0.7, label='UFUU + Möbius Fold Map (D=12)')

ax.scatter(higgs_positions[:, 0], higgs_positions[:, 1], higgs_positions[:, 2],
           c='yellow', s=60, alpha=0.9, edgecolors='gold', label='Higgs VEV Attractors')

ax.set_xlabel('X (Mpc)')
ax.set_ylabel('Y (Mpc)')
ax.set_zlabel('Z (Mpc)')
ax.set_title('UFUU OP8 D=12 SDSS Overlay (Offline)\nMöbius Fold + Realistic Structure + Higgs')
ax.legend()

plt.tight_layout()
plt.savefig('op8_d12_sdss_offline.png', dpi=400)
print("\nSaved D=12 plot to 'op8_d12_sdss_offline.png'")
plt.show()