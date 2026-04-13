import numpy as np
from functools import lru_cache
import matplotlib.pyplot as plt
from scipy.stats import linregress

# ====================== PAPER PARAMETERS ======================
PHI = (1 + np.sqrt(5)) / 2

# ====================== BASE CASE ======================
def c_path(path: str) -> float:
    """Binary fraction 0.path in [0,1) — exactly as in revised paper."""
    if not path:
        return 0.0
    frac = int(path, 2) / (1 << len(path))
    return frac

# ====================== FOLD FUNCTIONS ======================
def fold_golden(a: float, b: float) -> float:
    return a + b / PHI

def fold_modular(a: float, b: float, p: int = 17) -> float:
    return (a * b + a + 1) % p

def fold_xor_carry(a: float, b: float) -> tuple:
    """Returns (XOR, AND) tuple — multi-channel as specified."""
    return (a ^ b, a & b)   # works on floats via bit ops (Python int conversion)

def fold_mobius(a: float, b: float) -> float:
    """Möbius with recommended params (α=φ, β=1, γ=1, δ=φ)"""
    z = complex(a, b)
    num = PHI * z + 1
    den = z + PHI
    return np.abs(num / den)

def fold_pack_g2(a: float, b: float, lca: int, d: int) -> float:
    """pACK-G2 — exploratory fifth candidate (parameters as discussed)."""
    z = complex(a, b)
    conformal = np.abs((PHI * z + 1) / (z + PHI))
    exp_term = np.exp(-0.018 * (lca / d)**2)
    carry_term = b / PHI
    diff_term = 0.075 * abs(a - b) * (2 ** -lca)
    # Local Ricci placeholder (simple second-difference curvature proxy)
    ricci_proxy = 0.12 * (a + b - 2 * ((a + b) / 2))  # placeholder
    return conformal * exp_term + carry_term + diff_term * (1 + ricci_proxy)

# ====================== TREE BUILDER (bottom-up for efficiency) ======================
def build_tree(depth: int, fold_func, fold_name: str):
    """Bottom-up level-by-level computation. Returns leaf values in Morton order."""
    # At level 0 (leaves): 2^depth values
    n_leaves = 1 << depth
    leaves = np.zeros(n_leaves, dtype=np.float64)
    
    for i in range(n_leaves):
        path = f'{i:0{depth}b}'
        leaves[i] = c_path(path)
    
    current_level = leaves.copy()
    
    for level in range(1, depth + 1):
        parent_size = len(current_level) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)
        
        for i in range(parent_size):
            left = current_level[2 * i]
            right = current_level[2 * i + 1]
            lca_depth = depth - level  # distance to leaves
            
            if fold_name == "XOR-Carry":
                # For tuple fold we keep only first channel for simplicity in demo
                next_level[i] = fold_func(left, right)[0]
            elif fold_name == "pACK-G2":
                next_level[i] = fold_pack_g2(left, right, lca=lca_depth, d=depth)
            else:
                next_level[i] = fold_func(left, right)
        
        current_level = next_level
    
    root_value = current_level[0]
    return leaves, root_value

# ====================== MEASUREMENTS ======================
def morton_to_xy(idx: int, depth: int):
    """Convert Morton index to (x, y) coordinates."""
    x = y = 0
    for i in range(depth):
        x |= ((idx >> (2 * i)) & 1) << i
        y |= ((idx >> (2 * i + 1)) & 1) << i
    return x, y

def compute_correlation(leaves: np.ndarray, depth: int):
    """Two-point correlation C(r) on 2D grid (log-log fit for power-law)."""
    n = 1 << depth
    values = leaves
    coords = [morton_to_xy(i, depth) for i in range(n)]
    coords = np.array(coords)
    
    # Sample pairs (efficient random sampling for large n)
    n_samples = min(50_000, n * n // 2)
    i1 = np.random.randint(0, n, n_samples)
    i2 = np.random.randint(0, n, n_samples)
    dists = np.abs(coords[i1] - coords[i2]).sum(axis=1)
    corrs = values[i1] * values[i2]
    
    # Bin by distance
    max_r = int(np.sqrt(2) * (1 << (depth-1)))
    bins = np.arange(max_r + 1)
    hist_corr = np.bincount(dists, weights=corrs, minlength=max_r+1)
    hist_count = np.bincount(dists, minlength=max_r+1)
    C_r = np.zeros(max_r + 1)
    mask = hist_count > 0
    C_r[mask] = hist_corr[mask] / hist_count[mask]
    
    # Power-law fit on log-log (r > 0)
    valid = (bins > 0) & mask
    log_r = np.log(bins[valid])
    log_C = np.log(C_r[valid])
    slope, intercept, r_value, _, _ = linregress(log_r, log_C)
    return bins, C_r, slope, r_value**2

# ====================== MAIN TEST ======================
def run_test(depth=12):
    folds = {
        "Golden": fold_golden,
        "Modular (p=17)": lambda a,b: fold_modular(a,b,17),
        "XOR-Carry": fold_xor_carry,
        "Möbius": fold_mobius,
        "pACK-G2 (exploratory)": None  # handled specially
    }
    
    print(f"=== Testing Recursive Fold Architecture at depth d={depth} ===\n")
    
    for name, func in folds.items():
        print(f"Running {name} fold...")
        if name == "pACK-G2 (exploratory)":
            leaves, root = build_tree(depth, None, "pACK-G2")
        else:
            leaves, root = build_tree(depth, func, name)
        
        r_bins, C_r, slope, r2 = compute_correlation(leaves, depth)
        
        print(f"  Root value: {root:.6f}")
        print(f"  Correlation power-law exponent: {slope:.3f} (R²={r2:.3f})")
        print(f"  Mean leaf value: {leaves.mean():.4f}")
        print("-" * 60)

# ====================== RUN ======================
if __name__ == "__main__":
    run_test(depth=12)   # change to 10, 14, 16 as resources allow
    # For deeper runs (d=20+), increase sampling or run on cluster