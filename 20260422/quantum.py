import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import sys

phi = (1 + math.sqrt(5)) / 2
quantum_noise_sigma = 0.15  # tune this for more/less QM "spread"

def golden_fold_quantum(a, b, seed=None):
    """Quantum version of Tuttle's F_φ: deterministic + stochastic noise"""
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
        self.ghost_values = []   # for quantum superposition visualization

def build_tree(depth, curr_depth=0, path="", base_scale=1.0):
    if curr_depth == depth:
        c = binary_path_to_fraction(path)
        value = c * base_scale
        return TreeNode(value, depth=curr_depth, path=path, is_leaf=True)
    left = build_tree(depth, curr_depth + 1, path + "0", base_scale)
    right = build_tree(depth, curr_depth + 1, path + "1", base_scale)
    value = golden_fold_quantum(left.value, right.value)  # quantum fold at build
    node = TreeNode(value, depth=curr_depth, path=path)
    node.children = [left, right]
    return node

def assign_positions(node, center=np.zeros(3), radius=6.0, angle=0):
    golden_angle = 2 * math.pi * (1 - 1 / phi)
    if node.is_leaf:
        y = -radius * (node.depth / depth_max) * 1.8
        r = np.sqrt(max(0, radius**2 - y**2))
        theta = angle * golden_angle + node.depth * 0.5
        x = r * math.cos(theta)
        z = r * math.sin(theta)
        node.pos = np.array([x, y, z]) + center
        node.original_pos = node.pos.copy()
        return
    assign_positions(node.children[0], center, radius * 0.85, angle)
    assign_positions(node.children[1], center, radius * 0.85, angle + math.pi)
    node.pos = (node.children[0].pos + node.children[1].pos) / 2
    node.original_pos = node.pos.copy()

# ====================== SETUP ======================
depth_max = 6
np.random.seed(42)  # reproducible for first run
root = build_tree(depth_max)
assign_positions(root)

all_nodes = []
def collect_nodes(node):
    all_nodes.append(node)
    for child in node.children:
        collect_nodes(child)
collect_nodes(root)

print(f"✅ Quantum Golden Fold Tree ready (depth {depth_max})")
print(f"Root value (first sample): {root.value:.4f}  φ ≈ {phi:.6f}")
print("Controls:")
print("   Enter → next classical parent")
print("   r     → re-perform fold with NEW quantum noise (different answer)")
print("   q     → quit")

# ====================== INTERACTIVE QUANTUM ANIMATION ======================
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
plt.ion()

scatter = ax.scatter([], [], [], c=[], s=[], cmap='viridis', alpha=0.95, edgecolors='k')
ghost_scatter = ax.scatter([], [], [], c=[], s=[], cmap='plasma', alpha=0.25)  # quantum ghosts

ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_zlim(-8, 8)
ax.set_title('Quantum Golden Ratio Fold (Tuttle 2026 + QM)\n"Every time we perform the fold → every answer eventually"')

def update_plot(highlight_parents=None, ghosts=None):
    xs = [n.pos[0] for n in all_nodes]
    ys = [n.pos[1] for n in all_nodes]
    zs = [n.pos[2] for n in all_nodes]
    vals = [n.value for n in all_nodes]
    sizes = [35 * (1.3 ** (depth_max - n.depth)) for n in all_nodes]
    
    if highlight_parents:
        for i, n in enumerate(all_nodes):
            if n in highlight_parents:
                sizes[i] *= 2.5
                vals[i] = phi * 12  # bright gold
    
    scatter._offsets3d = (xs, ys, zs)
    scatter.set_array(np.array(vals))
    scatter.set_sizes(np.array(sizes))
    
    # Quantum ghost possibilities
    if ghosts:
        gxs, gys, gzs, gvals = [], [], [], []
        for g in ghosts:
            gxs.append(g[0]); gys.append(g[1]); gzs.append(g[2])
            gvals.append(g[3])
        ghost_scatter._offsets3d = (gxs, gys, gzs)
        ghost_scatter.set_array(np.array(gvals))
        ghost_scatter.set_sizes(np.full(len(gxs), 25))

update_plot()
plt.draw()
plt.pause(1.5)

# ====================== INTERACTIVE LOOP ======================
current_level = depth_max - 1
while current_level >= 0:
    print(f"\n🔄 Level {current_level + 1} children ready → NEXT PARENT (level {current_level})")
    cmd = input("   Press Enter (classical fold) or 'r' (quantum re-sample) or 'q' to quit: ").strip().lower()
    
    if cmd == 'q':
        break
    if cmd == 'r':
        print("   Quantum re-measurement: new noise injected...")
        # Re-compute parent with fresh quantum noise
        folding_children = [n for n in all_nodes if n.depth == current_level + 1]
        new_parents = []
        ghosts = []
        for node in all_nodes:
            if node.depth == current_level and node.children:
                # Quantum fold with new randomness
                new_val = golden_fold_quantum(node.children[0].value, node.children[1].value, seed=None)
                node.value = new_val
                node.ghost_values = [new_val + np.random.normal(0, quantum_noise_sigma*1.5) for _ in range(5)]  # ghost branches
                new_parents.append(node)
                # Generate ghost positions for visualization
                for gv in node.ghost_values:
                    ghost_pos = node.pos + np.random.normal(0, 0.4, 3)
                    ghosts.append((*ghost_pos, gv))
    
    # Normal or re-sampled fold animation
    folding_children = [n for n in all_nodes if n.depth == current_level + 1]
    parent_map = {}
    new_parents = []
    for node in all_nodes:
        if node.depth == current_level and node.children:
            parent_map[node.children[0]] = node
            parent_map[node.children[1]] = node
            new_parents.append(node)
    
    # Merge animation
    steps = 18
    for step in range(steps + 1):
        t = step / steps
        for child in folding_children:
            parent = parent_map.get(child)
            if parent:
                child.pos = (1 - t) * child.original_pos + t * parent.pos
        update_plot(highlight_parents=new_parents, ghosts=ghosts if 'ghosts' in locals() else None)
        plt.draw()
        plt.pause(0.025)
    
    # Snap
    for child in folding_children:
        parent = parent_map.get(child)
        if parent:
            child.pos = parent.pos.copy()
    
    update_plot(highlight_parents=new_parents, ghosts=ghosts if 'ghosts' in locals() else None)
    plt.draw()
    plt.pause(1.0)
    
    current_level -= 1

print("\n🎉 Quantum folding complete! Root now holds one possible measurement outcome.")
print("   (Run the script again or press 'r' repeatedly to see every other answer emerge)")
update_plot(highlight_parents=[root])
plt.draw()
plt.pause(4)

plt.ioff()
plt.show()