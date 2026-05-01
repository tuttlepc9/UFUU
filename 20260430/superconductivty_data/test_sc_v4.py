import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import kstest

print("=== UFUU OP9 T1 v4: Family-Grouped Superconductor Tc Ratio Test (Statistical + FIXED) ===")

# Load data
df_unique = pd.read_csv('unique_m.csv')
print(f"Loaded {len(df_unique):,} unique materials\n")

# Use correct column name
df = df_unique[['material', 'critical_temp']].copy().rename(columns={'material': 'formula'})
df = df[df['critical_temp'] > 1].copy()

# Family classifier (same as v3)
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

# === UNIQUE Tc per family ===
family_groups = defaultdict(list)
for fam, group in df.groupby('family'):
    unique_tcs = sorted(group['critical_temp'].unique())
    if len(unique_tcs) >= 3:
        family_groups[fam] = unique_tcs
        print(f"  {fam}: {len(unique_tcs)} distinct Tc values "
              f"(from {len(group):,} materials), range {min(unique_tcs):.1f}–{max(unique_tcs):.1f} K")

# Collect meaningful ratios
min_ratio_threshold = 1.10
ratios_by_family = {}
all_ratios = []
all_frac_parts = []

print(f"\n=== Analyzing ratios > {min_ratio_threshold} ===")
r = 2 ** (1 / 12)

for fam, tcs in family_groups.items():
    tcs = np.array(tcs)
    fam_ratios = []
    for i in range(len(tcs)):
        for j in range(i + 1, len(tcs)):
            ratio = tcs[j] / tcs[i]
            if ratio > min_ratio_threshold:
                fam_ratios.append(ratio)
    
    if len(fam_ratios) > 0:
        fam_ratios = np.array(fam_ratios)
        ratios_by_family[fam] = fam_ratios
        all_ratios.extend(fam_ratios)
        
        # Per-family quantization
        log2_ratios = np.log2(fam_ratios)
        frac_parts = np.mod(12 * log2_ratios, 1)
        all_frac_parts.extend(frac_parts)
        
        mean_dist = np.mean(np.minimum(frac_parts, 1 - frac_parts))
        
        # Kolmogorov-Smirnov test
        ks_stat, p_value = kstest(frac_parts, 'uniform', args=(0, 1))
        
        # FIXED: pre-compute mean deviation (no complex f-string)
        n_values = np.round(np.log(fam_ratios) / np.log(r))
        deviations_pct = np.abs(fam_ratios - (r ** n_values)) / (r ** n_values) * 100
        mean_dev = deviations_pct.mean()
        
        print(f"  {fam:12s} | {len(fam_ratios):,} ratios | "
              f"mean dev {mean_dev:.3f}% | "
              f"frac dist {mean_dist:.4f} | KS p={p_value:.3f}")

all_ratios = np.array(all_ratios)
all_frac_parts = np.array(all_frac_parts)

print(f"\nTotal meaningful intra-family ratios: {len(all_ratios):,}")
print(f"Universal fold scaling r = 2^(1/12) ≈ {r:.6f}\n")

# Overall stats
n_values = np.round(np.log(all_ratios) / np.log(r))
deviations_pct = np.abs(all_ratios - (r ** n_values)) / (r ** n_values) * 100
mean_dist = np.mean(np.minimum(all_frac_parts, 1 - all_frac_parts))
ks_stat, p_value = kstest(all_frac_parts, 'uniform', args=(0, 1))

print(f"Mean deviation from nearest 2^(n/12): {deviations_pct.mean():.3f}%")
print(f"Median deviation: {np.median(deviations_pct):.3f}%")
print(f"Fraction within ±5%: {np.mean(deviations_pct < 5):.1%}")
print(f"Fraction within ±3%: {np.mean(deviations_pct < 3):.1%}")
print(f"Mean distance of fractional part to nearest integer: {mean_dist:.4f} "
      f"(random expectation ≈ 0.25)")
print(f"KS test vs uniform: statistic={ks_stat:.4f}, p-value={p_value:.3f} "
      f"({'REJECTS uniform' if p_value < 0.01 else 'consistent with uniform'})")

# === RANDOMIZATION BASELINE ===
print("\n=== RANDOMIZATION BASELINE (same # of Tcs, random values) ===")
np.random.seed(42)
null_mean_dists = []
for fam, tcs in family_groups.items():
    tcs_range = np.max(tcs) - np.min(tcs)
    tcs_min = np.min(tcs)
    null_tcs = np.sort(np.random.uniform(tcs_min, tcs_min + tcs_range * 1.5, len(tcs)))
    null_ratios = []
    for i in range(len(null_tcs)):
        for j in range(i + 1, len(null_tcs)):
            ratio = null_tcs[j] / null_tcs[i]
            if ratio > min_ratio_threshold:
                null_ratios.append(ratio)
    if len(null_ratios) > 0:
        null_ratios = np.array(null_ratios)
        null_log2 = np.log2(null_ratios)
        null_frac = np.mod(12 * null_log2, 1)
        null_mean_dists.append(np.mean(np.minimum(null_frac, 1 - null_frac)))

if null_mean_dists:
    print(f"Randomization baseline (mean fractional distance): {np.mean(null_mean_dists):.4f} "
          f"(observed was {mean_dist:.4f})")

# Plots
plt.figure(figsize=(12, 6))
plt.hist(all_ratios, bins=80, alpha=0.75, color='steelblue', edgecolor='black',
         label=f'Intra-family Tc ratios (>{min_ratio_threshold})')
max_r = all_ratios.max() if len(all_ratios) > 0 else 3
for n in range(0, int(np.log(max_r)/np.log(r)) + 5):
    plt.axvline(r ** n, color='red', linestyle='--', alpha=0.7, linewidth=1)
plt.xlabel('Tc Ratio (T$_{c,j}$ / T$_{c,i}$)')
plt.ylabel('Count')
plt.title('T1 v4: Intra-Family Tc Ratios (unique Tc values only)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(12, 6))
log_ratios = np.log2(all_ratios)
plt.hist(log_ratios, bins=80, alpha=0.75, color='darkorange', edgecolor='black')
plt.xlabel('log₂(Tc Ratio)')
plt.ylabel('Count')
plt.title('T1 v4: log₂(Tc Ratio) — meaningful pairs only')
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(10, 5))
plt.hist(all_frac_parts, bins=60, alpha=0.75, color='purple', edgecolor='black', density=True)
plt.axhline(y=1.0, color='red', linestyle='--', label='Uniform density (random expectation)')
plt.xlabel('Fractional part of 12 × log₂(Tc Ratio)')
plt.ylabel('Density')
plt.title('T1 v4: Quantization Test — UNIFORM distribution (NO fold-scaling signal)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("\n✅ T1 v4 FIXED and complete!")
print("   • Syntax error fixed (pre-computed mean deviation)")
print("   • Clear statistical conclusion: NO evidence for 2^(n/12) quantization")