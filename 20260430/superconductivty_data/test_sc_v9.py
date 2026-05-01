import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

print("=== UFUU Backward Exploration v9: Plasma-Focused Probe (Cuprates only) ===")

# Load data
df_unique = pd.read_csv('unique_m.csv')
df_train = pd.read_csv('train.csv').drop(columns=['critical_temp'], errors='ignore')
df = df_unique[['material', 'critical_temp']].copy().rename(columns={'material': 'formula'})
df = df[df['critical_temp'] > 1].copy()

def get_family(formula):
    f = str(formula).upper()
    if 'CU' in f or 'YBA' in f or 'BI2SR' in f: return 'Cuprate'
    else: return 'Other'

df['family'] = df['formula'].apply(get_family)
df = pd.concat([df.reset_index(drop=True), df_train.reset_index(drop=True)], axis=1)

# Plasma proxy = weighted entropy
plasma_feature = 'wtd_entropy_atomic_mass'

# Restrict to cuprates (strongest plasma signal)
cuprates = df[df['family'] == 'Cuprate'].copy()
print(f"Cuprate materials: {len(cuprates):,}")

# 1. Plasma strength vs Tc
print(f"\nPlasma (entropy) vs Tc correlation in cuprates: {cuprates[plasma_feature].corr(cuprates['critical_temp']):.3f}")

# 2. Search for scaling in the plasma observable itself (entropy ratios)
print("\n=== Scaling search on plasma proxy (entropy ratios) in cuprates ===")
unique_entropy = sorted(cuprates[plasma_feature].unique())
ratios = []
for i in range(len(unique_entropy)):
    for j in range(i+1, len(unique_entropy)):
        ratio = unique_entropy[j] / unique_entropy[i]
        if ratio > 1.05:
            ratios.append(ratio)

ratios = np.array(ratios)
print(f"Entropy ratios computed: {len(ratios):,}")

r_theory = 2 ** (1/12)
n_values = np.round(np.log(ratios) / np.log(r_theory))
dev_pct = np.abs(ratios - r_theory**n_values) / (r_theory**n_values) * 100

print(f"Mean deviation from 2^(n/12): {dev_pct.mean():.3f}%")
frac_dist = np.mean(np.minimum(np.mod(12 * np.log2(ratios), 1), 1 - np.mod(12 * np.log2(ratios), 1)))
print(f"Frac dist (12×log₂): {frac_dist:.4f} (random ≈ 0.25)")

# 3. Plasma-binned Tc ratio test (high-plasma vs low-plasma subgroups)
print("\n=== Plasma-binned Tc ratios (high vs low entropy) ===")
median_entropy = cuprates[plasma_feature].median()
high_plasma = cuprates[cuprates[plasma_feature] > median_entropy]
low_plasma  = cuprates[cuprates[plasma_feature] <= median_entropy]

def compute_ratios(group):
    tcs = sorted(group['critical_temp'].unique())
    rs = []
    for i in range(len(tcs)):
        for j in range(i+1, len(tcs)):
            r = tcs[j] / tcs[i]
            if r > 1.1: rs.append(r)
    return np.array(rs) if rs else np.array([])

high_ratios = compute_ratios(high_plasma)
low_ratios  = compute_ratios(low_plasma)

for name, rs in [('High-plasma', high_ratios), ('Low-plasma', low_ratios)]:
    if len(rs) > 0:
        frac_dist = np.mean(np.minimum(np.mod(12 * np.log2(rs), 1), 1 - np.mod(12 * np.log2(rs), 1)))
        print(f"{name:12s} | {len(rs):,} ratios | frac dist = {frac_dist:.4f}")

# Plots
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(cuprates[plasma_feature], bins=80, alpha=0.75, color='purple')
plt.xlabel('Plasma proxy (wtd_entropy_atomic_mass)')
plt.ylabel('Count')
plt.title('Plasma Strength Distribution in Cuprates')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.scatter(cuprates[plasma_feature], np.log10(cuprates['critical_temp']), alpha=0.3, s=10)
plt.xlabel('Plasma proxy (entropy)')
plt.ylabel('log₁₀(Tc)')
plt.title('Plasma Strength vs log(Tc) in Cuprates')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n✅ v9 plasma probe complete!")
print("   • Focused exclusively on cuprates + entropy as plasma proxy")
print("   • Paste the output + plots and we’ll see if the fold pattern sharpens here.")