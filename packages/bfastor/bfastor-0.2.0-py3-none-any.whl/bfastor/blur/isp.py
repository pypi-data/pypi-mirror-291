import jax.scipy as jscipy
import jax
import jax.numpy as jnp
import chex
import bfastor.core
import numpy as np
import typing


def integrate_pixel_density_in_one_dimension(x, mean, sigma, b, apix):
    val1 = jscipy.special.erf(
        (2 * jnp.pi * (x - mean)) / (b + (sigma**2 * 8 * np.pi**2)) ** 0.5
    )
    val2 = jscipy.special.erf(
        (2 * jnp.pi * ((x + apix) - mean)) / (b + (sigma**2 * 8 * np.pi**2)) ** 0.5
    )
    return val2 - val1


_integrate_over_all_pixel_dimensions = jax.vmap(
    integrate_pixel_density_in_one_dimension,
    in_axes=(0, 0, None, None, 0),
)


def integrate_pixel_density(x, mean, sigma, a, b, apix):
    chex.assert_rank(x, 1)
    chex.assert_rank(apix, 1)
    chex.assert_rank(mean, 1)
    vals = _integrate_over_all_pixel_dimensions(
        x,
        mean,
        sigma,
        b,
        apix,
    )
    return a * jnp.prod(vals, axis=0)


_integrate_pixel_density_for_all_scattering_gaussians = jax.vmap(
    integrate_pixel_density, in_axes=(None, None, None, 0, 0, None)
)


def integrate_pixel_density_for_all_scattering_gaussians(
    x,
    mean,
    sigma,
    a,
    b,
    m,
    apix,
):
    chex.assert_rank(a, 1)
    chex.assert_rank(b, 1)
    chex.assert_rank(x, 1)
    gs = _integrate_pixel_density_for_all_scattering_gaussians(
        x, mean, sigma, a, b, apix
    )
    return (1 / m) * jnp.sum(gs, axis=0)


_integrate_pixel_densities = jax.vmap(
    integrate_pixel_density_for_all_scattering_gaussians,
    in_axes=(0, None, None, None, None, None, None),
)


def simulate_densities_from_single_atom(x, mean, sigma, a, b, m, apix):
    chex.assert_rank(x, 2)
    chex.assert_shape(mean, (3,))
    chex.assert_rank(a, 1)
    chex.assert_rank(b, 1)
    chex.assert_rank(sigma, 0)
    return _integrate_pixel_densities(
        x,
        mean,
        sigma,
        a,
        b,
        m,
        apix,
    )


_densities_from_multiple_atoms = jax.vmap(
    simulate_densities_from_single_atom,
    in_axes=(None, 0, 0, 0, 0, 0, None),
    out_axes=0,
)


def simulate_densities_summed_from_multiple_atoms(x, mean, sigma, a, b, m, apix):
    chex.assert_rank(x, 2)
    chex.assert_rank(mean, 2)
    chex.assert_rank(a, 2)
    chex.assert_rank(b, 2)
    chex.assert_rank(sigma, 1)
    densities = _densities_from_multiple_atoms(x, mean, sigma, a, b, m, apix)
    return jnp.sum(densities, axis=0)


def simulate_summed_densities_from_all_atoms(
    x: typing.Union[jnp.ndarray, np.ndarray],
    means: typing.Union[jnp.ndarray, np.ndarray],
    bfactors: typing.Union[jnp.ndarray, np.ndarray],
    a: typing.Union[jnp.ndarray, np.ndarray],
    b: typing.Union[jnp.ndarray, np.ndarray],
    mass: typing.Union[jnp.ndarray, np.ndarray],
    apix,
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
        simulate_densities_summed_from_multiple_atoms,
        in_axes=(0, 0, 0, 0, 0, 0, None),
        axis_size=x.shape[0],
    )(x, means, bfactors, a, b, mass, apix)


_simulate_gradient_in_one_dimension = jax.grad(
    integrate_pixel_density_in_one_dimension, argnums=(0,)
)


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
        params.apix,
    )
    return densities


def ijk_to_xyz(ijk_points, map_apix):
    return (jnp.flip(ijk_points, axis=1) * map_apix) - map_apix / 2
