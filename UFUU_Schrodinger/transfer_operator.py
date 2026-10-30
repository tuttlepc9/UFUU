"""
Transfer-operator / linearized fold helpers.

Goal: make the λ_sym computation that AI_RESEARCH_BRIEF.md attributes to
fold_schrodinger_sympy_verification.py actually exist as callable code.

Symmetric-mode gain under info-max alignment is αη. When α, η are omitted,
they are fixed from the Banach attractor U* via the vacuum+child model
    U* = 1 + λ_sym / 2,  λ_sym = α η,  α = η
so λ_sym = 2(U* − 1). That closes the α,η → λ_sym bridge encoded by
tests/test_one_true_answer.py (F2).
"""

from __future__ import annotations

import math
from typing import Optional, Tuple

try:
    import sympy as sp
except ImportError:  # pragma: no cover
    sp = None

from .scaling_identities import LAMBDA_SYM_REPORTED, U_STAR


def reported_lambda_sym() -> float:
    """Repo-reported numerical λ_sym (historical constant ≈ 0.259)."""
    return float(LAMBDA_SYM_REPORTED)


def reported_u_star() -> float:
    return float(U_STAR)


def normalize_alpha_eta_from_fixed_point(u_star: float = U_STAR) -> Tuple[float, float]:
    """
    Fix (α, η) from U ≅ F(U,U) at the Banach attractor U*.

    Model (equal factors, unit vacuum + symmetric child gain):
        U* = 1 + λ_sym / 2
        λ_sym = α η,  α = η
    ⇒ λ_sym = 2 (U* − 1),  α = η = √(2 (U* − 1)).

    This is the unique equal-factor normalization that places the attractor
    one unit above vacuum with total symmetric-mode gain λ_sym.
    """
    if u_star <= 1.0:
        raise ValueError(f"u_star must be > 1 for vacuum+child model; got {u_star}")
    lam = 2.0 * (u_star - 1.0)
    a = math.sqrt(lam)
    return a, a


def symmetric_mode_gain(alpha: complex, eta: complex, dtheta: float = 0.0, delta_sym: float = 0.0) -> complex:
    """
    Linearized symmetric-mode gain: δ_L = δ_R = 1, phase factor e^{i(Δθ+δ)}.

    From U_d^fluct = (α η / 2) (δ_L + δ_R e^{i(Δθ+δ)}):
        gain = (α η / 2) (1 + e^{i(Δθ+δ)})
    At info-max alignment Δθ+δ = 0: gain = α η.
    """
    import cmath

    phase = cmath.exp(1j * (dtheta + delta_sym))
    return (alpha * eta / 2.0) * (1.0 + phase)


def sympy_linearized_fold():
    """Return the same symbolic objects as fold_schrodinger_sympy_verification.py."""
    if sp is None:
        raise ImportError("sympy is required")
    delta_L, delta_R, alpha, eta, delta_sym = sp.symbols(
        "delta_L delta_R alpha eta delta", complex=True
    )
    dtheta = sp.symbols(r"\Delta\theta", real=True)
    phase_term = delta_R * sp.exp(sp.I * (dtheta + delta_sym))
    taylor_phase = phase_term.series(dtheta, 0, 3).removeO()
    U_d_fluct = (alpha * eta / 2) * (delta_L + taylor_phase)
    return {
        "taylor_phase": taylor_phase,
        "U_d_fluct": U_d_fluct,
        "laplacian_coeff": taylor_phase.coeff(dtheta**2),
    }


def transfer_matrix_symmetric(alpha: float, eta: float):
    """
    2×2 transfer matrix on (δ_L, δ_R) for aligned phase (Δθ+δ = 0):

        M = (αη/2) * [[1, 1], [1, 1]]

    Dominant eigenvalue is αη (= λ_sym); the antisymmetric mode has eigenvalue 0.
    """
    if sp is None:
        raise ImportError("sympy is required")
    g = alpha * eta / 2.0
    return sp.Matrix([[g, g], [g, g]])


def compute_lambda_sym_from_normalization(
    alpha: Optional[float] = None,
    eta: Optional[float] = None,
) -> float:
    """
    Obtain λ_sym from α, η under symmetric alignment.

    When α or η is omitted, both are fixed from the Banach attractor U* via
    `normalize_alpha_eta_from_fixed_point` (first-principles bridge from
    U ≅ F(U,U)). The result equals the dominant transfer-matrix eigenvalue.
    """
    if alpha is None or eta is None:
        alpha, eta = normalize_alpha_eta_from_fixed_point()
    gain = symmetric_mode_gain(alpha, eta, dtheta=0.0, delta_sym=0.0)
    return float(gain.real)
