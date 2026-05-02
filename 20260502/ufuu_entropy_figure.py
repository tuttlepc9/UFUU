"""
UFUU Entropy Monotonicity Baseline Figure
Formatted for Foundations of Physics submission (Springer)
Author: Jason Tuttle (tuttlepc9/UFUU)
Generated: 2026-05-02

Output: ufuu_entropy_fig_op4.pdf  (vector, 300+ dpi equivalent)
        ufuu_entropy_fig_op4.png  (600 dpi raster backup)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import json

# ── Load data ────────────────────────────────────────────────────────────────
with open('/mnt/user-data/uploads/ufuu_entropy_baseline_results.json') as f:
    raw = json.load(f)

depths  = np.array([int(k) for k in raw])
ufuu    = np.array([raw[k]['ufuu']  for k in raw])
means   = np.array([raw[k]['mean']  for k in raw])
stds    = np.array([raw[k]['std']   for k in raw])
maxima  = np.array([raw[k]['max']   for k in raw])

sigma_sep = (ufuu - means) / stds   # σ above random mean at each depth

# ── Springer / Foundations of Physics style setup ─────────────────────────
# Single-column width: 84 mm ≈ 3.31 in
# Double-column width: 174 mm ≈ 6.85 in  ← we use this for clarity
FIG_W   = 6.85
FIG_H   = 4.80

FONT_FAMILY = 'serif'
matplotlib.rcParams.update({
    'font.family':          FONT_FAMILY,
    'font.size':            9,
    'axes.titlesize':       9,
    'axes.labelsize':       9,
    'xtick.labelsize':      8,
    'ytick.labelsize':      8,
    'legend.fontsize':      8,
    'legend.framealpha':    0.92,
    'legend.edgecolor':     '#999999',
    'lines.linewidth':      1.4,
    'axes.linewidth':       0.8,
    'xtick.major.width':    0.8,
    'ytick.major.width':    0.8,
    'xtick.minor.width':    0.5,
    'ytick.minor.width':    0.5,
    'xtick.direction':      'in',
    'ytick.direction':      'in',
    'xtick.minor.visible':  True,
    'ytick.minor.visible':  True,
    'figure.dpi':           300,
    'savefig.dpi':          600,
    'savefig.bbox':         'tight',
    'savefig.pad_inches':   0.04,
    'pdf.fonttype':         42,   # embeds fonts (required by Springer)
    'ps.fonttype':          42,
})

# Colour palette (accessible, print-safe)
C_UFUU   = '#1a1a2e'   # near-black navy  — UFUU line
C_MEAN   = '#c0392b'   # deep red         — random mean
C_FILL   = '#e8a09a'   # pale red         — ±1σ fill
C_MAX    = '#7f8c8d'   # medium grey      — random max scatter
C_SIGMA  = '#2980b9'   # blue             — σ panel

# ── Figure layout: 2 rows, shared x-axis ─────────────────────────────────
fig, (ax_main, ax_sig) = plt.subplots(
    2, 1,
    figsize=(FIG_W, FIG_H),
    sharex=True,
    gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.08}
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOP PANEL — entropy curves
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ±1σ shaded band
ax_main.fill_between(
    depths, means - stds, means + stds,
    color=C_FILL, alpha=0.55, zorder=1,
    label=r'Random fold mean $\pm 1\sigma$ ($N=200$)'
)

# Random mean
ax_main.plot(
    depths, means,
    color=C_MEAN, lw=1.4, ls='--', zorder=2,
    label='Random fold mean'
)

# Random max scatter (individual best trials)
ax_main.scatter(
    depths, maxima,
    color=C_MAX, s=18, zorder=3, marker='v',
    label='Random fold maximum'
)

# UFUU — exact maximum entropy line
ax_main.plot(
    depths, ufuu,
    color=C_UFUU, lw=2.0, zorder=4,
    label=r'UFUU: $H(d) = d$ (exact maximum)'
)

# Ideal reference diagonal (dashed, very light)
ax_main.plot(
    depths, depths,
    color=C_UFUU, lw=0.6, ls=':', alpha=0.25, zorder=0
)

# Annotations at selected depths
for d_ann, va, offset in [(6, 'bottom', 0.4), (12, 'bottom', 0.4), (18, 'bottom', 0.4)]:
    idx = d_ann - 1
    gap = ufuu[idx] - maxima[idx]
    ax_main.annotate(
        f'$\\Delta = {gap:.2f}$ b',
        xy=(depths[idx], maxima[idx]),
        xytext=(depths[idx] + 0.3, maxima[idx] + 1.05),
        fontsize=6.5,
        color=C_UFUU,
        arrowprops=dict(arrowstyle='->', color=C_UFUU, lw=0.7),
        va=va,
    )

ax_main.set_ylabel('Shannon entropy $H$ (bits)', labelpad=4)
ax_main.set_xlim(0.5, 20.5)
ax_main.set_ylim(-0.5, 22)
ax_main.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(4))
ax_main.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))

# Legend (upper left, clean)
handles_main = [
    Line2D([0],[0], color=C_UFUU, lw=2.0,
           label=r'UFUU: $H(d)=d$ (exact maximum)'),
    Line2D([0],[0], color=C_MEAN, lw=1.4, ls='--',
           label=r'Random fold mean ($N=200$)'),
    mpatches.Patch(color=C_FILL, alpha=0.55,
                   label=r'$\pm 1\sigma$ random envelope'),
    Line2D([0],[0], color=C_MAX, lw=0, marker='v', ms=5,
           label='Random fold maximum'),
]
ax_main.legend(handles=handles_main, loc='upper left', frameon=True)

ax_main.text(
    0.98, 0.06,
    'Open Problem 4 — Entropy Monotonicity Baseline',
    transform=ax_main.transAxes,
    ha='right', va='bottom',
    fontsize=6.5, color='#555555', style='italic'
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BOTTOM PANEL — σ separation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ax_sig.bar(
    depths, sigma_sep,
    color=C_SIGMA, alpha=0.75, width=0.7, zorder=2
)
ax_sig.axhline(3, color='#e67e22', lw=0.9, ls='--', zorder=3)
ax_sig.text(20.3, 3.1, r'$3\sigma$', color='#e67e22', fontsize=7, va='bottom')

ax_sig.set_xlabel('Recursion depth $d$', labelpad=4)
ax_sig.set_ylabel(r'$\sigma$ above\nrandom mean', labelpad=4, fontsize=7.5)
ax_sig.set_ylim(0, 15)
ax_sig.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(3))
ax_sig.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
ax_sig.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
ax_sig.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Shared spine / tick cleanup
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for ax in (ax_main, ax_sig):
    ax.tick_params(which='both', top=True, right=True)
    ax.spines['top'].set_linewidth(0.5)
    ax.spines['right'].set_linewidth(0.5)

# Remove gap between panels
fig.subplots_adjust(top=0.97, bottom=0.09)

# ── Save ─────────────────────────────────────────────────────────────────────
pdf_path = '/mnt/user-data/outputs/ufuu_entropy_fig_op4.pdf'
png_path = '/mnt/user-data/outputs/ufuu_entropy_fig_op4.png'
fig.savefig(pdf_path)
fig.savefig(png_path)
print(f"Saved PDF: {pdf_path}")
print(f"Saved PNG: {png_path}")

# ── Print figure caption (copy into paper) ───────────────────────────────────
caption = """
FIGURE CAPTION (for paper):

Fig. X. Entropy monotonicity baseline comparison for the UFUU binary-fold operator
(Open Problem 4). Upper panel: Shannon entropy H(d) at recursion depth d for the
UFUU symmetric eigenmode (solid black; H = d exactly, by the information-maximization
constraint) versus a Monte Carlo ensemble of 200 random binary-fold operators with
phase offsets Delta-theta drawn uniformly from [0, 2pi) and local scaling factors
drawn from the same physical range used in the analytic derivation. The shaded band
shows the +/-1-sigma random envelope; inverted triangles mark the per-depth maximum
over all 200 trials. Annotated gaps Delta indicate the separation in bits between the
UFUU value and the best random realization at selected depths. Lower panel: sigma-
separation of the UFUU entropy from the random ensemble mean at each depth. The
dashed orange line marks the 3-sigma threshold. UFUU exceeds 3 sigma at d >= 5 and
reaches 13.1 sigma at d = 20. Entropy maximization is not a generic property of
binary-fold operators; it is a structural signature of the symmetric eigenmode
selected by the information-maximization primitive (Section 3).
"""
print(caption)
