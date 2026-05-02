import numpy as np
import json
from pathlib import Path

def shannon_entropy(probs):
    probs = np.array(probs)
    probs = probs[probs > 1e-12]
    return -np.sum(probs * np.log2(probs)) if len(probs) > 0 else 0.0

def ufuu_entropy(d):
    return float(d)  # perfect maximum entropy

def random_fold_entropy(d, n_trials=200):
    entropies = []
    for _ in range(n_trials):
        current_probs = np.array([1.0])
        for _ in range(d):
            splits = np.random.uniform(0.05, 0.95, len(current_probs))
            new_probs = np.concatenate([current_probs * splits, current_probs * (1 - splits)])
            current_probs = new_probs
        current_probs /= np.sum(current_probs)
        h = shannon_entropy(current_probs)
        entropies.append(h)
    return {
        'mean': float(np.mean(entropies)),
        'std': float(np.std(entropies)),
        'max': float(np.max(entropies)),
        'ufuu': ufuu_entropy(d)
    }

# Run the test
depths = list(range(1, 21))
results = {}
print("Running Monte Carlo entropy baseline (200 trials per depth)...\n")

for d in depths:
    print(f"→ Depth {d:2d} ...", end=" ")
    results[d] = random_fold_entropy(d)
    print("done")

# Print nice table
print("\nDepth | UFUU Entropy | Random Mean ± Std | Random Max | UFUU advantage")
print("------|--------------|-------------------|------------|----------------")
for d in depths:
    r = results[d]
    print(f"{d:5d} | {r['ufuu']:12.2f} | {r['mean']:5.2f} ± {r['std']:.2f} | {r['max']:5.2f} | {r['ufuu'] - r['max']:.2f}")

# Save full results to file
output_file = Path('ufuu_entropy_baseline_results.json')
with open(output_file, 'w') as f:
    json.dump({str(k): v for k, v in results.items()}, f, indent=2)

print(f"\n✅ All results saved to: {output_file.absolute()}")
print("You can now open ufuu_entropy_baseline_results.json in any editor.")