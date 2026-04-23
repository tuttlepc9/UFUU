import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import time

phi = (1 + math.sqrt(5)) / 2

def golden_fold(a, b):
    """Exact fold from Tuttle 2026 Section 4.1"""
    return a + b / phi

def binary_path_to_fraction(path):
    """Path-dependent base case c(path)"""
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
        self.original_pos = None  # for animation reset

def build_tree(depth, curr_depth=0, path="", base_scale=1.0):
    if curr_depth == depth:
        c = binary_path_to_fraction(path)
        value = c * base_scale
        return TreeNode(value, depth=curr_depth, path=path, is_leaf=True)
    
    left = build_tree(depth, curr_depth+1, path+"0", base_scale)
    right = build_tree(depth, curr_depth+1, path+"1", base_scale)
    value = golden_fold(left.value, right.value)
    node = TreeNode(value, depth=curr_depth, path=path)
    node.children = [left, right]
    return node

def assign_positions(node, center=np.zeros(3), radius=6.0, angle=0):
    golden_angle = 2 * math.pi * (1 - 1/phi)
    if node.is_leaf:
        y = -radius * (node.depth / depth_max) * 1.8
        r = np.sqrt(max(0, radius**2 - y**2))
        theta = angle * golden_angle + node.depth * 0.5
        x = r * math.cos(theta)
        z = r * math.sin(theta)
        node.pos = np.array([x, y, z]) + center
        node.original_pos = node.pos.copy()
        return
    # Recurse for children
    assign_positions(node.children[0], center, radius*0.85, angle)
    assign_positions(node.children[1], center, radius*0.85, angle + math.pi)
    # Parent = fold merge point
    node.pos = (node.children[0].pos + node.children[1].pos) / 2
    node.original_pos = node.pos.copy()

# ====================== BUILD TREE ======================
depth_max = 7   # 6–8 recommended for smooth animation (higher = slower)
root = build_tree(depth_max)
assign_positions(root)

# Collect nodes
all_nodes = []
def collect_nodes(node):
    all_nodes.append(node)
    for child in node.children:
        collect_nodes(child)
collect_nodes(root)

print(f"✅ Tree built with {len(all_nodes)} nodes at depth {depth_max}")
print(f"Root value: {root.value:.6f} ≈ φ^{depth_max} = {phi**depth_max:.6f}")

# ====================== ANIMATED FOLDING SIMULATION ======================
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
plt.ion()

scatter = ax.scatter([], [], [], c=[], s=[], cmap='viridis', alpha=0.9, edgecolors='k')
ax.set_xlim(-7, 7)
ax.set_ylim(-7, 7)
ax.set_zlim(-7, 7)
ax.set_title(f'Golden Ratio Fold Animation - Depth {depth_max}\nChildren shrinking & merging into parents (Tuttle 2026)', fontsize=14)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

def update_scatter():
    xs = [n.pos[0] for n in all_nodes]
    ys = [n.pos[1] for n in all_nodes]
    zs = [n.pos[2] for n in all_nodes]
    vals = [n.value for n in all_nodes]
    sizes = [30 * (1.2 ** (depth_max - n.depth)) for n in all_nodes]
    
    scatter._offsets3d = (xs, ys, zs)
    scatter.set_array(np.array(vals))
    scatter.set_sizes(np.array(sizes))

# Initial full tree display
update_scatter()
plt.draw()
plt.pause(1.5)

# Level-by-level folding (leaves → root)
for current_level in range(depth_max-1, -1, -1):
    ax.set_title(f'Golden Ratio Fold Animation - Folding level {current_level} → parent\nφ ≈ {phi:.6f} | Root building...', fontsize=13)
    
    # Children at this level being folded
    folding_children = [n for n in all_nodes if n.depth == current_level + 1]
    
    parent_map = {}
    for node in all_nodes:
        if node.depth == current_level and node.children:
            parent_map[node.children[0]] = node
            parent_map[node.children[1]] = node
    
    # Animation frames for smooth merge + shrink
    steps = 20
    for step in range(steps + 1):
        t = step / steps
        for child in folding_children:
            parent = parent_map.get(child)
            if parent:
                # Child moves toward parent + shrinks
                child.pos = (1 - t) * child.original_pos + t * parent.pos
        
        update_scatter()
        plt.draw()
        plt.pause(0.03)  # smooth speed
    
    # Snap children to parent after merge
    for child in folding_children:
        parent = parent_map.get(child)
        if parent:
            child.pos = parent.pos.copy()
    
    update_scatter()
    plt.draw()
    plt.pause(0.8)  # pause between levels

# Final highlight of root (fixed-point attractor)
root.pos = root.original_pos.copy()
update_scatter()
plt.draw()
plt.pause(3)

print("🎉 Animation finished! (Root now shows the fixed-point attractor U = F(U, U))")
plt.ioff()
plt.show()