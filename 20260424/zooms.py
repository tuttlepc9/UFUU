# ========================================================
# UFUU Interactive Explorer — True Infinite Zoom
# Click to dive deeper into the recursive binary fold
# ========================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

class RecursiveFold:
    def __init__(self, epsilon=0.618, nonlinearity=0.42, irreversibility=0.037):
        self.ε = epsilon          # asymmetry / non-commutativity
        self.α = nonlinearity     # emergence & novelty
        self.β = irreversibility  # time's arrow & stable structures

    def F(self, a, b):
        """Tuttle’s Triad in one expression"""
        avg = (a + b) / 2.0
        diff = a - b
        nl = self.α * np.sin(a * b * 1.618 + a**2 - b**2)   # nonlinear magic
        loss = self.β * (np.random.randn() * 0.01 if np.random.rand() < 0.3 else 0.0)
        return avg + self.ε * diff + nl + loss

    def iterate(self, c, max_iter=90):
        z = 0.0 + 0.0j
        for i in range(max_iter):
            z1 = self.F(z.real + z.imag * 1j, c)
            z2 = self.F(c, z.real + z.imag * 1j) * 0.5
            z = z1 + z2
            if abs(z) > 4.0:
                return i
        return max_iter   # stable structure

class UFUUExplorer:
    def __init__(self):
        self.fold = RecursiveFold()
        self.center = (-0.3, 0.0)
        self.zoom_level = 1.0
        self.max_iter = 90
        self.width = 900
        self.height = 600
        self.fig = None
        self.ax = None
        self.img = None

    def generate(self):
        print(f"   Generating {self.width}×{self.height} at zoom ×{self.zoom_level:.1f} (center {self.center})...")
        start = time.time()
        x = np.linspace(self.center[0] - 1.5/self.zoom_level, self.center[0] + 1.5/self.zoom_level, self.width)
        y = np.linspace(self.center[1] - 1.0/self.zoom_level, self.center[1] + 1.0/self.zoom_level, self.height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        escape = np.full((self.height, self.width), self.max_iter, dtype=int)
        for i in range(self.height):
            for j in range(self.width):
                escape[i, j] = self.fold.iterate(C[i, j], self.max_iter)
        print(f"✅ Done in {time.time() - start:.1f}s")
        return escape

    def onclick(self, event):
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        if event.button == 1:   # LEFT click = zoom IN + recenter
            self.center = (event.xdata, event.ydata)
            self.zoom_level *= 1.8
            print(f"🔎 Zooming IN → ×{self.zoom_level:.1f} at {self.center}")
        elif event.button == 3: # RIGHT click = zoom OUT
            self.zoom_level /= 1.8
            print(f"🔎 Zooming OUT → ×{self.zoom_level:.1f}")
        self.redraw()

    def redraw(self):
        escape = self.generate()
        self.img.set_array(escape)
        self.ax.set_title(f"UFUU — U = F(U, U)\n"
                          f"Recursive Binary Fold Universe  |  "
                          f"ε={self.fold.ε:.3f}  α={self.fold.α:.3f}  β={self.fold.β:.3f}  |  "
                          f"Zoom ×{self.zoom_level:.1f}  Center=({self.center[0]:.4f}, {self.center[1]:.4f})",
                          color='white', fontsize=14)
        self.fig.canvas.draw_idle()

    def run(self):
        # First render
        escape = self.generate()

        self.fig, self.ax = plt.subplots(figsize=(14, 9), dpi=120, facecolor='black')
        self.ax.set_facecolor('black')
        self.img = self.ax.imshow(escape, origin='lower', cmap=cm.inferno, interpolation='bilinear')
        plt.colorbar(self.img, label='Fold Depth / Stability')

        self.ax.set_title(f"UFUU — U = F(U, U)\n"
                          f"Recursive Binary Fold Universe  |  "
                          f"ε={self.fold.ε:.3f}  α={self.fold.α:.3f}  β={self.fold.β:.3f}  |  "
                          f"Zoom ×{self.zoom_level:.1f}  Center=({self.center[0]:.3f}, {self.center[1]:.3f})",
                          color='white', fontsize=14)

        plt.xlabel("← Fold Path (x) →", color='white')
        plt.ylabel("← Fold Path (y) →", color='white')

        # Instructions
        self.ax.text(0.02, 0.02, 
                     "LEFT CLICK anywhere = Zoom IN + recenter\n"
                     "RIGHT CLICK = Zoom OUT\n"
                     "Toolbar magnifier also works for manual drag-zoom",
                     transform=self.ax.transAxes, color='lime', fontsize=12,
                     bbox=dict(boxstyle="round", facecolor="black", alpha=0.85))

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.tight_layout()
        print("\n🚀 Interactive UFUU Explorer is LIVE!")
        print("   Click the image to explore infinitely — the math is generated on the fly!")
        plt.show()

if __name__ == "__main__":
    explorer = UFUUExplorer()
    explorer.run()