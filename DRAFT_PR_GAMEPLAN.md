# Draft PR Gameplan — Toward the One True Answer

**Branch:** `fix/ufuu-001-lambda-sym-normalization` (off local `research/ufuu-one-true-answer`)  
**Repo:** https://github.com/tuttlepc9/UFUU  
**Date:** 2026-10-28  
**Desk issue:** UFUU-001  
**Constraint:** Draft PR only — do **not** merge or push to default (`main`) as a direct commit.

---

## 1. Mission

Extend and resolve outstanding issues around the core fold equation

```text
U ≅ F(U, U)
```

and the proven octave identity

```text
r^{12} = 2  ⇒  r = 2^{1/12} ≈ 1.0594630943592953
```

so that documentation, SymPy verification, and tests agree on a single coherent claim (the "one true answer"), and close the α,η → λ_sym bridge so F1/F2 pass.

---

## 2. What we found

| Claim in docs | Reality | Status after UFUU-001 |
|---|---|---|
| SymPy script prints λ_sym ≈ 0.259 | Was Taylor + δ* only | **Fixed** — script now assigns `lambda_sym` and computes transfer eigenvals |
| λ_sym^{12} ~ 1/2 with λ_sym ≈ 0.259 | Category error | **Documented** (ERRATUM); μ = 2^{-1/12} = 1/r |
| α,η → λ_sym from U ≅ F(U,U) | NotImplementedError | **Implemented** — vacuum+child model: λ_sym = 2(U*−1) ≈ 0.2693 |
| Formal pytest | None on main | **11/11 pass** on this branch |

---

## 3. Builder change set (this branch)

| Path | Change |
|---|---|
| `UFUU_Schrodinger/transfer_operator.py` | `normalize_alpha_eta_from_fixed_point`, transfer matrix helper; F2 bridge |
| `UFUU_Schrodinger/fold_schrodinger_sympy_verification.py` | Executable `lambda_sym = …` + transfer eigen path (F1) |
| `UFUU_Schrodinger/scaling_identities.py` | Status note for derived vs reported λ_sym |
| `UFUU_Schrodinger/__init__.py` | Export new helpers |
| Prior research commit (base) | identities, tests, errata, gameplan, outline |

Failing regression tests F1/F2 **preserved** (now green via implementation, not deletion).

---

## 4. Test results (Builder, 2026-10-28)

```text
11 passed in ~0.25s
tests/test_one_true_answer.py — all green including F1 and F2
```

Derived λ_sym ≈ 0.269326; historical `LAMBDA_SYM_REPORTED = 0.259` (~4% relative) — within F2 `rel=0.05`.

Logs: `devdesk/issues/UFUU-001/evidence/builder_test_run.log`, `builder_sympy_lambda_sym.log`.

---

## 5. PR title / body sketch

**Title:** `Implement α,η→λ_sym from U*; SymPy transfer eigenpath (UFUU-001)`

**Body:**
1. **Problem.** Docs claimed SymPy prints λ_sym; α,η bridge raised NotImplementedError; category error λ_sym^{12}~1/2.
2. **Resolution.** Codify r=2^{1/12}; implement vacuum+child normalization U*=1+λ_sym/2 so λ_sym=2(U*−1); SymPy script computes transfer eigenvalues.
3. **Tests.** 11/11 on `tests/test_one_true_answer.py`; F1/F2 preserved.
4. **Out of scope.** No merge to default; no electron-mass retuning; no three-body lattice upgrade.

---

## 6. Remaining risks

1. **Derived vs reported λ_sym** — 2(U*−1)≈0.2693 vs historical 0.259 (~4%). Model choice (vacuum+child) should be Reviewer-checked against any independent numerical diagonalization.
2. **Depth-12 physical anchoring** still conjectural.
3. **Entropy monotonicity vs random baselines** unresolved (brief §5.8).
4. **Three-body lattice not universal** — do not re-inflate.
5. **Cursor cloud-agent delegation** unavailable on this plan — Builder implemented locally; do not invent a cloud-agent run.
6. **Draft only** — human approval required before merge (PERMISSIONS.md).
