import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

phi = (1 + math.sqrt(5)) / 2
p = 17

# =============================================================================
# EXACT MODULAR FOLD FROM THE PAPER
# =============================================================================
def modular_fold(left_g: int, right_g: int) -> int:
    return (left_g * right_g + left_g + 1) % p

# =============================================================================
# GAUGE ATTRACTOR LABEL (eventual fixed point or cycle)
# =============================================================================
def get_final_attractor(g_start: int) -> str:
    """Run full gauge iteration and return clean label: 'FP4', 'FP13', or 'CYCLE-X'"""
    x = g_start
    seen = {}
    orbit = []
    for step in range(100):
        if x in seen:
            cycle_start = seen[x]
            cycle = orbit[cycle_start:]
            if len(cycle) == 1:
                return f"FP{cycle[0]}"
            else:
                return f"CYCLE{len(cycle)}"
        seen[x] = step
        orbit.append(x)
        x = modular_fold(x, x)   # g → g*g + g + 1 mod 17
    return "UNKNOWN"

# Precompute for all 17 possible g-values
ATTRACTOR_MAP = {g: get_final_attractor(g) for g in range(p)}

# =============================================================================
# LEAVES (original binary-fraction version)
# =============================================================================
def leaves_gauge_only(d: int):
    n = 1 << d
    idx = np.arange(n, dtype=np.int64)
    return idx % p   # only g-seeds needed for this analysis

# =============================================================================
# MAIN ANALYSIS
# =============================================================================
def run_basin_entropy_analysis(depth: int = 18):
    print("=== Tuttle 2026 — Basin Entropy & Decoherence Depth Analysis ===")
    print(f"Depth = {depth}  ({1<<depth:,} leaves)\n")

    g_current = leaves_gauge_only(depth)

    records = []
    levels = list(range(depth, -1, -1))   # 18 (leaves) down to 0 (root)

    for k in levels:
        # Label every node at this level by its eventual attractor
        labels = np.array([ATTRACTOR_MAP[g] for g in g_current])

        # Basin proportions
        counter = Counter(labels)
        total = len(g_current)
        proportions = {label: count / total for label, count in counter.items()}

        # Shannon entropy H(B(k))
        if len(proportions) > 1:
            H = -sum(p * math.log2(p) for p in proportions.values())
        else:
            H = 0.0

        records.append({
            'Level_k': k,
            'Nodes': total,
            'Entropy_H': round(H, 6),
            'Basin_Proportions': {k: round(v, 4) for k, v in sorted(proportions.items(), key=lambda x: -x[1])}
        })

        print(f"  k={k:2d} | Nodes={total:7,} | H={H:.5f} bits  | {dict(proportions)}")

        if k == 0:
            break

        # Fold up one level
        left = g_current[0::2]
        right = g_current[1::2]
        g_current = np.array([modular_fold(l, r) for l, r in zip(left, right)])

    df = pd.DataFrame(records)

    # =============================================================================
    # PLOT
    # =============================================================================
    plt.figure(figsize=(11, 6))
    plt.plot(df['Level_k'], df['Entropy_H'], marker='o', linewidth=2.5, markersize=6, color='#1f77b4')
    plt.xlabel('Tree Level k  (18 = leaves  →  0 = root)', fontsize=12)
    plt.ylabel('Shannon Entropy H(B(k))  [bits]', fontsize=12)
    plt.title('Gauge Basin Entropy vs Folding Depth\n(Depth-18 tree — decoherence analysis)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(range(0, depth+1, 2))

    # Highlight predicted inflection region
    plt.axvspan(6, 9, alpha=0.18, color='orange', label='Predicted inflection / decoherence depth (6–9)')
    plt.legend()

    plt.tight_layout()
    plt.savefig('basin_entropy_decoherence.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("\n✅ Plot saved as 'basin_entropy_decoherence.png'")
    print("Prediction check:")
    print("   • Strictly monotone decreasing?", "YES" if np.all(np.diff(df['Entropy_H']) < 0) else "NO")
    print("   • Inflection visible around k=6–9?", "Check the plot above.")

    return df

# =============================================================================
# RUN
# =============================================================================
if __name__ == "__main__":
    df = run_basin_entropy_analysis(depth=18)
    print("\n" + "="*80)
    print(df[['Level_k', 'Entropy_H']].to_string(index=False))