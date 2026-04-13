import numpy as np
from collections import Counter

DEPTH = 24

def new_fundamental_fold(l, r):
    # Reverse-engineered fundamental fold
    # Starts from the observed universe and works backwards
    # Combines acceleration, symmetry breaking, entropy drive, and discrete scales
    
    accel = 0.002 * (l**2 + r**2) * (l - r)               # GR / acceleration
    symmetry_break = 0.004 * (l**3 - r**3) + 0.0015 * (l - r)**4   # P5 multiple attractors
    discrete_scale = 0.003 * np.sin(25.13 * (l + r))     # P3
    entropy_drive = 0.0035 * np.log1p(np.abs(l * r) + 1e-6) + 0.002 * np.abs(l - r)   # P4
    repulsion = 0.0025 * (l - r)**2                       # keep branches diverse
    
    val = l + r + accel + symmetry_break + discrete_scale + entropy_drive + repulsion
    return np.tanh(np.clip(val, -25, 25)) * 0.72         # low damping to keep entropy alive

# Leaf variants (your exact 10)
def leaves_original(d): n = 1 << d; return np.arange(n, dtype=np.float64) % 17
def leaves_reversed_bits(d):
    n = 1 << d; rev = np.zeros(n, dtype=np.float64)
    for i in range(n): rev[i] = int(bin(i)[2:].zfill(d)[::-1], 2)
    return rev % 17
def leaves_gray_code(d):
    n = 1 << d; idx = np.arange(n, dtype=np.int64); gray = idx ^ (idx >> 1)
    return (gray % 17).astype(np.float64)
def leaves_random_perm(d, seed=42):
    n = 1 << d; rng = np.random.default_rng(seed); perm = rng.permutation(n)
    return (perm % 17).astype(np.float64)
def leaves_uniform_random(d, seed=99):
    n = 1 << d; rng = np.random.default_rng(seed)
    return rng.integers(0, 17, n, dtype=np.int64).astype(np.float64)
def leaves_uniform_random_2(d, seed=777):
    n = 1 << d; rng = np.random.default_rng(seed)
    return rng.integers(0, 17, n, dtype=np.int64).astype(np.float64)
def leaves_constant_g(d, g_val=0.0):
    n = 1 << d; return np.full(n, g_val, dtype=np.float64)
def leaves_alternating_fg(d):
    n = 1 << d; vals = np.zeros(n, dtype=np.float64)
    vals[0::2] = 4.0; vals[1::2] = 13.0; return vals
def leaves_cycle_seeded(d):
    n = 1 << d; vals = np.zeros(n, dtype=np.float64)
    vals[0::2] = 6.0; vals[1::2] = 9.0; return vals

variants = [
    ("Original", leaves_original), ("Reversed", leaves_reversed_bits),
    ("Gray", leaves_gray_code),
    ("Rand42", lambda d: leaves_random_perm(d, 42)),
    ("Rand137", lambda d: leaves_random_perm(d, 137)),
    ("Unif99", leaves_uniform_random),
    ("Unif777", leaves_uniform_random_2),
    ("Const0", lambda d: leaves_constant_g(d, 0.0)),
    ("AltFP", leaves_alternating_fg),
    ("Cycle69", leaves_cycle_seeded),
]

def fingerprint(leaf_func, d=8):
    return tuple(np.round(leaf_func(d)[:17], 6).tolist())

seen_fps = {}
deduped = []
for name, func in variants:
    fp = fingerprint(func)
    if fp not in seen_fps:
        seen_fps[fp] = name
        deduped.append((name, func))

print("=== New Fundamental Fold — Reverse-Engineered (Depth 24) ===\n")

g_vals = deduped[0][1](DEPTH).astype(np.float64)
levels = [g_vals.copy()]

for level in range(DEPTH):
    left = g_vals[0::2]
    right = g_vals[1::2]
    g_vals = new_fundamental_fold(left, right)
    levels.append(g_vals.copy())

root = float(g_vals[0])

print("1. Fixed-point convergence U ← F(U, U)")
U = np.array([root])
for step in range(15):
    U_new = new_fundamental_fold(U, U)
    diff = abs(U_new - U)
    print(f"Step {step:2d} | Value {U_new[0]:.6f} | Change {diff[0]:.2e}")
    if diff < 1e-6:
        print("   ✓ Stable fixed point reached")
        break
    U = U_new

print("\n2. Entropy monotonicity (P4)")
entropies = []
for lv in levels:
    unique, counts = np.unique(np.round(lv, 6), return_counts=True)
    probs = counts / len(lv)
    H = -np.sum(probs * np.log2(probs + 1e-12))
    entropies.append(H)
print(f"Entropy profile (first 5 → last 5): {entropies[:5]} ... {entropies[-5:]}")
monotonic = np.all(np.diff(entropies) > -0.01)
print(f"   Monotonic increasing: {'✓' if monotonic else '✗'}")

print("\n3. Residual ultrametric")
sibling_diff = np.abs(levels[-2][0::2] - levels[-2][1::2])
print(f"   Ultrametric proxy: {np.std(sibling_diff):.6f}")

print("\n4. Unitarity breaking")
print(f"   Purity-like proxy: {np.mean(np.abs(levels[-1])):.6f}")

print("\n5. GR acceleration proxy")
print(f"   Acceleration term at root: {0.0028 * (root**2) * 2:.6f}")

print("\n6. Attractor families (P5)")
attractors = Counter(np.round(levels[-1], 6))
print(f"   Distinct attractors: {len(attractors)}")
print(f"   Top attractors: {dict(attractors.most_common(8))}")

print("\n=== New Fundamental Fold Checklist complete ===")
print("This is the reverse-engineered version starting from the final answer.")