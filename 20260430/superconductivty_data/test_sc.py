import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=== UFUU OP9 T1: Superconductor Tc Ratio Clustering Test ===")
print("Loading train.csv ...")
df = pd.read_csv('train.csv')
print(f"Shape: {df.shape}")
print(f"Columns include critical_temp: {'critical_temp' in df.columns}\n")

# Filter to actual superconductors (Tc > 1 K)
df_sc = df[df['critical_temp'] > 1].copy()
tc_values = df_sc['critical_temp'].values
print(f"Number of superconductors (Tc > 1 K): {len(tc_values):,}\n")

# Smart pairwise ratios (fast — only look ahead ~20 entries per starting point)
np.random.seed(42)
if len(tc_values) > 3000:
    tc_values = np.random.choice(tc_values, 3000, replace=False)  # still statistically powerful
tc_values = np.sort(tc_values)

ratios = []
max_lookahead = 30
for i in range(len(tc_values)):
    for j in range(i + 1, min(i + max_lookahead, len(tc_values))):
        ratio = tc_values[j] / tc_values[i]
        if ratio > 1.0:
            ratios.append(ratio)
ratios = np.array(ratios)

# Fold scaling r = 2^(1/12)
r = 2 ** (1 / 12)
print(f"Universal fold scaling ratio r = 2^(1/12) ≈ {r:.6f}\n")

# Find nearest n and deviation
n_values = np.round(np.log(ratios) / np.log(r))
deviations_pct = np.abs(ratios - (r ** n_values)) / (r ** n_values) * 100

print(f"Mean deviation from nearest 2^(n/12): {deviations_pct.mean():.3f}%")
print(f"Median deviation: {np.median(deviations_pct):.3f}%")
print(f"Fraction of ratios within ±5% of fold scaling: {np.mean(deviations_pct < 5):.1%}")
print(f"Fraction within ±3% : {np.mean(deviations_pct < 3):.1%}\n")

# Plot 1: Direct ratio histogram with predicted lines
plt.figure(figsize=(12, 6))
plt.hist(ratios, bins=120, alpha=0.75, color='steelblue', edgecolor='black', label='Observed Tc ratios')
max_ratio = ratios.max()
for n in range(0, int(np.log(max_ratio) / np.log(r)) + 2):
    plt.axvline(r ** n, color='red', linestyle='--', alpha=0.6, linewidth=1)
plt.xlabel('Tc Ratio (T_{c,j} / T_{c,i})')
plt.ylabel('Count')
plt.title('T1: Pairwise Tc Ratios in Superconductors\nRed dashes = exact fold scaling 2^(n/12)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Plot 2: Log2 view (makes the 1/12 periodicity obvious)
plt.figure(figsize=(12, 6))
log_ratios = np.log2(ratios)
plt.hist(log_ratios, bins=120, alpha=0.75, color='darkorange', edgecolor='black')
plt.xlabel('log₂(Tc Ratio)')
plt.ylabel('Count')
plt.title('T1: log₂(Tc Ratio) — expected peaks every integer (octave) with 1/12 spacing')
plt.grid(True, alpha=0.3)
plt.show()

print("✅ T1 analysis complete!")
print("   • Check the plots for clustering at the red dashed lines.")
print("   • Strong clustering = T1 passes → fold scaling appears in real superconductor families.")
print("   • Next: we can add formula-based family grouping using unique_m.csv if you want.")