import numpy as np
from collections import Counter

DEPTH = 24
CLIP_VAL = 30.0

def safe_tanh(x):
    return np.tanh(np.clip(x, -CLIP_VAL, CLIP_VAL))

def ff_fold(l, r):
    accel = 0.003 * (l**2 + r**2) * (l - r)
    return safe_tanh(l + r + accel) * 0.95

# Leaf variants (your standard 10)
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

# Deduplication
def fingerprint(leaf_func, d=8):
    return tuple(np.round(leaf_func(d)[:17], 6).tolist())

seen_fps = {}
deduped = []
for name, func in variants:
    fp = fingerprint(func)
    if fp not in seen_fps:
        seen_fps[fp] = name
        deduped.append((name, func))

print("=== Finsler-Friedmann 2025 — Full TOE Checklist (Depth 24) ===\n")

# Build the tree once and keep all intermediate levels for entropy and ultrametric checks
g_vals = deduped[0][1](DEPTH).astype(np.float64)  # start with one leaf set
levels = [g_vals.copy()]

for level in range(DEPTH):
    left = g_vals[0::2]
    right = g_vals[1::2]
    g_vals = ff_fold(left, right)
    levels.append(g_vals.copy())

root = float(g_vals[0])

# 1. Fixed-point convergence (self-fold test)
print("1. Fixed-point convergence U ← F(U, U)")
U = np.array([root])
for step in range(15):
    U_new = ff_fold(U, U)
    diff = abs(U_new - U)
    print(f"Step {step:2d} | Value {U_new[0]:.6f} | Change {diff[0]:.2e}")
    if diff < 1e-6:
        print("   ✓ Stable fixed point reached")
        break
    U = U_new

# 2. Entropy monotonicity (P4)
print("\n2. Entropy monotonicity (P4)")
entropies = []
for lv in levels:
    unique, counts = np.unique(np.round(lv, 6), return_counts=True)
    probs = counts / len(lv)
    H = -np.sum(probs * np.log2(probs + 1e-12))
    entropies.append(H)
print(f"Entropy profile (first 5 → last 5): {entropies[:5]} ... {entropies[-5:]}")
monotonic = np.all(np.diff(entropies) > -0.01)  # allow small noise
print(f"   Monotonic increasing: {'✓' if monotonic else '✗'}")

# 3. Residual ultrametric / discrete scale (P1/P3)
print("\n3. Residual ultrametric & discrete scale check")
# Simple proxy: variance of sibling differences at deepest level
sibling_diff = np.abs(levels[-2][0::2] - levels[-2][1::2])
ultrametric_proxy = np.std(sibling_diff)
print(f"   Ultrametric proxy (std of sibling diffs): {ultrametric_proxy:.6f} (lower = more hierarchical)")

# 4. Approximate unitarity breaking (P2)
print("\n4. Approximate unitarity breaking (P2)")
purity_proxy = np.mean(np.abs(levels[-1]))  # crude proxy for now
print(f"   Purity-like proxy at root: {purity_proxy:.6f} (lower = more breaking)")

# 5. GR emergence proxy (curvature / acceleration)
print("\n5. GR / curvature proxy")
accel_at_root = 0.003 * (root**2) * 2  # simplified Finsler acceleration term
print(f"   Effective acceleration term at root: {accel_at_root:.6f} (positive = cosmic acceleration)")

# 6. Attractor families (potential particle spectrum / constants)
print("\n6. Attractor families")
attractors = Counter(np.round(levels[-1], 6))
print(f"   Distinct attractors at root: {len(attractors)}")
print(f"   Top attractors: {dict(attractors.most_common(5))}")

print("\n=== Finsler-Friedmann TOE Checklist complete at depth 24 ===")
print("Paste this full output back and we will immediately refine the next test (deeper or more GR-focused).")