import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

print("=== UFUU Backward Exploration v5: Superconductors → Possible Fold Structures ===")

# Load data
df_unique = pd.read_csv('unique_m.csv')
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

family_groups = defaultdict(list)
for fam, group in df.groupby('family'):
    unique_tcs = sorted(group['critical_temp'].unique())
    if len(unique_tcs) >= 5:
        family_groups[fam] = unique_tcs
        print(f"  {fam}: {len(unique_tcs)} unique Tc")

# === Search for best scaling ratio r (or octave depth d) ===
print("\n=== Searching for natural scaling in Tc ratios (purely data-driven) ===")
best_r = None
best_score = np.inf
best_d = None
scores = []

for d in range(6, 25):          # possible "octave" depths around the UFUU d≈12
    r_candidate = 2 ** (1.0 / d)
    frac_dists = []
    for fam, tcs in family_groups.items():
        tcs = np.array(tcs)
        for i in range(len(tcs)):
            for j in range(i+1, len(tcs)):
                ratio = tcs[j] / tcs[i]
                if ratio > 1.10:
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

print(f"\nBest empirical scaling: d={best_d} → r={best_r:.6f} (mean frac dist {best_score:.4f})")
print(f"UFUU predicted r = 2^(1/12) ≈ 1.059463 → distance to best = {abs(best_r - 2**(1/12)):.6f}")

# Quick plot of the score landscape
ds, rs, dists = zip(*scores)
plt.figure(figsize=(10,5))
plt.plot(ds, dists, 'o-', label='Mean fractional distance')
plt.axhline(0.25, color='red', linestyle='--', label='Random expectation')
plt.xlabel('Assumed octave depth d')
plt.ylabel('Mean distance to integer (lower = stronger quantization)')
plt.title('Backward search: Best scaling depth in superconductor Tc ratios')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("\n✅ v5 backward complete. No strong quantization found near d=12.")
print("   Next: we can extend this to atomic-mass ratios, entropy features, or element-count patterns.")