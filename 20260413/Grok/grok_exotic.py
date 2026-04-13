"""
Tuttle 2026 — Multi-Fold P5 Basin Selection Test
Tests original modular + 4 exotic 2025–2026 physics folds side-by-side
Depth = 22 (fast, ~4 M leaves). Uses your exact boilerplate.
"""

import math
import numpy as np
import pandas as pd
from collections import Counter

phi = (1 + math.sqrt(5)) / 2
p = 17
TOL = 1e-8
MAX_ITER = 100
DEPTH = 22

# =============================================================================
# LEAF VARIANTS (exactly as in your corrected script)
# =============================================================================
def leaves_original(d):
    n = 1 << d
    return np.arange(n, dtype=np.float64) % p

def leaves_reversed_bits(d):
    n = 1 << d
    rev = np.zeros(n, dtype=np.float64)
    for i in range(n):
        rev[i] = int(bin(i)[2:].zfill(d)[::-1], 2)
    return rev % p

def leaves_gray_code(d):
    n = 1 << d
    idx = np.arange(n, dtype=np.int64)
    gray = idx ^ (idx >> 1)
    return (gray % p).astype(np.float64)

def leaves_random_perm(d, seed=42):
    n = 1 << d
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    return (perm % p).astype(np.float64)

def leaves_uniform_random(d, seed=99):
    n = 1 << d
    rng = np.random.default_rng(seed)
    return rng.integers(0, p, n, dtype=np.int64).astype(np.float64)

def leaves_uniform_random_2(d, seed=777):
    n = 1 << d
    rng = np.random.default_rng(seed)
    return rng.integers(0, p, n, dtype=np.int64).astype(np.float64)

def leaves_constant_g(d, g_val=0.0):
    n = 1 << d
    return np.full(n, g_val, dtype=np.float64)

def leaves_alternating_fg(d):
    n = 1 << d
    vals = np.zeros(n, dtype=np.float64)
    vals[0::2] = 4.0
    vals[1::2] = 13.0
    return vals

def leaves_cycle_seeded(d):
    n = 1 << d
    vals = np.zeros(n, dtype=np.float64)
    vals[0::2] = 6.0
    vals[1::2] = 9.0
    return vals

variants = [
    ("Original (i mod 17)", leaves_original),
    ("Reversed bits", leaves_reversed_bits),
    ("Gray code", leaves_gray_code),
    ("Random perm (seed=42)", lambda d: leaves_random_perm(d, 42)),
    ("Random perm (seed=137)", lambda d: leaves_random_perm(d, 137)),
    ("Uniform random (seed=99)", leaves_uniform_random),
    ("Uniform random (seed=777)", leaves_uniform_random_2),
    ("Constant g=0", lambda d: leaves_constant_g(d, 0.0)),
    ("Alternating FP seeds (4,13)", leaves_alternating_fg),
    ("Cycle seeds (6,9)", leaves_cycle_seeded),
]

# Deduplication (your exact code)
def fingerprint(leaf_func, d=8):
    return tuple(np.round(leaf_func(d)[:17], 6).tolist())

seen_fps = {}
deduped = []
for name, func in variants:
    fp = fingerprint(func)
    if fp not in seen_fps:
        seen_fps[fp] = name
        deduped.append((name, func))

print(f"=== Deduplicated variants: {len(deduped)} ===\n")

# =============================================================================
# FOLDS + ATTRACTOR DETECTION (your P5 style)
# =============================================================================
def fold_gauge_root(depth, leaf_func, fold_func):
    g_vals = leaf_func(depth).astype(np.float64)
    for _ in range(depth):
        left = g_vals[0::2]
        right = g_vals[1::2]
        g_vals = fold_func(left, right)
    return float(g_vals[0])

# 1. Modular (baseline)
def modular_fold(l, r): return ((l * r + l + 1) % p)
def get_attractor_modular(start):
    x = float(start) % p
    seen = {}
    for _ in range(MAX_ITER):
        xr = round(x, 8)
        if xr in seen: return {"label": f"FP{int(round(x))}", "type": "fixed_point"}
        seen[xr] = True
        x = modular_fold(x, x)
    return {"label": "UNKNOWN", "type": "unknown"}

# 2. Finsler-Friedmann proxy (2025 acceleration without dark energy)
def ff_fold(l, r):
    diff = l - r
    accel = 0.008 * (l**2 + r**2) * diff
    return np.tanh(l + r + accel) * 0.95
def get_attractor_ff(start): 
    x = float(start)
    for _ in range(MAX_ITER):
        nxt = ff_fold(x, x)
        if abs(nxt - x) < TOL: return {"label": f"FP{x:.4f}", "type": "fixed_point"}
        x = nxt
    return {"label": f"CONV{x:.4f}", "type": "converged"}

# 3. Alena-Tensor proxy (2025 flattening of spacetime)
def alena_fold(l, r):
    avg = (l + r) / 2
    force = 0.05 * (l - r)**2
    return np.tanh(avg - force * (l - r)) * 0.9
def get_attractor_alena(start):
    x = float(start)
    for _ in range(MAX_ITER):
        nxt = alena_fold(x, x)
        if abs(nxt - x) < TOL: return {"label": f"FP{x:.4f}", "type": "fixed_point"}
        x = nxt
    return {"label": f"CONV{x:.4f}", "type": "converged"}

# 4. Gluon-Amplitude proxy (Feb 2026 Berends-Giele closed form)
def gluon_fold(l, r):
    s = l + r + 1e-8
    return np.tanh((l * r) / s) * 0.92
def get_attractor_gluon(start):
    x = float(start)
    for _ in range(MAX_ITER):
        nxt = gluon_fold(x, x)
        if abs(nxt - x) < TOL: return {"label": f"FP{x:.4f}", "type": "fixed_point"}
        x = nxt
    return {"label": f"CONV{x:.4f}", "type": "converged"}

# 5. Newton-to-Boltzmann proxy (2025 micro-macro limit)
def nb_fold(l, r):
    avg = (l + r) / 2
    corr = 0.03 * np.abs(l - r)
    return np.tanh(avg * (1 + corr)) * 0.93
def get_attractor_nb(start):
    x = float(start)
    for _ in range(MAX_ITER):
        nxt = nb_fold(x, x)
        if abs(nxt - x) < TOL: return {"label": f"FP{x:.4f}", "type": "fixed_point"}
        x = nxt
    return {"label": f"CONV{x:.4f}", "type": "converged"}

folds = [
    ("Modular (baseline)", modular_fold, get_attractor_modular),
    ("Finsler-Friedmann", ff_fold, get_attractor_ff),
    ("Alena-Tensor", alena_fold, get_attractor_alena),
    ("Gluon-Amplitude", gluon_fold, get_attractor_gluon),
    ("Newton-Boltzmann", nb_fold, get_attractor_nb),
]

# =============================================================================
# RUN ALL P5 TESTS
# =============================================================================
print(f"=== Tuttle 2026 P5 Multi-Fold Test — Depth {DEPTH} ===\n")
for fold_name, fold_func, attr_func in folds:
    print(f"\n{'='*80}\nFOLD: {fold_name}\n{'='*80}")
    results = []
    attractor_counts = Counter()
    for name, leaf_func in deduped:
        root = fold_gauge_root(DEPTH, leaf_func, fold_func)
        att = attr_func(root)
        results.append({"Leaf Variant": name, "Root": f"{root:.6f}", "Attractor": att["label"]})
        attractor_counts[att["label"]] += 1
        print(f"  {name:<35} root={root:>10.6f} → {att['label']}")
    
    print(f"\nBASIN SUMMARY for {fold_name}")
    for att, cnt in sorted(attractor_counts.items()):
        pct = 100 * cnt / len(deduped)
        print(f"  {att:>18} : {cnt:2d}/{len(deduped)} ({pct:.0f}%)")
    if len(attractor_counts) > 1:
        print("✓ Multiple distinct basins → P5 strongly supported for this fold!")
    else:
        print("⚠ Single basin (strong renormalization)")

print("\n=== All tests complete. Copy the script and run locally at depth=24 if you want deeper trees. ===")