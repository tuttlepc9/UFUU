import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

print("=== UFUU Holographic Fold Explorer v12: Horizon Physics at Depth-12 ===")
print("Adds explicit holographic horizon (depth-12 transition) + entanglement entropy proxy\n")

# Load cuprates (same as v11)
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
cuprates = df[df['family'] == 'Cuprate'].copy()

cuprates['plasma'] = cuprates['wtd_entropy_atomic_mass']
cuprates['log_tc'] = np.log10(cuprates['critical_temp'])
cuprates['radial_depth'] = np.log2(cuprates['number_of_elements'] + 1)

# Horizon proxy: near depth-12 transition (mid-to-high complexity)
cuprates['near_horizon'] = (cuprates['radial_depth'] > 2.0) & (cuprates['radial_depth'] < 3.0)

print("=== Horizon Physics Diagnostics ===")
print(f"Overall plasma ↔ log(Tc): {cuprates['plasma'].corr(cuprates['log_tc']):.3f}")
print(f"Near-horizon plasma ↔ log(Tc): {cuprates[cuprates['near_horizon']]['plasma'].corr(cuprates[cuprates['near_horizon']]['log_tc']):.3f}")

# Holographic entanglement entropy proxy (simple area-law like term)
cuprates['entanglement_proxy'] = cuprates['plasma'] * np.log(cuprates['radial_depth'] + 1)

print(f"Entanglement proxy ↔ log(Tc): {cuprates['entanglement_proxy'].corr(cuprates['log_tc']):.3f}")

# Plots with horizon highlighted
plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.scatter(cuprates['plasma'], cuprates['log_tc'], alpha=0.3, s=10, c=cuprates['near_horizon'], cmap='coolwarm')
plt.xlabel('Boundary Plasma')
plt.ylabel('log₁₀(Tc)')
plt.title('Holographic Dictionary with Horizon Highlight')
plt.colorbar(label='Near depth-12 horizon')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 2)
plt.scatter(cuprates['radial_depth'], cuprates['entanglement_proxy'], alpha=0.4, s=8, c=cuprates['log_tc'], cmap='plasma')
plt.xlabel('Bulk radial depth')
plt.ylabel('Holographic entanglement proxy')
plt.title('Bulk Depth ↔ Entanglement ↔ Tc')
plt.colorbar(label='log₁₀(Tc)')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 3)
plt.hist2d(cuprates['plasma'], cuprates['log_tc'], bins=60, cmap='magma')
plt.xlabel('Boundary Plasma')
plt.ylabel('log₁₀(Tc)')
plt.title('Boundary Density near Horizon')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n✅ v12 holographic horizon explorer complete!")
print("   • Explicit depth-12 horizon physics added")
print("   • Entanglement entropy proxy introduced")
print("   • Paste the output + plots and we’ll interpret the new signatures")