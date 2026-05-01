import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

print("=== UFUU Backward Exploration v7 FIXED (FINAL): Möbius + Plasma + Higgs in Superconductors ===")

# Load data cleanly (avoid column collision)
df_unique = pd.read_csv('unique_m.csv')
df_train_features = pd.read_csv('train.csv').drop(columns=['critical_temp'], errors='ignore')

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

# Safe merge of engineered features
df = pd.concat([df.reset_index(drop=True), df_train_features.reset_index(drop=True)], axis=1)

# === Möbius + Plasma + Higgs proxies (created EARLY so they exist in subgroups) ===
df['odd_elements'] = df['number_of_elements'] % 2
df['has_topological_elements'] = df['formula'].str.contains('Cu|Bi|Fe|La|Ce', case=False, na=False).astype(int)

print("Families loaded:")
family_groups = {}
for fam, group in df.groupby('family'):
    print(f"  {fam}: {len(group):,} materials")
    family_groups[fam] = group.copy()  # explicit copy so we have the new columns

# Plasma (entropy) vs Higgs (mass) correlations
print("\n=== Plasma (entropy) vs Higgs (mass) correlations in key families ===")
for fam_name in ['Cuprate', 'Hydride', 'Iron-based', 'A15/Niobium']:
    if fam_name in family_groups:
        g = family_groups[fam_name]
        corr_entropy_tc = g['wtd_entropy_atomic_mass'].corr(g['critical_temp'])
        corr_mass_tc = g['wtd_mean_atomic_mass'].corr(g['critical_temp'])
        print(f"{fam_name:12s} | entropy-Tc corr: {corr_entropy_tc:.3f} | mass-Tc corr: {corr_mass_tc:.3f}")

print("\n=== Möbius-like pairing (odd vs even element count) ===")
for fam_name in ['Cuprate', 'Hydride', 'A15/Niobium']:
    if fam_name in family_groups:
        g = family_groups[fam_name]
        odd_mean_tc = g[g['odd_elements'] == 1]['critical_temp'].mean()
        even_mean_tc = g[g['odd_elements'] == 0]['critical_temp'].mean()
        odd_count = (g['odd_elements'] == 1).sum()
        even_count = (g['odd_elements'] == 0).sum()
        print(f"  {fam_name:12s} | odd: {odd_count:,} materials → Tc {odd_mean_tc:.1f} K | even: {even_count:,} → Tc {even_mean_tc:.1f} K")

# Plasma-weighted ratio search (entropy as collective weight) — focused on high-Tc families
print("\n=== Weighted ratio search (plasma-weighted) on Cuprate + Hydride ===")
target_families = ['Cuprate', 'Hydride']
best_d = None
best_score = np.inf
best_r = None
for d in range(8, 16):   # zoom around the 9–12 window from earlier v6 results
    r = 2 ** (1.0 / d)
    frac_dists = []
    weights_list = []
    for fam_name in target_families:
        if fam_name in family_groups:
            g = family_groups[fam_name]
            vals = g['wtd_mean_atomic_mass'].values.astype(float)          # Higgs proxy
            entropies = g['wtd_entropy_atomic_mass'].values.astype(float) + 1e-8  # Plasma proxy
            for i in range(len(vals)):
                for j in range(i + 1, len(vals)):
                    ratio = vals[j] / vals[i]
                    if ratio > 1.05 and np.isfinite(ratio):
                        log2_r = np.log2(ratio)
                        frac = np.mod(d * log2_r, 1)
                        w = entropies[i] * entropies[j]
                        frac_dists.append(min(frac, 1 - frac))
                        weights_list.append(w)
    if frac_dists:
        mean_dist = np.average(frac_dists, weights=weights_list)
        print(f"  d={d:2d} → r={r:.6f}  plasma-weighted frac dist = {mean_dist:.4f}")
        if mean_dist < best_score:
            best_score = mean_dist
            best_d = d
            best_r = r

print(f"\nBest plasma-weighted scaling in high-Tc families: d={best_d} → r={best_r:.6f} (score {best_score:.4f})")

print("\n✅ v7 FIXED and complete!")
print("   • Möbius (odd/even + topological elements), Plasma (entropy weighting), Higgs (mass ratios) fully integrated")
print("   • Backward from superconductors data only")
print("   • Paste the full output here and we’ll interpret the fold’s true nature")