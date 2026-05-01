import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

print("=== UFUU OP9 T1 v2: Family-Grouped Superconductor Tc Ratio Test (FIXED) ===")

# Load data
df_train = pd.read_csv('train.csv')   # kept for compatibility / future use
df_unique = pd.read_csv('unique_m.csv')
print(f"Loaded {len(df_unique):,} unique materials\n")

# FIXED: unique_m.csv uses 'material' column for the chemical formula (not 'formula')
df = df_unique[['material', 'critical_temp']].copy().rename(columns={'material': 'formula'})
df = df[df['critical_temp'] > 1].copy()  # real superconductors only

# Simple family classifier (expandable)
def get_family(formula):
    f = formula.upper()
    if 'CU' in f or 'YBA' in f or 'BI2SR' in f:
        return 'Cuprate'
    elif 'FE' in f and ('AS' in f or 'SE' in f or 'TE' in f):
        return 'Iron-based'
    elif 'NB' in f:
        return 'A15/Niobium'
    elif 'MGB' in f or 'MG B' in f:
        return 'Diboride'
    elif 'H' in f and len(f) > 3:  # crude hydride filter
        return 'Hydride'
    elif ('LA' in f and 'H' in f) or ('CE' in f and 'H' in f):
        return 'Hydride'
    else:
        return 'Other'

df['family'] = df['formula'].apply(get_family)

# Group Tc lists by family
family_groups = defaultdict(list)
for fam, group in df.groupby('family'):
    if len(group) >= 2:  # need at least two materials
        family_groups[fam] = sorted(group['critical_temp'].values)

print("Families with multiple materials:")
for fam, tcs in family_groups.items():
    print(f"  {fam}: {len(tcs)} materials, Tc range {min(tcs):.1f}–{max(tcs):.1f} K")

# Collect intra-family ratios
ratios = []
for fam, tcs in family_groups.items():
    tcs = np.array(tcs)
    for i in range(len(tcs)):
        for j in range(i+1, len(tcs)):
            ratio = tcs[j] / tcs[i]
            if ratio > 1.0:
                ratios.append(ratio)

ratios = np.array(ratios)
print(f"\nTotal intra-family ratios computed: {len(ratios):,}\n")

# Fold scaling
r = 2 ** (1 / 12)
print(f"Universal fold scaling r = 2^(1/12) ≈ {r:.6f}\n")

# Stats
n_values = np.round(np.log(ratios) / np.log(r))
deviations_pct = np.abs(ratios - (r ** n_values)) / (r ** n_values) * 100

print(f"Mean deviation from nearest 2^(n/12): {deviations_pct.mean():.3f}%")
print(f"Median deviation: {np.median(deviations_pct):.3f}%")
print(f"Fraction within ±5%: {np.mean(deviations_pct < 5):.1%}")
print(f"Fraction within ±3%: {np.mean(deviations_pct < 3):.1%}\n")

# Plots (same style as v1)
plt.figure(figsize=(12, 6))
plt.hist(ratios, bins=80, alpha=0.75, color='steelblue', edgecolor='black', label='Intra-family Tc ratios')
max_r = ratios.max() if len(ratios) > 0 else 3
for n in range(0, int(np.log(max_r)/np.log(r)) + 3):
    plt.axvline(r ** n, color='red', linestyle='--', alpha=0.7, linewidth=1)
plt.xlabel('Tc Ratio (T_{c,j} / T_{c,i})')
plt.ylabel('Count')
plt.title('T1 v2: Intra-Family Tc Ratios\nRed dashes = exact fold scaling 2^(n/12)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(12, 6))
log_ratios = np.log2(ratios)
plt.hist(log_ratios, bins=80, alpha=0.75, color='darkorange', edgecolor='black')
plt.xlabel('log₂(Tc Ratio)')
plt.ylabel('Count')
plt.title('T1 v2: log₂(Tc Ratio) — family-internal only')
plt.grid(True, alpha=0.3)
plt.show()

print("✅ T1 v2 complete!")
print("   • Fixed column name ('material' → 'formula')")
print("   • Much cleaner test (only within real families)")
print("   • If clustering at red lines is strong → T1 passes solidly")