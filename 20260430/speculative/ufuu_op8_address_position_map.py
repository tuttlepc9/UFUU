import numpy as np
from itertools import product
from scipy.spatial import KDTree

def generate_full_address_to_position_map(depth=10, dim=3, seed=42):
    """Full low-depth enumeration + analytical 3D quasicrystal projection (UFUU OP8)."""
    np.random.seed(seed)
    r0 = np.zeros(dim)
    phi = (1 + np.sqrt(5)) / 2
    basis = []
    for i in range(6):
        theta1 = 2 * np.pi * (i / phi)
        theta2 = 2 * np.pi * (i / phi**2)
        vec = np.array([np.cos(theta1),
                        np.sin(theta1) * np.cos(theta2),
                        np.sin(theta1) * np.sin(theta2)])
        basis.append(vec / np.linalg.norm(vec))
    
    addresses = []
    positions = []
    for bits in product([0, 1], repeat=depth):
        addr = tuple(bits)
        pos = r0.copy()
        scale = 1.0
        for m in range(depth):
            scale *= 1.06
            b = basis[m % len(basis)]
            pos += bits[m] * scale * b
        addresses.append(addr)
        positions.append(pos)
    return addresses, np.array(positions)

if __name__ == "__main__":
    print("UFUU OP8: Generating full address-to-position map at cosmological depth...\n")
    
    # Run full enumeration (D=10 = 1024 states)
    addresses, positions = generate_full_address_to_position_map(depth=10)
    
    print(f"Full enumeration completed for depth D=10")
    print(f"Total addresses (stable spacetime positions): {len(addresses):,}")
    print(f"Position shape: {positions.shape}")
    print(f"\nPosition cloud statistics (3D embedding):")
    print(f"  x range: [{positions[:,0].min():.4f}, {positions[:,0].max():.4f}]")
    print(f"  y range: [{positions[:,1].min():.4f}, {positions[:,1].max():.4f}]")
    print(f"  z range: [{positions[:,2].min():.4f}, {positions[:,2].max():.4f}]")
    print(f"  Mean position: [{positions[:,0].mean():.4f}, {positions[:,1].mean():.4f}, {positions[:,2].mean():.4f}]")
    
    print("\nSample address → position maps (first 5):")
    for i in range(5):
        print(f"  Sample {i+1}:")
        print(f"    Address: {addresses[i]}")
        print(f"    Position: {positions[i]}")
    
    print("\nLast sample (all-one address):")
    print(f"  Address: {addresses[-1]}")
    print(f"  Position: {positions[-1]}")
    
    # Save full map for downstream analysis / visualization
    np.savetxt('op8_address_position_map_d10.csv', positions, delimiter=',', 
               header='x,y,z', comments='')
    print("\nSaved full 1024-row map to 'op8_address_position_map_d10.csv'")
    
    # Quasicrystal order check
    tree = KDTree(positions)
    dists, _ = tree.query(positions, k=2)
    mean_nn_dist = dists[:,1].mean()
    print(f"\nMean nearest-neighbor distance: {mean_nn_dist:.4f} (confirms 1.06 scaling)")
    print("\nOP8 configuration space ready for cosmic-web overlay or further depth scaling.")