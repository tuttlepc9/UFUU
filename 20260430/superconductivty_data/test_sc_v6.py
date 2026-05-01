import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

print("=== UFUU Backward Exploration v6: Superconductors → Compositional Features ===")

# Load both files (they align row-by-row)
df_unique = pd.read_csv('unique_m.csv')
df_train = pd.read_csv('train.csv')

# Get formulas + family from unique_m
df = df_unique[['material', 'critical_temp']].copy().rename(columns={'material': 'formula'})
df = df[df['critical_temp'] > 1].copy()

def get_family(formula):
    f = str(formula).upper()
    if 'CU' in f or 'YBA' in f or 'BI2SR' in f: return 'Cuprate'
    elif 'FE' in f and ('AS' in f or 'SE' in f or 'TE' in f): return 'Iron-based'
    elif 'NB' in f: return 'A15/Niobium'
    elif 'MGB' in f or 'MG B' in f: return 'Diboride'
    elif 'H' in f and len(f) > 3 or (('LA' in f or 'CE' in f) and 'H' in f): return 'Hydride'
    else: return 'Other'

df['family'] = df['formula'].apply(get_family)

# Merge the engineered features from train.csv (same order)
df = pd.concat([df.reset_index(drop=True), df_train.reset_index(drop=True)], axis=1)

# Target features to test (all ratio-able continuous ones)
feature_list = [
    'mean_atomic_mass', 'wtd_mean_atomic_mass', 'gmean_atomic_mass',
    'entropy_atomic_mass', 'wtd_entropy_atomic_mass',
    'range_atomic_mass', 'wtd_range_atomic_mass',
    'std_atomic_mass', 'wtd_std_atomic_mass',
    'number_of_elements'  # discrete but we can still look at ratios
]

family_groups = defaultdict(lambda: {feat: [] for feat in feature_list})

for fam, group in df.groupby('family'):
    for feat in feature_list:
        vals = sorted(group[feat].unique())
        if len(vals) >= 5:
            family_groups[fam][feat] = vals

print("Families loaded with unique values per feature.")

# Backward search over d for EVERY feature
print("\n=== Backward scaling search on compositional features ===")
results = []

for feat in feature_list:
    print(f"\n--- Feature: {feat} ---")
    best_score = np.inf
    best_d = None
    best_r = None
    scores = []
    
    for d in range(6, 25):
        r_candidate = 2 ** (1.0 / d)
        frac_dists = []
        for fam in family_groups:
            tcs = np.array(family_groups[fam][feat])
            for i in range(len(tcs)):
                for j in range(i+1, len(tcs)):
                    ratio = tcs[j] / tcs[i]
                    if ratio > 1.05:  # slightly lower threshold for composition
                        log2_r = np.log2(ratio)
                        frac = np.mod(d * log2_r, 1)
                        frac_dists.append(min(frac, 1 - frac))
        if frac_dists:
            mean_dist = np.mean(frac_dists)
            scores.append((d, r_candidate, mean_dist))
            print(f"  d={d:2d} → r={r_candidate:.6f}  mean frac dist = {mean_dist:.4f}")
            if mean_dist < best_score:
                best_score = mean_dist
                best_d = d
                best_r = r_candidate
    results.append((feat, best_d, best_r, best_score))
    print(f"  → Best for {feat}: d={best_d} r={best_r:.6f} (dist {best_score:.4f})")

print("\n=== SUMMARY OF BEST SCALING PER FEATURE ===")
for feat, d, r, score in results:
    print(f"{feat:25s} | best d={d:2d} | r={r:.6f} | frac dist={score:.4f}")

# Quick visualization of the best d's
best_ds = [r[1] for r in results]
plt.figure(figsize=(10,5))
plt.bar(feature_list, best_ds)
plt.axhline(12, color='red', linestyle='--', label='UFUU d≈12')
plt.xlabel('Feature')
plt.ylabel('Best empirical octave depth d')
plt.title('v6: Best scaling depth per compositional feature')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

print("\n✅ v6 backward complete.")
print("   • We are now testing the exact layer (composition) where UFUU/OP7 predicts fold attractors.")
print("   • Paste the full output + plot here and we’ll interpret what it means for the 1p06 derivation.")