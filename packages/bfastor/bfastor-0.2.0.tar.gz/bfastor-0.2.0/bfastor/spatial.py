import functools
from typing import Union
import jax
import jax.numpy as jnp
import numpy as np
from scipy.spatial import KDTree

from bfastor.core import State


def get_radii_from_bfacs(bfactors, apix):
    radii = jnp.clip((jnp.nan_to_num(bfactors) * 6), 3 * jnp.max(apix), None)[
        :, None, None
    ]
    return radii


def make_atomic_kdtree(coordinates):
    tree = KDTree(
        coordinates,
    )
    return tree


def get_nearest_neighbour_indexes(
    coordinates: Union[jnp.ndarray, np.ndarray], window_size: int = 8
) -> tuple[jnp.ndarray, jnp.ndarray]:
    kdtree = make_atomic_kdtree(coordinates)
    neighbours = kdtree.query(coordinates, k=window_size, workers=-1)
    return jnp.asarray(neighbours[0]), jnp.asarray(neighbours[1])


@functools.partial(jax.jit, static_argnames="shape", inline=True)
def generate_random_indexes(bfactors, means, key, shape, apix, data_shape):
    key, subkey = jax.random.split(key)
    radii = get_radii_from_bfacs(bfactors, apix)
    # generate random coordinates in a sphere
    # taken from https://karthikkaranth.me/blog/generating-random-points-in-a-sphere/#using-normally-distributed-random-numbers
    xyz_normal = jax.random.normal(key, shape=shape)
    key, subkey = jax.random.split(key)
    mag = jnp.sqrt(jnp.sum(xyz_normal**2, axis=-1))
    c = jax.random.uniform(key, shape=(*shape[:-1], 1)) ** (1 / 3)
    scale = (c * radii) / jnp.expand_dims(mag, axis=-1)
    normalised_means = (means[:, None, :] / apix).round(0) * apix + (apix / 2)
    random_vectors = normalised_means + scale * xyz_normal
    maximum_size = data_shape * apix
    # clip the vectors so they stay inside the box
    random_vectors = jnp.clip(random_vectors, jnp.array((0.0, 0.0, 0.0)), maximum_size)
    # convert the vectors to indexes
    random_voxel_indexes = (random_vectors / apix).round(0).astype(int)

    return random_vectors, random_voxel_indexes, subkey


@functools.partial(jax.jit, static_argnames="shape", inline=True)
def _prepare_data(data, params, key, shape, apix, data_shape):
    rand_v, rand_ijk, key = generate_random_indexes(
        params.sigmas,
        params.coordinates,
        key,
        shape,
        apix,
        data_shape,
    )
    original_shape = rand_v.shape
    indexed_densities = data.densities[tuple(rand_ijk.reshape(-1, 3).T)].reshape(
        *original_shape[:-1], 1
    )
    return rand_v, indexed_densities, key


@functools.partial(jax.jit, inline=True)
def prepare_data_from_state(state: State):
    stochastic_vectors, indexed_densities, key = _prepare_data(
        state.data,
        state.params,
        state.key,
        state.extra_params.shape,
        state.extra_params.apix,
        state.extra_params.data_shape,
    )
    return stochastic_vectors, indexed_densities, key
