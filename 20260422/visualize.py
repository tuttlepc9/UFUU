import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

phi = (1 + math.sqrt(5)) / 2
print(f"Golden Ratio φ ≈ {phi:.8f}")

def golden_fold(a, b):
    """F_φ(a, b) = a + b / φ — exactly as in Tuttle 2026 Section 4.1"""
    return a + b / phi

def binary_path_to_fraction(path):
    """Path-dependent base case c(path) — minimal symmetry breaking"""
    if not path:
        return 0.5
    n = len(path)
    val = int(path, 2)
    return val / (2**n - 1)   # normalized ≈ [0,1)

class TreeNode:
    def __init__(self, value, pos=None, depth=0, path=""):
        self.value = value
        self.pos = pos
        self.children = []
        self.depth = depth
        self.path = path

def build_golden_fold_tree(depth, current_depth=0, path="", base_scale=1.0):
    if current_depth == depth:
        c = binary_path_to_fraction(path)
        value = c * base_scale
        return TreeNode(value, depth=current_depth, path=path)
    
    left = build_golden_fold_tree(depth, current_depth + 1, path + "0", base_scale)
    right = build_golden_fold_tree(depth, current_depth + 1, path + "1", base_scale)
    
    value = golden_fold(left.value, right.value)
    
    node = TreeNode(value, depth=current_depth, path=path)
    node.children = [left, right]
    return node

def assign_3d_positions(node, center=np.zeros(3), radius=5.0, angle_offset=0):
    """Golden-angle 3D phyllotaxis positioning (same style as Unity version)"""
    golden_angle = 2 * math.pi * (1 - 1/phi)
    
    if not node.children:  # leaf
        theta = angle_offset * golden_angle
        y = -radius * (1 - 2 * (node.depth / 10.0))
        r = np.sqrt(max(0, radius**2 - y**2))
        x = r * math.cos(theta)
        z = r * math.sin(theta)
        node.pos = np.array([x, y, z]) + center
        return
    
    # recurse children
    assign_3d_positions(node.children[0], center + np.array([0, radius*0.2, 0]), radius*0.7, angle_offset)
    assign_3d_positions(node.children[1], center - np.array([0, radius*0.2, 0]), radius*0.7, angle_offset + math.pi/2)
    
    # parent = average of children (fold visually merges)
    node.pos = (node.children[0].pos + node.children[1].pos) / 2.0

def collect_tree_data(root):
    nodes, edges = [], []
    def traverse(node, parent_pos=None):
        if node.pos is None: return
        nodes.append({'pos': node.pos, 'value': node.value, 'depth': node.depth})
        if parent_pos is not None:
            edges.append((parent_pos, node.pos))
        for child in node.children:
            traverse(child, node.pos)
    traverse(root)
    return nodes, edges

# ====================== RUN THE VISUALIZER ======================
max_depth = 8  # increase to 9–10 if your machine is fast
root = build_golden_fold_tree(max_depth)
assign_3d_positions(root)
nodes_data, edges_data = collect_tree_data(root)

print(f"✅ Tree built (depth {max_depth})")
print(f"Root value: {root.value:.6f}  (≈ φ^{max_depth} = {phi**max_depth:.6f})")

# ====================== 3D PLOT ======================
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

xs = [n['pos'][0] for n in nodes_data]
ys = [n['pos'][1] for n in nodes_data]
zs = [n['pos'][2] for n in nodes_data]
values = [n['value'] for n in nodes_data]
sizes = [20 * (1 + (max_depth - n['depth'])/max_depth) for n in nodes_data]

scatter = ax.scatter(xs, ys, zs, c=values, cmap='viridis', s=sizes, alpha=0.85, edgecolors='k', linewidth=0.3)

for start, end in edges_data:
    ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], 
            color='cyan', alpha=0.4, linewidth=1)

ax.set_title(f'Python Golden Ratio Fold Tree (Tuttle 2026)\nDepth {max_depth} | Root ≈ {root.value:.4f} | φ ≈ {phi:.6f}', fontsize=14)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')

cbar = plt.colorbar(scatter, ax=ax, shrink=0.6)
cbar.set_label('Fold Value')

plt.tight_layout()
plt.show()

# Optional: save image
# plt.savefig('golden_fold_tree_python.png', dpi=300)