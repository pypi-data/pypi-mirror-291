import jax.numpy as jnp
import typing
import chex
import jax.scipy as jscipy
import jax
import numpy as np
from bfastor.blur.utils import sum_logs
import bfastor.core


def log_gaussian(x, mean, cov_matrix):
    return jscipy.stats.multivariate_normal.logpdf(x, mean=mean, cov=cov_matrix)


# @chex.assert_max_traces(n=2)  # once for warmup jit and once for main grad/jit
def simulate_density_from_single_atom(
    x: typing.Union[jnp.ndarray, np.ndarray, int, float],
    atom_centre: typing.Union[jnp.ndarray, np.ndarray, int, float],
    b_factor: typing.Union[jnp.ndarray, np.ndarray, int, float],
):
    """Simulate the one density point from a single atom

    Args:
        x: Quantiles - the position of the coordinates we want to blur at.
            shape: (P, 3) for P positions
        atom_centre: Coordinate of the atom.
            shape: (3,)
        b_factor: B-factor of the atom
            shape: (1,)
    Returns:
        jnp.ndarray containing the probability density
    """
    chex.assert_shape(x, (3,))
    result = log_gaussian(
        x,
        atom_centre,
        b_factor**2,
    )
    chex.assert_rank(result, 0)
    return result


_simulate_densities_from_single_atom = jax.vmap(
    simulate_density_from_single_atom, in_axes=(0, None, None)
)


def simulate_densities_from_single_atom(
    x: typing.Union[jnp.ndarray, np.ndarray],
    atom_centre: typing.Union[jnp.ndarray, np.ndarray, float],
    b_factor: typing.Union[jnp.ndarray, np.ndarray, float],
):
    """Simulate the density at points around a single atom

    Args:
        x: Quantiles - the position of the coordinates we want to blur at.
            shape: (P, 3) for P positions
        atom_centre: Central coordinate of the atom.
            shape: (3,)
        b_factor: B-factor of the atom
            shape: (1,)
    Returns:
        jnp.ndarray containing the probability density
    """
    chex.assert_rank(x, 2)
    results = _simulate_densities_from_single_atom(x, atom_centre, b_factor)
    return results


def simulate_density_summed_from_multiple_atoms(
    x: typing.Union[jnp.ndarray, np.ndarray],
    atom_centres: typing.Union[jnp.ndarray, np.ndarray],
    b_factor: typing.Union[jnp.ndarray, np.ndarray],
):
    """Simulate the density at points including contributions from
    multiple atoms

    Args:
        x: Quantiles - the position of the coordinates we want to blur at
            shape: (P, 3) for blurring P positions around each atom
        atom_centres: Central coordinate of the atom
            shape: (Nn, 3) for blurring around N neighbouring atoms
        b_factor: B-factor of the atom
            shape: (Nn,) for blurring around N neighbouring atoms
    Returns:
        jnp.ndarray containing the probability density
    """
    chex.assert_rank(atom_centres, 2)
    chex.assert_rank(b_factor, 1)
    non_summed_points = jax.vmap(  # vectorise over multiple atoms
        simulate_densities_from_single_atom,
        in_axes=(None, 0, 0),
    )(
        x,
        atom_centres,
        b_factor,
    )
    chex.assert_rank(non_summed_points, 2)
    v = jax.vmap(sum_logs, in_axes=1)(non_summed_points)
    return v


def simulate_summed_points_from_all_atoms(
    x: typing.Union[jnp.ndarray, np.ndarray],
    atom_centres: typing.Union[jnp.ndarray, np.ndarray],
    b_factor: typing.Union[jnp.ndarray, np.ndarray],
):
    """Simulate the density at points including contributions from
    multiple atoms

    Args:
        x: The positions of the coordinates we want to blur at.
            shape: (N, P, 3) for blurring P positions around N atoms
        atom_centres: Central coordinate of the atom
            shape: (N, Nn, 3) for blurring density for N atoms, including
            contributions from Nn neighbouring atoms.
        b_factor: B-factor of the atom
            shape: (N, Nn,) for blurring density for N atoms, including
            contributions from Nn neighbouring atoms.
    Returns:
        jnp.ndarray containing the probability density
    """
    chex.assert_rank(atom_centres, 3)
    chex.assert_rank(b_factor, 2)
    densities = jax.vmap(  # vectorise to map over all axes simultaneously
        simulate_density_summed_from_multiple_atoms,
        in_axes=(0, 0, 0),
        axis_size=x.shape[0],
    )(
        x,
        atom_centres,
        b_factor,
    )
    chex.assert_rank(densities, 2)
    return densities


def simulate_densities_from_params(
    params: bfastor.core.Parameters, random_vectors: jax.Array, neighbours_ij: jax.Array
) -> jnp.ndarray:
    return simulate_summed_points_from_all_atoms(
        random_vectors,
        params.coordinates[neighbours_ij],
        params.sigmas[neighbours_ij],
    )


def ijk_to_xyz(ijk_points, map_apix):
    return jnp.flip(ijk_points, axis=1) * map_apix
