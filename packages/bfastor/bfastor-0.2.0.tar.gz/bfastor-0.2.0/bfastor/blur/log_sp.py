import functools

import jax
import jax.numpy as jnp
import chex
import numpy as np
import typing

import bfastor.core
from bfastor.blur.utils import sum_logs


@functools.partial(
    jax.jit,
    inline=True,
)
def simulate_single_gaussian(
    x: typing.Union[jnp.ndarray, np.ndarray],
    mean: typing.Union[jnp.ndarray, np.ndarray],
    bfactor: typing.Union[jnp.ndarray, np.ndarray, float],
    a: typing.Union[jnp.ndarray, np.ndarray, float],
    b: typing.Union[jnp.ndarray, np.ndarray, float],
) -> jnp.ndarray:
    """
    :param x: Point at which to simulate density. j/np.ndarray with shape (3,)
    :param mean: Atomic coordinate. j/np.ndarray with shape (3,)
    :param bfactor: Atomic B-factor. j/np.ndarray with shape () or float
    :param a: i'th atomic 'a' parameter. j/np.ndarray with shape () or float
    :param b:  i'th atomic 'b' parameter. j/np.ndarray with shape () or float
    :return: Simulated density point. jnp.ndarray with shape ()
    """
    chex.assert_shape(x, (3,))
    chex.assert_shape(mean, (3,))
    chex.assert_rank(a, 0)
    chex.assert_rank(b, 0)
    chex.assert_rank(bfactor, 0)

    exp = (
        (-4 * jnp.pi**2)
        * jnp.sum((x - mean) ** 2)
        / (b + (bfactor**2 * 8 * np.pi**2))
    )
    result = (
        jnp.log(a)
        + (3 / 2) * jnp.log((4 * jnp.pi) / (b + (bfactor**2 * 8 * np.pi**2)))
        + exp
    )
    return result


_simulate_density_from_one_atom = jax.vmap(
    simulate_single_gaussian,
    in_axes=(None, None, None, 0, 0),
    out_axes=0,
)


def simulate_density_from_single_atom(
    x: typing.Union[jnp.ndarray, np.ndarray],
    mean: typing.Union[jnp.ndarray, np.ndarray],
    bfactor: typing.Union[jnp.ndarray, np.ndarray, float],
    a: typing.Union[jnp.ndarray, np.ndarray],
    b: typing.Union[jnp.ndarray, np.ndarray],
    mass: typing.Union[jnp.ndarray, np.ndarray, float],
) -> jnp.ndarray:
    """
    :param x: Point at which to simulate density: j/np.ndarray with shape (3,)
    :param mean: Atomic coordinate: j/np.ndarray with shape (3,)
    :param bfactor: Atomic B-factor: j/np.ndarray with shape () or float
    :param a: Atomic 'a' parameters: j/np.ndarray with shape (4,)
    :param b:  Atomic 'b' parameters: j/np.ndarray with shape (4,)
    :param mass:  Atomic mass: j/np.ndarray with shape () or float
    :return: Simulated density point: jnp.ndarray with shape ()
    """
    chex.assert_shape(x, (3,))
    chex.assert_shape(mean, (3,))
    chex.assert_rank(a, 1)
    chex.assert_rank(b, 1)
    chex.assert_rank(bfactor, 0)
    non_summed_result = _simulate_density_from_one_atom(x, mean, bfactor, a, b)
    return jnp.log(1 / mass) + sum_logs(non_summed_result)


_simulate_densities_from_one_atom = jax.vmap(
    simulate_density_from_single_atom, in_axes=(0, None, None, None, None, None)
)


def simulate_densities_from_single_atom(
    x: typing.Union[jnp.ndarray, np.ndarray],
    mean: typing.Union[jnp.ndarray, np.ndarray],
    bfactor: typing.Union[jnp.ndarray, np.ndarray, float],
    a: typing.Union[jnp.ndarray, np.ndarray],
    b: typing.Union[jnp.ndarray, np.ndarray],
    mass: typing.Union[jnp.ndarray, np.ndarray, float],
) -> jnp.ndarray:
    """
    :param x: Points at which to simulate density. j/np.ndarray with shape (P, 3) for P points
    :param mean: Atomic coordinate: j/np.ndarray with shape (3,)
    :param bfactor: Atomic B-factor: j/np.ndarray with shape () or float
    :param a: Atomic 'a' parameters: j/np.ndarray with shape (4,)
    :param b:  Atomic 'b' parameters: j/np.ndarray with shape (4,)
    :param mass:  Atomic mass: j/np.ndarray with shape () or float
    :return: Simulated density points: jnp.ndarray with shape (P,) for P points
    """
    chex.assert_rank(x, 2)
    chex.assert_shape(mean, (3,))
    chex.assert_rank(a, 1)
    chex.assert_rank(b, 1)
    chex.assert_rank(bfactor, 0)
    return _simulate_densities_from_one_atom(x, mean, bfactor, a, b, mass)


_simulate_densities_from_multiple_atoms = jax.vmap(
    simulate_densities_from_single_atom,
    in_axes=(None, 0, 0, 0, 0, 0),
    out_axes=0,
)


def simulate_density_summed_from_multiple_atoms(
    x: typing.Union[jnp.ndarray, np.ndarray],
    means: typing.Union[jnp.ndarray, np.ndarray],
    bfactors: typing.Union[jnp.ndarray, np.ndarray],
    a: typing.Union[jnp.ndarray, np.ndarray],
    b: typing.Union[jnp.ndarray, np.ndarray],
    mass: typing.Union[jnp.ndarray, np.ndarray],
):
    """
    :param x: Points at which to simulate density. j/np.ndarray with shape (P, 3) for P points
    :param means: Atomic coordinates: j/np.ndarray with shape (Nn, 3,) for Nn neighbouring atoms
    :param bfactors: Atomic B-factors: j/np.ndarray with shape (Nn,) for Nn neighbouring atoms
    :param a: Atomic 'a' parameters: j/np.ndarray with shape (Nn, 4,) for Nn neighbouring atoms
    :param b:  Atomic 'b' parameters: j/np.ndarray with shape (Nn, 4,) for Nn neighbouring atoms
    :param mass:  Atomic mass: j/np.ndarray with shape (Nn) for Nn neighbouring atoms
    :return: Simulated density points: jnp.ndarray with shape (Nn, P,) for P points from Nn atoms
    """
    chex.assert_rank(x, 2)
    chex.assert_rank(means, 2)
    chex.assert_rank(a, 2)
    chex.assert_rank(b, 2)
    chex.assert_rank(bfactors, 1)
    chex.assert_rank(mass, 1)
    result = _simulate_densities_from_multiple_atoms(x, means, bfactors, a, b, mass)
    return jax.vmap(sum_logs, in_axes=1)(result)


def simulate_summed_densities_from_all_atoms(
    x: typing.Union[jnp.ndarray, np.ndarray],
    means: typing.Union[jnp.ndarray, np.ndarray],
    bfactors: typing.Union[jnp.ndarray, np.ndarray],
    a: typing.Union[jnp.ndarray, np.ndarray],
    b: typing.Union[jnp.ndarray, np.ndarray],
    mass: typing.Union[jnp.ndarray, np.ndarray],
) -> jnp.ndarray:
    """
    :param x: Points at which to simulate density. j/np.ndarray with shape (N, P, 3) for P points at N atoms
    :param means: Atomic coordinates: j/np.ndarray with shape (N, Nn, 3,) for Nn neighbouring atoms at N atoms
    :param bfactors: Atomic B-factors: j/np.ndarray with shape (N, Nn,) for Nn neighbouring atoms at N atoms
    :param a: Atomic 'a' parameters: j/np.ndarray with shape (N, Nn, 4,) for Nn neighbouring atoms at N atoms
    :param b:  Atomic 'b' parameters: j/np.ndarray with shape (N, Nn, 4,) for Nn neighbouring atoms at N atoms
    :param mass:  Atomic mass: j/np.ndarray with shape (N, Nn) for Nn neighbouring atoms at N atoms
    :return: Simulated density points: jnp.ndarray with shape (N, Nn, P,) for P points from Nn atoms at N atoms
    """
    chex.assert_rank(x, 3)
    chex.assert_rank(means, 3)
    chex.assert_rank(a, 3)
    chex.assert_rank(b, 3)
    chex.assert_rank(bfactors, 2)
    chex.assert_rank(mass, 2)
    return jax.vmap(
        simulate_density_summed_from_multiple_atoms,
        in_axes=(0, 0, 0, 0, 0, 0),
        axis_size=x.shape[0],
    )(x, means, bfactors, a, b, mass)


def simulate_densities_from_params(
    params: bfastor.core.Parameters, random_vectors: jax.Array, neighbours_ij: jax.Array
) -> jnp.ndarray:
    densities = simulate_summed_densities_from_all_atoms(
        random_vectors,
        params.coordinates[neighbours_ij],
        params.sigmas[neighbours_ij],
        params.a[neighbours_ij],
        params.b[neighbours_ij],
        params.mass[neighbours_ij],
    )
    return densities


def ijk_to_xyz(ijk_points, map_apix):
    return jnp.flip(ijk_points, axis=1) * map_apix
