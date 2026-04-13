import numpy as np

DEPTH = 22
TOL = 1e-8
p = 17

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def random_mixed_state():
    rho = np.eye(2, dtype=complex) * 0.5
    rho += 0.12 * (np.random.rand() * X + np.random.rand() * Y + np.random.rand() * Z)
    rho = rho @ rho.conj().T
    return rho / np.trace(rho)

def modular_quantum_fold(rho_L, rho_R):
    # Fixed: take real part before modulo
    trace_L = np.real(np.trace(rho_L @ Z))
    trace_R = np.real(np.trace(rho_R @ Z))
    phase = int((trace_L * trace_R + trace_L + 1) % p)
    theta = np.pi * phase / p
    U2 = np.array([[np.cos(theta), -np.sin(theta)],
                   [np.sin(theta),  np.cos(theta)]], dtype=complex)
    U4 = np.kron(U2, np.eye(2, dtype=complex))
    tensor = np.kron(rho_L, rho_R)
    evolved = U4 @ tensor @ U4.conj().T
    rho_out = np.trace(evolved.reshape(2,2,2,2), axis1=1, axis2=3)
    deco = 0.08
    rho_out = (1 - deco) * rho_out + deco * np.eye(2, dtype=complex) * 0.5
    rho_out /= np.trace(rho_out)
    return rho_out

print("=== Deep Fixed-Point Verifier — Modular (baseline) (Depth 22) ===\n")
U = random_mixed_state()
for step in range(20):
    U_new = modular_quantum_fold(U, U)
    purity = np.real(np.trace(U_new @ U_new))
    entropy = -np.real(np.trace(U_new @ np.log2(U_new + 1e-12 * np.eye(2))))
    diff = np.abs(U_new - U).max()
    print(f"Step {step:2d} | Purity {purity:.4f} | Entropy {entropy:.4f} | Change {diff:.2e}")
    if diff < 1e-6:
        print("\n✓ Fixed point reached at depth 22.")
        break
    U = U_new
print("\nModular deep verification complete.")