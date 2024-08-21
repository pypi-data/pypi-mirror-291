from dataclasses import dataclass
from typing import Union
import numpy as np

from scipy.spatial import ConvexHull


@dataclass
class PLRVs:
    """
    Privacy loss random variables.
    """

    lower_loss_Y: float
    lower_loss_Z: float
    pmf_Y: np.ndarray
    pmf_Z: np.ndarray


def _get_alpha(
    plrvs: PLRVs,
    beta: Union[float, np.ndarray],
):
    # get discrete points of alpha, beta
    alphas = np.cumsum(plrvs.pmf_Z) - plrvs.pmf_Z
    betas = np.cumsum(plrvs.pmf_Y)

    # numpy magic to get target index
    idx_Y = np.searchsorted(betas, beta)

    # sanity check: did we find the correct index?
    assert np.all(betas[idx_Y - 1] <= beta) and np.all(beta <= betas[idx_Y])

    # find gamma
    gamma = (betas[idx_Y] - beta) / plrvs.pmf_Y[idx_Y]

    # sanity check: gamma should be a positive and less than 1
    assert np.all(0 < gamma) and np.all(gamma < 1)

    # get index in the Y world
    idx_Z = -plrvs.lower_loss_Z - plrvs.lower_loss_Y - idx_Y

    # compute alpha
    alpha = alphas[idx_Z] + gamma * plrvs.pmf_Z[idx_Z]

    # sanity check: did we somehow go over to the next alpha?
    assert np.all(alphas[idx_Z] <= alpha) and np.all(alpha <= alphas[idx_Z + 1])

    # all sanity checks passed. Return alpha
    return alpha


def _get_beta(
    plrvs: PLRVs,
    alpha: Union[float, np.ndarray],
):
    # Get the discrete points of alpha, beta
    alphas = np.cumsum(plrvs.pmf_Z) - plrvs.pmf_Z
    betas = np.cumsum(plrvs.pmf_Y)

    # Binary search to find the right index.
    idx_Z = np.searchsorted(alphas, alpha) - 1

    # Sanity check: did we find the correct index?
    # Note that the alphas are in descending order.
    assert np.all(alphas[idx_Z] <= alpha) and np.all(alpha <= alphas[idx_Z + 1])

    # Find gamma.
    gamma = (alpha - alphas[idx_Z]) / plrvs.pmf_Z[idx_Z]

    # Sanity check: gamma should be a positive and less than 1
    assert np.all(0 < gamma) and np.all(gamma < 1)

    # Get index in the Y world
    idx_Y = -plrvs.lower_loss_Z - plrvs.lower_loss_Y - idx_Z

    # Compute beta.
    beta = betas[idx_Y] - gamma * plrvs.pmf_Y[idx_Y]

    # Sanity check: did we somehow go over to the next beta?
    assert np.all(betas[idx_Y - 1] <= beta) and np.all(beta <= betas[idx_Y])

    return beta


def _ensure_array(x):
    if isinstance(x, (int, float)):
        return np.array([x])
    return np.array(x)


def _symmetrize_trade_off_curves(alpha, beta1, beta2):
    # Combine alphas and betas into a single array of points
    points = np.column_stack(
        (
            np.concatenate((alpha, alpha)),
            np.concatenate((beta1, beta2)),
        )
    )

    # Calculate the convex hull
    hull = ConvexHull(points)

    # Get the vertices of the convex hull
    hull_vertices = points[hull.vertices]
    idx = np.argsort(hull_vertices[:, 0])
    return hull_vertices[idx, 0], hull_vertices[idx, 1]


def get_beta(
    plrvs: PLRVs,
    alpha: Union[float, np.ndarray],
    alpha_grid_step=1e-4,
) -> Union[float, np.ndarray]:
    """
    Get the trade-off curve from PLRVs.

    By Z we denote negative X, as that is the convention in dp_accounting.
    """
    alpha_prime = np.linspace(
        alpha_grid_step,
        1.0 - alpha_grid_step,
        int(np.ceil((1.0 - 2 * alpha_grid_step) / alpha_grid_step)),
    )
    beta1 = _get_beta(plrvs, alpha_prime)
    beta2 = _get_alpha(plrvs, alpha_prime)

    sym_alpha, sym_beta = _symmetrize_trade_off_curves(alpha_prime, beta1, beta2)

    return 1 - np.interp(
        _ensure_array(alpha), sym_alpha, 1 - sym_beta, left=0.0, right=1.0
    )
