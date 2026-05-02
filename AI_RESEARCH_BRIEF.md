# AI_RESEARCH_BRIEF.md
# UFUU Research Repository — Stateless Entry Point
# Author: Jason Tuttle (tuttlepc9/UFUU)
# Last updated: 2026-05-02
# Purpose: Enable any AI session (or new collaborator) to orient immediately,
#          understand what is solid vs. conjectural, and identify productive next steps.

---

## 0. How to Use This Document

Read sections 1–3 first. They tell you what the theory is, what is actually proven,
and what the file to start with is. Sections 4–6 give you the dependency map, the
honest weakness inventory, and suggested next-session tasks. Do not treat claims in
the repo as established unless they are marked [PROVEN] below.

---

## 1. Theory Architecture (Three Levels)

### Level 1 — Tuttle's Triad (top / universal)
Three abstract primitives that define the recursive fold architecture:
- **Recursive binary folding** — any state U decomposes into left/right sub-states
- **Information maximization** — the fold selects the phase that maximizes local
  von Neumann entropy / mutual information at each node
- **Symmetry breaking** — the fold is asymmetric; left and right branches are not
  equivalent

The Triad is the "why" layer. It is architecture, not a specific model.
It is not falsified by any single prediction failing.

### Level 2 — UFUU as Candidate Fold (middle / specific)
UFUU is one concrete instantiation of the Triad, defined by:

    U ≅ F(U,U)

realized as a Hilbert-space coalgebra with binary decomposition, an information-
maximizing symmetric eigenmode, and a depth-12 quantum-to-classical transition.

This yields:
- Dominant contraction eigenvalue: λ_sym ≈ 0.259
- Depth-12 scaling ratio: r = 2^{1/12} ≈ 1.059463  [PROVEN — see Section 3]
- Unique fixed-point attractor: U* ≈ 1.134663       [PROVEN — Banach FPT]

UFUU is the "how" layer. Its predictions are hypotheses about whether this particular
fold matches physical reality. If a prediction fails, UFUU may be the wrong fold;
the Triad is not thereby falsified.

### Level 3 — Specific Predictions / Applications (bottom / empirical)
Applications of the 2^{1/12} scaling and 14-eigenmode attractor count to:
- Three-body periodic orbit families
- Electron mass
- Higgs field structure
- OP7 chemistry ratios (Pauli exclusion, ionization energies)
- Cosmological filament spacing
- Biological connectome scaling

These are the "what it predicts" layer. Epistemic status varies — see Section 4.

---

## 2. The One Solid Result

> **The 2^{1/12} derivation is the load-bearing claim of the entire framework.**

Starting from U ≅ F(U,U) + information maximization alone, with zero free parameters:

    r^{12} = 2  →  r = 2^{1/12} ≈ 1.0594630943592953

This emerges as the exact dominant eigenvalue of the iterated renormalization
operator R^{12} under the symmetric eigenmode selected by information maximization.

This derivation is:
- First-principles (no tuning, no fitting)
- Symbolically verified (SymPy)
- Analytically sound
- The source of all downstream predictions

**If you are an AI session starting fresh, begin here:**
`UFUU_Research_Notebook_20260430_1p06_Derivation.md`

---

## 3. File Map with Epistemic Status

| File / Folder | What it does | Status |
|---|---|---|
| `UFUU_Research_Notebook_20260430_1p06_Derivation.md` | Analytical derivation of 2^{1/12} from binary fold + info-max | **[PROVEN]** |
| `UFUU_Schrodinger/fold_schrodinger_sympy_verification.py` | SymPy verification of transfer operator, prints λ_sym ≈ 0.259 | **[VERIFIED]** |
| `UFUU_RESEARCH_JOURNAL_INDEX.md` | Master index, P1–P5 status, overall architecture map | **[DOCUMENTED]** |
| `papers/submitted/Foundations_of_Physics_2026_04_11/` | Submitted paper (April 11 2026); not yet peer reviewed | **[SUBMITTED]** |
| `UFUU_Overarching_Narrative_20260430.docx` | Full explanatory document tying all layers together | **[DOCUMENTED]** |
| `UFUU_Electron_Mass_Prediction/` | Electron mass from fold scaling; requires 94/224 exponents | **[CONJECTURED / PARTIALLY TUNED]** |
| `UFUU_Fold_Higgs_Visualizations/` | Higgs potential as binary-fold isomorphism; visual only | **[ILLUSTRATIVE / CONJECTURAL]** |
| `UFUU_Fold_Verification_Open_Problem_4/` | OP4 entropy monotonicity; internally confirmed | **[INTERNALLY TESTED]** |
| `UFUU_Research_Notebook_20260430_OP7_Chemistry.md` | OP7 chemistry ratio predictions; no external check yet | **[UNTESTED]** |
| `annotations/` | Research notes; not load-bearing | **[NOTES]** |
| `20260412/` – `20260430/` + `20260611/` | 13 dated daily work folders; simulations, orbit plots, draft work | **[EXPLORATORY / MIXED]** |
| Three-body orbit work | Scattered across dated folders + OP6 notes; no single file | **[PARTIALLY TESTED — see below]** |

### Three-Body Status (detailed)
- Count match: UFUU produces 14 eigenmodes; catalog has 13 known families (not 14).
  Count correspondence is **weakened**.
- Period ratio test: Butterfly II / Butterfly I = 1.123206 vs 2^{2/12} = 1.122462.
  Deviation = **0.066%** (striking; one data point).
- Full inter-family lattice test (13 families, same reference): 3 of 13 within ~0.2%,
  remainder deviate 0.9–125%. Lattice is **not universal**.
- **Conclusion: suggestive clustering on a few families; not a confirmed universal law.**

---

## 4. Dependency Graph

```
fold_schrodinger_sympy_verification.py
    └─→ 1p06_Derivation.md  (SymPy-verified transfer operator)
            └─→ All notebooks, OP7_Chemistry, electron-mass folder
            └─→ UFUU_Overarching_Narrative_20260430.docx
            └─→ submitted paper (Foundations of Physics)

Dated folders (daily simulations)
    └─→ Higgs visualizations, orbit plots, annotation files

All notebooks + visualizations
    └─→ submitted paper

JOURNAL_INDEX.md
    └─→ ties P1–P5 status to all of the above
```

No circular dependencies. `1p06_Derivation.md` is the single source of truth
for the 2^{1/12} claim.

---

## 5. Known Weaknesses (honestly flagged)

1. **Electron mass not fully ab-initio.** Two phenomenological exponents (94/224)
   are required on top of the pure 2^{1/12} scaling. The prediction is partially
   tuned, not zero-parameter.

2. **Three-body lattice is not universal.** One ratio is impressive (0.066%).
   Full inter-family test fails. The 14-eigenmode count does not match the current
   catalog count of 13.

3. **Depth-12 physical scale is unanchored.** The depth-12 transition is
   structurally forced by the math but its mapping to real physical scales
   (Planck length? atomic units? something else?) remains conjectural.

4. **No external confirmation yet.** Paper submitted April 11 2026; no peer review
   response received. No independent replication.

5. **Retroactive explanation dominates.** Most predictions explain existing data
   rather than prospectively predicting new measurements. The framework needs at
   least one clean prospective prediction that can be tested before the result
   is known.

6. **Unitarity / quantum interpretation.** The complex fixed point and unitarity
   behavior under the fold (P2) are still exploratory.

7. **Entropy monotonicity in random baselines.** Earlier review noted that entropy
   monotonicity appears in random fold baselines, which would mean it is not a
   discriminating prediction. Status of this concern: unresolved.

---

## 6. Suggested Next-Session Tasks (for AI or collaborator)

**Highest priority — strengthens the core:**
- [ ] Formalize the mapping between UFUU eigenmodes and observable quantities.
      Currently informal; needs a precise definition of what "eigenmode k corresponds
      to observable X" means mathematically.
- [ ] Resolve entropy monotonicity baseline issue. Run random fold comparison and
      confirm whether UFUU's entropy behavior is distinguishable from noise.
- [ ] Identify one prospective prediction. Something measurable that the framework
      predicts *before* the experimental result is known.

**Medium priority — expands the framework:**
- [ ] Anchor depth-12 to a physical scale. What is the dimensional unit at d=12?
      This is the bridge between the abstract fold and real physics.
- [ ] Clean up electron mass derivation. Can the 94/224 exponents be derived from
      the fold structure, or are they inputs? If inputs, say so explicitly.
- [ ] OP7 chemistry: run at least one ratio against NIST data and report the result
      honestly, whatever it shows.

**Lower priority — presentation:**
- [ ] Consolidate three-body work into a single file with the honest inter-family
      table included.
- [ ] Update submitted paper abstract/section 8 to reflect the corrected three-body
      status (0.066% not 0.035%; 13 families not 14; lattice not universal).

---

## 7. What This Repo Is Not

- It is not a finished theory.
- It is not a peer-reviewed result.
- It is not a claim that UFUU is the correct fold for the universe.

It is: **a mathematically coherent candidate fold function with one strong
first-principles derivation (2^{1/12}), several suggestive empirical correspondences,
and a clear research program for strengthening or falsifying the framework.**

The 2^{1/12} derivation is real. Build from there.

---

*This brief was generated 2026-05-02 to serve as a stateless AI/collaborator
entry point. Update this file whenever a claim's status changes.*
