import numpy as np
from scipy.stats import linregress, entropy
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

PHI = (1 + np.sqrt(5)) / 2

def c_path(path: str) -> float:
    if not path: return 0.0
    return int(path, 2) / (1 << len(path))

# ====================== AGGRESSIVELY TUNED pACK-G2 (test8) ======================
def fold_pack_g2(a, b, lca, d):
    """pACK-G2 — FINAL AGGRESSIVE TUNING for target exponent ~−0.7 + attractors"""
    z = complex(a, b)
    conformal = np.abs((PHI * z + 1) / (z + PHI))
    exp_term = np.exp(-0.0085 * (lca / d)**2)          # slower decay for longer-range power-law
    carry_term = b / PHI
    diff_term = 0.42 * abs(a - b) * (2 ** -lca)        # STRONGER differentiation (as requested)
    # Enhanced nonlinear Ricci-like curvature (sin + cubic + quartic)
    ricci_proxy = (0.22 * np.sin(np.pi * (a + b)) +
                   0.15 * (a - b)**3 +
                   0.08 * (a - b)**4)
    return conformal * exp_term + carry_term + diff_term * (1 + ricci_proxy)

# ====================== OTHER FOLDS ======================
def fold_golden(a, b): return a + b / PHI

def fold_modular(a, b, p=17): return (a * b + a + 1) % p

def fold_xor_carry(a, b):
    ia, ib = int(a), int(b)
    return (ia ^ ib, ia & ib)

def fold_mobius(a, b):
    z = complex(a, b)
    return np.abs((PHI * z + 1) / (z + PHI))

# ====================== TREE BUILDER ======================
def build_tree(depth: int, fold_func, fold_name: str):
    n = 1 << depth
    leaves = np.array([c_path(f'{i:0{depth}b}') for i in range(n)], dtype=np.float64)
    current = leaves.copy()
    level_values = [leaves.copy()]

    for level in range(1, depth + 1):
        parent_size = len(current) // 2
        next_level = np.zeros(parent_size, dtype=np.float64)
        lca = depth - level

        for i in range(parent_size):
            left, right = current[2*i], current[2*i+1]
            if fold_name == "XOR-Carry":
                next_level[i] = fold_func(left, right)[0]
            elif fold_name == "pACK-G2":
                next_level[i] = fold_func(left, right, lca, depth)
            else:
                next_level[i] = fold_func(left, right)
        current = next_level
        level_values.append(current.copy())

    return leaves, current[0], level_values

# ====================== MEASUREMENTS ======================
def compute_correlation(leaves, depth, n_samples=80000):
    n = len(leaves)
    coords = np.zeros((n, 2), dtype=int)
    for i in range(n):
        x = y = 0
        for bit in range(depth):
            x |= ((i >> (2*bit)) & 1) << bit
            y |= ((i >> (2*bit + 1)) & 1) << bit
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

    valid = (bins >= 1) & mask
    if np.sum(valid) < 5:
        return bins, C_r, np.nan, 0.0
    log_r = np.log(bins[valid])
    log_C = np.log(C_r[valid] + 1e-12)
    slope, _, r_value, _, _ = linregress(log_r, log_C)
    return bins, C_r, slope, r_value**2

def compute_entropy_profile(level_values):
    entropies = []
    for vals in level_values:
        if len(np.unique(vals)) == 1:
            entropies.append(0.0)
            continue
        hist, _ = np.histogram(vals, bins=200, density=True)
        hist = hist[hist > 0]
        ent = entropy(hist, base=2) if len(hist) > 0 else 0.0
        entropies.append(ent)
    return entropies

def simple_attractor_scan(fold_func, fold_name, depth, n_samples=8000):
    fixed = set()
    cycles = []
    for _ in range(n_samples):
        x = np.random.uniform(0, 1)
        seen = {}
        for step in range(50):
            if fold_name == "XOR-Carry":
                nxt = fold_func(x, x)[0]
            elif fold_name == "pACK-G2":
                nxt = fold_func(x, x, 0, depth)
            else:
                nxt = fold_func(x, x)
            nxt = round(float(nxt), 6)
            if nxt in seen:
                period = step - seen[nxt]
                if period == 0:
                    fixed.add(nxt)
                elif 1 <= period <= 15:
                    cycles.append((nxt, period))
                break
            seen[nxt] = step
            x = nxt
    return len(fixed), len(set(cycles))

# ====================== MAIN ======================
def full_test(depth=14, plot=True):
    print(f"=== pACK-G2 FINAL AGGRESSIVE TUNING (test8) — depth d={depth} ===\n")
    
    test_folds = {
        "Golden": fold_golden,
        "Modular (p=17)": lambda a,b: fold_modular(a,b,17),
        "XOR-Carry": fold_xor_carry,
        "Möbius": fold_mobius,
        "pACK-G2": None
    }
    
    for name, func in test_folds.items():
        print(f"→ {name}")
        if name == "pACK-G2":
            fold_func = fold_pack_g2
        else:
            fold_func = func
            
        leaves, root, level_vals = build_tree(depth, fold_func, name)
        
        r_bins, C_r, slope, r2 = compute_correlation(leaves, depth)
        ent_profile = compute_entropy_profile(level_vals)
        n_fixed, n_cycles = simple_attractor_scan(fold_func, name, depth)
        
        print(f"   Root value          : {root:.6f}")
        print(f"   Power-law exponent  : {slope:.3f} (R² = {r2:.3f})")
        print(f"   Entropy (leaf → root): {ent_profile[0]:.3f} → {ent_profile[-1]:.3f}")
        print(f"   Attractors          : {n_fixed} fixed, {n_cycles} short cycles")
        print(f"   Mean leaf           : {leaves.mean():.4f}")
        print("-" * 90)
        
        if plot and name in ["Golden", "pACK-G2"]:
            plt.figure(figsize=(7,4))
            plt.loglog(r_bins[1:], C_r[1:], 'o-', label=f'{name} (slope {slope:.3f})')
            plt.xlabel('Distance r (Manhattan)')
            plt.ylabel('C(r)')
            plt.title(f'Spatial correlation — {name} (d={depth})')
            plt.legend()
            plt.grid(True, which='both', alpha=0.3)
            plt.show()

if __name__ == "__main__":
    full_test(depth=14, plot=True)   # Try depth=16 if you want maximum structure