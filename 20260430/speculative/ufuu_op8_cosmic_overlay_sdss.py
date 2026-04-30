import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import KDTree

print("UFUU OP8 SDSS Overlay (offline realistic version)...")

# === 1. Load UFUU map ===
positions_ufuu = np.loadtxt('op8_address_position_map_d10.csv', delimiter=',', skiprows=1)

# === 2. Generate Realistic SDSS-like Galaxy Distribution (offline) ===
np.random.seed(42)
n_gal = 3500

# Base random field
galaxies = np.random.normal(0, 80, (n_gal, 3))

# Add 12 major filamentary structures (mimicking SDSS cosmic web)
for i in range(12):
    t = np.linspace(-120, 120, 180)
    angle = i * np.pi / 6
    filament = np.column_stack((
        t * np.cos(angle) + np.random.normal(0, 4, len(t)),
        t * np.sin(angle) + np.random.normal(0, 4, len(t)),
        t * 0.3 + np.random.normal(0, 12, len(t))
    ))
    galaxies = np.vstack((galaxies, filament))

# Add 6 galaxy clusters (over-densities)
for _ in range(6):
    cluster_center = np.random.normal(0, 60, 3)
    cluster = cluster_center + np.random.normal(0, 8, (120, 3))
    galaxies = np.vstack((galaxies, cluster))

# Add voids (remove points in spherical regions)
for _ in range(5):
    void_center = np.random.normal(0, 70, 3)
    dists = np.linalg.norm(galaxies - void_center, axis=1)
    galaxies = galaxies[dists > 18]

print(f"Generated realistic SDSS-like web: {len(galaxies):,} galaxies (filaments + clusters + voids)")

# === 3. Möbius Fold + scaling ===
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

# === 4. Higgs VEV attractors ===
higgs_mask = np.linalg.norm(positions_scaled, axis=1) < 0.3 * np.max(np.linalg.norm(positions_scaled, axis=1))
higgs_positions = positions_scaled[higgs_mask]

print(f"Higgs VEV attractors highlighted: {len(higgs_positions)}")

# === 5. Plot ===
fig = plt.figure(figsize=(14, 11))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(galaxies[:, 0], galaxies[:, 1], galaxies[:, 2],
           c='coral', s=4, alpha=0.35, label='Realistic SDSS-like Galaxies (procedural)')

ax.scatter(positions_scaled[:, 0], positions_scaled[:, 1], positions_scaled[:, 2],
           c='cyan', s=12, alpha=0.75, label='UFUU + Möbius Fold Map (D=10)')

ax.scatter(higgs_positions[:, 0], higgs_positions[:, 1], higgs_positions[:, 2],
           c='yellow', s=80, alpha=0.9, edgecolors='gold', label='Higgs VEV Attractors')

ax.set_xlabel('X (Mpc)')
ax.set_ylabel('Y (Mpc)')
ax.set_zlabel('Z (Mpc)')
ax.set_title('UFUU OP8 SDSS Overlay (Offline)\nMöbius Fold + Realistic SDSS-like Structure + Higgs Embedding')
ax.legend()

plt.tight_layout()
plt.savefig('op8_cosmic_overlay_sdss_offline.png', dpi=400)
print("\nSaved plot to 'op8_cosmic_overlay_sdss_offline.png'")
plt.show()

print("\nOP8 offline real-data-style overlay complete. No internet required.")