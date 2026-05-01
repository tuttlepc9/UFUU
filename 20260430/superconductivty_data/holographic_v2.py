import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

print("=== UFUU Holographic Fold Explorer v11: Superconductors on the Boundary ===")
print("Binary-tree bulk (radial depth) ↔ boundary plasma + Tc order parameter")
print("Cuprates as holographic strange-metal / superconductor system\n")

# Load & prepare cuprates (boundary data)
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

print(f"Boundary data — Cuprate materials: {len(cuprates):,}\n")

# Holographic variables
cuprates['plasma'] = cuprates['wtd_entropy_atomic_mass']                    # Boundary entanglement / collective mode
cuprates['log_tc'] = np.log10(cuprates['critical_temp'])                   # Boundary order parameter (superconducting gap proxy)
cuprates['radial_scale'] = np.log2(cuprates['number_of_elements'] + 1)     # Bulk radial coordinate (RG depth proxy)

# Holographic dictionary diagnostics
print("=== Bulk-to-Boundary Mapping ===")
corr_plasma_tc = cuprates['plasma'].corr(cuprates['log_tc'])
print(f"Plasma (boundary entanglement) ↔ log(Tc) (order parameter): {corr_plasma_tc:.3f}")

# Scaling exponent (holographic RG flow)
slope, intercept, r_value, p_value, std_err = linregress(cuprates['plasma'], cuprates['log_tc'])
print(f"Holographic scaling exponent (d log(Tc)/d plasma): {slope:.3f} (r² = {r_value**2:.3f})")

# Radial (depth) dependence
print("\nRadial (bulk depth) dependence of boundary plasma:")
radial_bins = pd.cut(cuprates['radial_scale'], bins=5)
grouped = cuprates.groupby(radial_bins)
for name, g in grouped:
    if len(g) > 30:
        corr = g['plasma'].corr(g['log_tc'])
        print(f"  Bulk radial bin {name} (n={len(g)}): plasma–log(Tc) corr = {corr:.3f}")

# Plots — holographic dictionary
plt.figure(figsize=(14, 6))

plt.subplot(1, 3, 1)
plt.scatter(cuprates['plasma'], cuprates['log_tc'], alpha=0.35, s=10,
            c=cuprates['radial_scale'], cmap='viridis')
plt.xlabel('Boundary Plasma (entropy / collective mode)')
plt.ylabel('log₁₀(Tc) — boundary order parameter')
plt.title('Holographic Dictionary\nPlasma ↔ Superconducting Order Parameter')
plt.colorbar(label='Bulk radial depth (log₂ complexity)')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 2)
plt.hist2d(cuprates['plasma'], cuprates['log_tc'], bins=70, cmap='magma')
plt.xlabel('Boundary Plasma')
plt.ylabel('log₁₀(Tc)')
plt.title('Bulk-to-Boundary Density')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 3)
plt.scatter(cuprates['radial_scale'], cuprates['plasma'], alpha=0.4, s=8, c=cuprates['log_tc'], cmap='plasma')
plt.xlabel('Bulk radial depth (log₂(element multiplicity))')
plt.ylabel('Boundary plasma (entropy)')
plt.title('Bulk Depth ↔ Boundary Entanglement')
plt.colorbar(label='log₁₀(Tc)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n✅ v11 holographic explorer complete!")
print("   • Bulk (binary-tree radial scale) ↔ boundary (plasma + Tc) duality mapped")
print("   • Paste the output + 3 plots here and we’ll interpret the holographic signatures")
print("   • Next steps available: add horizon physics at depth-12, entanglement entropy proxies, or AdS-like scaling laws")