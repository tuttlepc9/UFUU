"""
UFUU scaling identities — the "one true answer" clarification.

Core equation (Level 2 candidate fold):
    U ≅ F(U, U)
equivalently written in the research logs as
    U = F(U, U) / U ≅ F(U, U)
when U is normalized near the fixed-point magnitude (the "/U" is a
normalization/coalgebra coassociativity shorthand, not a distinct physics law).

Two DISTINCT quantities that the April 30 notebook partially conflated:

1. Octave / observable scaling ratio r
       r^{12} = 2  ⇒  r = 2^{1/12} ≈ 1.0594630943592953
   Forced by: binary information doubling (factor 2 per full capacity cycle)
   together with the depth-12 quantum-to-classical transition (one "octave").
   This is the load-bearing first-principles claim.

2. Symmetric-mode fluctuation contraction eigenvalue λ_sym ≈ 0.259
   This is a Banach/transfer-operator contraction rate of linearized
   fluctuations around the attractor U* ≈ 1.134663. It is NOT the same
   object as r, and the notebook claim
       λ_sym^{12} ~ 1/2
   is FALSE for λ_sym ≈ 0.259 (0.259^{12} ≈ 9.1e-8, not 0.5).

   The octave contraction that *does* satisfy μ^{12} = 1/2 is
       μ = 2^{-1/12} = 1/r ≈ 0.943874
   which is the reciprocal of the observable spacing, not λ_sym.

Status (2026-10-28 UFUU-001):
- Identity (1) is analytically exact and implemented here.
- Identity (2): first-principles α,η → λ_sym via U* vacuum+child normalization
  is implemented in transfer_operator.py / fold_schrodinger_sympy_verification.py.
  Historical LAMBDA_SYM_REPORTED = 0.259 remains for category-error checks; the
  derived value is 2(U*−1) ≈ 0.2693 (within the F2 rel=0.05 window).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Documented numerical anchors from the repo (AI_RESEARCH_BRIEF.md)
U_STAR = 1.134663
LAMBDA_SYM_REPORTED = 0.259
DEPTH_OCTAVE = 12


@dataclass(frozen=True)
class OctaveScaling:
    """Exact binary-octave scaling forced by capacity doubling + depth-12."""

    depth: int = DEPTH_OCTAVE

    @property
    def r(self) -> float:
        return 2.0 ** (1.0 / self.depth)

    @property
    def mu(self) -> float:
        """Reciprocal per-level factor with μ^depth = 1/2."""
        return 2.0 ** (-1.0 / self.depth)

    def check_identities(self, tol: float = 1e-15) -> dict:
        r, mu, d = self.r, self.mu, self.depth
        return {
            "r": r,
            "mu": mu,
            "r_to_depth_equals_2": abs(r**d - 2.0) < tol,
            "mu_to_depth_equals_half": abs(mu**d - 0.5) < tol,
            "mu_equals_one_over_r": abs(mu - 1.0 / r) < tol,
            "lambda_sym_to_depth_equals_half": abs(LAMBDA_SYM_REPORTED**d - 0.5) < 1e-3,
            "lambda_sym_to_depth": LAMBDA_SYM_REPORTED**d,
            "category_error_documented": abs(LAMBDA_SYM_REPORTED**d - 0.5) > 0.4,
        }


def core_equation_normalized(U: complex, F_UU: complex, tol: float = 1e-9) -> bool:
    """
    Check the normalized coalgebra form U ≈ F(U,U)/U when |U| is away from 0,
    which is equivalent to U*U ≈ F(U,U) (i.e. U ≅ F(U,U) up to the fixed-point
    scaling convention used in the narrative docs).
    """
    if abs(U) < tol:
        return False
    return abs(U - F_UU / U) < tol or abs(U * U - F_UU) < tol


def r_ladder(n: int, depth: int = DEPTH_OCTAVE) -> float:
    """n-th rung on the 2^{k/depth} ladder."""
    return 2.0 ** (n / depth)


def butterfly_ii_over_i_prediction() -> float:
    """Predicted Butterfly II / Butterfly I period ratio = r^2 = 2^{2/12}."""
    return r_ladder(2)


if __name__ == "__main__":
    s = OctaveScaling()
    print("=== UFUU one-true-answer scaling identities ===")
    print(f"r = 2^(1/{s.depth}) = {s.r:.16f}")
    print(f"mu = 2^(-1/{s.depth}) = {s.mu:.16f}")
    for k, v in s.check_identities().items():
        print(f"  {k}: {v}")
    print(f"Butterfly II/I predicted ratio: {butterfly_ii_over_i_prediction():.12f}")
    print(f"Reported |Butterfly II/I - pred| ≈ {abs(1.123206 - butterfly_ii_over_i_prediction()):.6e}")
