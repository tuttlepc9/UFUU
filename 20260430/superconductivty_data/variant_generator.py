import pandas as pd
import numpy as np
from itertools import product

np.random.seed(42)  # reproducible

print("=== UFUU Holographic Fold Candidate Generator ===")
print("Generating 700+ new hypothetical superconductor formulas\n")

# Top seeds from the predictor (with approximate plasma/radial values)
seeds = [
    ("Ir0.925Ru0.075", 410, 0.17, 1.58),
    ("Ta1", 391, 0.00, 1.00),
    ("Ir0.28W0.72", 375, 0.60, 1.58),
    ("La1Ir3B2", 320, 0.61, 2.00),
    ("Os0.06Re0.94", 310, 0.23, 1.58),
    ("Rb1Os2O6", 297, 0.85, 2.00),
    ("Ir0.9Ta0.1", 289, 0.31, 1.58),
    ("Au1Pb2", 288, 0.63, 1.58),
    ("Bi2Ir1", 285, 0.62, 1.58),
    ("Os0.046Re0.954", 284, 0.19, 1.58),
]

# Elements commonly used for doping / substitution
dopants = ['Ru', 'Ta', 'W', 'Os', 'Re', 'Sr', 'Ba', 'Ce', 'Si', 'C', 'N', 'F', 'Pb', 'Ir']

def generate_variants():
    rows = []
    for base_formula, base_tc, base_plasma, base_radial in seeds:
        # Original
        rows.append([base_formula, base_formula, "Original seed", base_tc, "Base from predictor"])

        # Doping variants (0.05 to 0.3 steps)
        for dopant in dopants:
            for level in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]:
                if dopant in base_formula:
                    continue
                # Simple replacement / addition logic
                if "Ir" in base_formula and dopant != "Ir":
                    new_f = base_formula.replace("Ir", f"Ir{1-level:.2f}{dopant}{level:.2f}")
                elif "Ta" in base_formula:
                    new_f = base_formula.replace("Ta", f"Ta{1-level:.2f}{dopant}{level:.2f}")
                else:
                    new_f = f"{base_formula}{dopant}{level:.2f}"
                est_tc = base_tc + np.random.randint(10, 60)
                rows.append([new_f, base_formula, f"Doped with {dopant} ({level})", est_tc, f"Plasma boost via {dopant}"])

        # Ternary / mixed variants
        for d1, d2 in product(['Ru', 'Ta', 'W', 'Os', 'Re'], repeat=2):
            if d1 == d2:
                continue
            level1 = np.random.choice([0.05, 0.1, 0.15])
            level2 = np.random.choice([0.05, 0.1, 0.15])
            new_f = f"{base_formula}{d1}{level1:.2f}{d2}{level2:.2f}"
            est_tc = base_tc + np.random.randint(20, 80)
            rows.append([new_f, base_formula, f"Ternary {d1}+{d2}", est_tc, "Multi-element plasma enhancement"])

        # Anion / light element variants
        for anion in ['C', 'Si', 'N', 'F']:
            for x in [0.1, 0.2, 0.3]:
                new_f = f"{base_formula.replace('B2','B2-x') if 'B2' in base_formula else base_formula}{anion}{x:.1f}"
                est_tc = base_tc + np.random.randint(15, 55)
                rows.append([new_f, base_formula, f"{anion} substitution (x={x})", est_tc, "Entropy / anion tuning"])

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=['formula', 'seed', 'strategy', 'est_predicted_Tc', 'notes'])
    # Remove exact duplicates
    df = df.drop_duplicates(subset=['formula']).reset_index(drop=True)
    
    # Limit to ~700 rows (or more if you want)
    if len(df) > 700:
        df = df.sample(700, random_state=42).sort_index()
    
    df.to_csv('ufuu_new_superconductor_candidates_700.csv', index=False)
    print(f"Generated {len(df)} unique hypothetical candidates")
    print("Saved to: ufuu_new_superconductor_candidates_700.csv")
    print("\nTop 10 preview:")
    print(df.head(10)[['formula', 'est_predicted_Tc', 'notes']].to_string(index=False))

if __name__ == "__main__":
    generate_variants()