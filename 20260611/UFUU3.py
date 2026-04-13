import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

PHI = (1 + np.sqrt(5)) / 2

def c_path(path: str) -> float:
    if not path:
        return 0.0
    frac = int(path, 2) / (1 << len(path))
    return frac

# ====================== FOLDS ======================
def fold_golden(a: float, b: float) -> float:
    return a + b / PHI

def fold_modular(a: float, b: float, p: int = 17) -> float:
    return (a * b + a + 1) % p

def fold_xor_carry(a: float, b: float) -> tuple:
    ia, ib = int(a), int(b)
    return (ia ^ ib, ia & ib)

def fold_mobius(a: float, b: float) -> float:
    z = complex(a, b)
    num = PHI * z + 1
    den = z + PHI
    return np.abs(num / den)

def fold_pack_g2(a: float, b: float, lca: int, d: int) -> float:
    z = complex(a, b)
    conformal = np.abs((PHI * z + 1) / (z + PHI))
    exp_term = np.exp(-0.018 * (lca / d)**2)
    carry_term = b / PHI
    diff_term = 0.075 * abs(a - b) * (2 ** -lca)
    ricci_proxy = 0.12 * (a + b - 2 * ((a + b) / 2))
    return conformal * exp_term + carry_term + diff_term * (1 + ricci_proxy)

# ====================== TREE BUILDER ======================
def build_tree(depth: int, fold_func, fold_name: str):
    n_leaves = 1 << depth
    leaves = np.array([c_path(f'{i:0{depth}b}') for i in range(n_leaves)], dtype=np.float64)
    current = leaves.copy()

    for level in range(1, depth + 1):
        parent_size = len(current) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)
        lca = depth - level

        for i in range(parent_size):
            left, right = current[2*i], current[2*i + 1]
            if fold_name == "XOR-Carry":
                next_level[i] = fold_func(left, right)[0]          # XOR channel
            elif fold_name == "pACK-G2":
                next_level[i] = fold_pack_g2(left, right, lca, depth)
            else:
                next_level[i] = fold_func(left, right)
        current = next_level

    return leaves, current[0]

# ====================== CORRELATION (fixed) ======================
def compute_correlation(leaves: np.ndarray, depth: int, n_samples=50000):
    n = len(leaves)
    # Correct Morton -> (x, y)
    coords = np.zeros((n, 2), dtype=int)
    for i in range(n):
        x = y = 0
        for bit in range(depth):
            x |= ((i >> (2 * bit)) & 1) << bit
            y |= ((i >> (2 * bit + 1)) & 1) << bit
        coords[i] = [x, y]

    idx1 = np.random.randint(0, n, n_samples)
    idx2 = np.random.randint(0, n, n_samples)
    dists = np.abs(coords[idx1] - coords[idx2]).sum(axis=1)
    corrs = leaves[idx1] * leaves[idx2]

    max_r = dists.max() + 1
    bins = np.arange(max_r)
    hist_corr = np.bincount(dists, weights=corrs, minlength=max_r)
    hist_count = np.bincount(dists, minlength=max_r)
    
    mask = hist_count > 0
    C_r = np.zeros(max_r)
    C_r[mask] = hist_corr[mask] / hist_count[mask]
    
    # Power-law fit (r >= 1)
    valid = (bins >= 1) & mask
    if np.sum(valid) < 5:
        return bins, C_r, np.nan, 0.0
    log_r = np.log(bins[valid])
    log_C = np.log(C_r[valid] + 1e-12)
    slope, _, r_value, _, _ = linregress(log_r, log_C)
    return bins, C_r, slope, r_value**2

# ====================== MAIN ======================
def run_test(depth=12, plot=False):
    print(f"=== Recursive Fold Test — depth d={depth} ===\n")
    
    test_folds = {
        "Golden": fold_golden,
        "Modular (p=17)": lambda a,b: fold_modular(a,b,17),
        "XOR-Carry": fold_xor_carry,
        "Möbius": fold_mobius,
        "pACK-G2 (exploratory)": None
    }
    
    for name, func in test_folds.items():
        print(f"→ {name}")
        if name == "pACK-G2 (exploratory)":
            leaves, root = build_tree(depth, None, "pACK-G2")
        else:
            leaves, root = build_tree(depth, func, name)
        
        r_bins, C_r, slope, r2 = compute_correlation(leaves, depth)
        
        print(f"   Root value          : {root:.6f}")
        print(f"   Power-law exponent  : {slope:.3f} (R² = {r2:.3f})")
        print(f"   Mean leaf value     : {leaves.mean():.4f}")
        print("-" * 70)
        
        if plot and name in ["Golden", "Möbius", "pACK-G2 (exploratory)"]:
            plt.figure(figsize=(6,4))
            plt.loglog(r_bins[1:], C_r[1:], 'o-', label=f'{name} (slope {slope:.2f})')
            plt.xlabel('Distance r (Manhattan)')
            plt.ylabel('C(r)')
            plt.title(f'Spatial correlation — {name} (d={depth})')
            plt.legend()
            plt.grid(True, which='both', alpha=0.3)
            plt.show()

if __name__ == "__main__":
    run_test(depth=12, plot=True)   # ← change depth or set plot=False