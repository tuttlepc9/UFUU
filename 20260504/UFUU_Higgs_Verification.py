import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

# =============================================================================
# UFUU_Higgs_Verification.py
# Exact 11-step entropy-maximization procedure for the candidate fold F(a,b)
# =============================================================================

# 1. Constants and fixed-point values
ATTRACTOR_M = 1.134663          # numerical value of the attractor from UFUU notes
LAMBDA_SYM = 0.259              # target eigenvalue of linearized transfer operator
N_SAMPLES = 10000
N_ITER = 12
PHI_STD = 0.01                  # small Gaussian perturbation around symmetric point

# 2. Define the effective recursion map (from Taylor expansion)
def effective_map(phi, alpha, beta, m, gamma):
    """Effective recursion map for the order parameter φ."""
    linear_coeff = 2 * alpha + 2 * beta * m**2
    cubic_coeff = -2 * beta + 8 * gamma
    return linear_coeff * phi + cubic_coeff * phi**3

# 3. Parameter domain
beta_range = np.linspace(-0.05, 0.05, 21)
gamma_range = np.linspace(0.0, 0.2, 21)

# Compute alpha from linear constraint for each beta (at fixed m)
alpha_range = (LAMBDA_SYM - 2 * beta_range[:, None] * ATTRACTOR_M**2) / 2

# Stability condition λ > 0
def lambda_coeff(b, g):
    return 2 * b - 8 * g

stable_mask = lambda_coeff(beta_range[:, None], gamma_range) > 0

# 4. Initial distribution for φ
np.random.seed(42)
phi0 = np.random.normal(0, PHI_STD, N_SAMPLES)

# 5-6. Iterate map and compute Shannon entropy
def compute_final_entropy(alpha, beta, gamma, m=ATTRACTOR_M, n_iter=N_ITER):
    phi = phi0.copy()
    for _ in range(n_iter):
        phi = effective_map(phi, alpha, beta, m, gamma)
    
    # Histogram-based Shannon entropy
    hist, bin_edges = np.histogram(phi, bins=100, density=True)
    hist = hist[hist > 1e-12]
    bin_width = bin_edges[1] - bin_edges[0]
    entropy = -np.sum(hist * np.log2(hist)) * bin_width
    return entropy

# 7. Entropy maximization over grid
entropies = np.full((len(beta_range), len(gamma_range)), -np.inf)
max_entropy = -np.inf
best_alpha = best_beta = best_gamma = None

for i, beta in enumerate(beta_range):
    for j, gamma in enumerate(gamma_range):
        if not stable_mask[i, j]:
            continue
        alpha = (LAMBDA_SYM - 2 * beta * ATTRACTOR_M**2) / 2
        ent = compute_final_entropy(alpha, beta, gamma)
        entropies[i, j] = ent
        if ent > max_entropy:
            max_entropy = ent
            best_alpha = alpha
            best_beta = beta
            best_gamma = gamma

# 8-9. Compute Higgs-sector parameters
mu2 = 1 - (2 * best_alpha + 2 * best_beta * ATTRACTOR_M**2)
lambda_higgs = 2 * best_beta - 8 * best_gamma

# 11. Output summary
print("=== UFUU Higgs Parameter Fixing Results ===")
print(f"Best parameters (entropy-maximizing):")
print(f"  α = {best_alpha:.5f}")
print(f"  β = {best_beta:.5f}")
print(f"  γ = {best_gamma:.5f}")
print(f"  Max Shannon entropy ≈ {max_entropy:.4f}")
print(f"μ² = {mu2:.5f}  (positive → symmetric point is stable)")
print(f"λ  = {lambda_higgs:.5f}  (positive → broken vacua are stable)")
print(f"Double-well condition (μ² < 0) is NOT satisfied in this run.")

# Optional: save grid for later analysis
np.savez("higgs_entropy_grid.npz", beta=beta_range, gamma=gamma_range, entropies=entropies)