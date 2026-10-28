"""UFUU Schrödinger / transfer-operator package."""

from .scaling_identities import (
    DEPTH_OCTAVE,
    LAMBDA_SYM_REPORTED,
    U_STAR,
    OctaveScaling,
    butterfly_ii_over_i_prediction,
    core_equation_normalized,
    r_ladder,
)
from .transfer_operator import (
    compute_lambda_sym_from_normalization,
    normalize_alpha_eta_from_fixed_point,
    reported_lambda_sym,
    reported_u_star,
    symmetric_mode_gain,
    transfer_matrix_symmetric,
)

__all__ = [
    "DEPTH_OCTAVE",
    "LAMBDA_SYM_REPORTED",
    "U_STAR",
    "OctaveScaling",
    "butterfly_ii_over_i_prediction",
    "core_equation_normalized",
    "r_ladder",
    "compute_lambda_sym_from_normalization",
    "normalize_alpha_eta_from_fixed_point",
    "reported_lambda_sym",
    "reported_u_star",
    "symmetric_mode_gain",
    "transfer_matrix_symmetric",
]
