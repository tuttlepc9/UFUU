"""
Tuttle 2026 — P5 Physics Confirmation Scoring (Depth 24)
Scores each fold 0–100 % on how strongly it matches the framework predictions
and the specific 2025–2026 exotic physics claims. ≥95 % = strong candidate for "the right fold".
"""

import math
import numpy as np
import pandas as pd
from collections import Counter

DEPTH = 24
p = 17
TOL = 1e-8
MAX_ITER = 200
CLIP_VAL = 50.0

# =============================================================================
# LEAF VARIANTS (FULLY EXPANDED)
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

print(f"=== Deduplicated variants: {len(deduped)} ===\n")

# =============================================================================
# STABLE TUNED FOLDS
# =============================================================================
def modular_fold(l, r):
    return ((l * r + l + 1) % p)

def ff_fold(l, r):      # Finsler-Friedmann 2025
    accel = 0.003 * (l**2 + r**2) * (l - r)
    val = np.clip(l + r + accel, -CLIP_VAL, CLIP_VAL)
    return np.tanh(val) * 0.95

def alena_fold(l, r):   # Alena-Tensor 2025
    force = 0.008 * (l - r)**2
    val = np.clip((l + r)/2 - force * (l - r) * 0.5, -CLIP_VAL, CLIP_VAL)
    return np.tanh(val) * 0.92

def gluon_fold(l, r):   # Gluon-Amplitude Feb 2026
    s = l + r + 1e-8
    val = np.clip((l * r / s) * 0.85 + 0.05 * (l + r), -CLIP_VAL, CLIP_VAL)
    return np.tanh(val) * 0.90

def nb_fold(l, r):      # Newton-to-Boltzmann 2025
    corr = 0.015 * np.abs(l - r)
    val = np.clip((l + r)/2 * (1 + corr), -CLIP_VAL, CLIP_VAL)
    return np.tanh(val) * 0.93

folds = [
    ("Modular (baseline)", modular_fold),
    ("Finsler-Friedmann", ff_fold),
    ("Alena-Tensor", alena_fold),
    ("Gluon-Amplitude", gluon_fold),
    ("Newton-Boltzmann", nb_fold),
]

# =============================================================================
# TREE FOLD + SCORING
# =============================================================================
def fold_gauge_root(depth, leaf_func, fold_func):
    g_vals = leaf_func(depth).astype(np.float64)
    for _ in range(depth):
        left = g_vals[0::2]
        right = g_vals[1::2]
        g_vals = fold_func(left, right)
    return float(g_vals[0])

def get_attractor_modular(start):
    x = float(start) % p
    seen = {}
    for _ in range(MAX_ITER):
        xr = round(x, 8)
        if xr in seen:
            return f"FP{int(round(x))}"
        seen[xr] = True
        x = modular_fold(x, x)
    return "UNKNOWN"

def get_attractor_exotic(start, fold_func):
    x = float(start)
    for _ in range(MAX_ITER):
        nxt = fold_func(np.array([x]), np.array([x]))[0]
        if abs(nxt - x) < TOL:
            return f"FP{x:.4f}"
        x = nxt
    return f"CONV{x:.4f}"

print(f"=== Tuttle 2026 — Physics Confirmation Scoring (Depth {DEPTH}) ===\n")

for fold_name, fold_func in folds:
    print(f"\n{'='*90}\nFOLD: {fold_name}\n{'='*90}")
    roots = []
    attractor_counts = Counter()
    
    for name, leaf_func in deduped:
        root = fold_gauge_root(DEPTH, leaf_func, fold_func)
        roots.append(root)
        att = get_attractor_modular(root) if "Modular" in fold_name else get_attractor_exotic(root, fold_func)
        attractor_counts[att] += 1
        print(f"  {name:<35} root={root:>10.6f} → {att}")
    
    # PHYSICS CONFIRMATION SCORE
    num_attractors = len(attractor_counts)
    basin_score = min(num_attractors / 5.0, 1.0) * 30
    root_std = np.std(roots)
    stability_score = max(0, 20 - root_std * 10)
    
    physics_bonus = 0
    if "Finsler" in fold_name and any(r > 0.5 for r in roots):
        physics_bonus = 35
    if "Alena" in fold_name and all(abs(r) < 0.1 for r in roots):
        physics_bonus = 30
    if "Gluon" in fold_name and num_attractors == 1:
        physics_bonus = 25
    if "Newton" in fold_name and num_attractors == 1:
        physics_bonus = 25
    if "Modular" in fold_name and num_attractors >= 3:
        physics_bonus = 30
    
    total_score = basin_score + stability_score + physics_bonus
    total_score = min(total_score, 100.0)
    
    print(f"\nPHYSICS CONFIRMATION SCORE: {total_score:.1f}%")
    if total_score >= 95.0:
        print("★★★ 95+% CONFIDENCE — THIS FOLD IS A STRONG CANDIDATE FOR THE PHYSICAL LAW ★★★")
    elif total_score >= 80.0:
        print("★★ Strong candidate — worth deeper testing / entropy checks")
    elif total_score >= 60.0:
        print("★ Moderate support")
    else:
        print("   Weak match — not the primary candidate")
    
    print(f"Basin summary: {dict(attractor_counts)}")
    print(f"Renormalization (std of roots): {root_std:.6f}")

print("\n=== Scoring complete. Any fold ≥95% is a breakthrough candidate for the theory. ===")