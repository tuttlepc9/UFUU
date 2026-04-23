import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import os
from PIL import Image  # pip install pillow if needed

phi = (1 + math.sqrt(5)) / 2
quantum_noise_sigma = 0.12
depth_max = 6
num_runs = 5

def golden_fold_quantum(a, b, seed=None):
    if seed is not None:
        np.random.seed(seed)
    noise = np.random.normal(0, quantum_noise_sigma)
    return a + b / phi + noise

def binary_path_to_fraction(path):
    if not path:
        return 0.5
    n = len(path)
    val = int(path, 2)
    return val / (2**n - 1)

class TreeNode:
    def __init__(self, value, pos=None, depth=0, path="", is_leaf=False):
        self.value = value
        self.pos = pos
        self.children = []
        self.depth = depth
        self.path = path
        self.is_leaf = is_leaf
        self.original_pos = None

def build_tree(depth, curr_depth=0, path="", base_scale=1.0, seed=None):
    if curr_depth == depth:
        c = binary_path_to_fraction(path)
        return TreeNode(c * base_scale, depth=curr_depth, path=path, is_leaf=True)
    left = build_tree(depth, curr_depth + 1, path + "0", base_scale, seed)
    right = build_tree(depth, curr_depth + 1, path + "1", base_scale, seed)
    value = golden_fold_quantum(left.value, right.value, seed)
    node = TreeNode(value, depth=curr_depth, path=path)
    node.children = [left, right]
    return node

def assign_positions(node, center=np.zeros(3), radius=6.0, angle=0):
    golden_angle = 2 * math.pi * (1 - 1 / phi)
    if node.is_leaf:
        y = -radius * (node.depth / depth_max) * 1.8
        r = np.sqrt(max(0, radius**2 - y**2))
        theta = angle * golden_angle + node.depth * 0.5
        node.pos = np.array([r * math.cos(theta), y, r * math.sin(theta)]) + center
        node.original_pos = node.pos.copy()
        return
    assign_positions(node.children[0], center, radius * 0.85, angle)
    assign_positions(node.children[1], center, radius * 0.85, angle + math.pi)
    node.pos = (node.children[0].pos + node.children[1].pos) / 2
    node.original_pos = node.pos.copy()

def update_plot(ax, scatter, ghost_scatter, all_nodes, highlight_parents=None, ghosts=None):
    xs = [n.pos[0] for n in all_nodes]
    ys = [n.pos[1] for n in all_nodes]
    zs = [n.pos[2] for n in all_nodes]
    vals = [n.value for n in all_nodes]
    sizes = [35 * (1.3 ** (depth_max - n.depth)) for n in all_nodes]

    if highlight_parents:
        for i, n in enumerate(all_nodes):
            if n in highlight_parents:
                sizes[i] *= 2.5
                vals[i] = phi * 12

    scatter._offsets3d = (xs, ys, zs)
    scatter.set_array(np.array(vals))
    scatter.set_sizes(np.array(sizes))

    if ghosts:
        gxs, gys, gzs, gvals = [], [], [], []
        for g in ghosts:
            gxs.append(g[0]); gys.append(g[1]); gzs.append(g[2]); gvals.append(g[3])
        ghost_scatter._offsets3d = (gxs, gys, gzs)
        ghost_scatter.set_array(np.array(gvals))
        ghost_scatter.set_sizes(np.full(len(gxs), 25))

def run_simulation(run_id):
    print(f"🚀 Running Quantum Fold simulation {run_id+1}/{num_runs}...")
    np.random.seed(run_id * 42)
    root = build_tree(depth_max, seed=run_id * 42)
    assign_positions(root)

    all_nodes = []
    def collect(n):
        all_nodes.append(n)
        for c in n.children: collect(c)
    collect(root)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-8, 8); ax.set_ylim(-8, 8); ax.set_zlim(-8, 8)
    scatter = ax.scatter([], [], [], c=[], s=[], cmap='viridis', alpha=0.95, edgecolors='k')
    ghost_scatter = ax.scatter([], [], [], c=[], s=[], cmap='plasma', alpha=0.25)

    frames = []  # for GIF

    # Initial tree
    update_plot(ax, scatter, ghost_scatter, all_nodes)
    ax.set_title(f'Quantum Golden Fold Run #{run_id+1} — Initial Tree', fontsize=14)
    plt.draw()
    frames.append(fig.canvas.copy_from_bbox(fig.bbox))

    current_level = depth_max - 1
    while current_level >= 0:
        folding_children = [n for n in all_nodes if n.depth == current_level + 1]
        parent_map = {}
        new_parents = []
        ghosts = []
        for node in all_nodes:
            if node.depth == current_level and node.children:
                new_val = golden_fold_quantum(node.children[0].value, node.children[1].value)
                node.value = new_val
                node.ghost_values = [new_val + np.random.normal(0, quantum_noise_sigma*1.5) for _ in range(5)]
                new_parents.append(node)
                for gv in node.ghost_values:
                    ghost_pos = node.pos + np.random.normal(0, 0.4, 3)
                    ghosts.append((*ghost_pos, gv))
                parent_map[node.children[0]] = node
                parent_map[node.children[1]] = node

        # Smooth merge (25 frames)
        for step in range(25):
            t = step / 25
            for child in folding_children:
                parent = parent_map.get(child)
                if parent:
                    child.pos = (1 - t) * child.original_pos + t * parent.pos
            update_plot(ax, scatter, ghost_scatter, all_nodes, new_parents, ghosts)
            ax.set_title(f'Run #{run_id+1} — Folding level {current_level} (t={t:.2f})', fontsize=14)
            plt.draw()
            frames.append(fig.canvas.copy_from_bbox(fig.bbox))

        # Snap + dramatic pause
        for child in folding_children:
            parent = parent_map.get(child)
            if parent:
                child.pos = parent.pos.copy()
        update_plot(ax, scatter, ghost_scatter, all_nodes, new_parents, ghosts)
        ax.set_title(f'Run #{run_id+1} — New Parent Formed at level {current_level}', fontsize=14)
        plt.draw()
        for _ in range(8): frames.append(fig.canvas.copy_from_bbox(fig.bbox))  # pause

        current_level -= 1

    # Final root highlight
    update_plot(ax, scatter, ghost_scatter, all_nodes, [root])
    ax.set_title(f'Run #{run_id+1} — Root Attractor (one possible answer)', fontsize=14)
    plt.draw()
    for _ in range(15): frames.append(fig.canvas.copy_from_bbox(fig.bbox))

    # Save final PNG
    png_name = f'golden_fold_quantum_run_{run_id+1:03d}.png'
    plt.savefig(png_name, dpi=200, bbox_inches='tight')
    print(f'   ✅ Saved {png_name}')

    plt.close(fig)

    # Save GIF for this run (or we can combine all later)
    return frames, png_name

# ====================== BATCH RUN ======================
all_gif_frames = []
print("Starting multi-run Quantum Golden Fold simulation...\n")
for i in range(num_runs):
    frames, png = run_simulation(i)
    all_gif_frames.extend(frames)  # collect for full animation

print("\n🎉 All runs complete!")
print(f"   → {num_runs} incremental PNG files saved")

# Create beautiful full animation GIF
print("Creating animated GIF with smooth timing...")
gif_name = "golden_fold_quantum_full_animation.gif"
images = []
for frame in all_gif_frames:
    # Convert canvas to PIL Image
    img = Image.frombytes('RGB', frame.get_size(), frame.tostring('raw', 'RGB'))
    images.append(img)

images[0].save(gif_name, save_all=True, append_images=images[1:], duration=40, loop=0)  # 40ms per frame = nice pacing
print(f"   ✅ Saved {gif_name} (visually appealing timing)")

print("\nOpen the GIF and the PNGs to see the quantum folding in action!")