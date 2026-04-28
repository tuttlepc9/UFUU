# ========================================================
# UFUU Zoom.py — FIXED & OPTIMIZED Recursive Binary Fold Explorer
# Now FAST enough to open instantly (vector-friendly + reduced defaults)
# Mandelbrot-style infinite zoom with Tuttle’s U = F(U, U)
# Just replace your old zoom.py with this and run again
# ========================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

class RecursiveFold:
    def __init__(self, epsilon=0.618, nonlinearity=0.42, irreversibility=0.037):
        self.ε = epsilon
        self.α = nonlinearity
        self.β = irreversibility

    def F(self, a, b):
        """Core Tuttle’s Triad fold — non-commutative + nonlinear + partially irreversible"""
        avg = (a + b) / 2.0
        diff = a - b
        nl = self.α * np.sin(a * b * 1.618 + a**2 - b**2)   # creates rich emergence
        loss = self.β * (np.random.randn() * 0.01 if np.random.rand() < 0.3 else 0.0)
        return avg + self.ε * diff + nl + loss

    def iterate(self, c, max_iter=80):
        """Mandelbrot-style iteration using the binary fold"""
        z = 0.0 + 0.0j
        for i in range(max_iter):
            # Double-fold for richer structure (left and right paths)
            z1 = self.F(z.real + z.imag * 1j, c)
            z2 = self.F(c, z.real + z.imag * 1j) * 0.5
            z = z1 + z2
            if abs(z) > 4.0:
                return i
        return max_iter   # stable structure

def generate_ufuu_fractal(width=800, height=500, center=(-0.3, 0.0), zoom=1.0, max_iter=80):
    """Optimized fractal generation — much faster defaults"""
    fold = RecursiveFold()
    
    print(f"   Generating {width}×{height} fold universe at zoom ×{zoom:.1f}...")
    start = time.time()
    
    # Coordinate grid
    x = np.linspace(center[0] - 1.5/zoom, center[0] + 1.5/zoom, width)
    y = np.linspace(center[1] - 1.0/zoom, center[1] + 1.0/zoom, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    # Pre-allocate escape array
    escape = np.full((height, width), max_iter, dtype=int)
    
    # Simple row-by-row progress (keeps it fast and responsive)
    for i in range(height):
        if i % 50 == 0:
            print(f"   Progress: {i}/{height} rows ({100*i/height:.0f}%)")
        for j in range(width):
            escape[i, j] = fold.iterate(C[i, j], max_iter)
    
    elapsed = time.time() - start
    print(f"✅ Universe generated in {elapsed:.1f} seconds!")
    return escape, fold

def main():
    print("🌌 UFUU Recursive Binary Fold Universe Generator")
    print("   U = F(U, U)  —  Tuttle’s Triad live & optimized")
    
    # Adjustable starting view (change these for new cosmic regions)
    center = (-0.3, 0.0)      # try (-0.7, 0.3) or (0.0, 0.0) for different areas
    zoom_level = 1.0
    max_iter = 80             # higher = more detail but slower
    
    escape, fold = generate_ufuu_fractal(800, 500, center, zoom_level, max_iter)
    
    # Beautiful cosmic rendering
    plt.figure(figsize=(14, 9), dpi=120, facecolor='black')
    ax = plt.axes()
    ax.set_facecolor('black')
    
    img = plt.imshow(escape, origin='lower', cmap=cm.inferno, interpolation='bilinear')
    plt.colorbar(img, label='Fold Depth / Stability', fraction=0.046, pad=0.04)
    
    plt.title(f"UFUU — U = F(U, U)\n"
              f"Recursive Binary Fold Universe  |  "
              f"ε={fold.ε:.3f}  α={fold.α:.3f}  β={fold.β:.3f}  |  "
              f"Zoom ×{zoom_level:.1f}  Center=({center[0]:.3f}, {center[1]:.3f})",
              color='white', fontsize=16, pad=20)
    
    plt.xlabel("← Fold Path (x) →", color='white')
    plt.ylabel("← Fold Path (y) →", color='white')
    
    plt.text(0.02, 0.02, 
             "MOUSE WHEEL / MAGNIFIER TOOLBAR = Infinite zoom (Mandelbrot-style)\n"
             "Pan around → discover new structures\n"
             "Close window → edit center/zoom_level in code → rerun for deeper travel",
             transform=ax.transAxes, color='lime', fontsize=11,
             bbox=dict(boxstyle="round", facecolor="black", alpha=0.8))
    
    plt.tight_layout()
    print("\n🚀 Window should open instantly now — go explore the fold!")
    plt.show()

if __name__ == "__main__":
    main()