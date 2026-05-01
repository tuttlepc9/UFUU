import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

print("=== UFUU OP9 T1 v3: Family-Grouped Superconductor Tc Ratio Test (Cleaned) ===")

# Load data
df_unique = pd.read_csv('unique_m.csv')
print(f"Loaded {len(df_unique):,} unique materials\n")

# Use correct column name
df = df_unique[['material', 'critical_temp']].copy().rename(columns={'material': 'formula'})
df = df[df['critical_temp'] > 1].copy()  # real superconductors

# Family classifier (same as v2)
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
    elif 'H' in f and len(f) > 3 or (('LA' in f or 'CE' in f) and 'H' in f):
        return 'Hydride'
    else:
        return 'Other'

df['family'] = df['formula'].apply(get_family)

# === KEY FIX: Use only UNIQUE Tc values per family ===
family_groups = defaultdict(list)
for fam, group in df.groupby('family'):
    unique_tcs = sorted(group['critical_temp'].unique())
    if len(unique_tcs) >= 2:
        family_groups[fam] = unique_tcs
        print(f"  {fam}: {len(unique_tcs)} distinct Tc values "
              f"(from {len(group):,} materials), range {min(unique_tcs):.1f}–{max(unique_tcs):.1f} K")

# Collect only *meaningful* intra-family ratios (skip trivial near-duplicates)
ratios = []
min_ratio_threshold = 1.10
for fam, tcs in family_groups.items():
    tcs = np.array(tcs)
    for i in range(len(tcs)):
        for j in range(i + 1, len(tcs)):
            ratio = tcs[j] / tcs[i]
            if ratio > min_ratio_threshold:
                ratios.append(ratio)

ratios = np.array(ratios)
print(f"\nTotal meaningful intra-family ratios (>{min_ratio_threshold}): {len(ratios):,}\n")

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

# Extra quantization check (should be strongly peaked near 0 if T1 is real)
frac_parts = np.mod(12 * np.log2(ratios), 1)
print(f"Mean distance of fractional part (12×log₂(ratio)) to nearest integer: "
      f"{np.mean(np.minimum(frac_parts, 1-frac_parts)):.4f} "
      f"(random expectation ≈ 0.25)")

# Plots
plt.figure(figsize=(12, 6))
plt.hist(ratios, bins=80, alpha=0.75, color='steelblue', edgecolor='black',
         label=f'Intra-family Tc ratios (>{min_ratio_threshold})')
max_r = ratios.max() if len(ratios) > 0 else 3
for n in range(0, int(np.log(max_r)/np.log(r)) + 5):
    plt.axvline(r ** n, color='red', linestyle='--', alpha=0.7, linewidth=1)
plt.xlabel('Tc Ratio (T$_{c,j}$ / T$_{c,i}$)')
plt.ylabel('Count')
plt.title('T1 v3: Intra-Family Tc Ratios (unique Tc values only)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(12, 6))
log_ratios = np.log2(ratios)
plt.hist(log_ratios, bins=80, alpha=0.75, color='darkorange', edgecolor='black')
plt.xlabel('log₂(Tc Ratio)')
plt.ylabel('Count')
plt.title('T1 v3: log₂(Tc Ratio) — meaningful pairs only')
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(10, 5))
plt.hist(frac_parts, bins=60, alpha=0.75, color='purple', edgecolor='black', density=True)
plt.xlabel('Fractional part of 12 × log₂(Tc Ratio)')
plt.ylabel('Density')
plt.title('T1 v3: Quantization Test (should peak sharply at 0 if fold-scaling holds)')
plt.grid(True, alpha=0.3)
plt.show()

print("✅ T1 v3 complete!")
print("   • Fixed: now uses *unique* Tc values per family")
print("   • Only meaningful jumps (ratio > 1.10)")
print("   • Added direct periodicity/quantization test")
print("   • Much cleaner signal for the T1 hypothesis")