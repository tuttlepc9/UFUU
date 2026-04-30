import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product
import random

print("UFUU OP8 Spaceship Path Animation — Continual Looping Travel...")

# === Generate D=12 UFUU map ===
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

ufuu_positions = generate_full_address_to_position_map()
print(f"Generated D=12 map: {len(ufuu_positions):,} positions")

# === Realistic SDSS-like galaxy web ===
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

# === Generate a long path of successive address edits (single-bit flips) ===
path_length = 300
path_indices = [random.randint(0, len(ufuu_positions)-1)]
for _ in range(path_length):
    current = path_indices[-1]
    bit_to_flip = random.randint(0, 11)  # flip one random bit
    new_idx = current ^ (1 << bit_to_flip)
    path_indices.append(new_idx)

path_positions = ufuu_positions[path_indices]

# === Continual Looping Animation ===
fig = plt.figure(figsize=(14, 11))
ax = fig.add_subplot(111, projection='3d')

# Background galaxies
ax.scatter(galaxies[:, 0], galaxies[:, 1], galaxies[:, 2], c='coral', s=3, alpha=0.25, label='SDSS-like Cosmic Web')

# UFUU cloud (faint)
ax.scatter(ufuu_positions[:, 0], ufuu_positions[:, 1], ufuu_positions[:, 2], c='cyan', s=6, alpha=0.15, label='UFUU D=12 Fold Map')

# Higgs VEV attractors
higgs_mask = np.linalg.norm(ufuu_positions, axis=1) < 0.3 * np.max(np.linalg.norm(ufuu_positions, axis=1))
ax.scatter(ufuu_positions[higgs_mask, 0], ufuu_positions[higgs_mask, 1], ufuu_positions[higgs_mask, 2],
           c='yellow', s=80, alpha=0.9, edgecolors='gold', label='Higgs VEV Attractors')

# Spaceship (bright moving point + short trail)
ship, = ax.plot([], [], [], 'o', color='lime', markersize=14, label='Spaceship (Fold Travel)')
trail, = ax.plot([], [], [], '-', color='lime', linewidth=2, alpha=0.7)

ax.set_xlabel('X (Mpc)')
ax.set_ylabel('Y (Mpc)')
ax.set_zlabel('Z (Mpc)')
ax.set_title('UFUU OP8 Spaceship Path Animation\nContinual Discrete Fold Jumps — “Memory Address Editing” Travel')
ax.legend()

step = 0
trail_x, trail_y, trail_z = [], [], []

print("Animation running — close the window to stop.")

while True:
    idx = step % len(path_positions)
    pos = path_positions[idx]
    
    # Update trail (last 15 positions)
    trail_x.append(pos[0])
    trail_y.append(pos[1])
    trail_z.append(pos[2])
    if len(trail_x) > 15:
        trail_x.pop(0)
        trail_y.pop(0)
        trail_z.pop(0)
    
    ship.set_data([pos[0]], [pos[1]])
    ship.set_3d_properties([pos[2]])
    
    trail.set_data(trail_x, trail_y)
    trail.set_3d_properties(trail_z)
    
    plt.pause(0.08)   # speed of travel — adjust if too fast/slow
    step += 1
    fig.canvas.draw_idle()