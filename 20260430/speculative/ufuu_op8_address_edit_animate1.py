import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product
import time

print("UFUU OP8 Address-Edit Animation: Visualizing 'memory address editing'...")

# Generate D=12 UFUU map (same as before)
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

positions = generate_full_address_to_position_map()

# Realistic SDSS-like web (same as previous)
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

# Pick a starting address and flip one bit (a single fold operation)
start_idx = 0
start_pos = positions[start_idx].copy()

# Flip the middle bit (any single bit works)
flip_bit = 6
new_bits = list(bin(start_idx)[2:].zfill(12))
new_bits[flip_bit] = '1' if new_bits[flip_bit] == '0' else '0'
new_idx = int(''.join(new_bits), 2)
new_pos = positions[new_idx]

print(f"Starting address → position: {start_pos}")
print(f"After single fold (bit {flip_bit} flipped) → {new_pos}")

# Animation
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Background galaxies
ax.scatter(galaxies[:, 0], galaxies[:, 1], galaxies[:, 2], c='coral', s=3, alpha=0.2, label='SDSS-like Cosmic Web')

# Starting position
point = ax.scatter([start_pos[0]], [start_pos[1]], [start_pos[2]], c='cyan', s=120, label='Starting Position')
arrow = ax.quiver(start_pos[0], start_pos[1], start_pos[2], 0, 0, 0, color='yellow', linewidth=3)

ax.set_xlabel('X (Mpc)')
ax.set_ylabel('Y (Mpc)')
ax.set_zlabel('Z (Mpc)')
ax.set_title('UFUU OP8 Address-Edit Animation\nSingle Fold Operation = Instant Relocation')

for i in range(20):
    t = i / 19.0
    interp = start_pos * (1 - t) + new_pos * t
    point._offsets3d = ([interp[0]], [interp[1]], [interp[2]])
    arrow.remove()
    arrow = ax.quiver(interp[0], interp[1], interp[2], new_pos[0]-interp[0], new_pos[1]-interp[1], new_pos[2]-interp[2], color='yellow', linewidth=3)
    plt.pause(0.05)
    fig.canvas.draw()

plt.legend()
plt.tight_layout()
plt.savefig('op8_address_edit_animation.png', dpi=300)
plt.show()

print("\nAnimation complete. Saved to 'op8_address_edit_animation.png'")
print("This visualizes the exact 'memory address editing' mechanism from the OP8 notebook.")