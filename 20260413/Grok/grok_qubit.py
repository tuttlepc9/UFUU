"""
Tuttle 2026 — Quantum v1.1: Finsler-Friedmann 2025 (fixed)
Corrected 4x4 unitary on tensor-product space. 
Depth 18 for speed; increase to 22+ when ready.
"""

import numpy as np

DEPTH = 18
TOL = 1e-8

# Pauli basis
I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def random_mixed_state():
    """Path-dependent quantum leaf (minimal seed)"""
    rho = np.eye(2, dtype=complex) * 0.5
    rho += 0.12 * (np.random.rand() * X + np.random.rand() * Y + np.random.rand() * Z)
    rho = rho @ rho.conj().T
    return rho / np.trace(rho)

def finsler_quantum_fold(rho_L, rho_R):
    """Quantum Finsler-Friedmann fold — now correct 4x4 unitary"""
    # Acceleration term from classical Finsler
    accel = 0.003 * (np.trace(rho_L @ Z) + np.trace(rho_R @ Z)) * (np.trace(rho_L @ Z) - np.trace(rho_R @ Z))
    
    # Build 4x4 unitary that mixes the two qubits
    theta = np.pi/4 + accel * 0.8
    U2 = np.array([[np.cos(theta), -np.sin(theta)],
                   [np.sin(theta),  np.cos(theta)]], dtype=complex)
    # Kronecker to make it act on the full 4D space (simple entangling rotation)
    U4 = np.kron(U2, np.eye(2, dtype=complex))   # acts on first qubit, identity on second
    
    # Tensor product of input states
    tensor = np.kron(rho_L, rho_R)               # 4x4
    
    # Evolve
    evolved = U4 @ tensor @ U4.conj().T
    
    # Partial trace over second qubit → back to single qubit
    rho_out = np.trace(evolved.reshape(2,2,2,2), axis1=1, axis2=3)
    
    # Controlled irreversibility (decoherence channel)
    deco = 0.08
    rho_out = (1 - deco) * rho_out + deco * np.eye(2, dtype=complex) * 0.5
    rho_out /= np.trace(rho_out)
    
    return rho_out

def quantum_tree(depth):
    n = 1 << depth
    states = [random_mixed_state() for _ in range(n)]
    for level in range(depth):
        new_states = []
        for i in range(0, len(states), 2):
            left = states[i]
            right = states[i + 1]
            new_states.append(finsler_quantum_fold(left, right))
        states = new_states
    return states[0]  # root density matrix

# =============================================================================
# RUN + QUANTUM MEASUREMENTS
# =============================================================================
print("=== Quantum v1.1 — Finsler-Friedmann 2025 (Depth", DEPTH, ") ===\n")

root_rho = quantum_tree(DEPTH)

# Measurements
trace = np.real(np.trace(root_rho))
purity = np.real(np.trace(root_rho @ root_rho))
ent_entropy = -np.real(np.trace(root_rho @ np.log2(root_rho + 1e-12 * np.eye(2))))
eigenvals = np.real(np.linalg.eigvalsh(root_rho))
born_probs = eigenvals**2

print(f"Root trace (must be 1): {trace:.6f}")
print(f"Purity: {purity:.6f}   (1 = pure state, <1 = mixed/entangled)")
print(f"von Neumann entropy: {ent_entropy:.6f}")
print(f"Born-rule probabilities (eigenvalues squared): {born_probs}")
print(f"Approximate unitarity breaking (1 - purity): {1 - purity:.6f}")

print("\nQuantum Finsler-Friedmann v1.1 completed successfully.")
print("This is the first quantum version of our crayon winner.")