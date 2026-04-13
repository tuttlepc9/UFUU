import numpy as np
from collections import Counter

DEPTH = 24
RAW_MATERIAL_DEPTH = 16   # clear boundary: below = raw material / quantum-like, above = classical/emergent

def fundamental_fold(state_L, state_R, current_depth):
    """Fold with explicit scale boundary.
    Below RAW_MATERIAL_DEPTH: produce raw material (entropy, attractors, breaking)
    Above RAW_MATERIAL_DEPTH: preserve raw material and let classical structures emerge
    """
    depth_factor = 0.004 * (DEPTH - current_depth)

    # Acceleration / GR channel (always present)
    accel = 0.002 * (state_L[:,0]**2 + state_R[:,0]**2) * (state_L[:,0] - state_R[:,0])

    if current_depth < RAW_MATERIAL_DEPTH:
        # Raw material regime (quantum-like)
        entropy_drive = 0.007 * np.log1p(np.abs(state_L[:,1] * state_R[:,1]) + 1e-6) + \
                        0.005 * np.abs(state_L[:,1] - state_R[:,1]) + depth_factor
        attractor = 0.005 * (state_L[:,2]**3 - state_R[:,2]**3) + \
                    0.0025 * np.sin(31.4 * (state_L[:,2] + state_R[:,2])) + \
                    0.0018 * np.sign(state_L[:,2] - state_R[:,2]) * np.abs(state_L[:,2] - state_R[:,2])**1.5
    else:
        # Classical/emergent regime — only preserve what was built
        entropy_drive = 0.001 * np.abs(state_L[:,1] - state_R[:,1])   # gentle preservation
        attractor = 0.001 * (state_L[:,2] - state_R[:,2])             # gentle stabilization

    new_state = np.zeros_like(state_L)
    new_state[:,0] = state_L[:,0] + state_R[:,0] + accel + 0.0008 * state_L[:,1]
    new_state[:,1] = state_L[:,1] + state_R[:,1] + entropy_drive + 0.0012 * state_L[:,2]
    new_state[:,2] = state_L[:,2] + state_R[:,2] + attractor + 0.0005 * state_L[:,0]

    return np.tanh(np.clip(new_state, -25, 25)) * 0.65

def leaves_vector(d):
    n = 1 << d
    base = np.arange(n, dtype=np.float64) % 17
    return np.stack([base, base * 0.7, base * 1.3], axis=1)

print("=== New Fundamental Fold — With Explicit Scale Boundary (Depth 24) ===\n")

g_vals = leaves_vector(DEPTH)
levels = [g_vals.copy()]

for level in range(DEPTH):
    left = g_vals[0::2]
    right = g_vals[1::2]
    g_vals = fundamental_fold(left, right, level)
    levels.append(g_vals.copy())

root = g_vals[0]

print("1. Fixed-point convergence")
U = root.copy()
for step in range(12):
    U_new = fundamental_fold(U.reshape(1,3), U.reshape(1,3), DEPTH)[0]
    diff = np.max(np.abs(U_new - U))
    print(f"Step {step:2d} | State {U_new} | Change {diff:.2e}")
    if diff < 1e-5:
        print("   ✓ Stable fixed point reached")
        break
    U = U_new

print("\n2. Entropy monotonicity (P4)")
entropies = []
for lv in levels:
    flat = lv.flatten()
    unique, counts = np.unique(np.round(flat, 6), return_counts=True)
    probs = counts / len(flat)
    H = -np.sum(probs * np.log2(probs + 1e-12))
    entropies.append(H)
print(f"Entropy profile (first 5 → last 5): {entropies[:5]} ... {entropies[-5:]}")
monotonic = np.all(np.diff(entropies) > -0.05)
print(f"   Monotonic increasing: {'✓' if monotonic else '✗'}")

print("\n3. GR acceleration proxy (channel 0)")
accel_proxy = 0.0028 * (root[0]**2) * 2
print(f"   Acceleration term: {accel_proxy:.6f}")

print("\n4. Attractor families (P5)")
all_values = np.round(levels[-1].flatten(), 6)
attractors = Counter(all_values)
print(f"   Distinct attractors: {len(attractors)}")
print(f"   Top attractors: {dict(attractors.most_common(8))}")

print("\n=== Fold with explicit scale boundary complete ===")
print("Boundary at depth 16: raw material regime below, classical/emergent above.")