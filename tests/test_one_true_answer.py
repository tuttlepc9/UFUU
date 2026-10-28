"""
Pytest suite for the UFUU "one true answer" scaling claims.

Passing tests encode analytically closed identities (r^{12}=2).
Failing tests encode documented gaps that a draft PR must close:
  F1. fold_schrodinger_sympy_verification.py still does not *compute* λ_sym.
  F2. λ_sym is not first-principles-computable without fixing α, η
      (open normalization problem).
"""

from __future__ import annotations

import math
import pathlib
import re

import pytest

from UFUU_Schrodinger.scaling_identities import (
    DEPTH_OCTAVE,
    LAMBDA_SYM_REPORTED,
    U_STAR,
    OctaveScaling,
    butterfly_ii_over_i_prediction,
    core_equation_normalized,
)
from UFUU_Schrodinger.transfer_operator import (
    compute_lambda_sym_from_normalization,
    reported_lambda_sym,
    symmetric_mode_gain,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SYMPY_SCRIPT = REPO_ROOT / "UFUU_Schrodinger" / "fold_schrodinger_sympy_verification.py"
BRIEF = REPO_ROOT / "AI_RESEARCH_BRIEF.md"
DERIVATION = REPO_ROOT / "UFUU_Research_Notebook_20260430_1p06_Derivation.md"


# ---------------------------------------------------------------------------
# Passing: closed analytic identities
# ---------------------------------------------------------------------------

def test_octave_identity_exact():
    s = OctaveScaling()
    assert math.isclose(s.r**DEPTH_OCTAVE, 2.0, rel_tol=0, abs_tol=1e-15)
    assert math.isclose(s.mu**DEPTH_OCTAVE, 0.5, rel_tol=0, abs_tol=1e-15)
    assert math.isclose(s.mu, 1.0 / s.r, rel_tol=0, abs_tol=1e-15)


def test_r_matches_documented_constant():
    assert math.isclose(OctaveScaling().r, 1.0594630943592953, rel_tol=0, abs_tol=1e-15)


def test_butterfly_ratio_prediction():
    pred = butterfly_ii_over_i_prediction()
    empirical = 1.123206
    assert abs(empirical - pred) / pred < 0.001


def test_core_equation_normalized_form():
    U = complex(U_STAR, 0.0)
    F_UU = U * U
    assert core_equation_normalized(U, F_UU)


def test_symmetric_mode_gain_alignment():
    g = symmetric_mode_gain(0.5, 0.518, dtheta=0.0, delta_sym=0.0)
    assert math.isclose(g.real, 0.5 * 0.518, rel_tol=1e-12)
    assert abs(g.imag) < 1e-15


def test_reported_lambda_sym_constant():
    assert reported_lambda_sym() == pytest.approx(0.259)


def test_category_error_is_real():
    """Sanity: λ_sym^{12} is nowhere near 1/2."""
    assert abs(LAMBDA_SYM_REPORTED**DEPTH_OCTAVE - 0.5) > 0.4
    checks = OctaveScaling().check_identities()
    assert checks["category_error_documented"] is True
    assert checks["lambda_sym_to_depth_equals_half"] is False


def test_derivation_notebook_has_erratum():
    """After local rework, the 1p06 notebook must correct the category error."""
    text = DERIVATION.read_text(encoding="utf-8")
    assert "ERRATUM" in text
    assert ("category error" in text.lower()) or ("2^{-1/12}" in text)


def test_brief_no_longer_marks_sympy_lambda_verified():
    brief = BRIEF.read_text(encoding="utf-8")
    # The sympy script row must not claim [VERIFIED] for λ_sym anymore.
    for line in brief.splitlines():
        if "fold_schrodinger_sympy_verification.py" in line:
            assert "[VERIFIED]" not in line
            assert "gap" in line.lower() or "PARTIAL" in line
            break
    else:
        pytest.fail("brief missing sympy verification row")


# ---------------------------------------------------------------------------
# Failing: open implementation gaps
# ---------------------------------------------------------------------------

def _executable_source(path: pathlib.Path) -> str:
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("#"):
            continue
        lines.append(line)
    return "\n".join(lines)


def test_sympy_verification_script_computes_lambda_sym():
    """
    FAILING BY DESIGN until the SymPy script gains a real λ_sym computation.

    Mentions inside comments (erratum notes) do not count.
    """
    code = _executable_source(SYMPY_SCRIPT)
    assigns = re.search(r"\b(lambda_sym|lam_sym)\s*=", code)
    prints_val = ("0.259" in code) or re.search(
        r"print\(.*(lambda_sym|lam_sym)", code
    )
    has_eigen_call = re.search(r"eigen|matrix_eigen|transfer", code, re.I)
    assert assigns and (prints_val or has_eigen_call), (
        "fold_schrodinger_sympy_verification.py still lacks executable "
        "λ_sym computation (assignment + eigenvalue/gain path). Mentions in "
        "comments do not count. See "
        "transfer_operator.compute_lambda_sym_from_normalization."
    )


def test_lambda_sym_first_principles_from_script_normalization():
    """
    FAILING BY DESIGN: α, η normalization bridge from U ≅ F(U,U) → λ_sym
    is not implemented yet.
    """
    try:
        lam = compute_lambda_sym_from_normalization()
    except NotImplementedError as exc:
        pytest.fail(str(exc))
    assert lam == pytest.approx(0.259, rel=0.05)
