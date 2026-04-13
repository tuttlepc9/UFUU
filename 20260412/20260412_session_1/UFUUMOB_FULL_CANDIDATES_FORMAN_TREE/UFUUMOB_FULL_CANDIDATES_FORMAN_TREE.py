"""
UFUUMOB_FULL_CANDIDATES_FORMAN_TREE.py
Forman-Ricci curvature DIRECTLY on the binary tree topology
All four official candidates + Random baseline
Matches manuscript protocol (Sec 7.3 + B2) with Forman-Ricci as suggested
"""

import numpy as np
from scipy.stats import linregress, entropy

PHI = (1 + np.sqrt(5)) / 2
np.random.seed(42)
print("Random seed: 42 (fixed for reproducible comparison)\n")

def c_path(path: str) -> float:
    if not path: return 0.0
    return int(path, 2) / (1 << len(path))

# ====================== OFFICIAL CANDIDATE FOLDS ======================
def fold_golden(a: float, b: float) -> float:
    return a + b / PHI

def fold_modular(a: float, b: float, p: int = 17) -> float:
    return (a * b + a + 1) % p

def fold_xor_carry(a: float, b: float):
    ia, ib = int(a), int(b)
    return (ia ^ ib, ia & ib)   # XOR channel

def fold_mobius(a: float, b: float) -> float:
    z = complex(a, b)
    return np.abs((PHI * z + 1) / (z + PHI))

def fold_random(a: float, b: float) -> float:
    return np.random.uniform(0, 1)

# ====================== TREE BUILDER (returns graph + values) ======================
def build_tree_graph(depth: int, fold_func, fold_name: str):
    n = 1 << depth
    leaves = np.array([c_path(f'{i:0{depth}b}') for i in range(n)], dtype=np.float64)
    current = leaves.copy()
    level_values = [leaves.copy()]

    # Build graph: nodes 0..2^d-1 are leaves, parents are higher indices
    # For Forman-Ricci we only need parent-child edges at each level
    edges = []  # list of (parent_idx, child_idx) at parent level
    node_values = leaves.copy()  # final parent values will be at the end

    for level in range(1, depth + 1):
        parent_size = len(current) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)
        parent_offset = len(node_values)  # where parents start in full array
        for i in range(parent_size):
            left, right = current[2*i], current[2*i+1]
            if fold_name == "XOR-Carry":
                result = fold_func(left, right)
                next_level[i] = result[0] if isinstance(result, tuple) else result
            else:
                next_level[i] = fold_func(left, right)
            # Record edges: parent → left child, parent → right child
            edges.append((parent_offset + i, 2*i))      # left child
            edges.append((parent_offset + i, 2*i + 1))  # right child
        node_values = np.concatenate([node_values, next_level])
        current = next_level

    # Final parents are the last parent_size values
    parents = current.copy()
    return parents, edges, node_values  # edges for Forman-Ricci

def forman_ricci_on_tree(edges, node_values):
    """Forman-Ricci curvature on each edge of the tree"""
    # For trees (acyclic), Forman-Ricci simplifies
    # Standard formula for edge e=(u,v): F(e) = 2 - deg(u) - deg(v) + sum over common neighbors (but trees have none)
    # In practice for unweighted tree: F(e) = 2 - deg(u) - deg(v)  (often scaled)
    # We use the common combinatorial version used in discrete GR tests
    ricci = np.zeros(len(edges))
    degrees = np.zeros(len(node_values), dtype=int)
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1

    for idx, (u, v) in enumerate(edges):
        ricci[idx] = 2 - degrees[u] - degrees[v]   # basic Forman for trees
    return ricci

def compute_tree_gr_proxy(parents, edges, node_values):
    """GR proxy using Forman-Ricci on tree edges + asymmetry energy"""
    ricci = forman_ricci_on_tree(edges, node_values)
    # Asymmetry proxy: local leaf-parent difference averaged per edge
    asymmetry = np.zeros(len(edges))
    for i, (u, v) in enumerate(edges):
        asymmetry[i] = abs(node_values[u] - node_values[v])

    R_proxy = ricci
    T_proxy = asymmetry
    residual = np.abs(R_proxy - 8 * np.pi * T_proxy).mean()
    return residual

# ====================== ULTRAMETRIC + ENTROPY ======================
def compute_ultrametric_correlation(leaves, depth, n_samples=80000):
    n = len(leaves)
    idx1 = np.random.randint(0, n, n_samples)
    idx2 = np.random.randint(0, n, n_samples)
    lca_depths = []
    for i1, i2 in zip(idx1, idx2):
        xor = int(i1) ^ int(i2)
        lca_depths.append(depth if xor == 0 else depth - xor.bit_length())
    lca_depths = np.array(lca_depths)
    corrs = leaves[idx1] * leaves[idx2]
    max_lca = depth + 1
    bins = np.arange(max_lca)
    hist_corr = np.bincount(lca_depths, weights=corrs, minlength=max_lca)
    hist_count = np.bincount(lca_depths, minlength=max_lca)
    mask = hist_count > 0
    C_lca = np.zeros(max_lca)
    C_lca[mask] = hist_corr[mask] / hist_count[mask]
    valid = (bins >= 1) & mask
    if np.sum(valid) < 5:
        return np.nan
    log_lca = np.log(bins[valid])
    log_C = np.log(C_lca[valid] + 1e-12)
    slope, _, _, _, _ = linregress(log_lca, log_C)
    return slope

def compute_entropy_profile(level_values):
    entropies = []
    for vals in level_values:
        unique = np.unique(vals)
        if len(unique) <= 1:
            entropies.append(0.0)
            continue
        n_bins = min(200, max(50, int(len(unique) * 1.5)))
        hist, _ = np.histogram(vals, bins=n_bins, density=True)
        hist = hist[hist > 0]
        ent = entropy(hist, base=2) if len(hist) > 0 else 0.0
        entropies.append(ent)
    return np.array(entropies)

# ====================== MAIN ======================
if __name__ == "__main__":
    depths = [12, 14, 15, 16, 18, 20]
    print("=== FULL PAPER CANDIDATES — Forman-Ricci DIRECT on Tree Topology ===\n")
    print("d     | Fold          | Root      | Ultra slope |  Tree GR residual | P4 monotonic?")
    print("-" * 95)

    folds = {
        "Golden": fold_golden,
        "Modular": lambda a,b: fold_modular(a,b,17),
        "XOR-Carry": fold_xor_carry,
        "Möbius": fold_mobius,
        "Random": fold_random
    }

    for d in depths:
        for name, fold_func in folds.items():
            parents, edges, node_values = build_tree_graph(d, fold_func, name)
            leaves = node_values[: (1 << d)]  # first 2^d are leaves

            ultra_slope = compute_ultrametric_correlation(leaves, d)
            residual = compute_tree_gr_proxy(parents, edges, node_values)

            # For P4 we only need leaf + final parent level
            ent_profile = compute_entropy_profile([leaves, parents])
            monotonic = "YES" if np.all(np.diff(ent_profile) <= 0) else "NO"

            print(f"{d:2d}    | {name:13s} | {parents[-1]:.6f} | {ultra_slope:9.4f}  | "
                  f"{residual:12.6f}     | {monotonic}")

    print("\n✅ Forman-Ricci tree baseline complete.")
    print("   This is the exact next step recommended in your own analysis notes.")
    print("   Compare Tree GR residual column vs Random baseline.")