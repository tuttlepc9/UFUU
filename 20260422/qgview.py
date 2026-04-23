import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from PIL import Image

phi = (1 + math.sqrt(5)) / 2
quantum_noise_sigma = 1.8      # ← increased so variation is obvious
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
                sizes[i] *= 3.0
                # Use ACTUAL root value for color (no more forced golden)
                vals[i] = n.value

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
    np.random.seed(run_id * 137)   # different seed per run
    root = build_tree(depth_max, seed=run_id * 137)
    assign_positions(root)

    all_nodes = []
    def collect(n):
        all_nodes.append(n)
        for c in n.children: collect(c)
    collect(root)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-8, 8); ax.set_ylim(-8, 8); ax.set_zlim(-8, 8)
    scatter = ax.scatter([], [], [], c=[], s=[], cmap='plasma', alpha=0.95, edgecolors='k')
    ghost_scatter = ax.scatter([], [], [], c=[], s=[], cmap='plasma', alpha=0.25)

    # Initial tree
    update_plot(ax, scatter, ghost_scatter, all_nodes)
    ax.set_title(f'Quantum Golden Fold Run #{run_id+1} — Initial Tree', fontsize=14)
    plt.draw()

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

        # Smooth merge
        for step in range(25):
            t = step / 25.0
            for child in folding_children:
                parent = parent_map.get(child)
                if parent:
                    child.pos = (1 - t) * child.original_pos + t * parent.pos
            update_plot(ax, scatter, ghost_scatter, all_nodes, new_parents, ghosts)
            ax.set_title(f'Run #{run_id+1} — Folding level {current_level} (t={t:.2f})', fontsize=14)
            plt.draw()

        # Snap + pause
        for child in folding_children:
            parent = parent_map.get(child)
            if parent:
                child.pos = parent.pos.copy()
        update_plot(ax, scatter, ghost_scatter, all_nodes, new_parents, ghosts)
        ax.set_title(f'Run #{run_id+1} — New Parent Formed at level {current_level}', fontsize=14)
        plt.draw()
        for _ in range(8): plt.pause(0.01)   # dramatic pause

        current_level -= 1

    # FINAL ROOT — now uses real value for color + size + text label
    update_plot(ax, scatter, ghost_scatter, all_nodes, [root])
    root_value = root.value
    ax.text(0, 8, 8, f'Root = {root_value:.4f}', fontsize=16, color='yellow', 
            bbox=dict(facecolor='black', alpha=0.7))
    ax.set_title(f'Run #{run_id+1} — Root Attractor (one possible answer)', fontsize=14)
    plt.draw()

    # Save PNG
    png_name = f'golden_fold_quantum_run_{run_id+1:03d}.png'
    plt.savefig(png_name, dpi=250, bbox_inches='tight')
    print(f'   ✅ Saved {png_name}  (Root = {root_value:.4f})')

    plt.close(fig)
    return png_name

# ====================== RUN ALL 5 ======================
print("Starting multi-run Quantum Golden Fold (visibly different each time)...\n")
for i in range(num_runs):
    run_simulation(i)

print("\n🎉 All 5 runs complete!")
print("   → Each PNG now shows a clearly different root attractor")
print("   → Quantum variation is strong and visible (like hitting 'r' repeatedly)")
print("Open the PNGs — you’ll see 5 different yellow root values!")